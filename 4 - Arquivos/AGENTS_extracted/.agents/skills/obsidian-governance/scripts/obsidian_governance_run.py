#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / ".agents" / "skills" / "obsidian-governance" / "scripts"
REPORTS_DIR = ROOT / ".obsidian-governance" / "reports"


def run_cmd(cmd: list[str], title: str) -> tuple[int, str, str]:
    print(f"\n=== {title} ===")
    print("$", " ".join(cmd))
    import os
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip(), file=sys.stderr)
    return proc.returncode, proc.stdout, proc.stderr



def run_python_script(script_name: str, *args: str, title: str) -> tuple[int, str, str]:
    script = SCRIPTS / script_name
    return run_cmd([sys.executable, str(script), *args], title=title)


def parse_json_output(stdout_text: str) -> dict:
    txt = (stdout_text or "").strip()
    if not txt:
        return {}
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        return {}


def write_report(report: dict) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    out = REPORTS_DIR / f"governance-report-{ts}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def validate_forbidden_tags() -> tuple[int, dict]:
    script = r"""
import json, re, yaml
from pathlib import Path
root = Path('.')
exclude = {'.git','.agents','.cursor','node_modules','.obsidian'}
forbidden = {'geral','trabalho','areas'}
hits = []
for p in root.rglob('*.md'):
    if any(x in exclude for x in p.parts):
        continue
    t = p.read_text(encoding='utf-8', errors='replace')
    m = re.match(r'\A---\s*\n(.*?)\n---\s*', t, re.S)
    if not m:
        continue
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception:
        continue
    tags = fm.get('tags')
    if isinstance(tags, list):
        low = {str(x).strip().lower() for x in tags if str(x).strip()}
        bad = sorted(low & forbidden)
        if bad:
            hits.append({'file': str(p), 'bad_tags': bad})
print(json.dumps({'count': len(hits), 'hits': hits}, ensure_ascii=False))
"""
    rc, out, err = run_cmd([sys.executable, "-c", script], title="Validation: forbidden tags")
    if rc != 0:
        return rc, {"count": -1, "hits": [], "error": err}
    data = json.loads(out.strip() or "{}")
    if data.get("count", 0) > 0:
        print(f"Forbidden tag hits: {data['count']}", file=sys.stderr)
        for h in data.get("hits", [])[:20]:
            print(f"- {h['file']}: {', '.join(h['bad_tags'])}", file=sys.stderr)
        return 2, data
    print("Forbidden tags: OK")
    return 0, data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="One-click Obsidian governance pipeline: status -> changed -> tags -> icons -> validation -> optional mark"
    )
    parser.add_argument("--mark", action="store_true", help="Mark current HEAD as processed if pipeline succeeds")
    parser.add_argument("--skip-tags", action="store_true", help="Skip tag normalization step")
    parser.add_argument("--skip-icons", action="store_true", help="Skip folder icon normalization step")
    args = parser.parse_args()

    report: dict = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(ROOT),
        "mark_requested": args.mark,
        "steps": [],
        "summary": {},
    }

    steps = [
        ("obsidian_delta.py", ["status"], "Step 1: Baseline status"),
        ("obsidian_delta.py", ["changed", "--markdown-only"], "Step 2: Changed markdown files"),
    ]

    status_payload: dict = {}
    before_payload: dict = {}
    after_payload: dict = {}

    for script, script_args, title in steps:
        rc, out, err = run_python_script(script, *script_args, title=title)
        step_info = {"title": title, "script": script, "args": script_args, "exit_code": rc}
        parsed = parse_json_output(out)
        if parsed:
            step_info["payload"] = parsed
        if err:
            step_info["stderr"] = err.strip()
        report["steps"].append(step_info)
        if title.startswith("Step 1"):
            status_payload = parsed
        elif title.startswith("Step 2"):
            before_payload = parsed
        if rc != 0:
            report["summary"] = {"ok": False, "reason": f"failed at {title}"}
            report_path = write_report(report)
            print(f"\nGovernance report: {report_path}")
            return rc

    if not args.skip_tags:
        delta_payload_path = ROOT / ".obsidian-governance" / "reports" / "last-changed-markdown.json"
        delta_payload_path.parent.mkdir(parents=True, exist_ok=True)
        delta_payload_path.write_text(
            json.dumps(before_payload if isinstance(before_payload, dict) else {}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        rc, out, err = run_python_script(
            "tag_vault_notes.py",
            "--only-files-json",
            str(delta_payload_path),
            title="Step 3: Tag governance",
        )
        report["steps"].append(
            {
                "title": "Step 3: Tag governance",
                "script": "tag_vault_notes.py",
                "args": ["--only-files-json", str(delta_payload_path)],
                "exit_code": rc,
                "stdout": out.strip(),
            }
        )
        if rc != 0:
            report["summary"] = {"ok": False, "reason": "tag governance failed"}
            report_path = write_report(report)
            print(f"\nGovernance report: {report_path}")
            return rc

    if not args.skip_icons:
        rc, out, err = run_python_script("populate_folder_icons.py", title="Step 4: Icon governance")
        report["steps"].append(
            {
                "title": "Step 4: Icon governance",
                "script": "populate_folder_icons.py",
                "exit_code": rc,
                "stdout": out.strip(),
            }
        )
        if rc != 0:
            report["summary"] = {"ok": False, "reason": "icon governance failed"}
            report_path = write_report(report)
            print(f"\nGovernance report: {report_path}")
            return rc

    rc, validation_data = validate_forbidden_tags()
    report["steps"].append({"title": "Validation: forbidden tags", "exit_code": rc, "payload": validation_data})
    if rc != 0:
        report["summary"] = {"ok": False, "reason": "forbidden tags validation failed"}
        report_path = write_report(report)
        print(f"\nGovernance report: {report_path}")
        return rc

    rc, out, err = run_python_script("obsidian_delta.py", "changed", "--markdown-only", title="Step 5: Post-check delta")
    after_payload = parse_json_output(out)
    report["steps"].append(
        {
            "title": "Step 5: Post-check delta",
            "script": "obsidian_delta.py",
            "args": ["changed", "--markdown-only"],
            "exit_code": rc,
            "payload": after_payload,
        }
    )
    if rc != 0:
        report["summary"] = {"ok": False, "reason": "post-check delta failed"}
        report_path = write_report(report)
        print(f"\nGovernance report: {report_path}")
        return rc

    mark_payload: dict = {}
    if args.mark:
        rc, out, err = run_python_script("obsidian_delta.py", "mark", title="Step 6: Mark baseline")
        mark_payload = parse_json_output(out)
        report["steps"].append(
            {
                "title": "Step 6: Mark baseline",
                "script": "obsidian_delta.py",
                "args": ["mark"],
                "exit_code": rc,
                "payload": mark_payload,
            }
        )
        if rc != 0:
            report["summary"] = {"ok": False, "reason": "mark baseline failed"}
            report_path = write_report(report)
            print(f"\nGovernance report: {report_path}")
            return rc
    else:
        print("\nMark step skipped. Re-run with --mark to store new baseline.")

    before_count = int(before_payload.get("count", 0)) if isinstance(before_payload, dict) else 0
    after_count = int(after_payload.get("count", 0)) if isinstance(after_payload, dict) else 0
    report["summary"] = {
        "ok": True,
        "base_commit": status_payload.get("base"),
        "head_commit": status_payload.get("head"),
        "changed_markdown_before": before_count,
        "changed_markdown_after": after_count,
        "mark_applied": bool(args.mark),
        "forbidden_tags_hits": int(validation_data.get("count", 0)),
    }
    if mark_payload:
        report["summary"]["new_baseline"] = mark_payload.get("last_processed_commit")

    report_path = write_report(report)
    print("\n=== Governance Summary ===")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"Governance report: {report_path}")
    print("\nObsidian governance run: SUCCESS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
