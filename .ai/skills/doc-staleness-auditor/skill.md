---
name: doc-staleness-auditor
triggers: [scheduled review, linked repository change]
inputs: [artifact metadata, repository changes]
outputs: [staleness findings]
---

# Documentation Staleness Auditor

Compare `last_reviewed` plus `review_cadence_days` with the current date. Report stale artifacts with their owners and relevant changes. Suggest task drafts; do not modify source artifacts.
