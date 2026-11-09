---
name: diagram-sync
triggers: [architecture or flow changed]
inputs: [source documents, existing diagrams]
outputs: [diagram change proposal]
---

# Diagram Sync

Compare text-based diagrams in `diagrams/` with their referenced architecture and flow documents. Propose the smallest Mermaid, D2, or PlantUML update and identify changed relationships. Do not create binary diagrams.
