from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts import generate_dashboard_assets as dashboard
from tests.fixtures.profile_fixture import (
    FIXED_NOW,
    REPO_LANGUAGES,
    REPOS,
    USER,
)


def assert_accessible_svg(svg_text: str) -> ET.Element:
    root = ET.fromstring(svg_text)
    assert root.attrib.get("role") == "img"
    labelled_by = root.attrib.get("aria-labelledby")
    assert labelled_by
    ids = {
        element.attrib.get("id") for element in root.iter() if "id" in element.attrib
    }
    for identifier in labelled_by.split():
        assert identifier in ids
    return root


def test_hero_banner_fixture_regression(monkeypatch) -> None:
    monkeypatch.setattr(
        dashboard,
        "get_skillicon_base64",
        lambda icon_name: f"https://skillicons.dev/icons?i={icon_name}",
    )

    svg = dashboard.generate_hero_banner_svg()

    assert_accessible_svg(svg)
    assert 'width="1280" height="500"' in svg
    assert "HIRING SNAPSHOT" in svg
    assert "PRIMARY STACK" in svg
    assert "best fit:" in svg
    assert "Open to backend, data/AI and automation-heavy roles" in svg
    assert "skillicons.dev/icons?i=py" in svg
    assert "skillicons.dev/icons?i=rust" in svg
    assert "skillicons.dev/icons?i=java" in svg
    assert "skillicons.dev/icons?i=githubactions" in svg


def test_dashboard_summary_fixture_regression() -> None:
    svg = dashboard.generate_summary_svg(USER, REPOS, now=FIXED_NOW)

    assert_accessible_svg(svg)
    assert 'width="1240" height="700"' in svg
    assert "Engineering dashboard" in svg
    assert "Active since Oct 2020" in svg
    assert "Repository freshness trail" in svg
    assert "Compact telemetry" in svg
    for month in [
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
        "JAN",
        "FEB",
        "MAR",
        "APR",
    ]:
        assert f">{month}<" in svg
    assert "PUBLIC REPOS" in svg
    assert "FOLLOWERS" in svg
    assert "PUBLIC STARS" in svg
    assert "PUBLIC FORKS" in svg
    assert "ACTIVE &lt;= 90D" in svg
    assert "OPEN ISSUES" in svg
    assert ">10<" in svg
    assert ">3<" in svg
    assert ">4<" in svg
    assert "Recent surface: Mentorzx, formae, mcp-register" in svg


def test_engineering_matrix_fixture_regression(monkeypatch) -> None:
    monkeypatch.setattr(
        dashboard,
        "get_skillicon_base64",
        lambda icon_name: f"https://skillicons.dev/icons?i={icon_name}",
    )

    svg = dashboard.generate_engineering_matrix_svg(REPOS, REPO_LANGUAGES)

    assert_accessible_svg(svg)
    assert 'width="1280" height="1600"' in svg
    assert "Compact stack map" in svg
    assert "Most used public languages" in svg
    assert "Data Engineering" in svg
    assert "Front-end" in svg
    assert "DevOps" in svg
    assert "AI Engineering" in svg
    assert "Backend Engineering" in svg
    assert "AI &amp; data systems" in svg
    assert "Backend &amp; ops systems" in svg
    assert "Product &amp; platform" in svg
    assert "Kafka" in svg
    assert "PostgreSQL" in svg
    assert "Elasticsearch" in svg
    assert "Logstash" in svg
    assert "Kibana" in svg
    assert "skillicons.dev/icons?i=py" in svg
    assert "skillicons.dev/icons?i=rust" in svg
    assert "skillicons.dev/icons?i=java" in svg
    assert "skillicons.dev/icons?i=react" in svg
    assert "ELK" not in svg
    assert "pandas" not in svg.lower()
    assert "pytorch" not in svg.lower()


def test_write_profile_assets_to_custom_root(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        dashboard,
        "get_skillicon_base64",
        lambda icon_name: f"https://skillicons.dev/icons?i={icon_name}",
    )

    written = dashboard.write_profile_assets(
        USER,
        REPOS,
        REPO_LANGUAGES,
        output_root=tmp_path,
        now=FIXED_NOW,
    )

    hero_path = tmp_path / "assets" / "profile" / "hero-banner.svg"
    summary_path = tmp_path / "assets" / "metrics" / "dashboard-summary.svg"
    matrix_path = (
        tmp_path / "assets" / "profile" / "architecture" / "engineering-matrix.svg"
    )
    production_card_path = (
        tmp_path / "assets" / "profile" / "cards" / "production-fix-flow-card.svg"
    )

    assert written["hero"] == hero_path
    assert written["summary"] == summary_path
    assert written["matrix"] == matrix_path
    assert written["card:production-fix-flow"] == production_card_path
    assert hero_path.exists()
    assert summary_path.exists()
    assert matrix_path.exists()
    assert production_card_path.exists()
    assert_accessible_svg(hero_path.read_text(encoding="utf-8"))
    assert_accessible_svg(summary_path.read_text(encoding="utf-8"))
    assert_accessible_svg(matrix_path.read_text(encoding="utf-8"))
    assert_accessible_svg(production_card_path.read_text(encoding="utf-8"))


def test_profile_asset_root_env_uses_repo_shape(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setenv("PROFILE_ASSET_ROOT", str(tmp_path))
    metrics_dir, architecture_dir = dashboard.resolve_output_dirs()

    assert metrics_dir == tmp_path / "assets" / "metrics"
    assert architecture_dir == tmp_path / "assets" / "profile" / "architecture"
    assert metrics_dir.exists()
    assert architecture_dir.exists()


def test_readme_local_assets_exist() -> None:
    readme_path = Path(__file__).resolve().parents[1] / "README.md"
    readme = readme_path.read_text(encoding="utf-8")

    asset_refs = {
        match.group(1) or match.group(2)
        for match in re.finditer(
            r'src="(\./assets/[^"]+)"|!\[[^\]]*]\((\./assets/[^)]+)\)',
            readme,
        )
    }
    image_refs = {
        match.group(1) for match in re.finditer(r"!\[[^\]]*]\((image/[^)]+)\)", readme)
    }

    assert asset_refs
    assert "dashboard-languages.svg" not in readme
    assert "isocalendar.svg" not in readme

    repo_root = readme_path.parent
    for readme_ref in sorted(asset_refs | image_refs):
        asset_path = repo_root / readme_ref.removeprefix("./")
        assert asset_path.exists(), f"Missing README asset: {readme_ref}"


def test_readme_avoids_fragile_hardcoded_repo_stats() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "Public%20repos-11" not in readme
    assert "Public%20stars-2" not in readme
