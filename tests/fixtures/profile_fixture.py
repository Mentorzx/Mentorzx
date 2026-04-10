from __future__ import annotations

import datetime as dt


FIXED_NOW = dt.datetime(2025, 4, 15, 12, 0, tzinfo=dt.UTC)

USER = {
    "created_at": "2020-10-03T12:00:00Z",
    "followers": 3,
    "following": 6,
    "public_repos": 10,
}

REPOS = [
    {
        "name": "audcifra",
        "updated_at": "2024-09-12T12:00:00Z",
        "description": "Audio and data workflow for transcription and harmony.",
        "topics": ["audio", "ml"],
        "language": "Python",
        "fork": False,
        "stargazers_count": 0,
        "forks_count": 0,
        "open_issues_count": 0,
    },
    {
        "name": "hermes",
        "updated_at": "2024-11-09T12:00:00Z",
        "description": "NLP API for sentiment and language analysis.",
        "topics": ["nlp", "api"],
        "language": "Python",
        "fork": False,
        "stargazers_count": 0,
        "forks_count": 0,
        "open_issues_count": 0,
    },
    {
        "name": "compvision",
        "updated_at": "2025-01-06T12:00:00Z",
        "description": "Computer vision experiments and data-heavy prototypes.",
        "topics": ["vision", "data"],
        "language": "Python",
        "fork": False,
        "stargazers_count": 0,
        "forks_count": 0,
        "open_issues_count": 0,
    },
    {
        "name": "mcp-register",
        "updated_at": "2025-04-05T12:00:00Z",
        "description": "MCP backend with semantic registration and retrieval.",
        "topics": ["mcp", "backend"],
        "language": "Python",
        "fork": False,
        "stargazers_count": 1,
        "forks_count": 0,
        "open_issues_count": 1,
    },
    {
        "name": "production-fix-flow",
        "updated_at": "2025-02-18T12:00:00Z",
        "description": "Backend orchestration, observability, and runtime guards.",
        "topics": ["backend", "docker"],
        "language": "Python",
        "fork": False,
        "stargazers_count": 0,
        "forks_count": 1,
        "open_issues_count": 1,
    },
    {
        "name": "formae",
        "updated_at": "2025-04-10T12:00:00Z",
        "description": "Local-first product with PWA delivery and browser privacy.",
        "topics": ["react", "vite", "pwa"],
        "language": "TypeScript",
        "fork": False,
        "stargazers_count": 1,
        "forks_count": 1,
        "open_issues_count": 0,
    },
    {
        "name": "Mentorzx",
        "updated_at": "2025-04-12T12:00:00Z",
        "description": "Profile README and generated presentation assets.",
        "topics": ["profile"],
        "language": "Markdown",
        "fork": False,
        "stargazers_count": 0,
        "forks_count": 0,
        "open_issues_count": 0,
    },
]

REPO_LANGUAGES = {
    "audcifra": {
        "Python": 720,
        "Shell": 120,
    },
    "hermes": {
        "Python": 640,
        "Shell": 80,
    },
    "compvision": {
        "Cython": 880,
        "Python": 360,
        "Tcl": 460,
    },
    "mcp-register": {
        "Python": 520,
        "Shell": 120,
    },
    "production-fix-flow": {
        "Python": 460,
        "Shell": 280,
    },
    "formae": {
        "TypeScript": 940,
        "JavaScript": 220,
        "Rust": 70,
    },
}
