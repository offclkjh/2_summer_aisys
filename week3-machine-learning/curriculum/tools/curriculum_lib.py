"""Shared loader and dependency helpers for curriculum tools."""

from __future__ import annotations

import tomllib
from pathlib import Path


CURRICULUM_ROOT = Path(__file__).resolve().parents[1]


def load_curriculum() -> tuple[dict, list[dict], dict[str, dict]]:
    with (CURRICULUM_ROOT / "curriculum.toml").open("rb") as file:
        document = tomllib.load(file)
    sessions = document["sessions"]
    return document, sessions, {session["id"]: session for session in sessions}


def load_external_concepts() -> dict[str, dict]:
    with (CURRICULUM_ROOT / "concepts" / "registry.toml").open("rb") as file:
        document = tomllib.load(file)
    return {concept["id"]: concept for concept in document["concepts"]}


def load_authoring_contracts() -> dict[str, dict]:
    with (CURRICULUM_ROOT / "authoring.toml").open("rb") as file:
        document = tomllib.load(file)
    return {session["id"]: session for session in document["sessions"]}


def concept_teachers(sessions: list[dict]) -> dict[str, str]:
    teachers: dict[str, str] = {}
    for session in sessions:
        for concept in session["taught_here"]:
            if concept in teachers:
                raise ValueError(
                    f"concept {concept!r} is taught by both "
                    f"{teachers[concept]} and {session['id']}"
                )
            teachers[concept] = session["id"]
    return teachers


def ancestors(session_id: str, by_id: dict[str, dict]) -> set[str]:
    found: set[str] = set()
    visiting: set[str] = set()

    def visit(current: str) -> None:
        if current in visiting:
            raise ValueError(f"dependency cycle reaches {current}")
        if current in found:
            return
        visiting.add(current)
        for dependency in by_id[current]["depends_on"]:
            if dependency not in by_id:
                raise ValueError(f"{current} depends on missing session {dependency}")
            visit(dependency)
            found.add(dependency)
        visiting.remove(current)

    visit(session_id)
    return found
