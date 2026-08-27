import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

VAULT_ROOT = Path(r"C:/Users/ModalGR/Documents/Obsidian Vault")
DAILY_FOLDER = VAULT_ROOT / "0 Diario"  # after rename it's 0 Diário; use without accent for filesystem
TEMPLATE = VAULT_ROOT / "Templates" / "daily_template.md"

def is_weekday(date: datetime) -> bool:
    return date.weekday() < 5  # Monday=0, Friday=4

def create_daily_note():
    today = datetime.now()
    if not is_weekday(today):
        print("Weekend – no note created")
        return
    # Ensure folder exists
    DAILY_FOLDER.mkdir(parents=True, exist_ok=True)
    filename = today.strftime("%d-%m-%Y.md")
    note_path = DAILY_FOLDER / filename
    if note_path.exists():
        print(f"Note already exists: {note_path}")
        return
    # Read template and replace placeholders
    if TEMPLATE.is_file():
        content = TEMPLATE.read_text(encoding="utf-8")
        title = today.strftime("%d-%m-%Y – %A")
        content = content.replace("{{date:dd-MM-YYYY}}", today.strftime("%d-%m-%Y"))
        content = content.replace("{{date:dddd}}", today.strftime("%A"))
        content = content.replace("title: ", f"title: {title}\n")
    else:
        # Fallback minimal content
        title = today.strftime("%d-%m-%Y – %A")
        content = f"---\ntitle: {title}\ntags:\n  - tipo/geral/diario\n---\n\n> [!info] Resumo do dia\n"
    note_path.write_text(content, encoding="utf-8")
    print(f"Created daily note: {note_path}")

if __name__ == "__main__":
    create_daily_note()
