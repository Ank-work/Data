# Onshape + FeatureScript + Architectural CAD Sheets — Summary

> ## ⭐ USE THIS ONE: [`MASTER-PROMPT-DALLAS-CAD.md`](./MASTER-PROMPT-DALLAS-CAD.md)
> Single self-contained work order merging every doc below — tool reality, the anti-"boxes" contract, all coordinates, AutoLISP + ezdxf routines, 14 phases, QA gates, and the disclaimer. Paste it whole into ChatGPT with Computer Use. Everything else here is background.
>
> **Paragraph prompt for ChatGPT Computer Use + AutoCAD Mac:** [`CHATGPT-AUTOCAD-MAC-PARAGRAPH-PROMPT.md`](./CHATGPT-AUTOCAD-MAC-PARAGRAPH-PROMPT.md)

**Full research (primary):** [`onshape-featurescript-cad-drawings.md`](./onshape-featurescript-cad-drawings.md) · **ChatGPT Chrome + FeatureScript playbook (Dallas DC):** [`onshape-chatgpt-chrome-featurescript-playbook.md`](./onshape-chatgpt-chrome-featurescript-playbook.md) · **A1.0 detail target (match the annotated reference):** [`a10-detail-fidelity-target.md`](./a10-detail-fidelity-target.md)

> **Active build plan:** [`dallas-autocad-web-phased-build.md`](./dallas-autocad-web-phased-build.md) — AutoCAD Web + ezdxf, phase by phase, to a client-ready nine-sheet set.
>
> **Hand to ChatGPT (Computer Use + local AutoCAD):** [`CHATGPT-AUTOCAD-DALLAS-BUILD-ORDER.md`](./CHATGPT-AUTOCAD-DALLAS-BUILD-ORDER.md) — self-contained end-to-end directive with all coordinates, AutoLISP routines, and the poché/furniture/door-swing requirements that fix the "just boxes" problem.

Interactive report: [onshape-featurescript-cad-drawings.canvas.tsx](/Users/ankurkulkarni/.cursor/projects/Users-ankurkulkarni-Arcomurray/canvases/onshape-featurescript-cad-drawings.canvas.tsx)

Grounded against: Conceptual Data Center Floor Plan (Sheet A1.0).

## Executive findings

1. **Onshape** is cloud-native mechanical CAD (Parasolid) with a Git-like document model: Document → Elements (Part Studio / Assembly / Drawing / Feature Studio), Workspace ≈ branch, Version ≈ tag, Microversion ≈ commit.
2. **FeatureScript** is the native language for parametric 3D features and custom Part Studio tables — not Drawing-sheet automation. Syntax is C-like; geometry ops (`opExtrude`, `opPattern`, sketches) run during regeneration.
3. The **sample A1.0 sheet** (grids, fire-rated walls, door schedule, keynotes, CRAH airflow, PDU feeds, parking, title/rev blocks) is architectural/MEP drafting fidelity — primarily AutoCAD / Revit / DraftSight.
4. **Onshape fits well** for rack/CRAH/PDU 3D massing, FeatureScript patterns (rack farms, aisle offsets, parking stalls), live 3D collaboration, and branching design options.
5. **Onshape fits poorly** for AIA-style discipline layers, fire-rated wall types, linked door/keynote schedules, and dense symbolic MEP annotation.
6. **Recommended path**: hybrid — AEC tool owns the sheet; Onshape owns equipment layout; exchange via DXF/DWG; optional ARES Kudo for DWG editing inside Onshape documents.
7. **REST API** can create drawings and tables; cannot insert DWG blocks; FeatureScript cannot drive Drawing annotations.
8. **Drawings** in Onshape are application elements: strong for mechanical projected views; weak for multi-discipline plan sheets; one editor at a time (no simultaneous Drawing collab).

## Key resources

- Full doc: [`onshape-featurescript-cad-drawings.md`](./onshape-featurescript-cad-drawings.md)
- https://cad.onshape.com/FsDoc/
- https://onshape-public.github.io/docs/api-intro/architecture/
- https://onshape-public.github.io/docs/api-adv/drawings/

*Compiled August 2026.*
