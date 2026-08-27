#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
REPORTS_DIR = ROOT / ".obsidian-governance" / "reports"

EXCLUDE_DIRS = {".git", ".obsidian", ".agents", "node_modules", ".trash", "scripts"}

DEPRECATED_AUTO_TAGS = {
    "projetos",
    "areas",
    "recursos",
    "estudos",
    "biblioteca",
    "templates",
    "arquivos",
    "assets",
    "conhecimento",
    "diario",
    "geral",
    "trabalho",
}

PATH_TAG_BLOCKLIST = {
    "00",
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "diario",
    "projetos",
    "areas",
    "recursos",
    "arquivo",
    "assets",
    "caixa",
    "entrada",
}

STOPWORDS_PT = {
    "a",
    "o",
    "as",
    "os",
    "de",
    "da",
    "do",
    "das",
    "dos",
    "e",
    "em",
    "para",
    "por",
    "com",
    "no",
    "na",
    "nos",
    "nas",
    "um",
    "uma",
}

KEYWORDS = {
    "aws": "AWS",
    "azure": "Azure",
    "api": "API",
    "python": "Python",
    "sql": "SQL",
    "powerbi": "PowerBI",
    "n8n": "n8n",
    "obsidian": "Obsidian",
    "excalidraw": "Excalidraw",
    "mercadopago": "MercadoPago",
    "bi": "BI",
    "dw": "DW",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "github": "GitHub",
}

# Controlled taxonomy: only these tags are auto-applied.
APPROVED_TAXONOMY_TAGS = {
    "AWS",
    "Azure",
    "API",
    "API Recintos",
    "Python",
    "SQL",
    "PowerBI",
    "n8n",
    "Obsidian",
    "Excalidraw",
    "MercadoPago",
    "BI",
    "DW",
    "Docker",
    "Kubernetes",
    "GitHub",
    "UNIMED",
    "MOVECTA",
    "ABA006",
    "BRG067",
    "MVT019",
    "MVT020",
}


def normalize_token(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower()


APPROVED_TAXONOMY_TAGS_NORMALIZED = {normalize_token(t) for t in APPROVED_TAXONOMY_TAGS}


def is_api_recintos_context(rel: Path, body: str) -> bool:
    rel_norm = normalize_token(str(rel).replace("\\", "/"))
    body_norm = normalize_token(body)
    return "api recintos" in rel_norm or "api recintos" in body_norm


def is_approved_tag(tag: str) -> bool:
    return normalize_token(tag) in APPROVED_TAXONOMY_TAGS_NORMALIZED


def slug_tag(s: str) -> str:
    s = re.sub(r"\s+", "_", s.strip())
    s = re.sub(r"[^\w\-/]", "", s, flags=re.UNICODE)
    return s[:80] if s else ""


def is_year_tag(s: str) -> bool:
    return bool(re.fullmatch(r"(19|20)\d{2}", s))


def split_frontmatter(text: str) -> tuple[dict, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            raw = text[4:end]
            body = text[end + 5 :]
            data = yaml.safe_load(raw) or {}
            if not isinstance(data, dict):
                data = {}
            return data, body
    return {}, text


def dump_frontmatter(data: dict) -> str:
    return f"---\n{yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip()}\n---\n"


def tokenize_text(text: str) -> list[str]:
    n = normalize_token(text)
    return [t for t in re.split(r"[^a-z0-9]+", n) if t]


def tags_from_keywords(text: str) -> set[str]:
    tokens = set(tokenize_text(text))
    tags: set[str] = set()
    for kw, tag in KEYWORDS.items():
        if normalize_token(kw) in tokens:
            tags.add(tag)
    return tags


def tags_from_path_and_filename(rel: Path) -> set[str]:
    tags: set[str] = set()
    candidates = list(rel.parts[:-1]) + [rel.stem]
    for item in candidates:
        for raw in re.split(r"[^A-Za-z0-9À-ÿ]+", item):
            if not raw:
                continue
            tok = normalize_token(raw)
            if len(tok) < 3:
                continue
            if is_year_tag(tok):
                continue
            if tok in STOPWORDS_PT or tok in PATH_TAG_BLOCKLIST:
                continue
            if tok in KEYWORDS:
                tags.add(KEYWORDS[tok])
            else:
                tag = slug_tag(raw)
                if tag:
                    tags.add(tag)
    return tags


def strip_tasks_fenced_blocks(text: str) -> str:
    return re.sub(r"^```tasks\s*[\s\S]*?^```\s*", "", text, flags=re.MULTILINE)


def diary_focus_text(text: str) -> str:
    text = strip_tasks_fenced_blocks(text)
    resumo = ""
    tarefas = ""
    m_res = re.search(r"^##\s+Resumo\s*$([\s\S]*?)(?=^##\s+|^#\s+|\Z)", text, flags=re.MULTILINE | re.IGNORECASE)
    if m_res:
        resumo = m_res.group(1).strip()
    m_tar = re.search(r"^###\s+Tarefas\s*$([\s\S]*?)(?=^###\s+|^##\s+|^#\s+|\Z)", text, flags=re.MULTILINE | re.IGNORECASE)
    if m_tar:
        tarefas = m_tar.group(1).strip()
    return "\n".join(x for x in [resumo, tarefas] if x).strip()


def is_diary(rel: Path) -> bool:
    return rel.parts and rel.parts[0] == "00. Diario"


def coerce_tags(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for v in value:
            if isinstance(v, str):
                out.append(v)
        return out
    return []


def normalize_tag_value(tag: str) -> str:
    return tag.strip().lstrip("#")


def clean_tag_list(tags: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in tags:
        s = normalize_tag_value(raw)
        if not s:
            continue
        if is_year_tag(s):
            continue
        key = normalize_token(s)
        if is_year_tag(key):
            continue
        if key in DEPRECATED_AUTO_TAGS or key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def merge_tags(existing: list[str], inferred: set[str], ignored_set: set[str] | None = None) -> list[str]:
    # Keep user/order intent from existing tags, then append new inferred tags.
    base = clean_tag_list(existing)
    if ignored_set:
        base = [t for t in base if normalize_token(t) not in ignored_set]
    seen = {normalize_token(t) for t in base}
    inferred_clean = clean_tag_list(sorted(inferred, key=lambda x: x.lower()))
    for t in inferred_clean:
        key = normalize_token(t)
        if key in seen:
            continue
        if ignored_set and key in ignored_set:
            continue
        seen.add(key)
        base.append(t)
    return base


def infer_tags(rel: Path, body: str) -> tuple[set[str], set[str]]:
    if is_diary(rel):
        source = diary_focus_text(body)
    else:
        source = body
    tags_to_apply = set(tags_from_keywords(source))
    suggested_tags = set()

    for candidate in tags_from_path_and_filename(rel):
        if is_approved_tag(candidate):
            tags_to_apply.add(candidate)
        else:
            suggested_tags.add(candidate)

    # Taxonomy rule: notes from API Recintos context should use a specific tag.
    if is_api_recintos_context(rel, body):
        tags_to_apply = {t for t in tags_to_apply if normalize_token(t) != "api"}
        suggested_tags = {t for t in suggested_tags if normalize_token(t) != "api"}
        tags_to_apply.add("API Recintos")

    return tags_to_apply, suggested_tags


def run(prune_only: bool = False, only_files: list[str] | None = None) -> tuple[int, int, dict[str, list[str]]]:
    changed = 0
    total = 0
    suggestions_by_file: dict[str, list[str]] = {}
    targets: list[Path] = []
    if only_files:
        for rel_str in only_files:
            rel = Path(rel_str)
            if rel.suffix.lower() != ".md":
                continue
            if any(part in EXCLUDE_DIRS for part in rel.parts):
                continue
            p = ROOT / rel
            if p.exists() and p.is_file():
                targets.append(p)
    else:
        for p in ROOT.rglob("*.md"):
            rel = p.relative_to(ROOT)
            if any(part in EXCLUDE_DIRS for part in rel.parts):
                continue
            targets.append(p)

    for p in targets:
        rel = p.relative_to(ROOT)
        total += 1
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="latin-1", errors="replace")
        fm, body = split_frontmatter(content)
        existing_tags = coerce_tags(fm.get("tags"))
        ignored_tags = coerce_tags(fm.get("ignored_tags") or fm.get("exclude_tags"))
        ignored_set = {normalize_token(t) for t in ignored_tags}
        
        if prune_only:
            inferred = set()
            suggested = set()
        else:
            inferred, suggested = infer_tags(rel, body)
            if suggested and ignored_set:
                suggested = {t for t in suggested if normalize_token(t) not in ignored_set}
            if suggested:
                suggestions_by_file[str(rel).replace("\\", "/")] = sorted(suggested, key=lambda x: x.lower())

        merged = merge_tags(existing_tags, inferred, ignored_set)
        if merged != existing_tags:
            fm["tags"] = merged
            out = dump_frontmatter(fm) + body.lstrip("\n")
            p.write_text(out, encoding="utf-8")
            changed += 1
    return total, changed, suggestions_by_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply Obsidian tags for markdown notes.")
    parser.add_argument("--prune", action="store_true", help="Only remove deprecated tags from existing frontmatter.")
    parser.add_argument(
        "--only-files-json",
        help="JSON file with {'files': ['relative/path.md', ...]} to process only changed markdown files.",
    )
    args = parser.parse_args()

    only_files: list[str] | None = None
    if args.only_files_json:
        payload = json.loads(Path(args.only_files_json).read_text(encoding="utf-8"))
        files = payload.get("files", []) if isinstance(payload, dict) else []
        if isinstance(files, list):
            only_files = [str(x).replace("\\", "/") for x in files if isinstance(x, str)]

    total, changed, suggestions_by_file = run(prune_only=args.prune, only_files=only_files)
    unique_suggestions = sorted(
        {tag for tags in suggestions_by_file.values() for tag in tags},
        key=lambda x: x.lower(),
    )
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    suggestions_report_path = REPORTS_DIR / "tag-suggestions-latest.json"
    suggestions_report_path.write_text(
        json.dumps(
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "notes_scanned": total,
                "notes_changed": changed,
                "suggested_tags_unicas": unique_suggestions,
                "por_arquivo": suggestions_by_file,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("notes_scanned", total)
    print("notes_changed", changed)
    print("mode", "prune" if args.prune else "full")
    print("tag_suggestions_count", len(unique_suggestions))
    print("tag_suggestions_report", suggestions_report_path)


if __name__ == "__main__":
    main()
