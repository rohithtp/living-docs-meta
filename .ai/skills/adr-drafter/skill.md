---
name: adr-drafter
triggers: [architecture decision requested]
inputs: [problem, options, constraints]
outputs: [draft ADR]
---

# ADR Drafter

Draft an immutable decision record in `adr/` using the required sections in `standards.md`. Make alternatives and consequences explicit, validate referenced IDs, and mark the document as a draft for human review. Never edit an accepted ADR.
