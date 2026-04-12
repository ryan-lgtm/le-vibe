"""H2: requirements.txt must use pinned versions for reproducible SBOM + pip-audit."""

from __future__ import annotations

from pathlib import Path


def test_requirements_txt_uses_exact_pins():
    p = Path(__file__).resolve().parents[1] / "requirements.txt"
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        assert "==" in line, f"expected pinned dependency (==): {line!r}"
