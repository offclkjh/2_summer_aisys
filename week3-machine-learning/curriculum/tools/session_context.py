#!/usr/bin/env python3
"""Print the prerequisite context needed to author or tutor one session."""

from __future__ import annotations

import argparse
import json
import tomllib

try:
    from .curriculum_lib import (
        CURRICULUM_ROOT,
        ancestors,
        concept_teachers,
        load_authoring_contracts,
        load_curriculum,
        load_external_concepts,
    )
except ImportError:  # Direct execution: python3 tools/session_context.py
    from curriculum_lib import (
        CURRICULUM_ROOT,
        ancestors,
        concept_teachers,
        load_authoring_contracts,
        load_curriculum,
        load_external_concepts,
    )


def build_context(session_id: str) -> dict:
    _, sessions, by_id = load_curriculum()
    external = load_external_concepts()
    authoring = load_authoring_contracts()
    teachers = concept_teachers(sessions)
    session_id = session_id.upper()
    if session_id not in by_id:
        raise SystemExit(f"unknown session: {session_id}")

    session = by_id[session_id]
    available_ancestors = ancestors(session_id, by_id)
    required = []
    for concept_id in session["required_concepts"]:
        if concept_id in external:
            concept = external[concept_id]
            required.append(
                {
                    "id": concept_id,
                    "source": "external prerequisite",
                    "level": concept["level"],
                    "refresh": str(CURRICULUM_ROOT / "concepts" / concept["card"]),
                }
            )
            continue
        teacher = teachers.get(concept_id)
        if teacher is None:
            required.append({"id": concept_id, "source": "MISSING"})
            continue
        teacher_dir = CURRICULUM_ROOT / "sessions" / teacher
        problem = teacher_dir / "PROBLEM.md"
        source_status = by_id[teacher]["status"]
        refresh = None
        local_contract = teacher_dir / "session.toml"
        if local_contract.is_file():
            with local_contract.open("rb") as file:
                local = tomllib.load(file)
            anchor = local.get("concept_anchors", {}).get(concept_id)
            if anchor:
                refresh = str(teacher_dir / anchor)
        required.append(
            {
                "id": concept_id,
                "source": teacher,
                "source_status": source_status,
                "available_through_dependency": teacher in available_ancestors,
                "refresh": refresh,
            }
        )

    return {
        "id": session["id"],
        "title": session["title"],
        "phase": session["phase"],
        "status": session["status"],
        "depends_on": session["depends_on"],
        "one_of_tracks": session.get("one_of_tracks", []),
        "required_concepts": required,
        "taught_here": session["taught_here"],
        "authoring": authoring[session_id],
    }


def print_human(context: dict) -> None:
    print(f"{context['id']} — {context['title']}")
    print(f"phase/status: {context['phase']} / {context['status']}")
    dependencies = ", ".join(context["depends_on"]) or "없음"
    print(f"선수 세션: {dependencies}")
    if context["one_of_tracks"]:
        print(f"선택 선수 트랙(하나): {', '.join(context['one_of_tracks'])}")
    authoring = context["authoring"]
    print(f"중심 질문: {authoring['question']}")
    print(f"중심 사례: {authoring['core_case']}")
    print(f"핵심 범위: {authoring['core']}")
    print(f"제외 범위: {authoring['exclude']}")
    print(f"교재 주제: {', '.join(authoring['textbook_topics'])}")
    print("필요 개념:")
    for concept in context["required_concepts"]:
        source = concept["source"]
        if source.startswith("S") and not concept["available_through_dependency"]:
            source += " (선수 경로에서 접근 불가)"
        elif source.startswith("S") and concept["source_status"] != "ready":
            source += f" ({concept['source_status']}: 복습 문제 미출제)"
        print(f"- {concept['id']}: {source}")
        if concept.get("refresh"):
            print(f"  복습: {concept['refresh']}")
    print("이번 세션에서 새로 배우는 개념:")
    for concept in context["taught_here"]:
        print(f"- {concept}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("session_id", help="S01 through S40")
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--for-authoring",
        action="store_true",
        help="allow context output for a planned session while authoring its problem",
    )
    args = parser.parse_args()
    context = build_context(args.session_id)
    if context["status"] != "ready" and not args.for_authoring:
        raise SystemExit(
            f"{context['id']} is {context['status']}; its problem is not ready. "
            "Use --for-authoring only when creating the problem."
        )
    if args.json:
        print(json.dumps(context, ensure_ascii=False, indent=2))
    else:
        print_human(context)


if __name__ == "__main__":
    main()
