#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DATA_JSON = ROOT / ".obsidian" / "plugins" / "obsidian-icon-folder" / "data.json"
REPORTS_DIR = ROOT / ".obsidian-governance" / "reports"

EXCLUDE = {".git", ".agents", "scripts", "node_modules"}

# Explicit mapping for high-priority folders.
OVERRIDES = {
    ".obsidian": "LiSettings",
    ".obsidian/icons": "LiPalette",
    ".obsidian/plugins": "LiPuzzle",
    ".obsidian/snippets": "LiScissors",
    ".obsidian/themes": "LiPaintbrush",
    ".obsidian/plugins/calendar": "LiCalendarDays",
    ".obsidian/plugins/copilot": "LiBot",
    ".obsidian/plugins/dataview": "LiTable2",
    ".obsidian/plugins/folder-note-plugin": "LiNotebookPen",
    ".obsidian/plugins/obsidian-icon-folder": "LiFolderCog",
    ".obsidian/plugins/obsidian-projects": "LiFolders",
    ".obsidian/plugins/obsidian-style-settings": "LiSlidersHorizontal",
    ".obsidian/plugins/obsidian-tasks-plugin": "LiListChecks",
    ".obsidian/plugins/obsidian-tracker": "LiActivity",
    ".obsidian/plugins/obsidian-vault-statistics-plugin": "LiChartColumnIncreasing",
    ".obsidian/plugins/remotely-save": "LiCloudUpload",
    ".obsidian/plugins/templater-obsidian": "LiFileTemplate",
    ".obsidian/themes/Blue Topaz": "LiPalette",
    ".obsidian/themes/Obsidian Nord": "LiMoonStar",
    "00. Diario": "LiCalendarDays",
    "01. Projetos": "LiKanbanSquare",
    "01. Projetos/Plataforma de Ingressos": "LiTicket",
    "01. Projetos/TTRPG": "LiDices",
    "02. Areas": "LiBriefcase",
    "03. Recursos": "LiLibrary",
    "04. Arquivo": "LiArchive",
    "05. Assets": "LiImage",
    "07. Caixa de Entrada": "LiInbox",
    "02. Areas/Trabalho Mosten": "LiBuilding2",
    "02. Areas/Estudos": "LiGraduationCap",
    "03. Recursos/Tech": "LiWrench",
    "03. Recursos/Codigos": "LiCode2",
    "03. Recursos/N8N": "LiWorkflow",
    "05. Assets/Excalidraw": "LiPencilRuler",
    "05. Assets/Templates": "LiFileTemplate",
    "05. Assets/Attachments": "LiPaperclip",
    "04. Arquivo/Bibliotecas": "LiBookOpen",
    # Trabalho Mosten - clientes (100% personalizado)
    # Família visual: Indústria e Manufatura
    "02. Areas/Trabalho Mosten/Bridgestone": "LiFactory",
    "02. Areas/Trabalho Mosten/Kluber": "LiFactory",
    # Família visual: Saúde
    "02. Areas/Trabalho Mosten/UNIMED": "LiHeartPulse",
    "02. Areas/Trabalho Mosten/HSMC": "LiStethoscope",
    # Família visual: Logística e Portos
    "02. Areas/Trabalho Mosten/MOVECTA": "LiShip",
    "02. Areas/Trabalho Mosten/Transmaroni": "LiTruck",
    "02. Areas/Trabalho Mosten/Ogmo Santos": "LiAnchor",
    "02. Areas/Trabalho Mosten/[VESSEL] - ENC_ Ref._ Relatórios - OBRA 1830 Praça Bauru": "LiShipWheel",
    # Família visual: Cloud / Dados / Tecnologia
    "02. Areas/Trabalho Mosten/AWS Mosten": "LiCloudCog",
    "02. Areas/Trabalho Mosten/BI META API": "LiDatabaseZap",
    "02. Areas/Trabalho Mosten/MAIA": "LiBot",
    "02. Areas/Trabalho Mosten/ABA": "LiNetwork",
    "02. Areas/Trabalho Mosten/ABA/Api Recintos": "LiPlugZap",
    "02. Areas/Trabalho Mosten/ABA/Api Recintos/Adonai": "LiBuilding2",
    "02. Areas/Trabalho Mosten/ABA/Api Recintos/Eudmarco": "LiContainer",
    "02. Areas/Trabalho Mosten/ABA/Api Recintos/Eudmarco/Banco API Recintos Eudmarco": "LiDatabase",
    "02. Areas/Trabalho Mosten/ABA/Api Recintos/Eudmarco/Assets": "LiImage",
    "02. Areas/Trabalho Mosten/ABA/Api Recintos/Eudmarco/Documents": "LiFileText",
    # Família visual: Negócios / Consultoria
    "02. Areas/Trabalho Mosten/HKC001-26 Sebrae": "LiBriefcaseBusiness",
    "02. Areas/Trabalho Mosten/Nita": "LiHandshake",
    "02. Areas/Trabalho Mosten/SONAE": "LiStore",
    "02. Areas/Trabalho Mosten/Slopss": "LiShieldCheck",
    "02. Areas/Trabalho Mosten/Pátio Inteligente": "LiContainer",
    "02. Areas/Trabalho Mosten/Orçamentos": "LiReceiptText",
    # Cliente-level common subfolders
    "02. Areas/Trabalho Mosten/Bridgestone/BRG067-25 Capabilidade": "LiGauge",
    "02. Areas/Trabalho Mosten/Bridgestone/BRG067-25 Capabilidade/Acessos": "LiKeyRound",
    "02. Areas/Trabalho Mosten/Bridgestone/BRG067-25 Capabilidade/Documents": "LiFileText",
    "02. Areas/Trabalho Mosten/Bridgestone/BRG067-25 Capabilidade/Reuniões": "LiMessagesSquare",
    "02. Areas/Trabalho Mosten/MOVECTA/MVT019": "LiRoute",
    "02. Areas/Trabalho Mosten/MOVECTA/MVT019/Reuniões": "LiMessagesSquare",
    "02. Areas/Trabalho Mosten/Ogmo Santos/Reuniões": "LiMessagesSquare",
    "02. Areas/Trabalho Mosten/Ogmo Santos/Documents": "LiFileText",
    "02. Areas/Trabalho Mosten/UNIMED/Reuniões": "LiMessagesSquare",
    "02. Areas/Trabalho Mosten/UNIMED/Reuniões/Daily": "LiCalendarCheck",
    "02. Areas/Trabalho Mosten/ABA/Financeiro": "LiBadgeDollarSign",
    "02. Areas/Trabalho Mosten/HSMC/Gráficos Nao resolvidos": "LiChartNoAxesCombined",
    "01. Projetos/Plataforma de Ingressos/Fluxos de testes QA/Comprador": "LiUserRound",
    "01. Projetos/Plataforma de Ingressos/Fluxos de testes QA/Produtores": "LiStore",
    "02. Areas/Trabalho Mosten/Obisidian Guibao": "LiNotebookText",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes": "LiBuilding2",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Interno": "LiUsers",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Produtos": "LiPackage",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Recursos": "LiLibrary",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes/4Infra": "LiBuilding",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes/Agro Galaxy": "LiWheat",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes/Baltic": "LiShip",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes/Bridgestone": "LiFactory",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes/Grupo ABA": "LiNetwork",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes/HSMC": "LiStethoscope",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes/Movecta": "LiTruck",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes/Unimed": "LiHeartPulse",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes/Vessel": "LiShipWheel",
    "02. Areas/Trabalho Mosten/Obisidian Guibao/Clientes/Zurich": "LiShieldCheck",
}


def infer_icon(path_str: str) -> tuple[str, str]:
    if path_str in OVERRIDES:
        return OVERRIDES[path_str], "override"
    s = path_str.lower()
    s_norm = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    tokens = set(t for t in re.split(r"[^a-z0-9]+", s_norm) if t)

    def has_any(*kws: str) -> bool:
        for kw in kws:
            kw_norm = unicodedata.normalize("NFKD", kw.lower()).encode("ascii", "ignore").decode("ascii")
            if " " in kw_norm:
                if kw_norm in s_norm:
                    return True
            elif kw_norm in tokens:
                return True
        return False

    rules = [
        # Operational / navigation
        (("reuniao", "reunioes", "meeting", "meetings", "daily", "status report"), "LiMessagesSquare"),
        (("acesso", "acessos", "credentials", "credenciais", "vpn"), "LiKeyRound"),
        (("documents", "documentos", "documentacao", "documentacao", "docs"), "LiFileText"),
        (("assets", "asset", "anexo", "anexos", "attachments"), "LiImage"),
        (("caixa de entrada", "inbox"), "LiInbox"),
        (("arquivo", "archive"), "LiArchive"),
        (("geral",), "LiFolderOpen"),
        # People / companies / clients
        (("cliente", "clientes"), "LiBuilding2"),
        (("unimed", "saude"), "LiHeartPulse"),
        (("bridgestone",), "LiFactory"),
        (("movecta", "logistica"), "LiShip"),
        (("sebrae",), "LiBriefcaseBusiness"),
        # Study / knowledge
        (("diario",), "LiCalendarDays"),
        (("estudos", "faculdade", "school", "curso", "semestre"), "LiGraduationCap"),
        (("cybersec", "tryhack", "pentest", "osint", "kali"), "LiShield"),
        (("rooms",), "LiDoorOpen"),
        (("ferramentas", "tools"), "LiWrench"),
        (("conhecimentos", "knowledge"), "LiLightbulb"),
        # Projects
        (("projeto", "projetos"), "LiFolders"),
        (("ingresso", "ticket"), "LiTicket"),
        (("ttrpg", "rpg"), "LiDices"),
        # Tech stack
        (("aws", "cloud"), "LiCloud"),
        (("n8n", "workflow"), "LiWorkflow"),
        (("python", "codigo", "codigos", "code"), "LiCode2"),
        (("api",), "LiPlug"),
        (("sql", "banco", "database"), "LiDatabase"),
        (("powerbi", "dashboard", "bi"), "LiBarChart3"),
        (("git",), "LiGitBranch"),
        # Resources / assets
        (("recursos",), "LiLibrary"),
        (("assets", "asset"), "LiImage"),
        (("attachments", "anexo"), "LiPaperclip"),
        (("excalidraw",), "LiPencilRuler"),
        (("templates", "template"), "LiFileTemplate"),
        (("biblioteca", "book", "novel"), "LiBookOpen"),
        (("cozinha", "receita"), "LiChefHat"),
        (("aba006", "mvt019", "mvt020", "brg067", "hkc001"), "LiFolderKanban"),
        (("trash",), "LiTrash2"),
    ]
    for kws, icon in rules:
        if has_any(*kws):
            return icon, "rule"
    return "LiFolder", "fallback"


def main() -> None:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    settings = data.get("settings", {})
    existing = {k: v for k, v in data.items() if k != "settings"}

    all_dirs: list[str] = []
    for p in ROOT.rglob("*"):
        if not p.is_dir():
            continue
        rel = p.relative_to(ROOT)
        parts = rel.parts
        if not parts:
            continue
        if any(x in EXCLUDE for x in parts):
            continue
        all_dirs.append(str(rel).replace("\\", "/"))

    all_dirs = sorted(set(all_dirs))

    merged = dict(existing)
    added = 0
    updated = 0
    icon_suggestions: list[dict[str, str]] = []
    for d in all_dirs:
        inferred, source = infer_icon(d)
        if d not in merged:
            merged[d] = inferred
            added += 1
        else:
            if merged[d] != inferred:
                merged[d] = inferred
                updated += 1
        if source == "fallback":
            icon_suggestions.append(
                {
                    "path": d,
                    "icon_sugerido": "LiFolderOpen",
                    "motivo": "contexto novo sem regra específica de override/token",
                }
            )

    out = {"settings": settings}
    for k in sorted(merged.keys(), key=lambda x: x.lower()):
        out[k] = merged[k]

    DATA_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    suggestion_payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "suggestions_count": len(icon_suggestions),
        "suggestions": sorted(icon_suggestions, key=lambda x: x["path"].lower()),
    }
    suggestions_path = REPORTS_DIR / "icon-suggestions-latest.json"
    suggestions_path.write_text(json.dumps(suggestion_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("folders_total", len(all_dirs))
    print("icons_existing", len(existing))
    print("icons_added", added)
    print("icons_updated", updated)
    print("icons_final", len(merged))
    print("icon_suggestions_count", len(icon_suggestions))
    print("icon_suggestions_report", suggestions_path)


if __name__ == "__main__":
    main()
