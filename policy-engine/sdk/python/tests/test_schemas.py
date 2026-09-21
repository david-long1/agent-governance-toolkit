# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""The spec/schema documents ship with the package and match the spec tree."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_control_specification import schemas

SPEC_SCHEMA_DIR = Path(__file__).resolve().parents[3] / "spec" / "schema"
EXPECTED = (
    "approval",
    "cedar_advice",
    "manifest",
    "wire/effect",
    "wire/policy-input",
    "wire/request",
    "wire/result",
    "wire/snapshot",
    "wire/verdict",
)


def test_every_spec_schema_is_shipped() -> None:
    assert schemas.names() == EXPECTED


@pytest.mark.parametrize("name", EXPECTED)
def test_shipped_schema_is_a_json_schema_document(name: str) -> None:
    document = schemas.load(name)
    assert document.get("$schema", "").startswith("http")
    assert isinstance(document.get("title") or document.get("$id"), str)


@pytest.mark.skipif(not SPEC_SCHEMA_DIR.is_dir(), reason="spec tree not present (installed package)")
@pytest.mark.parametrize("name", EXPECTED)
def test_shipped_schema_matches_the_spec_tree(name: str) -> None:
    source = SPEC_SCHEMA_DIR / f"{name}.schema.json"
    assert schemas.text(name) == source.read_text(encoding="utf-8"), (
        f"{name} drifted from spec/schema; copy the file into agent_control_specification/schema/"
    )
    assert schemas.load(name) == json.loads(source.read_text(encoding="utf-8"))


def test_unknown_schema_name_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown schema"):
        schemas.text("nope")
