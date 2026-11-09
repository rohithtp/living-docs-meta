# Documentation Standards

## Naming and structure

All repository directories and filenames use lowercase kebab-case with ASCII letters, digits, and hyphens. The sole case-sensitive path exception is `.github/CODEOWNERS`. Supporting assets must also use lowercase names.

| Directory | Filename pattern | Lifecycle | Required sections |
| --- | --- | --- | --- |
| `adr/` | `nnnn-title.md` | Immutable | Context, Decision, Consequences, Alternatives Considered |
| `architecture/` | `domain-or-service.md` | Living | C4 Context/Container, Dependencies, Data Flow, Changelog |
| `specs/` | `spec-nnn-title.md` | Living | Problem & Goals, System Design, Security, Rollout Plan, Changelog |
| `impl-notes/` | `impl-nnn-title.md` | Living | Context & Scope, Implementation Details, Gotchas, Changelog |
| `flows/` | `flow-nnn-title.md` | Living | Trigger & Actors, Step-by-Step Sequence, Error Paths, Changelog |
| `simulations/` | `sim-nnn-title.md` | Living | Hypothesis, Environment & Inputs, Execution, Success Criteria |
| `sop/` | `nnn-title.md` | Living | Prerequisites, Procedure, Verification, Rollback, Changelog |
| `runbooks/` | `nnn-symptom.md` | Living | Trigger/Alert, Impact, Triage & Mitigation, Escalation |
| `postmortems/` | `yyyy-mm-dd-slug.md` | Immutable | Summary, Timeline, Root Cause, Action Items (`tracked_by`) |
| `evidences/` | `evid-nnn-title.md` | Immutable | Subject & Scope, Execution Summary, Metrics/Logs, Verdict (PASS/FAIL) |
| `tasks/` | `task-nnn-title.md` | Living | Objective, Context, Acceptance Criteria |

Identifiers are globally unique and match the artifact type, such as `ADR-0001`, `SPEC-001`, or `EVID-001`. Living artifacts advance with semantic versions. Immutable artifacts remain at `1.0.0`; corrections should be captured through a superseding artifact rather than editing accepted content in place.

## Metadata and relationships

Every Markdown artifact begins with YAML frontmatter validated against `schemas/frontmatter.schema.json`. Required fields include `id`, `type`, `title`, `version`, `status`, `owner`, `service`, `created_at`, `last_reviewed`, and `review_cadence_days`. AI-authored or updated content sets `ai_assisted: true` and names its `agent_id`. Tasks also require `priority` and `task_status`.

Relationship values are lists of artifact IDs. Supported keys are `implements`, `realizes`, `validates`, `evidenced_by`, `verifies`, `tracked_by`, `resolves`, `depends_on`, `blocked_by`, `supersedes`, and `superseded_by`. Referenced IDs must exist. A superseded artifact must identify its replacement using `superseded_by`.

## Governance

The `owner` metadata value must identify a team or GitHub handle represented in `.github/CODEOWNERS`. Service values must be keys in `catalog/services.yaml`. Owners review living documents at their declared cadence (90, 180, or 365 days).

Requirements in `specs/`, `sop/`, and `runbooks/` use RFC 2119 terms (`MUST`, `SHOULD`, and `MAY`) consistently. System diagrams are text-based Mermaid, D2, or PlantUML files stored in `diagrams/`; binary system diagrams are not accepted.

AI agents are assistants, not approvers. They MUST NOT commit to `main`, approve pull requests, modify accepted ADRs or evidence, or edit `.ai/`, `schemas/`, or `standards.md`. Human review is required for every proposed change.
