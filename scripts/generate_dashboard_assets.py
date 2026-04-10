from __future__ import annotations

import base64
import calendar
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any, cast
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape


_ICON_CACHE: dict[str, str] = {}

SKILLICONS_BASE_URL = "https://skillicons.dev/icons?i="
SKILLICONS_USER_AGENT = "mentorzx-profile-assets"
GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_ACCEPT_HEADER = "application/vnd.github+json"
GITHUB_USER_AGENT = "mentorzx-profile-dashboard"
PROFILE_ASSET_ROOT_ENV = "PROFILE_ASSET_ROOT"
SUMMARY_ASSET_NAME = "dashboard-summary.svg"
ENGINEERING_MATRIX_ASSET_NAME = "engineering-matrix.svg"
HERO_ASSET_NAME = "hero-banner.svg"
DEFAULT_MONTH_COUNT = 12
RECENCY_LIVE_DAYS = 30
RECENCY_WARM_DAYS = 90
RECENCY_STABLE_DAYS = 180
SIGNAL_FRESHNESS_CAP_DAYS = 120
SPACE_2XS = 4
SPACE_XS = 8
SPACE_SM = 16
SPACE_MD = 24
SPACE_LG = 32
SPACE_XL = 64
SUITE_WIDTH = 1280
SUITE_HEIGHT = 1600
SUITE_INNER_WIDTH = 1244
PROJECT_CARD_WIDTH = 680
PROJECT_CARD_HEIGHT = 304


def get_skillicon_base64(icon_name: str) -> str:
    if icon_name in _ICON_CACHE:
        return _ICON_CACHE[icon_name]
    url = f"{SKILLICONS_BASE_URL}{icon_name}"
    try:
        req = Request(url, headers={"User-Agent": SKILLICONS_USER_AGENT})
        with urlopen(req) as resp:
            svg_data = resp.read()
            encoded = base64.b64encode(svg_data).decode("utf-8")
            data_uri = f"data:image/svg+xml;base64,{encoded}"
            _ICON_CACHE[icon_name] = data_uri
            return data_uri
    except Exception as e:
        print(f"Error fetching icon {icon_name}: {e}")
        return url


OWNER = os.getenv("GITHUB_USER", "Mentorzx")
TOKEN = os.getenv("METRICS_TOKEN") or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")

DEFAULT_ROOT = Path(__file__).resolve().parents[1]

CANVAS_BG = "#111827"
SURFACE_BG = "#0B1220"
CARD_BG = "#0F172A"
BORDER = "#23314D"
TEXT = "#E5E7EB"
MUTED = "#94A3B8"
SOFT_TEXT = "#CBD5E1"
ACCENT = "#60A5FA"
ACCENT_ALT = "#38BDF8"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
VIOLET = "#A78BFA"
TEAL = "#2DD4BF"

LANGUAGE_NORMALIZATION = {
    "Batchfile": "Shell",
    "Cython": "Python",
    "Dockerfile": "Shell",
    "HTML": "HTML",
    "Jupyter Notebook": "Python",
    "PowerShell": "Shell",
    "Shell": "Shell",
}

LANGUAGE_META = {
    "C": {
        "abbr": "C",
        "color": "#555555",
        "text": "#F8FAFC",
        "icon": "c",
    },
    "C++": {
        "abbr": "C++",
        "color": "#F34B7D",
        "text": "#F8FAFC",
        "icon": "cpp",
    },
    "C#": {
        "abbr": "C#",
        "color": "#178600",
        "text": "#F8FAFC",
        "icon": "cs",
    },
    "CSS": {
        "abbr": "CSS",
        "color": "#563D7C",
        "text": "#F8FAFC",
        "icon": "css",
    },
    "Cython": {
        "abbr": "Cy",
        "color": "#FEDF5B",
        "text": "#111827",
        "icon": "py",
    },
    "HTML": {
        "abbr": "H",
        "color": "#E34C26",
        "text": "#F8FAFC",
        "icon": "html",
    },
    "Java": {
        "abbr": "Jv",
        "color": "#B07219",
        "text": "#F8FAFC",
        "icon": "java",
    },
    "JavaScript": {
        "abbr": "JS",
        "color": "#F1E05A",
        "text": "#111827",
        "icon": "js",
    },
    "MATLAB": {
        "abbr": "Mb",
        "color": "#E16737",
        "text": "#F8FAFC",
        "icon": "matlab",
    },
    "Other": {
        "abbr": "..",
        "color": "#475569",
        "text": "#F8FAFC",
        "icon": "bash",
    },
    "Python": {
        "abbr": "Py",
        "color": "#3572A5",
        "text": "#F8FAFC",
        "icon": "py",
    },
    "Rust": {
        "abbr": "Rs",
        "color": "#DEA584",
        "text": "#111827",
        "icon": "rust",
    },
    "Shell": {
        "abbr": "Sh",
        "color": "#89E051",
        "text": "#0F172A",
        "icon": "bash",
    },
    "TypeScript": {
        "abbr": "TS",
        "color": "#3178C6",
        "text": "#F8FAFC",
        "icon": "ts",
    },
}

REPO_DOMAIN_OVERRIDES = {
    "audcifra": "ai-data",
    "calcnumaval1": "ai-data",
    "compvision": "ai-data",
    "formae": "product",
    "hermes": "ai-data",
    "mcp-register": "backend",
    "production-fix-flow": "backend",
    "siacscrapping": "ai-data",
    "snakeaigame": "ai-data",
}

DOMAIN_ORDER = ["ai-data", "backend", "product"]
DOMAIN_CONFIG = {
    "ai-data": {
        "label": "AI DATA",
        "title": "AI & data engineering",
        "subtitle": "Live byte share from ML, retrieval and data-heavy repos.",
        "accent": ACCENT_ALT,
        "glow": ACCENT_ALT,
    },
    "backend": {
        "label": "BACKEND",
        "title": "Backend engineering",
        "subtitle": ("Live byte share from APIs, orchestration and telemetry repos."),
        "accent": TEAL,
        "glow": TEAL,
    },
    "product": {
        "label": "PRODUCT",
        "title": "Product & platform",
        "subtitle": ("Live byte share from product, extension and web delivery repos."),
        "accent": VIOLET,
        "glow": VIOLET,
    },
}

SURFACE_LANGUAGE_IGNORED = {
    "CSS",
    "Fortran",
    "HTML",
    "Lua",
    "Smarty",
    "Tcl",
    "XSLT",
}

STACK_MAP_GROUPS = [
    (
        "AI Engineering",
        [
            "Embeddings",
            "Sentence Transformers",
            "Transformers",
            "LangChain",
            "Vector Search",
            "LightGBM",
            "GNN",
            "RotatE",
            "AnyBURL",
            "PyClause",
            "MATLAB",
            "Prolog",
        ],
        WARNING,
    ),
    (
        "Data Engineering",
        [
            "Python",
            "SQL",
            "NoSQL",
            "PostgreSQL",
            "SQLite",
            "Cassandra",
            "Kafka",
            "FAISS",
        ],
        ACCENT_ALT,
    ),
    (
        "Backend Engineering",
        [
            "FastAPI",
            "Flask",
            "Node.js",
            ".NET",
            "Redis",
            "Web Services",
            "CRUD",
            "Architectures",
            "Oracle",
        ],
        TEAL,
    ),
    (
        "Front-end",
        [
            "HTML",
            "CSS",
            "JavaScript",
            "TypeScript",
            "React",
            "React Native",
            "Tailwind",
            "Vite",
            "Android",
            "PWA",
            "MV3",
        ],
        VIOLET,
    ),
    (
        "DevOps",
        [
            "Linux",
            "Windows",
            "GitHub",
            "GitHub Actions",
            "Docker",
            "AWS",
            "Grafana",
            "Elasticsearch",
            "Logstash",
            "Kibana",
            "Zabbix",
            "Pytest",
            "Mypy",
            "Scrum",
        ],
        SUCCESS,
    ),
]

PRIMARY_STACK_ITEMS = [
    ("Python", "py", "#3572A5"),
    ("Rust", "rust", "#DEA584"),
    ("C", "c", "#A8B9CC"),
    ("C++", "cpp", "#F34B7D"),
    ("Java", "java", "#B07219"),
    ("Shell", "bash", "#89E051"),
]

SECONDARY_STACK_ITEMS = [
    ("SQL", None, "#0EA5E9"),
    ("Linux", "linux", "#F59E0B"),
    ("Kafka", "kafka", "#F97316"),
    ("GitHub Actions", "githubactions", "#2088FF"),
    ("Docker", "docker", "#2496ED"),
    ("Web Services", None, "#38BDF8"),
]

STACK_ITEM_META = {
    "Python": {"icon": "py", "color": "#3572A5"},
    "Rust": {"icon": "rust", "color": "#DEA584"},
    "C": {"icon": "c", "color": "#A8B9CC"},
    "C++": {"icon": "cpp", "color": "#F34B7D"},
    "C#": {"icon": "cs", "color": "#178600"},
    "Java": {"icon": "java", "color": "#B07219"},
    "Shell": {"icon": "bash", "color": "#89E051"},
    "SQL": {"icon": None, "color": "#0EA5E9"},
    "NoSQL": {"icon": None, "color": "#06B6D4"},
    "Kafka": {"icon": "kafka", "color": "#F97316"},
    "Oracle": {"icon": None, "color": "#DC2626"},
    "PostgreSQL": {"icon": "postgres", "color": "#4169E1"},
    "SQLite": {"icon": None, "color": "#0F766E"},
    "Cassandra": {"icon": "cassandra", "color": "#1287B1"},
    "JavaScript": {"icon": "js", "color": "#F1E05A"},
    "HTML": {"icon": "html", "color": "#E34C26"},
    "CSS": {"icon": "css", "color": "#563D7C"},
    "TypeScript": {"icon": "ts", "color": "#3178C6"},
    "React": {"icon": "react", "color": "#61DAFB"},
    "React Native": {"icon": "react", "color": "#61DAFB"},
    "Tailwind": {"icon": "tailwind", "color": "#38BDF8"},
    "Vite": {"icon": "vite", "color": "#646CFF"},
    "PWA": {"icon": None, "color": "#22C55E"},
    "MV3": {"icon": None, "color": "#A855F7"},
    "Android": {"icon": "androidstudio", "color": "#3DDC84"},
    "Linux": {"icon": "linux", "color": "#F59E0B"},
    "Windows": {"icon": "windows", "color": "#0EA5E9"},
    "Docker": {"icon": "docker", "color": "#2496ED"},
    "GitHub": {"icon": "github", "color": "#E5E7EB"},
    "GitHub Actions": {"icon": "githubactions", "color": "#2088FF"},
    "AWS": {"icon": "aws", "color": "#F59E0B"},
    "Grafana": {"icon": "grafana", "color": "#F97316"},
    "Elasticsearch": {"icon": None, "color": "#F59E0B"},
    "Logstash": {"icon": None, "color": "#A78BFA"},
    "Kibana": {"icon": None, "color": "#38BDF8"},
    "Zabbix": {"icon": None, "color": "#DC2626"},
    "Pytest": {"icon": "pytest", "color": "#22C55E"},
    "Mypy": {"icon": None, "color": "#A78BFA"},
    "Scrum": {"icon": None, "color": "#38BDF8"},
    "Embeddings": {"icon": None, "color": "#22C55E"},
    "Sentence Transformers": {"icon": None, "color": "#14B8A6"},
    "Transformers": {"icon": None, "color": "#F59E0B"},
    "LangChain": {"icon": None, "color": "#10B981"},
    "Vector Search": {"icon": None, "color": "#2DD4BF"},
    "Knowledge Graphs": {"icon": None, "color": "#8B5CF6"},
    "XAI": {"icon": None, "color": "#F97316"},
    "Pipelines": {"icon": None, "color": "#EAB308"},
    "TransE": {"icon": None, "color": "#8B5CF6"},
    "LightGBM": {"icon": None, "color": "#22C55E"},
    "GNN": {"icon": None, "color": "#06B6D4"},
    "RotatE": {"icon": None, "color": "#8B5CF6"},
    "AnyBURL": {"icon": None, "color": "#38BDF8"},
    "PyClause": {"icon": None, "color": "#F472B6"},
    "MATLAB": {"icon": "matlab", "color": "#E16737"},
    "Prolog": {"icon": None, "color": "#6366F1"},
    "FAISS": {"icon": None, "color": "#22C55E"},
    "Scraping": {"icon": None, "color": "#F97316"},
    "Automation": {"icon": None, "color": "#38BDF8"},
    "Telemetry": {"icon": None, "color": "#A78BFA"},
    "Semantic Search": {"icon": None, "color": "#38BDF8"},
    "CRUD": {"icon": None, "color": "#F59E0B"},
    "Architectures": {"icon": None, "color": "#CBD5E1"},
    "Local-first": {"icon": None, "color": "#22C55E"},
    "Rust/WASM": {"icon": "rust", "color": "#DEA584"},
    "PWA + MV3": {"icon": None, "color": "#A855F7"},
    "Product UX": {"icon": None, "color": "#F472B6"},
    "Audio ML": {"icon": None, "color": "#38BDF8"},
    "Async processing": {"icon": None, "color": "#2DD4BF"},
    "Structured export": {"icon": None, "color": "#CBD5E1"},
    "SVM": {"icon": None, "color": "#F59E0B"},
    "NLP": {"icon": None, "color": "#60A5FA"},
    "API delivery": {"icon": None, "color": "#CBD5E1"},
    "Notion sync": {"icon": None, "color": "#E5E7EB"},
    "FastAPI": {"icon": "fastapi", "color": "#059669"},
    "Flask": {"icon": "flask", "color": "#E5E7EB"},
    "Node.js": {"icon": "nodejs", "color": "#22C55E"},
    ".NET": {"icon": "dotnet", "color": "#8B5CF6"},
    "Redis": {"icon": "redis", "color": "#DC382D"},
    "Web Services": {"icon": None, "color": "#38BDF8"},
}

PROJECT_CARD_CONFIG = [
    {
        "filename": "production-fix-flow-card.svg",
        "repo": "production-fix-flow",
        "label": "AI + BACKEND",
        "accent": SUCCESS,
        "glow": ACCENT_ALT,
        "summary": "Validation-first orchestration for APIs, automations, telemetry and knowledge-backed runtime decisions.",
        "proof": ["TransE", "LightGBM", "Automation", "XAI"],
        "stack": ["Python", "FastAPI", "Kafka", "PostgreSQL", "Docker"],
    },
    {
        "filename": "mcp-register-card.svg",
        "repo": "MCP-register",
        "label": "VECTOR SEARCH",
        "accent": TEAL,
        "glow": ACCENT_ALT,
        "summary": "Local semantic registration service with embeddings, CRUD flows and vector lookup.",
        "proof": ["Embeddings", "Vector Search", "Semantic Search", "CRUD"],
        "stack": ["Python", "SQLite", "Vector Search", "Web Services"],
    },
    {
        "filename": "formae-card.svg",
        "repo": "formae",
        "label": "PRODUCT SYSTEM",
        "accent": VIOLET,
        "glow": ACCENT_ALT,
        "summary": "Local-first academic product with browser privacy, shared systems core and PWA delivery.",
        "proof": ["Rust/WASM", "Local-first", "PWA + MV3", "Product UX"],
        "stack": ["TypeScript", "React", "Vite", "Rust", "PWA"],
    },
    {
        "filename": "audcifra-card.svg",
        "repo": "AudCifra",
        "label": "PIPELINE",
        "accent": WARNING,
        "glow": "#FB7185",
        "summary": "Audio pipeline for transcription, chord detection and structured document export.",
        "proof": ["Pipelines", "Audio ML", "Async processing", "Structured export"],
        "stack": ["Python", "Shell", "Web Services"],
    },
    {
        "filename": "hermes-card.svg",
        "repo": "Hermes",
        "label": "NLP API",
        "accent": "#A78BFA",
        "glow": "#A78BFA",
        "summary": "Tweet sentiment and figurative-language analysis exposed through a simple API.",
        "proof": ["SVM", "1.6M tweets", "NLP", "API delivery"],
        "stack": ["Python", "Flask", "SQL", "Web Services"],
    },
    {
        "filename": "siacscrapping-card.svg",
        "repo": "SiacScrapping",
        "label": "AUTOMATION",
        "accent": "#F97316",
        "glow": "#F59E0B",
        "summary": "Scraping and workflow automation that synchronizes operational data into Notion flows.",
        "proof": ["Scraping", "Automation", "Pipelines", "Notion sync"],
        "stack": ["Python", "C", "Shell"],
    },
]


def github_headers() -> dict[str, str]:
    headers = {
        "Accept": GITHUB_ACCEPT_HEADER,
        "User-Agent": GITHUB_USER_AGENT,
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def github_json(url: str) -> Any:
    request = Request(url, headers=github_headers())
    with urlopen(request) as response:
        return json.load(response)


def github_paginated(url: str) -> list[dict[str, Any]]:
    page = 1
    results: list[dict[str, Any]] = []
    while True:
        batch = cast(list[dict[str, Any]], github_json(f"{url}&page={page}"))
        if not batch:
            break
        results.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return results


def resolve_output_dirs(
    output_root: Path | None = None,
) -> tuple[Path, Path]:
    root_env = os.getenv(PROFILE_ASSET_ROOT_ENV)
    root = output_root or (Path(root_env) if root_env else DEFAULT_ROOT)
    metrics_dir = root / "assets" / "metrics"
    architecture_dir = root / "assets" / "profile" / "architecture"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    architecture_dir.mkdir(parents=True, exist_ok=True)
    return metrics_dir, architecture_dir


def estimate_text_width(
    value: str,
    *,
    font_size: int,
    letter_spacing: float = 0,
) -> int:
    glyph_units = 0.0
    for char in value:
        if char in {" ", ".", "/", "|"}:
            glyph_units += 0.34
        elif char in {"-", "_"}:
            glyph_units += 0.42
        elif char.isupper():
            glyph_units += 0.68
        elif char.isdigit():
            glyph_units += 0.56
        else:
            glyph_units += 0.58
    spacing_units = max(0, len(value) - 1) * letter_spacing
    return int(glyph_units * font_size + spacing_units)


def chip_width(
    label: str,
    *,
    font_size: int = 11,
    has_icon: bool = False,
) -> int:
    text_width = estimate_text_width(label, font_size=font_size)
    icon_width = 22 if has_icon else 0
    return 30 + text_width + icon_width


def section_kicker(
    x: int,
    y: int,
    label: str,
    width: int,
) -> list[str]:
    return [
        rect(x, y, width, 22, SURFACE_BG, radius=9, stroke="#22314A"),
        text(
            x + width // 2,
            y + 15,
            label.upper(),
            size=10,
            weight=700,
            fill=MUTED,
            anchor="middle",
            letter_spacing=1.2,
        ),
    ]


def tech_meta(label: str) -> dict[str, str | None]:
    meta = STACK_ITEM_META.get(label)
    if meta is not None:
        return meta
    return {
        "icon": None,
        "color": "#64748B",
    }


def tech_chip(
    x: int,
    y: int,
    label: str,
    *,
    font_size: int = 11,
    height: int = 26,
    fill: str = SURFACE_BG,
    stroke: str = "#1E293B",
    fill_opacity: float | None = None,
    tint_bg: bool = False,
) -> tuple[str, int]:
    meta = tech_meta(label)
    icon_name = cast(str | None, meta["icon"])
    color = cast(str, meta["color"])
    has_icon = icon_name is not None
    width = chip_width(label, font_size=font_size, has_icon=has_icon)
    content_y = y + (height - 16) // 2
    parts = [
        rect(
            x,
            y,
            width,
            height,
            fill,
            radius=min(10, height // 2),
            stroke=stroke,
            fill_opacity=fill_opacity,
        )
    ]
    cursor = x + 12
    if icon_name is not None:
        parts.append(
            f'<image href="{get_skillicon_base64(icon_name)}" '
            f'x="{cursor}" y="{content_y}" width="16" height="16" />'
        )
        cursor += 22
    else:
        parts.append(
            f'<circle cx="{cursor + 4}" cy="{y + height // 2}" r="4" fill="{color}" opacity="0.92" />'
        )
        cursor += 14
    parts.append(
        text(
            cursor,
            y + height // 2 + 4,
            label,
            size=font_size,
            weight=600,
            fill=color if tint_bg else TEXT,
        )
    )
    return "".join(parts), width


def layout_chip_rows(
    labels: list[str],
    *,
    max_width: int,
    gap_x: int = 8,
    font_size: int = 11,
) -> list[list[tuple[str, int]]]:
    rows: list[list[tuple[str, int]]] = []
    row: list[tuple[str, int]] = []
    row_width = 0

    for label in labels:
        has_icon = cast(str | None, tech_meta(label)["icon"]) is not None
        width = chip_width(label, font_size=font_size, has_icon=has_icon)
        projected_width = width if not row else row_width + gap_x + width
        if row and projected_width > max_width:
            rows.append(row)
            row = [(label, width)]
            row_width = width
            continue
        row.append((label, width))
        row_width = projected_width

    if row:
        rows.append(row)
    return rows


def render_chip_rows(
    x: int,
    y: int,
    rows: list[list[tuple[str, int]]],
    *,
    max_width: int,
    gap_x: int = 8,
    gap_y: int = 8,
    chip_height: int = 26,
    font_size: int = 11,
    justify: bool = False,
    justify_last_row: bool = False,
    tint_bg: bool = False,
) -> tuple[list[str], int]:
    parts: list[str] = []
    cursor_y = y
    max_extra_gap = 18

    for row_index, row in enumerate(rows):
        cursor_x = x
        used_width = sum(width for _, width in row)
        base_gaps = max(0, len(row) - 1) * gap_x
        extra_gap = 0.0
        if (
            justify
            and (row_index < len(rows) - 1 or justify_last_row)
            and len(row) > 1
            and used_width + base_gaps < max_width
        ):
            extra_gap = min(
                max_extra_gap,
                (max_width - used_width - base_gaps) / max(1, len(row) - 1),
            )

        for chip_index, (label, width) in enumerate(row):
            fill = cast(str, tech_meta(label)["color"]) if tint_bg else SURFACE_BG
            fill_opacity = 0.1 if tint_bg else None
            chip_svg, _ = tech_chip(
                int(round(cursor_x)),
                cursor_y,
                label,
                font_size=font_size,
                height=chip_height,
                fill=fill,
                fill_opacity=fill_opacity,
                tint_bg=tint_bg,
            )
            parts.append(chip_svg)
            cursor_x += width
            if chip_index < len(row) - 1:
                cursor_x += gap_x + extra_gap

        cursor_y += chip_height + gap_y

    used_height = max(
        chip_height,
        cursor_y - y - gap_y,
    )
    return parts, used_height


def flow_tech_chips(
    x: int,
    y: int,
    labels: list[str],
    *,
    max_width: int,
    gap_x: int = 8,
    gap_y: int = 8,
    chip_height: int = 26,
    font_size: int = 11,
    justify: bool = False,
    justify_last_row: bool = False,
) -> tuple[list[str], int]:
    rows = layout_chip_rows(
        labels,
        max_width=max_width,
        gap_x=gap_x,
        font_size=font_size,
    )
    return render_chip_rows(
        x,
        y,
        rows,
        max_width=max_width,
        gap_x=gap_x,
        gap_y=gap_y,
        chip_height=chip_height,
        font_size=font_size,
        justify=justify,
        justify_last_row=justify_last_row,
    )


def rect(
    x: int,
    y: int,
    width: int,
    height: int,
    fill: str,
    radius: int = 20,
    stroke: str | None = None,
    stroke_width: float = 1,
    opacity: float | None = None,
    fill_opacity: float | None = None,
) -> str:
    extra: list[str] = []
    if stroke:
        extra.append(f' stroke="{stroke}" stroke-width="{stroke_width}"')
    if opacity is not None:
        extra.append(f' opacity="{opacity}"')
    if fill_opacity is not None:
        extra.append(f' fill-opacity="{fill_opacity}"')
    attrs = "".join(extra)
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="{radius}" fill="{fill}"{attrs} />'
    )


def text(
    x: int,
    y: int,
    value: str,
    size: int = 16,
    weight: int = 400,
    fill: str = TEXT,
    anchor: str = "start",
    letter_spacing: float | None = None,
) -> str:
    spacing = ""
    if letter_spacing is not None:
        spacing = f' letter-spacing="{letter_spacing}"'
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}"{spacing}>'
        f"{escape(value)}</text>"
    )


def multiline_text(
    x: int,
    y: int,
    lines: list[str],
    *,
    size: int = 14,
    weight: int = 400,
    fill: str = MUTED,
    line_gap: int = 16,
) -> str:
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_gap
        tspans.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
        f'font-weight="{weight}">{"".join(tspans)}</text>'
    )


def wrap_text_lines(
    value: str,
    *,
    max_width: int,
    font_size: int,
) -> list[str]:
    words = value.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if estimate_text_width(candidate, font_size=font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def animated_bar(
    x: int,
    y: int,
    width: int,
    height: int,
    fill: str,
    opacity: float,
    x_values: str,
    duration: str,
) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="{height // 2}" fill="{fill}" opacity="{opacity}">'
        f'<animate attributeName="x" values="{x_values}" dur="{duration}" '
        'repeatCount="indefinite" />'
        '<animate attributeName="opacity" values="0.14;0.52;0.14" '
        f'dur="{duration}" repeatCount="indefinite" /></rect>'
    )


def animated_circle(
    x: int,
    y: int,
    radius: int,
    fill: str,
    values: str,
    duration: str,
    opacity: float | None = None,
) -> str:
    opacity_attr = f' opacity="{opacity}"' if opacity is not None else ""
    return (
        f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}"'
        f"{opacity_attr}>"
        f'<animate attributeName="opacity" values="{values}" '
        f'dur="{duration}" repeatCount="indefinite" /></circle>'
    )


def parse_timestamp(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def month_sequence(
    now: dt.datetime,
    total_months: int = DEFAULT_MONTH_COUNT,
) -> list[dt.date]:
    months: list[dt.date] = []
    current_total = now.year * 12 + (now.month - 1)
    for offset in range(total_months - 1, -1, -1):
        year, month_index = divmod(current_total - offset, 12)
        months.append(dt.date(year, month_index + 1, 1))
    return months


def compact_label(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return f"{value[: limit - 1]}..."


def relative_age(days: int) -> str:
    if days < 30:
        return f"{days}d ago"
    if days < 365:
        return f"{max(1, days // 30)}mo ago"
    return f"{max(1, days // 365)}y ago"


def normalize_language(language: str) -> str:
    return LANGUAGE_NORMALIZATION.get(language, language)


def language_meta(language: str) -> dict[str, str]:
    if language in LANGUAGE_META:
        return LANGUAGE_META[language]
    abbreviation = language[:2].upper() if len(language) > 2 else language.upper()
    return {
        "abbr": abbreviation,
        "color": "#475569",
        "text": "#F8FAFC",
        "icon": "bash",
    }


def repo_domain(repo: dict[str, Any]) -> str:
    name = str(repo["name"]).lower()
    if name in REPO_DOMAIN_OVERRIDES:
        return REPO_DOMAIN_OVERRIDES[name]

    blob_parts = [name, str(repo.get("description") or "")]
    blob_parts.extend(str(topic) for topic in (repo.get("topics") or []))
    blob = " ".join(blob_parts).lower()

    product_keywords = (
        "browser",
        "frontend",
        "mv3",
        "pwa",
        "react",
        "tailwind",
        "vite",
        "web",
    )
    backend_keywords = (
        "api",
        "backend",
        "docker",
        "fastapi",
        "fastmcp",
        "mcp",
        "redis",
    )
    ai_keywords = (
        "ai",
        "analytics",
        "audio",
        "data",
        "ml",
        "nlp",
        "postgresql",
        "vector",
        "vision",
    )

    if any(keyword in blob for keyword in product_keywords):
        return "product"
    if any(keyword in blob for keyword in backend_keywords):
        return "backend"
    if any(keyword in blob for keyword in ai_keywords):
        return "ai-data"

    primary_language = normalize_language(str(repo.get("language") or ""))
    if primary_language in {"CSS", "HTML", "JavaScript", "Rust", "TypeScript"}:
        return "product"
    if primary_language in {"Python", "Cython", "MATLAB"}:
        return "ai-data"
    return "backend"


def public_repositories(repos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    public_repos = [repo for repo in repos if not repo.get("fork")]
    return sorted(
        public_repos,
        key=lambda repo: parse_timestamp(str(repo["updated_at"])),
        reverse=True,
    )


def fetch_repo_languages(
    repos: list[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    repo_languages: dict[str, dict[str, int]] = {}
    for repo in repos:
        name = str(repo["name"])
        if name.lower() == OWNER.lower():
            continue

        normalized: dict[str, int] = {}
        try:
            payload = cast(
                dict[str, Any],
                github_json(str(repo["languages_url"])),
            )
        except Exception:
            payload = {}

        for language, size in payload.items():
            normalized_name = normalize_language(str(language))
            normalized[normalized_name] = normalized.get(normalized_name, 0) + int(size)

        if not normalized and repo.get("language"):
            primary_language = normalize_language(str(repo["language"]))
            normalized[primary_language] = 1

        repo_languages[name] = normalized
    return repo_languages


def surface_language_totals(
    repo_languages: dict[str, dict[str, int]],
) -> list[tuple[str, int, int]]:
    totals: dict[str, int] = {}
    repo_counts: dict[str, int] = {}
    for languages in repo_languages.values():
        seen: set[str] = set()
        for language, size in languages.items():
            if language in SURFACE_LANGUAGE_IGNORED:
                continue
            normalized = normalize_language(language)
            totals[normalized] = totals.get(normalized, 0) + int(size)
            if normalized not in seen:
                repo_counts[normalized] = repo_counts.get(normalized, 0) + 1
                seen.add(normalized)
    ordered = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    return [
        (language, size, repo_counts.get(language, 0)) for language, size in ordered
    ]


def domain_language_totals(
    repos: list[dict[str, Any]],
    repo_languages: dict[str, dict[str, int]],
) -> dict[str, dict[str, Any]]:
    domains: dict[str, dict[str, Any]] = {}
    for domain_key in DOMAIN_ORDER:
        domains[domain_key] = {"repos": [], "languages": {}}

    for repo in repos:
        name = str(repo["name"])
        if name.lower() == OWNER.lower():
            continue

        domain_key = repo_domain(repo)
        domains[domain_key]["repos"].append(name)

        for language, size in repo_languages.get(name, {}).items():
            current = int(domains[domain_key]["languages"].get(language, 0))
            domains[domain_key]["languages"][language] = current + int(size)

    return domains


def top_language_rows(
    language_totals: dict[str, int],
    row_limit: int = 4,
) -> list[tuple[str, float]]:
    ordered = sorted(
        language_totals.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    if not ordered:
        return [("Other", 100.0)]

    total = sum(size for _, size in ordered)
    display = ordered
    if len(ordered) > row_limit:
        remainder = sum(size for _, size in ordered[row_limit - 1 :])
        display = ordered[: row_limit - 1]
        display.append(("Other", remainder))

    return [
        (language, (size / total * 100) if total else 0.0) for language, size in display
    ]


def monthly_activity_counts(
    repos: list[dict[str, Any]],
    now: dt.datetime,
) -> tuple[list[dt.date], list[int]]:
    months = month_sequence(now)
    counts: list[int] = []
    for month_start in months:
        count = 0
        for repo in repos:
            updated = parse_timestamp(str(repo["updated_at"])).date()
            if updated.year == month_start.year and updated.month == month_start.month:
                count += 1
        counts.append(count)
    return months, counts


def recency_bucket_counts(
    repos: list[dict[str, Any]],
    now: dt.datetime,
) -> list[tuple[str, int, str]]:
    live = 0
    warm = 0
    stable = 0
    watch = 0
    for repo in repos:
        updated = parse_timestamp(str(repo["updated_at"]))
        days = max((now - updated).days, 0)
        if days <= RECENCY_LIVE_DAYS:
            live += 1
        elif days <= RECENCY_WARM_DAYS:
            warm += 1
        elif days <= RECENCY_STABLE_DAYS:
            stable += 1
        else:
            watch += 1

    return [
        (f"Live <={RECENCY_LIVE_DAYS}d", live, ACCENT_ALT),
        (f"Warm <={RECENCY_WARM_DAYS}d", warm, TEAL),
        (f"Stable <={RECENCY_STABLE_DAYS}d", stable, WARNING),
        (f"Watch >{RECENCY_STABLE_DAYS}d", watch, VIOLET),
    ]


def repo_signal_score(repo: dict[str, Any], now: dt.datetime) -> int:
    updated = parse_timestamp(str(repo["updated_at"]))
    days = max((now - updated).days, 0)
    freshness = max(1, SIGNAL_FRESHNESS_CAP_DAYS - min(days, SIGNAL_FRESHNESS_CAP_DAYS))
    stars = int(repo.get("stargazers_count", 0))
    forks = int(repo.get("forks_count", 0))
    owner_bonus = 50 if str(repo["name"]).lower() == OWNER.lower() else 0
    return freshness + stars * 20 + forks * 12 + owner_bonus


def top_repository_rows(
    repos: list[dict[str, Any]],
    now: dt.datetime,
    limit: int = 5,
) -> list[dict[str, Any]]:
    scored_rows: list[dict[str, Any]] = []
    for repo in repos:
        updated = parse_timestamp(str(repo["updated_at"]))
        scored_rows.append(
            {
                "name": str(repo["name"]),
                "days": max((now - updated).days, 0),
                "stars": int(repo.get("stargazers_count", 0)),
                "forks": int(repo.get("forks_count", 0)),
                "score": repo_signal_score(repo, now),
            }
        )

    scored_rows.sort(
        key=lambda row: (int(row["score"]), -int(row["days"]), str(row["name"])),
        reverse=True,
    )
    return scored_rows[:limit]


def generate_summary_svg(
    user: dict[str, Any],
    repos: list[dict[str, Any]],
    now: dt.datetime | None = None,
) -> str:
    now = now or dt.datetime.now(dt.UTC)
    public_repos = public_repositories(repos)
    created = parse_timestamp(str(user["created_at"]))
    active_since = created.strftime("%b %Y")

    public_repo_count = int(user.get("public_repos", len(public_repos)))
    public_stars = sum(int(repo.get("stargazers_count", 0)) for repo in public_repos)
    public_forks = sum(int(repo.get("forks_count", 0)) for repo in public_repos)
    open_issues = sum(int(repo.get("open_issues_count", 0)) for repo in public_repos)
    active_90d = sum(
        1
        for repo in public_repos
        if (now - parse_timestamp(str(repo["updated_at"]))).days <= RECENCY_WARM_DAYS
    )

    months, counts = monthly_activity_counts(public_repos, now)
    max_count = max(counts) if counts else 1
    chart_left = 82
    chart_bottom = 382
    chart_height = 138
    bar_width = 28
    bar_gap = 12

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" shape-rendering="geometricPrecision" '
        'width="1240" height="700" viewBox="0 0 1240 700" '
        'role="img" aria-labelledby="title desc">',
        '<title id="title">GitHub engineering dashboard and telemetry</title>',
        '<desc id="desc">Animated dashboard summarizing repository freshness, public metrics, recency mix and top repository signals for Mentorzx.</desc>',
        "<defs>",
        '<linearGradient id="canvas" x1="40" y1="18" x2="1200" y2="680" '
        'gradientUnits="userSpaceOnUse">',
        f'<stop stop-color="{SURFACE_BG}" />',
        f'<stop offset="1" stop-color="{CANVAS_BG}" />',
        "</linearGradient>",
        '<linearGradient id="surface" x1="18" y1="18" x2="1222" y2="682" '
        'gradientUnits="userSpaceOnUse">',
        '<stop stop-color="#09111F" />',
        f'<stop offset="1" stop-color="{CANVAS_BG}" />',
        "</linearGradient>",
        '<linearGradient id="beam" x1="964" y1="60" x2="1120" y2="60" '
        'gradientUnits="userSpaceOnUse">',
        '<stop stop-color="#22C55E" stop-opacity="0" />',
        '<stop offset="0.5" stop-color="#38BDF8" />',
        '<stop offset="1" stop-color="#60A5FA" stop-opacity="0" />',
        "</linearGradient>",
        '<linearGradient id="activityFill" x1="0" y1="244" x2="0" y2="382" '
        'gradientUnits="userSpaceOnUse">',
        '<stop stop-color="#38BDF8" stop-opacity="0.92" />',
        '<stop offset="1" stop-color="#2DD4BF" stop-opacity="0.48" />',
        "</linearGradient>",
        '<linearGradient id="activityArea" x1="82" y1="244" x2="564" y2="382" '
        'gradientUnits="userSpaceOnUse">',
        '<stop stop-color="#38BDF8" stop-opacity="0.24" />',
        '<stop offset="1" stop-color="#2DD4BF" stop-opacity="0.02" />',
        "</linearGradient>",
        '<linearGradient id="repoFill" x1="320" y1="0" x2="940" y2="0" '
        'gradientUnits="userSpaceOnUse">',
        f'<stop stop-color="{ACCENT}" />',
        f'<stop offset="1" stop-color="{SUCCESS}" />',
        "</linearGradient>",
        '<radialGradient id="glow" cx="0" cy="0" r="1" '
        'gradientUnits="userSpaceOnUse" '
        'gradientTransform="translate(1048 66) rotate(90) scale(202 262)">',
        '<stop stop-color="#38BDF8" stop-opacity="0.22" />',
        '<stop offset="1" stop-color="#38BDF8" stop-opacity="0" />',
        "</radialGradient>",
        "</defs>",
        "<style>",
        "text{font-family:'Segoe UI',Arial,sans-serif}",
        "@media (prefers-reduced-motion: reduce) { * { animation: none !important; opacity: 1 !important; transform: none !important; } }",
        "</style>",
        rect(0, 0, 1240, 700, "url(#canvas)", radius=28),
        animated_circle(
            1048,
            66,
            202,
            "url(#glow)",
            "0.42;0.9;0.42",
            "8.4s",
            opacity=0.82,
        ),
        rect(18, 18, 1204, 664, "url(#surface)", radius=24, stroke=BORDER),
        '<path d="M48 116H1192" stroke="#1E293B" '
        'stroke-dasharray="5 7" opacity="0.56" />',
        rect(48, 40, 210, 28, CARD_BG, radius=14, stroke=BORDER),
        text(
            153,
            58,
            "GITHUB TELEMETRY",
            size=12,
            weight=700,
            fill=MUTED,
            anchor="middle",
            letter_spacing=1.2,
        ),
        text(48, 102, "Engineering dashboard", size=34, weight=700),
        text(
            48,
            128,
            "Public signal, repository freshness and portfolio momentum in one animated board.",
            size=15,
            fill=MUTED,
        ),
        animated_bar(964, 78, 132, 8, "url(#beam)", 0.34, "964;996;964", "9.2s"),
        animated_circle(1140, 82, 4, ACCENT_ALT, "0.35;1;0.35", "4.6s"),
        text(
            1180,
            58,
            f"Active since {active_since}",
            size=15,
            weight=600,
            fill=ACCENT,
            anchor="end",
        ),
        rect(48, 150, 544, 274, CARD_BG, radius=22, stroke=BORDER),
        rect(614, 150, 578, 330, CARD_BG, radius=22, stroke=BORDER),
        rect(48, 500, 1144, 152, CARD_BG, radius=22, stroke=BORDER),
    ]

    parts.extend(section_kicker(70, 168, "Monthly freshness", 170))
    parts.extend(section_kicker(636, 168, "Public signal", 136))
    parts.extend(section_kicker(70, 462, "Top repository signal", 178))
    parts.extend(
        [
            text(70, 208, "Repository freshness trail", size=26, weight=700),
            text(
                70,
                232,
                "Count of public repositories touched in the last 12 months.",
                size=13,
                fill=MUTED,
            ),
            text(636, 208, "Compact telemetry", size=26, weight=700),
            text(
                636,
                232,
                "Public metrics and recency buckets pulled from the live public profile surface.",
                size=13,
                fill=MUTED,
            ),
            text(70, 502, "Top repository signal", size=24, weight=700),
            text(
                1180,
                528,
                "Stars, forks and recency blended into one quick ranking.",
                size=12,
                fill=MUTED,
                anchor="end",
            ),
        ]
    )

    for guide_y in (260, 290, 320, 350, 380):
        parts.append(
            f'<path d="M82 {guide_y}H564" stroke="#1E293B" '
            'stroke-dasharray="4 7" opacity="0.46" />'
        )

    area_points: list[str] = []
    line_points: list[str] = []
    point_centers: list[int] = []
    for index, (month, count) in enumerate(zip(months, counts, strict=False)):
        x = chart_left + index * (bar_width + bar_gap)
        center_x = x + bar_width // 2
        bar_height = (
            8 if count == 0 else max(18, round(chart_height * count / max_count))
        )
        fill_y = chart_bottom - bar_height
        shimmer_y = fill_y + min(5, max(bar_height - 4, 0))
        month_label = calendar.month_abbr[month.month].upper()

        parts.extend(
            [
                rect(
                    x,
                    244,
                    bar_width,
                    chart_height,
                    SURFACE_BG,
                    radius=13,
                    stroke="#162033",
                ),
                rect(x, fill_y, bar_width, bar_height, "url(#activityFill)", radius=13),
                animated_bar(
                    x,
                    shimmer_y,
                    bar_width,
                    4,
                    ACCENT_ALT,
                    0.28,
                    f"{x};{x + 4};{x}",
                    f"{5.0 + index * 0.2:.1f}s",
                ),
                text(
                    center_x,
                    402,
                    month_label,
                    size=11,
                    fill=MUTED,
                    anchor="middle",
                ),
                animated_circle(
                    center_x,
                    fill_y,
                    4,
                    ACCENT_ALT if index % 2 == 0 else TEAL,
                    "0.35;1;0.35",
                    f"{4.6 + index * 0.18:.1f}s",
                ),
            ]
        )
        if count > 0:
            parts.append(
                text(
                    center_x,
                    fill_y - 8,
                    str(count),
                    size=11,
                    weight=700,
                    fill=SOFT_TEXT,
                    anchor="middle",
                )
            )

        point_centers.append(center_x)
        area_points.append(f"{center_x} {fill_y}")
        line_points.append(f"{center_x} {fill_y}")

    if point_centers:
        first_center = point_centers[0]
        last_center = point_centers[-1]
        area_path = (
            f"M {first_center} {chart_bottom} L "
            + " L ".join(area_points)
            + f" L {last_center} {chart_bottom} Z"
        )
        line_path = "M " + " L ".join(line_points)
        parts.extend(
            [
                f'<path d="{area_path}" fill="url(#activityArea)" opacity="0.82" />',
                f'<path d="{line_path}" fill="none" stroke="{ACCENT_ALT}" '
                'stroke-width="2.4" stroke-linecap="round" '
                'stroke-linejoin="round" stroke-dasharray="540" '
                'stroke-dashoffset="540">'
                '<animate attributeName="stroke-dashoffset" values="540;0;0" '
                'dur="8.8s" repeatCount="indefinite" /></path>',
            ]
        )

    metric_cards = [
        ("PUBLIC REPOS", str(public_repo_count), ACCENT),
        ("FOLLOWERS", str(int(user.get("followers", 0))), TEAL),
        ("PUBLIC STARS", str(public_stars), SUCCESS),
        ("PUBLIC FORKS", str(public_forks), WARNING),
        (f"ACTIVE <= {RECENCY_WARM_DAYS}D", str(active_90d), ACCENT_ALT),
        ("OPEN ISSUES", str(open_issues), VIOLET),
    ]
    metric_positions = [
        (636, 254),
        (822, 254),
        (1008, 254),
        (636, 326),
        (822, 326),
        (1008, 326),
    ]

    for index, ((label, value, color), (x, y)) in enumerate(
        zip(metric_cards, metric_positions, strict=False)
    ):
        pill_width = max(90, len(label) * 7 + 26)
        parts.extend(
            [
                rect(x, y, 162, 58, SURFACE_BG, radius=16, stroke="#22314A"),
                rect(
                    x + 12,
                    y + 10,
                    pill_width,
                    16,
                    CARD_BG,
                    radius=8,
                    stroke="#162033",
                ),
                text(
                    x + 12 + pill_width // 2,
                    y + 22,
                    label,
                    size=9,
                    weight=700,
                    fill=MUTED,
                    anchor="middle",
                    letter_spacing=0.8,
                ),
                animated_bar(
                    x + 114,
                    y + 14,
                    24,
                    5,
                    color,
                    0.32,
                    f"{x + 114};{x + 122};{x + 114}",
                    f"{4.8 + index * 0.35:.1f}s",
                ),
                animated_circle(
                    x + 144,
                    y + 16,
                    3,
                    color,
                    "0.35;1;0.35",
                    f"{4.2 + index * 0.25:.1f}s",
                ),
                text(x + 16, y + 46, value, size=24, weight=700),
            ]
        )

    bucket_rows = recency_bucket_counts(public_repos, now)
    bucket_max = max(count for _, count, _ in bucket_rows) or 1
    parts.append(text(636, 408, "Recency mix", size=14, weight=700, fill=SOFT_TEXT))
    for index, (label, count, color) in enumerate(bucket_rows):
        y = 434 + index * 20
        fill_width = 12 if count == 0 else max(24, int(336 * count / bucket_max * 0.9))
        parts.extend(
            [
                text(636, y, label, size=11, weight=600, fill=MUTED),
                rect(764, y - 8, 336, 10, CARD_BG, radius=5, stroke="#162033"),
                rect(764, y - 8, fill_width, 10, color, radius=5, opacity=0.72),
                animated_bar(
                    764,
                    y - 7,
                    min(52, fill_width),
                    8,
                    color,
                    0.34,
                    f"764;{764 + max(fill_width - 52, 0)};764",
                    f"{6.0 + index * 0.3:.1f}s",
                ),
                text(1122, y, str(count), size=11, weight=700, anchor="end"),
            ]
        )

    top_rows = top_repository_rows(public_repos, now)
    max_score = max(int(row["score"]) for row in top_rows) if top_rows else 1
    for index, row in enumerate(top_rows):
        y = 552 + index * 18
        fill_width = max(40, int(620 * int(row["score"]) / max_score * 0.97))
        parts.extend(
            [
                text(70, y, str(row["name"]), size=13, weight=700),
                text(
                    220,
                    y,
                    f'updated {relative_age(int(row["days"]))}',
                    size=11,
                    fill=MUTED,
                ),
                rect(320, y - 9, 620, 10, SURFACE_BG, radius=5, stroke="#162033"),
                rect(320, y - 9, fill_width, 10, "url(#repoFill)", radius=5),
                animated_bar(
                    320,
                    y - 8,
                    64,
                    8,
                    ACCENT_ALT,
                    0.26,
                    f"320;{320 + max(fill_width - 64, 0)};320",
                    f"{6.8 + index * 0.35:.1f}s",
                ),
                animated_circle(
                    320 + fill_width,
                    y - 4,
                    3,
                    SUCCESS,
                    "0.35;1;0.35",
                    f"{4.8 + index * 0.2:.1f}s",
                ),
                rect(968, y - 15, 98, 24, SURFACE_BG, radius=10, stroke="#1E293B"),
                rect(1080, y - 15, 98, 24, SURFACE_BG, radius=10, stroke="#1E293B"),
                text(
                    1017,
                    y + 1,
                    f'STARS {int(row["stars"])}',
                    size=10,
                    weight=700,
                    fill=ACCENT,
                    anchor="middle",
                ),
                text(
                    1129,
                    y + 1,
                    f'FORKS {int(row["forks"])}',
                    size=10,
                    weight=700,
                    fill=SUCCESS,
                    anchor="middle",
                ),
            ]
        )

    recent_surface = ", ".join(str(row["name"]) for row in top_rows[:3])
    parts.extend(
        [
            text(
                48,
                678,
                "Computed from public repositories and profile metadata.",
                size=13,
                fill=MUTED,
            ),
            text(
                1184,
                678,
                f"Recent surface: {recent_surface}",
                size=13,
                fill=MUTED,
                anchor="end",
            ),
            "</svg>",
        ]
    )

    return "".join(parts)


def generate_hero_banner_svg() -> str:
    focus_blocks = [
        (
            "Data + AI systems",
            ["Embeddings, knowledge", "graphs and pipelines."],
            ACCENT_ALT,
        ),
        (
            "Backend engineering",
            ["Service boundaries,", "observability and APIs."],
            TEAL,
        ),
        (
            "Production ops",
            ["Kafka automations,", "Elastic + Zabbix + Linux."],
            WARNING,
        ),
        (
            "Product delivery",
            ["Local-first UX,", "shared systems core and PWA."],
            VIOLET,
        ),
    ]
    hero_typing_phrase = "backend | data / ai | automation"
    padding_x = 26
    hero_typing_width = (
        estimate_text_width(hero_typing_phrase, font_size=13) + padding_x
    )
    hero_cursor_start = 252
    hero_cursor_end = hero_cursor_start + hero_typing_width - 10
    best_fit_lines = [
        "Open to backend, data/AI and automation-heavy roles where execution",
        "and systems thinking matter.",
    ]
    best_fit_height = 15 + max(0, len(best_fit_lines) - 1) * 18
    primary_stack_height = 102
    blue_text_y = 278
    primary_stack_y = blue_text_y + best_fit_height + 28
    best_fit_rect_width = hero_cursor_end - 80 + 26

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" shape-rendering="geometricPrecision" '
        'width="1280" height="500" viewBox="0 0 1280 500" '
        'role="img" aria-labelledby="title desc">',
        '<title id="title">Alex Lira portfolio banner</title>',
        '<desc id="desc">Animated portfolio banner highlighting backend, data, applied AI and local-first product engineering.</desc>',
        "<defs>",
        '<linearGradient id="heroCanvas" x1="48" y1="40" x2="1232" y2="332" gradientUnits="userSpaceOnUse">',
        '<stop stop-color="#081120" />',
        f'<stop offset="1" stop-color="{CANVAS_BG}" />',
        "</linearGradient>",
        '<linearGradient id="heroPanel" x1="48" y1="48" x2="1232" y2="320" gradientUnits="userSpaceOnUse">',
        '<stop stop-color="#09111F" />',
        f'<stop offset="1" stop-color="{CANVAS_BG}" />',
        "</linearGradient>",
        '<radialGradient id="heroGlow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(1028 62) rotate(90) scale(176 248)">',
        '<stop stop-color="#38BDF8" stop-opacity="0.22" />',
        '<stop offset="1" stop-color="#38BDF8" stop-opacity="0" />',
        "</radialGradient>",
        f'<clipPath id="heroTypeClip"><rect x="252" y="208" width="{hero_typing_width}" height="30">'
        f'<animate attributeName="width" values="{hero_typing_width};{hero_typing_width};'
        f'0;0;{hero_typing_width}" '
        'keyTimes="0;0.7;0.8;0.88;1" dur="9.6s" '
        'repeatCount="indefinite" />'
        "</rect></clipPath>",
        "</defs>",
        "<style>",
        "text{font-family:'Segoe UI',Arial,sans-serif}",
        "@media (prefers-reduced-motion: reduce) { * { animation: none !important; opacity: 1 !important; transform: none !important; } }",
        "</style>",
        rect(0, 0, 1280, 500, "url(#heroCanvas)", radius=28),
        animated_circle(
            1028, 62, 176, "url(#heroGlow)", "0.34;0.86;0.34", "8.2s", opacity=0.82
        ),
        rect(48, 48, 1184, 404, "url(#heroPanel)", radius=24, stroke=BORDER),
        '<path d="M78 132H676" stroke="#23314D" stroke-dasharray="4 7" opacity="0.48" />',
        '<path d="M78 202H676" stroke="#23314D" stroke-dasharray="4 7" opacity="0.34" />',
        '<path d="M78 292H676" stroke="#23314D" stroke-dasharray="4 7" opacity="0.24" />',
        '<path d="M78 364H1202" stroke="#23314D" stroke-dasharray="4 7" opacity="0.18" />',
        '<path d="M78 428H1202" stroke="#23314D" stroke-dasharray="4 7" opacity="0.14" />',
    ]

    parts.extend(section_kicker(80, 78, "Hiring snapshot", 188))
    parts.extend(
        [
            text(80, 146, "Alex Lira", size=46, weight=700),
            multiline_text(
                80,
                184,
                [
                    "Backend, data and applied AI engineer shipping reliable",
                    "systems across API, search and product boundaries.",
                ],
                size=18,
                weight=500,
                fill="#D7E2F0",
                line_gap=22,
            ),
            rect(
                80,
                214,
                best_fit_rect_width,
                34,
                SURFACE_BG,
                radius=14,
                stroke="#29476A",
            ),
            '<circle cx="98" cy="231" r="3" fill="#22C55E" opacity="0.92">'
            '<animate attributeName="opacity" values="0.25;1;0.25" dur="2.2s" repeatCount="indefinite" /></circle>',
            '<circle cx="112" cy="231" r="3" fill="#38BDF8" opacity="0.62" />',
            '<circle cx="126" cy="231" r="3" fill="#A78BFA" opacity="0.42" />',
            '<text x="144" y="235" fill="#CBD5E1" font-size="13" font-weight="600" font-family="Consolas, SFMono-Regular, Menlo, monospace">&gt; best fit:</text>',
            multiline_text(
                80,
                blue_text_y,
                best_fit_lines,
                size=15,
                weight=600,
                fill=ACCENT_ALT,
                line_gap=21,
            ),
        ]
    )
    parts.extend(
        [
            '<text x="252" y="235" fill="#38BDF8" font-size="13" '
            'font-weight="700" font-family="Consolas, SFMono-Regular, Menlo, monospace" '
            'clip-path="url(#heroTypeClip)">'
            f"{escape(hero_typing_phrase)}</text>",
            f'<text x="{hero_cursor_start}" y="235" fill="#A5F3FC" '
            'font-size="13" font-weight="700" '
            'font-family="Consolas, SFMono-Regular, Menlo, monospace">|'
            f'<animate attributeName="x" values="{hero_cursor_end};'
            f"{hero_cursor_end};{hero_cursor_start};{hero_cursor_start};"
            f'{hero_cursor_end}" '
            'keyTimes="0;0.7;0.8;0.88;1" dur="9.6s" '
            'repeatCount="indefinite" />'
            '<animate attributeName="opacity" values="1;0.35;1;0.35;1" '
            'dur="0.9s" repeatCount="indefinite" /></text>',
        ]
    )

    block_x = 688
    block_y = 84
    for index, (title_value, subtitle_lines, color) in enumerate(focus_blocks):
        x = block_x + (index % 2) * 232
        y = block_y + (index // 2) * 120
        parts.extend(
            [
                rect(x, y, 214, 104, SURFACE_BG, radius=18, stroke="#22314A"),
                rect(x + 18, y + 16, 14, 14, color, radius=7, opacity=0.92),
                text(x + 44, y + 30, title_value, size=15, weight=700),
                multiline_text(
                    x + 18,
                    y + 62,
                    subtitle_lines,
                    size=12,
                    fill="#AEBCCD",
                    line_gap=21,
                ),
                animated_bar(
                    x + 18,
                    y + 86,
                    72,
                    6,
                    color,
                    0.24,
                    f"{x + 16};{x + 30};{x + 16}",
                    f"{6.0 + index * 0.4:.1f}s",
                ),
            ]
        )

    parts.extend(section_kicker(80, primary_stack_y, "Primary stack", 138))

    gap_x = 12
    gap_y = 12
    max_w = 1100

    chip_x = 80
    chip_y = primary_stack_y + 36
    for label, _, color in PRIMARY_STACK_ITEMS:
        chip_svg, width = tech_chip(chip_x, chip_y, label, height=28, font_size=12)
        if chip_x + width > 80 + max_w:
            chip_x = 80
            chip_y += 28 + gap_y
            chip_svg, width = tech_chip(chip_x, chip_y, label, height=28, font_size=12)
        parts.append(chip_svg.replace('stroke="#1E293B"', f'stroke="{color}"'))
        chip_x += width + gap_x

    chip_x = 80
    chip_y += 28 + 18
    for label, _, color in SECONDARY_STACK_ITEMS:
        chip_svg, width = tech_chip(chip_x, chip_y, label, height=26, font_size=11)
        if chip_x + width > 80 + max_w:
            chip_x = 80
            chip_y += 26 + gap_y
            chip_svg, width = tech_chip(chip_x, chip_y, label, height=26, font_size=11)
        parts.append(chip_svg.replace('stroke="#1E293B"', f'stroke="{color}"'))
        chip_x += width + gap_x

    parts.append("</svg>")
    return "".join(parts)


def generate_engineering_matrix_svg(
    repos: list[dict[str, Any]],
    repo_languages: dict[str, dict[str, int]],
) -> str:
    language_rows = surface_language_totals(repo_languages)[:6]
    language_card_height = 232
    matrix_card_height = 392

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" shape-rendering="geometricPrecision" '
        f'width="{SUITE_WIDTH}" height="{SUITE_HEIGHT}" '
        f'viewBox="0 0 {SUITE_WIDTH} {SUITE_HEIGHT}" '
        'role="img" aria-labelledby="title desc">',
        '<title id="title">Stack, language telemetry and engineering matrix</title>',
        '<desc id="desc">Unified animated block with compact stack map, most used public languages and engineering surface evidence for Mentorzx.</desc>',
        "<defs>",
        '<linearGradient id="suiteCanvas" x1="40" y1="18" x2="1240" y2="1220" gradientUnits="userSpaceOnUse">',
        f'<stop stop-color="{SURFACE_BG}" />',
        f'<stop offset="1" stop-color="{CANVAS_BG}" />',
        "</linearGradient>",
        '<linearGradient id="suiteSurface" x1="18" y1="18" x2="1262" y2="1230" gradientUnits="userSpaceOnUse">',
        '<stop stop-color="#09111F" />',
        f'<stop offset="1" stop-color="{CANVAS_BG}" />',
        "</linearGradient>",
        "</defs>",
        "<style>",
        "text{font-family:'Segoe UI',Arial,sans-serif}",
        "@media (prefers-reduced-motion: reduce) { * { animation: none !important; opacity: 1 !important; transform: none !important; } }",
        "</style>",
        rect(0, 0, SUITE_WIDTH, SUITE_HEIGHT, "url(#suiteCanvas)", radius=28),
        rect(
            18,
            18,
            SUITE_INNER_WIDTH,
            SUITE_HEIGHT - 36,
            "url(#suiteSurface)",
            radius=24,
            stroke=BORDER,
        ),
        '<path d="M48 120H1232" stroke="#1E293B" stroke-dasharray="5 7" opacity="0.56" />',
    ]

    parts.extend(section_kicker(50, 42, "Profile stack suite", 208))
    parts.extend(
        [
            text(
                50,
                88,
                "Compact stack map + language telemetry + engineering matrix",
                size=28,
                weight=700,
            ),
            text(
                50,
                108,
                "Repo data is merged with verified profile and curriculum evidence, then normalized for README readability.",
                size=14,
                fill=MUTED,
            ),
        ]
    )

    parts.extend(section_kicker(50, 140, "Primary stack", 136))

    gap_x = 12
    gap_y = 12
    max_w = 1180

    x = 50
    y = 174
    for label, icon_name, color in PRIMARY_STACK_ITEMS:
        chip_svg, width = tech_chip(x, y, label, height=28, font_size=12)
        if x + width > 50 + max_w:
            x = 50
            y += 28 + gap_y
            chip_svg, width = tech_chip(x, y, label, height=28, font_size=12)
        parts.append(chip_svg.replace('stroke="#1E293B"', f'stroke="{color}"'))
        x += width + gap_x

    x = 50
    y += 28 + 18
    for label, _, color in SECONDARY_STACK_ITEMS:
        chip_svg, width = tech_chip(x, y, label, height=26, font_size=11)
        if x + width > 50 + max_w:
            x = 50
            y += 26 + gap_y
            chip_svg, width = tech_chip(x, y, label, height=26, font_size=11)
        parts.append(chip_svg.replace('stroke="#1E293B"', f'stroke="{color}"'))
        x += width + gap_x

    parts.append(
        '<path d="M48 254H1232" stroke="#1E293B" stroke-dasharray="4 7" opacity="0.42" />'
    )
    parts.extend(section_kicker(50, 272, "Compact stack map", 188))

    row_y = 308
    for label, items, color in STACK_MAP_GROUPS:
        row_height = 84
        parts.append(
            rect(50, row_y, 1180, row_height, CARD_BG, radius=16, stroke="#22314A")
        )
        parts.append(
            rect(50, row_y, 220, row_height, SURFACE_BG, radius=16, stroke="#22314A")
        )
        parts.append(
            rect(66, row_y + 28, 138, 28, CANVAS_BG, radius=14, stroke="#22314A")
        )
        parts.append(
            text(
                135, row_y + 47, label, size=12, weight=700, fill=color, anchor="middle"
            )
        )
        parts.append(
            animated_bar(80, row_y + 62, 96, 4, color, 0.22, "80;108;80", "6.2s")
        )
        chips, used_height = flow_tech_chips(
            282,
            row_y + 16,
            items,
            max_width=936,
            chip_height=26,
            gap_x=12,
            gap_y=12,
        )
        parts.extend(chips)
        row_y += max(row_height, used_height + 32) + 10

    parts.append(
        f'<path d="M48 {row_y + 10}H1232" stroke="#1E293B" stroke-dasharray="4 7" opacity="0.32" />'
    )

    languages_card_y = row_y + 28
    parts.extend(section_kicker(50, languages_card_y, "Most used languages", 188))
    parts.append(
        rect(
            50,
            languages_card_y + 34,
            1180,
            language_card_height,
            CARD_BG,
            radius=22,
            stroke="#22314A",
        )
    )
    parts.append(
        text(
            72, languages_card_y + 74, "Most used public languages", size=24, weight=700
        )
    )
    parts.append(
        text(
            72,
            languages_card_y + 98,
            "Public byte share folded into surface languages, then summarized for fast scanning.",
            size=13,
            fill=MUTED,
        )
    )

    totals_sum = sum(size for _, size, _ in language_rows) or 1
    bar_x = 72
    bar_y = languages_card_y + 126
    bar_width = 1136
    bar_height = 24
    parts.extend(
        [
            '<clipPath id="languageStackClip">',
            f'<rect x="{bar_x}" y="{bar_y}" width="{bar_width}" '
            f'height="{bar_height}" rx="{bar_height // 2}" />',
            "</clipPath>",
            rect(
                bar_x,
                bar_y,
                bar_width,
                bar_height,
                SURFACE_BG,
                radius=bar_height // 2,
                stroke="#162033",
            ),
            f'<g clip-path="url(#languageStackClip)">',
        ]
    )

    segment_x = bar_x
    segment_positions: list[tuple[str, int, int, float, int, str, str]] = []
    for index, (language, size, _) in enumerate(language_rows):
        percentage = size / totals_sum * 100
        meta = language_meta(language)
        remaining_width = bar_x + bar_width - segment_x
        if index == len(language_rows) - 1:
            segment_width = remaining_width
        else:
            segment_width = max(20, int(round(bar_width * percentage / 100)))
            segment_width = min(segment_width, remaining_width)
        parts.append(
            rect(
                segment_x,
                bar_y,
                segment_width,
                bar_height,
                str(meta["color"]),
                radius=0,
                opacity=0.72,
                stroke="#0F172A",
                stroke_width=2,
            )
        )
        parts.append(
            animated_bar(
                segment_x,
                bar_y + 2,
                min(80, segment_width),
                bar_height - 4,
                "#E2E8F0",
                0.18,
                f"{segment_x};{segment_x + max(segment_width - 80, 0)};{segment_x}",
                f"{5.0 + index * 0.25:.1f}s",
            )
        )
        segment_positions.append(
            (
                language,
                segment_x,
                segment_width,
                percentage,
                index,
                str(meta["color"]),
                str(meta["icon"]),
            )
        )
        segment_x += segment_width
    parts.extend(
        [
            "</g>",
            rect(
                bar_x,
                bar_y,
                bar_width,
                bar_height,
                "none",
                radius=bar_height // 2,
                stroke="#22314A",
            ),
        ]
    )

    legend_y = languages_card_y + 174
    columns = 4
    gap_x = 32
    col_width = (bar_width - (gap_x * (columns - 1))) // columns

    grid_index = 0
    for (
        language,
        segment_start,
        segment_width,
        percentage,
        _,
        color,
        icon_name,
    ) in sorted(segment_positions, key=lambda item: item[1]):
        repo_count = next(count for lang, _, count in language_rows if lang == language)
        label_width = max(132, estimate_text_width(language, font_size=13) + 78)

        label_x = bar_x + (grid_index % columns) * (col_width + gap_x)
        label_y = legend_y + (grid_index // columns) * 36

        x_centro = segment_start + segment_width // 2
        y_start = bar_y + bar_height + 2
        y_mid = y_start + 10
        y_end = label_y - 14

        parts_to_add = []
        parts_to_add.extend(
            [
                f'<image href="{get_skillicon_base64(icon_name)}" '
                f'x="{label_x}" y="{label_y - 2}" width="16" height="16" />',
                text(label_x + 22, label_y + 10, language, size=13, weight=700),
                text(
                    label_x + label_width,
                    label_y + 10,
                    f"{percentage:.1f}%",
                    size=12,
                    weight=700,
                    fill=color,
                    anchor="end",
                ),
                text(
                    label_x + 22,
                    label_y + 25,
                    f"{repo_count} repos",
                    size=11,
                    fill=MUTED,
                ),
            ]
        )
        parts.extend(parts_to_add)
        grid_index += 1

    matrix_y = languages_card_y + language_card_height + 58
    parts.append(
        f'<path d="M48 {matrix_y - 20}H1232" stroke="#1E293B" stroke-dasharray="4 7" opacity="0.28" />'
    )
    parts.extend(section_kicker(50, matrix_y, "Engineering matrix", 176))

    matrix_cards = [
        {
            "title": "AI & data systems",
            "subtitle_lines": [
                "Public proof of embeddings, pipelines,",
                "NLP and classical ML delivery.",
            ],
            "repo_lines": [
                "Repos: MCP-register · AudCifra",
                "Hermes · SiacScrapping",
            ],
            "proof": ["Embeddings", "Knowledge Graphs", "Pipelines", "Scraping"],
            "stack": ["Python", "SQL", "Kafka", "PostgreSQL"],
            "accent": ACCENT_ALT,
            "icon": "py",
        },
        {
            "title": "Backend & ops systems",
            "subtitle_lines": [
                "Production APIs, observability,",
                "Kafka-aware automation and telemetry.",
            ],
            "repo_lines": [
                "Repos: production-fix-flow",
                "MCP-register",
            ],
            "proof": ["TransE", "LightGBM", "Automation", "Telemetry"],
            "stack": ["FastAPI", "Redis", "Docker", "GitHub Actions"],
            "accent": TEAL,
            "icon": "fastapi",
        },
        {
            "title": "Product & platform",
            "subtitle_lines": [
                "Local-first product delivery with",
                "shared systems core and browser-facing UX.",
            ],
            "repo_lines": ["Repos: formae"],
            "proof": ["Rust/WASM", "Local-first", "PWA + MV3", "Product UX"],
            "stack": ["TypeScript", "React", "Vite", "Web Services"],
            "accent": VIOLET,
            "icon": "react",
        },
    ]

    matrix_card_width = 382
    matrix_card_inner_width = matrix_card_width - 36
    proof_layouts: list[list[list[tuple[str, int]]]] = []
    stack_layouts: list[list[list[tuple[str, int]]]] = []
    proof_heights: list[int] = []
    stack_heights: list[int] = []
    repo_heights: list[int] = []

    for card in matrix_cards:
        proof_rows = layout_chip_rows(
            cast(list[str], card["proof"]),
            max_width=matrix_card_inner_width,
            gap_x=8,
            font_size=10,
        )
        stack_rows = layout_chip_rows(
            cast(list[str], card["stack"]),
            max_width=matrix_card_inner_width,
            gap_x=8,
            font_size=10,
        )
        proof_layouts.append(proof_rows)
        stack_layouts.append(stack_rows)
        proof_heights.append(
            max(24, len(proof_rows) * 24 + max(0, len(proof_rows) - 1) * 10)
        )
        stack_heights.append(
            max(24, len(stack_rows) * 24 + max(0, len(stack_rows) - 1) * 10)
        )
        repo_heights.append(
            11 + max(0, len(cast(list[str], card["repo_lines"])) - 1) * 16
        )

    proof_block_height = max(proof_heights)
    stack_block_height = max(stack_heights)
    repo_block_height = max(repo_heights)
    proof_label_top = 170
    section_gap = 20
    section_label_gap = 12

    for index, card in enumerate(matrix_cards):
        x = 50 + index * 394
        y = matrix_y + 34
        accent = str(card["accent"])
        icon_name = str(card["icon"])
        parts.append(
            rect(
                x,
                y,
                matrix_card_width,
                matrix_card_height,
                CARD_BG,
                radius=22,
                stroke="#22314A",
            )
        )
        parts.append(
            rect(x + 18, y + 16, 34, 34, SURFACE_BG, radius=17, stroke="#22314A")
        )
        parts.append(
            f'<image href="{get_skillicon_base64(icon_name)}" '
            f'x="{x + 27}" y="{y + 25}" width="16" height="16" />'
        )
        parts.append(
            rect(x + 62, y + 20, 170, 18, SURFACE_BG, radius=9, stroke="#22314A")
        )
        parts.append(
            text(
                x + 147,
                y + 33,
                str(card["title"]).upper(),
                size=10,
                weight=700,
                fill=accent,
                anchor="middle",
                letter_spacing=0.9,
            )
        )
        parts.append(text(x + 18, y + 76, str(card["title"]), size=24, weight=700))
        parts.append(
            multiline_text(
                x + 18,
                y + 104,
                cast(list[str], card["subtitle_lines"]),
                size=13,
                fill=MUTED,
                line_gap=20,
            )
        )
        proof_label_y = y + proof_label_top
        proof_chips_y = proof_label_y + 14
        stack_label_y = (
            proof_chips_y + proof_block_height + section_gap + section_label_gap
        )
        stack_chips_y = stack_label_y + 14
        repo_y = (
            stack_chips_y + stack_block_height + section_gap + section_label_gap + 6
        )
        parts.append(
            text(
                x + 18,
                proof_label_y,
                "PROOF",
                size=11,
                weight=700,
                fill=MUTED,
                letter_spacing=1.2,
            )
        )
        proof_parts, _ = render_chip_rows(
            x + 18,
            proof_chips_y,
            proof_layouts[index],
            max_width=matrix_card_inner_width,
            chip_height=24,
            font_size=10,
            gap_y=10,
            justify=True,
        )
        parts.append(
            text(
                x + 18,
                stack_label_y,
                "STACK",
                size=11,
                weight=700,
                fill=MUTED,
                letter_spacing=1.2,
            )
        )
        stack_parts, _ = render_chip_rows(
            x + 18,
            stack_chips_y,
            stack_layouts[index],
            max_width=matrix_card_inner_width,
            chip_height=24,
            font_size=10,
            gap_y=10,
            justify=True,
        )
        parts.extend(proof_parts)
        parts.extend(stack_parts)
        parts.append(
            multiline_text(
                x + 18,
                repo_y,
                cast(list[str], card["repo_lines"]),
                size=11,
                fill=SOFT_TEXT,
                line_gap=16,
            )
        )

    parts.append("</svg>")

    return "".join(parts)


def generate_project_card_svg(config: dict[str, Any]) -> str:
    repo = str(config["repo"])
    label = str(config["label"])
    summary = str(config["summary"])
    proof = cast(list[str], config["proof"])
    stack = cast(list[str], config["stack"])
    accent = str(config["accent"])
    glow = str(config["glow"])
    content_x = 32
    content_width = PROJECT_CARD_WIDTH - 64
    section_gap = 24
    section_width = (content_width - section_gap) // 2
    proof_x = content_x
    stack_x = content_x + section_width + section_gap
    summary_lines = wrap_text_lines(summary, max_width=content_width, font_size=15)
    summary_height = 15 + max(0, len(summary_lines) - 1) * 18
    proof_rows = layout_chip_rows(
        proof,
        max_width=section_width,
        gap_x=8,
        font_size=10,
    )
    stack_rows = layout_chip_rows(
        stack,
        max_width=section_width,
        gap_x=8,
        font_size=10,
    )
    proof_height = max(24, len(proof_rows) * 24 + max(0, len(proof_rows) - 1) * 10)
    stack_height = max(24, len(stack_rows) * 24 + max(0, len(stack_rows) - 1) * 10)
    content_height = max(proof_height, stack_height)
    top_padding = 24
    title_y = 92
    summary_y = 122
    section_label_y = summary_y + summary_height + 28
    section_content_y = section_label_y + 14
    cta_height = 36
    cta_y = section_content_y + content_height + 24
    cta_width = content_width
    card_height = cta_y + cta_height + 20
    cta_label = "CLICK HERE TO REPOSITORY"
    cta_label_width = estimate_text_width(cta_label, font_size=12, letter_spacing=0.8)
    inner_width = 16 + 12 + 26 + 12 + cta_label_width + 16 + 14
    start_x = content_x + (cta_width - inner_width) // 2

    cta_icon_x = start_x
    cta_bar_x = cta_icon_x + 16 + 12
    cta_text_x = cta_bar_x + 26 + 12 + cta_label_width // 2
    cta_arrow_x = start_x + inner_width

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" shape-rendering="geometricPrecision" '
        f'width="{PROJECT_CARD_WIDTH}" height="{card_height}" '
        f'viewBox="0 0 {PROJECT_CARD_WIDTH} {card_height}" '
        'role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(repo)} repository proof card</title>',
        f'<desc id="desc">{escape(summary)}</desc>',
        "<defs>",
        f'<linearGradient id="cardPanel" x1="0" y1="0" x2="{PROJECT_CARD_WIDTH}" y2="{card_height}" gradientUnits="userSpaceOnUse">',
        '<stop stop-color="#09111F" />',
        f'<stop offset="1" stop-color="{CANVAS_BG}" />',
        "</linearGradient>",
        f'<radialGradient id="cardGlow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(734 44) rotate(90) scale(120 180)"><stop stop-color="{glow}" stop-opacity="0.18" /><stop offset="1" stop-color="{glow}" stop-opacity="0" /></radialGradient>',
        "</defs>",
        "<style>",
        "text{font-family:'Segoe UI',Arial,sans-serif}",
        "@media (prefers-reduced-motion: reduce) { * { animation: none !important; opacity: 1 !important; transform: none !important; } }",
        "</style>",
        rect(0, 0, PROJECT_CARD_WIDTH, card_height, "url(#cardPanel)", radius=24),
        animated_circle(
            PROJECT_CARD_WIDTH - 126,
            44,
            120,
            "url(#cardGlow)",
            "0.36;0.82;0.36",
            "7.2s",
            opacity=0.78,
        ),
        rect(
            1,
            1,
            PROJECT_CARD_WIDTH - 2,
            card_height - 2,
            "none",
            radius=23,
            stroke=BORDER,
        ),
    ]

    parts.extend(section_kicker(34, top_padding, label, max(118, len(label) * 10)))
    parts.append(text(34, title_y, repo, size=30, weight=700))
    parts.append(
        multiline_text(
            34,
            summary_y,
            summary_lines,
            size=15,
            fill=SOFT_TEXT,
            line_gap=21,
        )
    )
    parts.append(
        text(
            proof_x,
            section_label_y,
            "PROOF",
            size=11,
            weight=700,
            fill=MUTED,
            letter_spacing=1.2,
        )
    )
    parts.append(
        text(
            stack_x,
            section_label_y,
            "STACK",
            size=11,
            weight=700,
            fill=MUTED,
            letter_spacing=1.2,
        )
    )

    parts.append(
        rect(
            proof_x - 12,
            section_label_y - 12,
            section_width + 24,
            content_height + 46,
            "#FFFFFF",
            opacity=0.03,
            radius=12,
        )
    )
    parts.append(
        rect(
            stack_x - 12,
            section_label_y - 12,
            section_width + 24,
            content_height + 46,
            "#FFFFFF",
            opacity=0.03,
            radius=12,
        )
    )

    proof_chips, _ = render_chip_rows(
        proof_x,
        section_content_y,
        proof_rows,
        max_width=section_width,
        chip_height=24,
        font_size=11,
        gap_y=8,
        tint_bg=True,
    )
    stack_chips, _ = render_chip_rows(
        stack_x,
        section_content_y,
        stack_rows,
        max_width=section_width,
        chip_height=24,
        font_size=11,
        gap_y=8,
        tint_bg=True,
    )
    parts.extend(proof_chips)
    parts.extend(stack_chips)
    parts.append(
        rect(
            content_x,
            cta_y,
            cta_width,
            cta_height,
            "#132033",
            radius=18,
            stroke="#35507A",
        )
    )
    parts.append(
        f'<image href="{get_skillicon_base64("github")}" '
        f'x="{cta_icon_x}" y="{cta_y + 10}" width="16" height="16" />'
    )
    parts.append(
        animated_bar(
            cta_bar_x,
            cta_y + 14,
            26,
            6,
            accent,
            0.28,
            f"{cta_bar_x};{cta_bar_x + 14};{cta_bar_x}",
            "4.8s",
        )
    )
    parts.append(
        text(
            cta_text_x,
            cta_y + 23,
            cta_label,
            size=12,
            weight=700,
            fill="#A5F3FC",
            anchor="middle",
            letter_spacing=0.8,
        )
    )
    parts.append(
        text(
            cta_arrow_x,
            cta_y + 23,
            "↗",
            size=14,
            weight=700,
            fill="#A5F3FC",
            anchor="end",
        )
    )
    parts.append("</svg>")
    return "".join(parts)


def collect_profile_snapshot() -> (
    tuple[dict[str, Any], list[dict[str, Any]], dict[str, dict[str, int]]]
):
    user = cast(dict[str, Any], github_json(f"{GITHUB_API_BASE_URL}/users/{OWNER}"))
    repos = public_repositories(
        github_paginated(
            f"{GITHUB_API_BASE_URL}/users/{OWNER}/repos?per_page=100&type=owner&sort=updated"
        )
    )
    repo_languages = fetch_repo_languages(repos)
    return user, repos, repo_languages


def write_profile_assets(
    user: dict[str, Any],
    repos: list[dict[str, Any]],
    repo_languages: dict[str, dict[str, int]],
    output_root: Path | None = None,
    now: dt.datetime | None = None,
) -> dict[str, Path]:
    metrics_dir, architecture_dir = resolve_output_dirs(output_root)
    profile_dir = architecture_dir.parent
    cards_dir = profile_dir / "cards"
    summary_path = metrics_dir / SUMMARY_ASSET_NAME
    matrix_path = architecture_dir / ENGINEERING_MATRIX_ASSET_NAME
    hero_path = profile_dir / HERO_ASSET_NAME
    cards_dir.mkdir(parents=True, exist_ok=True)

    hero_svg = generate_hero_banner_svg()
    summary_svg = generate_summary_svg(user, repos, now=now)
    matrix_svg = generate_engineering_matrix_svg(repos, repo_languages)
    card_paths: dict[str, Path] = {}

    hero_path.write_text(hero_svg, encoding="utf-8")
    summary_path.write_text(summary_svg, encoding="utf-8")
    matrix_path.write_text(matrix_svg, encoding="utf-8")
    for card in PROJECT_CARD_CONFIG:
        card_path = cards_dir / str(card["filename"])
        card_path.write_text(generate_project_card_svg(card), encoding="utf-8")
        card_paths[str(card["repo"])] = card_path
    return {
        "hero": hero_path,
        "summary": summary_path,
        "matrix": matrix_path,
        **{f"card:{name}": path for name, path in card_paths.items()},
    }


def main() -> None:
    user, repos, repo_languages = collect_profile_snapshot()
    write_profile_assets(user, repos, repo_languages)


if __name__ == "__main__":
    main()
