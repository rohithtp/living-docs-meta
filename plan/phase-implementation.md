# Phase Implementation Plan

## Phase 1: Repository foundation

Status: in progress

- Establish the lowercase directory layout, ownership policy, standards, and documentation entry point.
- Define the service catalog and shared frontmatter schema.
- Add local validation for metadata, service references, relationship IDs, and supersession.
- Run validation, Markdown lint, and link checks in pull-request CI.
- Keep AI skills and agent definitions declarative; do not grant unattended write or approval permissions.

Exit criteria:

- The empty starter repository passes local and CI validation.
- Every artifact directory has a documented filename pattern and required sections in `standards.md`.
- At least one real service and owner are registered before the first service artifact is merged.

## Phase 2: Artifact adoption

- Register services, repositories, and owners in `catalog/services.yaml`.
- Migrate or create initial ADRs, architecture views, specifications, flows, and runbooks with valid metadata.
- Add CODEOWNERS entries that reflect the actual teams and directory responsibilities.
- Add diagram and RFC 2119 checks after the document conventions are exercised by real artifacts.

Exit criteria:

- Initial artifacts validate and all registered services have an accountable owner.
- Reviewers confirm that filename patterns, relationship keys, and required sections work for real documents.

## Phase 3: Freshness and AI operations

- Enable scheduled stale-document reporting using `review_cadence_days` and `last_reviewed`.
- Connect declarative agents to an approved runtime with read/write scopes and human review.
- Add task creation or pull-request drafting only after permissions, secrets, auditability, and HITL behavior are tested.
- Prohibit unattended merges, approvals, and edits to accepted ADRs or evidence artifacts.

Exit criteria:

- Scheduled checks report actionable findings without changing protected artifacts.
- Agent-generated changes are reviewable, attributable, and constrained to approved paths.
