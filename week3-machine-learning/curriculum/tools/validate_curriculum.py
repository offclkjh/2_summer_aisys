#!/usr/bin/env python3
"""Validate session IDs, dependencies, concepts, and ready-session files."""

from __future__ import annotations

import re

try:
    from .curriculum_lib import (
        CURRICULUM_ROOT,
        ancestors,
        concept_teachers,
        load_authoring_contracts,
        load_curriculum,
        load_external_concepts,
    )
except ImportError:  # Direct execution: python3 tools/validate_curriculum.py
    from curriculum_lib import (
        CURRICULUM_ROOT,
        ancestors,
        concept_teachers,
        load_authoring_contracts,
        load_curriculum,
        load_external_concepts,
    )


def main() -> None:
    _, sessions, by_id = load_curriculum()
    external = load_external_concepts()
    authoring = load_authoring_contracts()
    errors: list[str] = []

    expected_ids = [f"S{number:02d}" for number in range(1, 41)]
    actual_ids = [session["id"] for session in sessions]
    if actual_ids != expected_ids:
        errors.append(f"session order/IDs differ: {actual_ids}")
    if set(authoring) != set(expected_ids):
        errors.append("authoring.toml must contain exactly S01 through S40")
    for session_id, contract in authoring.items():
        for key in ("question", "textbook_topics", "core_case", "core", "exclude"):
            if not contract.get(key):
                errors.append(f"{session_id}: authoring contract lacks {key}")

    try:
        teachers = concept_teachers(sessions)
    except ValueError as error:
        errors.append(str(error))
        teachers = {}

    for session in sessions:
        session_id = session["id"]
        if session["status"] not in {"planned", "draft", "ready"}:
            errors.append(f"{session_id}: invalid status {session['status']!r}")
        try:
            available = ancestors(session_id, by_id)
        except ValueError as error:
            errors.append(str(error))
            available = set()
        for dependency in session["depends_on"]:
            if dependency >= session_id:
                errors.append(f"{session_id}: dependency {dependency} is not earlier")
        for track in session.get("one_of_tracks", []):
            if track not in by_id:
                errors.append(f"{session_id}: missing optional track {track}")
            elif track >= session_id:
                errors.append(f"{session_id}: optional track {track} is not earlier")
        for concept in session["required_concepts"]:
            if concept in external:
                continue
            teacher = teachers.get(concept)
            if teacher is None:
                errors.append(f"{session_id}: required concept {concept!r} has no source")
            elif teacher not in available:
                errors.append(
                    f"{session_id}: concept {concept!r} is taught in {teacher}, "
                    "which is outside its dependency ancestry"
                )
        if session["status"] == "ready":
            session_dir = CURRICULUM_ROOT / "sessions" / session_id
            for dependency in session["depends_on"]:
                if by_id[dependency]["status"] != "ready":
                    errors.append(f"{session_id}: prerequisite {dependency} is not ready")
            tracks = session.get("one_of_tracks", [])
            if tracks and not any(by_id[track]["status"] == "ready" for track in tracks):
                errors.append(f"{session_id}: no optional prerequisite track is ready")
            for filename in ("session.toml", "PROBLEM.md"):
                if not (session_dir / filename).is_file():
                    errors.append(f"{session_id}: ready session lacks {filename}")
            if (session_dir / "PROBLEM.md").is_file():
                text = (session_dir / "PROBLEM.md").read_text()
                required_headings = (
                    "## 목표와 비목표",
                    "## 시작 전 선수지식 확인",
                    "## 문제에서 주어진 정보",
                    "## 과제",
                    "## 완료 기준",
                )
                for heading in required_headings:
                    if heading not in text:
                        errors.append(f"{session_id}: PROBLEM.md lacks {heading}")
                if re.search(r"판본.*확인|필요 시|chosen model", text, re.IGNORECASE):
                    errors.append(f"{session_id}: PROBLEM.md contains unresolved wording")
            session_contract = session_dir / "session.toml"
            if session_contract.is_file():
                import tomllib

                with session_contract.open("rb") as file:
                    local = tomllib.load(file)
                for key in (
                    "id",
                    "title",
                    "status",
                    "depends_on",
                    "required_concepts",
                    "taught_here",
                ):
                    if local.get(key) != session.get(key):
                        errors.append(
                            f"{session_id}: session.toml {key} differs from curriculum.toml"
                        )
                if local.get("core_minutes", 121) > 120:
                    errors.append(f"{session_id}: core_minutes exceeds 120")
                for file_key in ("problem", "starter", "test"):
                    filename = local.get(file_key)
                    if not filename or not (session_dir / filename).is_file():
                        errors.append(f"{session_id}: missing declared {file_key} file")
                standard_api = local.get("standard_api")
                if standard_api and not (session_dir / standard_api).is_file():
                    errors.append(f"{session_id}: missing declared standard_api file")
                anchors = local.get("concept_anchors", {})
                for concept in session["taught_here"]:
                    anchor = anchors.get(concept)
                    if not anchor:
                        errors.append(f"{session_id}: no refresh anchor for {concept}")
                    elif not (session_dir / anchor.split("#", 1)[0]).is_file():
                        errors.append(f"{session_id}: broken refresh anchor for {concept}")
            for concept in session["required_concepts"]:
                if concept in external:
                    card = CURRICULUM_ROOT / "concepts" / external[concept]["card"]
                    if not card.is_file():
                        errors.append(f"{session_id}: external refresh card missing for {concept}")
                    continue
                teacher = teachers.get(concept)
                if teacher and by_id[teacher]["status"] != "ready":
                    errors.append(f"{session_id}: concept source {teacher} is not ready")

    link_pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for markdown in CURRICULUM_ROOT.rglob("*.md"):
        for target in link_pattern.findall(markdown.read_text()):
            if target.startswith(("http://", "https://", "#")):
                continue
            path_text = target.split("#", 1)[0]
            if path_text and not (markdown.parent / path_text).resolve().exists():
                errors.append(f"{markdown.relative_to(CURRICULUM_ROOT)}: broken link {target}")

    if errors:
        print("curriculum validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"curriculum validation passed: {len(sessions)} sessions")


if __name__ == "__main__":
    main()
