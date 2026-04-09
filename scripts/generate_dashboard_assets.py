from __future__ import annotations

import datetime as dt
import json
import os
from collections import Counter
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape


OWNER = os.getenv("GITHUB_USER", "Mentorzx")
TOKEN = os.getenv("METRICS_TOKEN") or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "metrics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CARD_BG = "#0F172A"
CARD_ALT = "#111827"
BORDER = "#23314D"
TEXT = "#E5E7EB"
MUTED = "#94A3B8"
ACCENT = "#60A5FA"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"

LANGUAGE_COLORS = {
    "TypeScript": "#3178C6",
    "JavaScript": "#F1E05A",
    "Python": "#3572A5",
    "Rust": "#DEA584",
    "CSS": "#563D7C",
    "HTML": "#E34C26",
    "Bash": "#89E051",
    "Other": "#475569",
}

LANGUAGE_GROUPS = {
    "TypeScript": "TypeScript",
    "TSX": "TypeScript",
    "JavaScript": "JavaScript",
    "JSX": "JavaScript",
    "Python": "Python",
    "Rust": "Rust",
    "CSS": "CSS",
    "SCSS": "CSS",
    "HTML": "HTML",
    "Shell": "Bash",
    "Batchfile": "Bash",
    "PowerShell": "Bash",
}

PRODUCT_LANGUAGE_PRIORITY = [
    "Python",
    "TypeScript",
    "JavaScript",
    "Rust",
    "HTML",
    "CSS",
    "Bash",
]


def github_json(url: str) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "mentorzx-profile-dashboard",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = Request(url, headers=headers)
    with urlopen(request) as response:
        return json.load(response)


def github_paginated(url: str) -> list[dict]:
    page = 1
    results: list[dict] = []
    while True:
        batch = github_json(f"{url}&page={page}")
        if not batch:
            break
        results.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return results


def human_bytes(value: int) -> str:
    if value <= 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB"]
    size = float(value)
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024
        idx += 1
    precision = 1 if size < 10 and idx > 0 else 0
    return f"{size:.{precision}f} {units[idx]}"


def rect(x: int, y: int, width: int, height: int, fill: str, radius: int = 20, stroke: str | None = None) -> str:
    extra = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="{radius}" fill="{fill}"{extra} />'
    )


def text(
    x: int,
    y: int,
    value: str,
    size: int = 16,
    weight: int = 400,
    fill: str = TEXT,
    anchor: str = "start",
) -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'
    )


def generate_summary_svg(user: dict, repos: list[dict], stars: int, forks: int) -> str:
    cards = [
        ("Public repos", str(user["public_repos"]), "visible portfolio surface"),
        ("Followers", str(user["followers"]), "people watching the profile"),
        ("Following", str(user["following"]), "network and collaboration"),
        ("Public stars", str(stars), "signals on shipped repos"),
        ("Public forks", str(forks), "reuse and derivation"),
        ("Hireable", "Yes" if user.get("hireable") else "No", "profile flag from GitHub"),
    ]

    created = dt.datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
    active_since = created.strftime("%b %Y")

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="420" viewBox="0 0 960 420" role="img" aria-label="Engineering summary dashboard">',
        "<style>",
        "text{font-family:'Segoe UI',Arial,sans-serif}",
        "</style>",
        rect(0, 0, 960, 420, CARD_ALT, radius=28),
        rect(18, 18, 924, 384, "#0B1220", radius=24, stroke=BORDER),
        text(42, 62, "Engineering summary", size=28, weight=700),
        text(42, 92, "Public GitHub telemetry, kept large enough to scan in one glance.", size=15, fill=MUTED),
        text(918, 62, f"Active since {active_since}", size=15, weight=600, fill=ACCENT, anchor="end"),
    ]

    start_x = 42
    start_y = 122
    gap_x = 20
    gap_y = 18
    card_w = 278
    card_h = 108

    for index, (label, value, helper) in enumerate(cards):
        row = index // 3
        col = index % 3
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        accent = [ACCENT, "#2DD4BF", "#A78BFA", SUCCESS, WARNING, "#38BDF8"][index]
        parts.extend(
            [
                rect(x, y, card_w, card_h, CARD_BG, radius=18, stroke=BORDER),
                rect(x + 18, y + 18, 10, 10, accent, radius=5),
                text(x + 42, y + 28, label.upper(), size=13, weight=700, fill=MUTED),
                text(x + 22, y + 72, value, size=34, weight=700, fill=TEXT),
                text(x + 22, y + 92, helper, size=14, fill="#CBD5E1"),
            ]
        )

    repo_focus = ", ".join(repo["name"] for repo in repos[:4])
    footer = (
        "Computed from public repositories, excluding the profile repo from language analysis. "
        f"Recent repo surface: {repo_focus}"
    )
    parts.append(text(42, 382, footer, size=13, fill=MUTED))
    parts.append("</svg>")
    return "".join(parts)


def generate_languages_svg(language_counter: Counter[str], total_bytes: int) -> str:
    top_languages = language_counter.most_common(6)
    if not top_languages:
        top_languages = [("Other", 1)]
        total_bytes = 1

    top_total = sum(size for _, size in top_languages)
    if total_bytes > top_total:
        top_languages.append(("Other", total_bytes - top_total))

    display_languages = top_languages[:6]
    bar_total = sum(size for _, size in display_languages) or 1

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="500" viewBox="0 0 960 500" role="img" aria-label="Language surface dashboard">',
        "<style>",
        "text{font-family:'Segoe UI',Arial,sans-serif}",
        "</style>",
        rect(0, 0, 960, 500, CARD_ALT, radius=28),
        rect(18, 18, 924, 464, "#0B1220", radius=24, stroke=BORDER),
        text(42, 62, "Most used product languages", size=28, weight=700),
        text(
            42,
            92,
            "Grouped from GitHub language bytes across public repositories, focused on the languages that actually define the product surface.",
            size=15,
            fill=MUTED,
        ),
    ]

    bar_x = 42
    bar_y = 126
    bar_w = 876
    bar_h = 22
    parts.append(rect(bar_x, bar_y, bar_w, bar_h, "#111827", radius=11, stroke=BORDER))

    cursor = bar_x
    for language, size in display_languages:
        width = max(10, round(bar_w * size / bar_total))
        if cursor + width > bar_x + bar_w:
            width = (bar_x + bar_w) - cursor
        parts.append(rect(cursor, bar_y, width, bar_h, LANGUAGE_COLORS.get(language, LANGUAGE_COLORS["Other"]), radius=0))
        cursor += width
        if cursor >= bar_x + bar_w:
            break

    parts.append(text(918, 144, f"{human_bytes(total_bytes)} tracked", size=14, weight=600, fill=ACCENT, anchor="end"))

    card_w = 428
    card_h = 74
    start_x = 42
    start_y = 182
    gap_x = 22
    gap_y = 16

    for index, (language, size) in enumerate(display_languages[:6]):
        row = index // 2
        col = index % 2
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        share = (size / total_bytes * 100) if total_bytes else 0
        color = LANGUAGE_COLORS.get(language, LANGUAGE_COLORS["Other"])
        parts.extend(
            [
                rect(x, y, card_w, card_h, CARD_BG, radius=18, stroke=BORDER),
                rect(x + 18, y + 18, 12, 12, color, radius=6),
                text(x + 42, y + 30, language, size=20, weight=700),
                text(x + 42, y + 56, human_bytes(size), size=14, fill=MUTED),
                text(x + card_w - 22, y + 46, f"{share:.1f}%", size=28, weight=700, fill=color, anchor="end"),
            ]
        )

    parts.append(
        text(
            42,
            472,
            "TSX is grouped into TypeScript and JSX into JavaScript, so the chart reflects the code surface you actually ship.",
            size=13,
            fill=MUTED,
        )
    )
    parts.append("</svg>")
    return "".join(parts)


def main() -> None:
    user = github_json(f"https://api.github.com/users/{OWNER}")
    repos = github_paginated(
        f"https://api.github.com/users/{OWNER}/repos?per_page=100&type=owner&sort=updated"
    )

    public_repos = [repo for repo in repos if not repo.get("fork")]
    public_stars = sum(repo["stargazers_count"] for repo in public_repos)
    public_forks = sum(repo["forks_count"] for repo in public_repos)

    language_counter: Counter[str] = Counter()

    for repo in public_repos:
        if repo["name"].lower() == OWNER.lower():
            continue
        try:
            language_payload = github_json(repo["languages_url"])
        except HTTPError:
            continue
        for language, size in language_payload.items():
            grouped = LANGUAGE_GROUPS.get(language, language)
            size_value = int(size)
            language_counter[grouped] += size_value

    product_languages: Counter[str] = Counter()
    for language, size in language_counter.items():
        if language in PRODUCT_LANGUAGE_PRIORITY:
            product_languages[language] += size

    ordered_languages: Counter[str] = Counter()
    for language in PRODUCT_LANGUAGE_PRIORITY:
        if product_languages.get(language):
            ordered_languages[language] = product_languages[language]

    total_language_bytes = sum(ordered_languages.values())

    summary_svg = generate_summary_svg(user, public_repos, public_stars, public_forks)
    languages_svg = generate_languages_svg(ordered_languages, total_language_bytes)

    (OUTPUT_DIR / "dashboard-summary.svg").write_text(summary_svg, encoding="utf-8")
    (OUTPUT_DIR / "dashboard-languages.svg").write_text(languages_svg, encoding="utf-8")


if __name__ == "__main__":
    main()
