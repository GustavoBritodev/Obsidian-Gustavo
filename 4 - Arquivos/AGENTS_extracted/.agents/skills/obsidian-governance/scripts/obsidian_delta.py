#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
STATE_DIR = ROOT / ".obsidian-governance"
STATE_FILE = STATE_DIR / "state.json"


def run_git(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        return proc.stdout.decode("utf-8").strip()
    except UnicodeDecodeError:
        return proc.stdout.decode("cp1252", errors="replace").strip()



def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def current_head() -> str:
    return run_git(["rev-parse", "HEAD"])


def changed_files_since(base_commit: str) -> list[str]:
    names = set()
    out = run_git(["diff", "--name-only", f"{base_commit}..HEAD"])
    names.update([x.strip() for x in out.splitlines() if x.strip()])
    out = run_git(["diff", "--name-only"])
    names.update([x.strip() for x in out.splitlines() if x.strip()])
    out = run_git(["diff", "--cached", "--name-only"])
    names.update([x.strip() for x in out.splitlines() if x.strip()])
    out = run_git(["ls-files", "--others", "--exclude-standard"])
    names.update([x.strip() for x in out.splitlines() if x.strip()])
    return sorted(names)


def filter_markdown(paths: list[str]) -> list[str]:
    return [p for p in paths if p.lower().endswith(".md")]


def cmd_init(args: argparse.Namespace) -> int:
    commit = args.commit or current_head()
    state = {
        "last_processed_commit": commit,
        "updated_at": run_git(["show", "-s", "--format=%cI", commit]),
        "notes": "Baseline for Obsidian governance delta checks",
    }
    save_state(state)
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    state = load_state()
    if not state:
        print("State not initialized. Run: python .agents/obsidian-governance/scripts/obsidian_delta.py init")
        return 1
    head = current_head()
    base = state.get("last_processed_commit", "")
    ahead = run_git(["rev-list", "--count", f"{base}..HEAD"]) if base else "?"
    print(json.dumps({"base": base, "head": head, "commits_ahead": int(ahead)}, indent=2))
    return 0


def cmd_changed(args: argparse.Namespace) -> int:
    state = load_state()
    base = args.commit or state.get("last_processed_commit")
    if not base:
        print("No baseline commit. Run init first or pass --commit.", file=sys.stderr)
        return 2
    changed = changed_files_since(base)
    if args.markdown_only:
        changed = filter_markdown(changed)
    payload = {"base": base, "count": len(changed), "files": changed}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_mark(args: argparse.Namespace) -> int:
    state = load_state()
    commit = args.commit or current_head()
    state["last_processed_commit"] = commit
    state["updated_at"] = run_git(["show", "-s", "--format=%cI", commit])
    save_state(state)
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Track markdown delta from last governance baseline commit.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Initialize baseline commit")
    p_init.add_argument("--commit", help="Optional commit hash, defaults to HEAD")
    p_init.set_defaults(func=cmd_init)

    p_status = sub.add_parser("status", help="Show baseline/head status")
    p_status.set_defaults(func=cmd_status)

    p_changed = sub.add_parser("changed", help="List changed files since baseline")
    p_changed.add_argument("--commit", help="Override baseline commit")
    p_changed.add_argument("--markdown-only", action="store_true", default=True, help="Only return .md files")
    p_changed.set_defaults(func=cmd_changed)

    p_mark = sub.add_parser("mark", help="Mark commit as processed")
    p_mark.add_argument("--commit", help="Commit hash to store, defaults to HEAD")
    p_mark.set_defaults(func=cmd_mark)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
