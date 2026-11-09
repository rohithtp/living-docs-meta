#!/usr/bin/env python3
"""Validate documentation paths, frontmatter, services, and relationships."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/frontmatter.schema.json"
SERVICES_PATH = ROOT / "catalog/services.yaml"
ARTIFACT_DIRS = {
    "adr", "architecture", "specs", "impl-notes", "flows", "simulations",
    "sop", "runbooks", "postmortems", "evidences", "tasks",
}
ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]{3,4}$")
FILENAME_PATTERNS = {
    "adr": re.compile(r"^[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
    "architecture": re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
    "specs": re.compile(r"^spec-[0-9]{3,4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
    "impl-notes": re.compile(r"^impl-[0-9]{3,4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
    "flows": re.compile(r"^flow-[0-9]{3,4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
    "simulations": re.compile(r"^sim-[0-9]{3,4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
    "sop": re.compile(r"^[0-9]{3,4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
    "runbooks": re.compile(r"^[0-9]{3,4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
    "postmortems": re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
    "evidences": re.compile(r"^evid-[0-9]{3,4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
    "tasks": re.compile(r"^task-[0-9]{3,4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"),
}


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise ValueError(f"{path.relative_to(ROOT)}: {error}") from error


def read_frontmatter(path: Path, errors: list[str]) -> dict | None:
    relative = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{relative}: missing YAML frontmatter")
        return None
    header, separator, _ = text[4:].partition("\n---\n")
    if not separator:
        errors.append(f"{relative}: frontmatter is not closed")
        return None
    try:
        metadata = yaml.safe_load(header)
    except yaml.YAMLError as error:
        errors.append(f"{relative}: invalid frontmatter YAML: {error}")
        return None
    if not isinstance(metadata, dict):
        errors.append(f"{relative}: frontmatter must be a mapping")
        return None
    for field in ("created_at", "last_reviewed"):
        if isinstance(metadata.get(field), date):
            metadata[field] = metadata[field].isoformat()
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-staleness", action="store_true", help="fail when artifacts exceed their review cadence")
    args = parser.parse_args()
    errors: list[str] = []

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    catalog = load_yaml(SERVICES_PATH)
    services = catalog.get("services", {}) if isinstance(catalog, dict) else None
    if not isinstance(services, dict):
        errors.append("catalog/services.yaml: expected a 'services' mapping")
        services = {}
    for service_name, details in services.items():
        if not isinstance(service_name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", service_name):
            errors.append(f"catalog/services.yaml: invalid service key {service_name!r}")
        if not isinstance(details, dict) or not details.get("owner") or not details.get("repo"):
            errors.append(f"catalog/services.yaml: service {service_name!r} needs owner and repo")

    artifacts: list[tuple[Path, dict]] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative != ".github/CODEOWNERS" and not re.fullmatch(r"[a-z0-9._/-]+", relative):
            errors.append(f"{relative}: paths may contain only lowercase letters, digits, hyphens, dots, and slashes")
        relative_parts = path.relative_to(ROOT).parts
        if not path.is_file() or path.suffix != ".md" or relative_parts[0] not in ARTIFACT_DIRS:
            continue
        if not FILENAME_PATTERNS[relative_parts[0]].fullmatch(path.name):
            errors.append(f"{relative}: filename does not match the documented pattern")
        metadata = read_frontmatter(path, errors)
        if metadata is None:
            continue
        for issue in validator.iter_errors(metadata):
            location = ".".join(str(part) for part in issue.absolute_path)
            errors.append(f"{relative}: {location}: {issue.message}")
        artifacts.append((path, metadata))

    known_ids: dict[str, Path] = {}
    for path, metadata in artifacts:
        relative = path.relative_to(ROOT).as_posix()
        artifact_id = metadata.get("id")
        if isinstance(artifact_id, str):
            if artifact_id in known_ids:
                errors.append(f"{relative}: duplicate id {artifact_id} (also in {known_ids[artifact_id].relative_to(ROOT)})")
            known_ids[artifact_id] = path
        for service_name in metadata.get("service", []):
            if service_name not in services:
                errors.append(f"{relative}: unknown service {service_name!r}")
        relationships = metadata.get("relationships", {})
        if not isinstance(relationships, dict):
            continue
        if metadata.get("status") == "superseded" and not relationships.get("superseded_by"):
            errors.append(f"{relative}: superseded artifact needs relationships.superseded_by")
        if args.check_staleness and isinstance(metadata.get("last_reviewed"), str):
            cadence = metadata.get("review_cadence_days")
            try:
                last_reviewed = date.fromisoformat(metadata["last_reviewed"])
            except ValueError:
                last_reviewed = None
            if isinstance(cadence, int) and last_reviewed and date.today() > last_reviewed + timedelta(days=cadence):
                errors.append(f"{relative}: review is overdue (last reviewed {last_reviewed}, cadence {cadence} days)")

    for path, metadata in artifacts:
        relationships = metadata.get("relationships", {})
        if not isinstance(relationships, dict):
            continue
        for relation, targets in relationships.items():
            if not isinstance(targets, list):
                continue
            for target in targets:
                if not ID_PATTERN.fullmatch(target):
                    errors.append(f"{path.relative_to(ROOT)}: invalid {relation} id {target!r}")
                elif target not in known_ids:
                    errors.append(f"{path.relative_to(ROOT)}: {relation} references missing id {target}")

    if errors:
        print("Documentation validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Documentation validation passed ({len(artifacts)} artifacts, {len(services)} services).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())