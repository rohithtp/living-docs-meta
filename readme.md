# living-docs-meta

Schema-driven, AI-maintained living documentation meta-repository for ADRs, specs, architecture, flows, SOPs, runbooks, simulations, evidences, and tasks.

## Project naming

- Project name: Living Docs Meta
- Repository name: `living-docs-meta`

## Repository map

- `.ai/`: composable skills and guarded agent definitions.
- `.github/`: ownership and automated documentation checks.
- `catalog/`: service registry used by document metadata.
- `schemas/`: machine-readable metadata contracts.
- `adr/`, `architecture/`, `specs/`, `impl-notes/`, `flows/`, `simulations/`, `sop/`, `runbooks/`, `postmortems/`, `evidences/`, and `tasks/`: documentation artifacts grouped by lifecycle.
- `diagrams/`: text-based diagrams.
- `plan/`: phased repository implementation and adoption plan.

## Getting started

1. Add services and owners to `catalog/services.yaml`.
2. Read `standards.md` before adding documentation.
3. Use the artifact patterns and metadata schema in `schemas/frontmatter.schema.json`.
4. Run `python scripts/validate_docs.py` before opening a pull request.

CI also runs Markdown linting and link checks. Artifact validation requires Python 3 and the packages in `requirements.txt`.
