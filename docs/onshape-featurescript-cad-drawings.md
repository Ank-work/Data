# Onshape, FeatureScript & Architectural CAD Sheets

Research compilation: cloud CAD architecture, FeatureScript for parametric layout, and an honest fit assessment against a conceptual data-center A1.0 floor plan.

**Grounded against:** Conceptual Data Center Floor Plan (Sheet A1.0, scale 3/32" = 1'-0", May 2024) — alphanumeric grid, fire-rated wall hatches, door schedule, keynotes, cold/hot aisle CRAH airflow, PDU-A/B feeds, security mantraps, site parking with ADA stalls, north arrow, graphic scale, legend, revision block.

**Related:** short stub summary — [`onshape-featurescript-cad-drawings-summary.md`](./onshape-featurescript-cad-drawings-summary.md) · interactive canvas — `onshape-featurescript-cad-drawings.canvas.tsx`

*Compiled August 2026 from Onshape help, FsDoc, public API docs, and inspection of the sample sheet.*

---

## Table of contents

1. [Overview / executive findings](#1-overview--executive-findings)
2. [Onshape in detail](#2-onshape-in-detail)
3. [FeatureScript in detail](#3-featurescript-in-detail)
4. [CAD drawings / architectural sheets](#4-cad-drawings--architectural-sheets)
5. [Sample A1.0 → Onshape mapping](#5-sample-a10--onshape-mapping)
6. [Recommended hybrid workflows](#6-recommended-hybrid-workflows)
7. [Limitations](#7-limitations)
8. [Resources / links](#8-resources--links)

---

## 1. Overview / executive findings

### Fit verdict for the sample A1.0 sheet

Onshape is a **cloud-native mechanical 3D CAD** platform. A conceptual data-center floor plan like the sample (rated walls, door schedule, keynotes, HVAC airflow, PDU feeds, parking, title/revision blocks) is primarily **AutoCAD / Revit / DraftSight** territory. Onshape can model equipment in 3D, pattern racks with FeatureScript, and produce mechanical drawings — but **not** architectural-grade multi-discipline A-sheets at that fidelity alone.

| Signal | Meaning |
|--------|---------|
| Cloud CAD | Browser UI; Parasolid kernel |
| FeatureScript | Native parametric language (inside regeneration) |
| Mechanical | Best-fit domain |
| Hybrid | Practical path for A1.0-level fidelity |

### What the sample drawing demands

The sheet combines:

- Building floor plan + site/parking on one A1.0 sheet
- Structural grid (1–14 / A–G, ~20'–25' bays)
- Fire-rated wall symbology (2 HR / 1 HR / non-rated)
- Door schedule (mark, size, type, rating)
- Numbered keynotes and a dense legend
- Cold/hot aisle CRAH airflow and PDU feed linework
- Title block, revision block, north arrow, graphic scale

### Capability fit at a glance

| Capability class | Sample need | Onshape fit |
|------------------|-------------|-------------|
| 3D equipment layout | 42U racks, CRAH, UPS blocks | **Strong** — Part Studio / Assembly + FeatureScript patterns |
| Plan annotation density | Keynotes, room tags, egress paths | **Partial** — Drawing notes/tables; weak vs AutoCAD layers |
| Discipline layers & ratings | 2HR / 1HR / non-rated walls | **Weak** — no BIM wall types or fire schedules |
| Door / equipment schedules | Mark, size, HM type, rating | **Partial** — Drawing tables / custom tables; not Revit schedules |
| Sheet standards (A1.0) | Title, rev, north, graphic scale | **Partial** — templates + DWG insert; ARES for full DWG edit |

### Executive findings (summary)

1. **Onshape** is cloud-native mechanical CAD (Parasolid) with a Git-like document model: Document → Elements (Part Studio / Assembly / Drawing / Feature Studio), Workspace ≈ branch, Version ≈ tag, Microversion ≈ commit.
2. **FeatureScript** is the native language for parametric 3D features and custom Part Studio tables — **not** Drawing-sheet automation. Syntax is C-like; geometry ops (`opExtrude`, `opPattern`, sketches) run during regeneration.
3. The **sample A1.0 sheet** is architectural/MEP drafting fidelity — primarily AutoCAD / Revit / DraftSight.
4. **Onshape fits well** for rack/CRAH/PDU 3D massing, FeatureScript patterns (rack farms, aisle offsets, parking stalls), live 3D collaboration, and branching design options.
5. **Onshape fits poorly** for AIA-style discipline layers, fire-rated wall types, linked door/keynote schedules, and dense symbolic MEP annotation.
6. **Recommended path**: hybrid — AEC tool owns the sheet; Onshape owns equipment layout; exchange via DXF/DWG; optional ARES Kudo for DWG editing inside Onshape documents.
7. **REST API** can create drawings and tables; cannot insert DWG blocks; FeatureScript cannot drive Drawing annotations.
8. **Drawings** in Onshape are application elements: strong for mechanical projected views; weak for multi-discipline plan sheets; one editor at a time (no simultaneous Drawing collab).

---

## 2. Onshape in detail

### What Onshape is

Onshape is a fully cloud-native CAD system (PTC). Geometry runs on the **Parasolid** kernel; the UI is the browser. There is **no local file checkout model** — the document is the project, with Git-like history built into the data model.

### Document model (Git analogy)

| Onshape | ≈ Git | Role |
|---------|-------|------|
| Document | Repository | Container for all project tabs |
| Element (tab) | File | Part Studio, Assembly, Drawing, Feature Studio, Blob, App |
| Workspace | Branch | Mutable tip where edits land |
| Version | Tag | Named immutable snapshot of the whole document |
| Microversion | Commit | Every edit; full restore points |

API contexts use `w` / `v` / `m` (workspace / version / microversion).

### Element types

#### Part Studio (3D)

Ordered parametric feature list. Multiple parts share one feature tree. Sketches, extrudes, booleans, and patterns regenerate on every change. Best place for FeatureScript custom features.

#### Assembly (3D)

Instance tree + mates. Onshape mates are **degrees-of-freedom based** (not SolidWorks-style mates-only). Supports in-context edit, linked documents by version, and configurations for variants.

#### Drawing (2D)

Application element (special app tab / iframe-managed). Projected / section / detail views from parts or assemblies, dimensions, notes, BOM/tables, title block layers. **Simultaneous multi-user edit is not supported** on drawings — one editor at a time.

Architecture detail: tessellation is generated on demand, not stored as persistent BREP display.

#### Feature Studio (code)

Author FeatureScript feature types and custom table types. Features appear in the Part Studio toolbar once committed; they regenerate with the model.

### Collaboration & versions

- Multiple users edit the same workspace live (**except Drawings** — one editor at a time).
- Branch from a version to explore alternatives; merge back.
- Linked documents always pin a **specific version**; Reference Manager notifies when newer versions exist.

### Export / import formats

| Format | Use | Notes |
|--------|-----|-------|
| Parasolid (`.x_t` / `.x_b`) | Best kernel fidelity | Preferred with SolidWorks / NX ecosystems |
| STEP / IGES | Neutral exchange | Robust; validate topology for CAM |
| STL / 3MF / glTF / OBJ | Mesh / viz / print | Not for redesign |
| DWG / DXF / DWT / PDF | 2D drawings & sketches | Drawing export; sketch export; template import |
| Native translators | SW / Inventor / Creo / CATIA | Geometry-focused; history usually lost |

### Strengths vs desktop CAD

| Tool | Domain | Onshape vs it |
|------|--------|---------------|
| SolidWorks | Mechanical 3D + drawings | Similar Parasolid modeling; Onshape wins on PDM-less collab & branching; SW wins desktop ecosystem/add-ins |
| AutoCAD | 2D drafting / AEC sheets | Onshape Drawings are mechanical; AutoCAD far stronger for layers, Xrefs, arch symbols |
| Revit | BIM / AEC | Different product class — walls, rooms, schedules, MEP systems are Revit |
| Fusion 360 | Mech + CAM cloud | Closest peer; Onshape stronger pure cloud/version model |
| DraftSight / ARES | DWG editing | Onshape App Store **ARES Kudo** fills DWG edit gap inside Onshape docs |

---

## 3. FeatureScript in detail

### What it is

FeatureScript is Onshape's proprietary, **strongly typed** language for building parametric 3D features and custom Part Studio tables. Built-in features (Extrude, Fillet, Helix, …) are themselves FeatureScript. Custom features run **inside regeneration** — not as external macros.

| Trait | Detail |
|-------|--------|
| Syntax | C-like; familiar to JS / C# developers |
| Typing | Runtime types, checked at execution |
| Units | Units-aware: `ValueWithUnits` + `Vector` |

### Purpose & where it lives

| Concept | Detail |
|---------|--------|
| Feature Studio | Tab that holds FeatureScript modules / feature type definitions |
| `defineFeature` | `precondition` (UI params) + body (ops that mutate `Context`) |
| std library | Imported by default; open-source public "std" document |
| Custom tables | FeatureScript table types that query Part Studio data |
| Regeneration | Runs when params change, upstream features change, or rollback bar moves |

### FeatureScript vs macros / REST API

| Approach | Runs where | Good for | Not for |
|----------|------------|----------|---------|
| FeatureScript | Inside Part Studio regen | Parametric geometry, patterns, robust queries | Sheet annotation, PDF export, multi-doc orchestration |
| Onshape REST API | External app / server | Create drawings, tables, export, PLM hooks | Deep BREP feature authoring (limited) |
| Desktop macros (VBA/SW) | Local CAD session | UI automation on desktop files | Cloud collab model |

### Types & semantics

**Standard types:** `boolean`, `number`, `string`, `array`, `map`, `box`, `function`, `builtin`, `undefined`.

**Type tags / tests:** via `as` / `is`.

**Geometry types:** `Vector`, `ValueWithUnits`, `Query`, `Context`, `Id`.

**Syntax highlights:**

- Declarations: `var` / `const`
- Loops: `for` / `for-in`
- Lambdas: `x => x^2`
- Arrow calls: `x->f(y)`
- String concat: `~`
- Power: `^`

### Pattern: server rack grid (sketch + extrude + `opPattern`)

Prefer calculated transforms + `opPattern` on bodies/faces. Sketch linear-pattern APIs are awkward; loops that place coordinates are idiomatic.

```featurescript
annotation { "Feature Type Name" : "Rack Array" }
export const rackArray = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Rows" }
        isInteger(definition.rows, positive);
        annotation { "Name" : "Columns" }
        isInteger(definition.columns, positive);
        annotation { "Name" : "Rack W" }
        isLength(definition.rackW, { "min" : 0 * inch });
        annotation { "Name" : "Rack D" }
        isLength(definition.rackD, { "min" : 0 * inch });
        annotation { "Name" : "Rack H" }
        isLength(definition.rackH, { "min" : 0 * inch });
        annotation { "Name" : "Pitch X" }
        isLength(definition.pitchX, { "min" : 0 * inch });
        annotation { "Name" : "Pitch Y" }
        isLength(definition.pitchY, { "min" : 0 * inch });
    }
    {
        // One rack solid
        const sk = newSketchOnPlane(context, id + "sk", {
            "sketchPlane" : qCreatedBy(makeId("Top"), EntityType.FACE)
        });
        skRectangle(sk, "r1", {
            "firstCorner" : vector(0, 0) * meter,
            "secondCorner" : vector(definition.rackW, definition.rackD)
        });
        skSolve(sk);
        opExtrude(context, id + "ex", {
            "entities" : qSketchRegion(id + "sk"),
            "endBound" : BoundingType.BLIND,
            "depth" : definition.rackH
        });

        var transforms = [];
        var names = [];
        for (var r = 0; r < definition.rows; r += 1)
        {
            for (var c = 0; c < definition.columns; c += 1)
            {
                if (r == 0 && c == 0)
                    continue;
                transforms = append(transforms,
                    transform(vector(c * definition.pitchX, r * definition.pitchY, 0 * meter)));
                names = append(names, "R" ~ r ~ "C" ~ c);
            }
        }
        if (size(transforms) > 0)
        {
            opPattern(context, id + "pat", {
                "entities" : qCreatedBy(id + "ex", EntityType.BODY),
                "transforms" : transforms,
                "instanceNames" : names
            });
        }
    });
```

### Pattern: hot / cold aisle offset

Alternate row offset so racks face opposite aisles; optionally compose a Z rotation for facing.

```featurescript
// Alternate row offset: cold aisle facing (mirror every other row)
for (var r = 0; r < rows; r += 1)
{
    const y = r * (rackD + aisleWidth);
    const x0 = (r % 2 == 0) ? 0 * meter : aisleOffset; // face opposite aisle
    for (var c = 0; c < cols; c += 1)
    {
        const xf = transform(vector(x0 + c * pitchX, y, 0 * meter));
        // optionally compose rotation about Z for facing:
        // rotationAround(line(vector(0,0,0)*meter, vector(0,0,1)), 180 * degree)
        transforms = append(transforms, xf);
    }
}
```

### Pattern: parking stall sketch loop

Useful for site massing or Drawing "show sketch appearances." ADA stalls: wider corners; add aisle strip as separate rectangles.

```featurescript
const stallW = 9 * foot;
const stallD = 18 * foot;
const sk = newSketchOnPlane(context, id + "park", { "sketchPlane" : topPlane });
for (var i = 0; i < stallCount; i += 1)
{
    const x = i * stallW;
    skRectangle(sk, "s" ~ i, {
        "firstCorner" : vector(x, 0) * meter,
        "secondCorner" : vector(x + stallW, stallD)
    });
}
// ADA stalls: wider firstCorner/secondCorner, add aisle strip as separate rectangles
skSolve(sk);
// Keep as sketch entities for Drawing "show sketch appearances",
// or extrude thin slabs for 3D site massing.
```

### Debugging

| Tool | Behavior |
|------|----------|
| `println(value)` | Writes to FeatureScript notices flyout |
| `debug(context, queryOrGeom)` | Highlights entities (visible while the feature dialog is open) |
| `try` / `throw` + `reportFeatureError` | User-facing failures |

Remove debug calls before shipping features.

```featurescript
debug(context, qCreatedBy(id + "ex", EntityType.BODY));
println("transforms: " ~ size(transforms));
```

### REST API / App Store (drawings automation)

The Drawings API can:

- Create drawings
- Set borders / zones / titleblock flags
- Modify content (e.g. add `Onshape::Table::GeneralTable`)
- Export drawing JSON to discover coordinates

**Limits:**

- No DWG block insert via API
- Architectural symbol libraries stay in AutoCAD / ARES templates
- FeatureScript cannot drive Drawing annotations

**ARES Kudo** (App Store) edits DWG/DXF blobs stored in Onshape documents for true 2D drafting.

---

## 4. CAD drawings / architectural sheets

Using the sample Conceptual Data Center Floor Plan (A1.0) as the fidelity bar.

### Anatomy of an A1.0-style sheet

| Element | Sample example | Purpose |
|---------|----------------|---------|
| Plan view | Entire building + site | Horizontal cut ~4' AFF; walls, doors, equipment footprints |
| Grid system | 1–14 / A–G, 20'–25' bays | Structural coordination; dimension anchors |
| Layers / colors | Blue supply, red return, yellow/orange PDU | Discipline readability (AIA/NCS conventions vary by firm) |
| Wall ratings | 2 HR / 1 HR / non-rated hatch | Life safety / code; legend-driven |
| Door schedule | Mark, 3'-0"×7'-0", H.M., rating | Spec + hardware coordination |
| Keynotes | 1–6 (racks, PDU, rated walls) | Dense annotation without cluttering plan |
| Legend | Symbols for FE, pull station, exit | Graphic dictionary for the sheet |
| Title block | Project, location, date, scale, A1.0 | Sheet identity; often company standard |
| Revision block | Rev 1 Conceptual Issue | Issue tracking |
| HVAC airflow | Cold/hot aisle arrows, CRAH-1…8 | Conceptual MEP intent |
| Electrical | PDU-A / PDU-D dashed feeds | Distribution path (not full one-line) |
| Site / parking | Stalls, ADA, trees, drive arrows | Civil/site context on same sheet |
| Scale / north | 3/32"=1'-0", north arrow | Orientation & measurement |

### Sample sheet content (grounding detail)

From the Conceptual Data Center Floor Plan image:

- **Title block:** Conceptual Data Center · Anytown, USA · Sheet A1.0 · Scale 3/32" = 1'-0" · Date May 15, 2024 · Rev 1 Conceptual Issue
- **Data hall (Room 200):** rack rows, cold (blue) / hot (red) aisle arrows, CRAH-1…8 at perimeter, overhead supply/return dashed paths
- **West office wing:** offices 101–103, conference 104, storage, IT closet, restrooms, break room 109
- **Entry / security:** vestibule 100, lobby 110, security mantrap 120 → data hall entrance 121
- **East power/support:** UPS 210, battery 211, electrical/switchgear 212, telecom/network 213, staging/loading 214
- **Site:** parking (standard + ADA), one-way vehicle entrance, landscaping trees, north arrow, graphic scale (0–48')
- **Legend / schedules:** wall rating hatches, door types, egress/FE/pull stations, HVAC arrows, cable trays, electrical distribution A/B, CHWS/R piping, column symbol; keynotes 1–6; door schedule (Mark / Size / Type / Fire Rating)

### 2D drafting vs 3D → 2D generation

| Approach | Characteristics |
|----------|-----------------|
| **Native 2D drafting** (AutoCAD lineage) | Lines, blocks, Xrefs, paper space viewports, layer states. Ideal for conceptual plans, legends, and schedules that are primarily symbolic. **Fidelity of the sample lives here.** |
| **3D → Drawing views** (Onshape / SW / Revit) | Model geometry; generate projected views; add dimensions/notes. Excellent when the truth is the 3D model (racks, CRAH boxes). Weak when the sheet is mostly 2D symbology and code annotations. |

### Lineweights & discipline colors (typical practice)

- Walls cut in plan: **heavy**
- Equipment footprints: **medium**
- Hidden / overhead: **dashed**
- Demo / egress: distinct dashed (often green)
- HVAC supply / return: cool / warm hues
- Electrical distribution: dashed accent colors

Never rely on color alone for print — line type + legend matter for B&W plots.

### BIM note

Revit would encode rooms, wall types, door instances, and schedules as data. The sample is a **conceptual presentation drawing** — it can be pure 2D CAD with dumb geometry + tables, or a lightweight BIM export. Onshape has neither full AIA layer standards nor Revit-like room/wall objects.

---

## 5. Sample A1.0 → Onshape mapping

Honest mapping from the Conceptual Data Center Floor Plan to Onshape tools.

**Fit legend:** Strong = native strength · Partial / OK = workaround · Weak = poor fit · Hybrid = best practical path

| Sample element | Onshape approach | Fit | Notes |
|----------------|------------------|-----|-------|
| 42U rack rows / aisles | FeatureScript rack array + Assembly instances | Strong | Parametric pitch, row count, aisle width |
| CRAH / UPS / switchgear blocks | Simplified solids in Part Studio | Strong | Massing, not vendor BIM families |
| Building shell / rooms | Extruded walls from sketch or imported DXF profile | Partial | No wall types / fire rating parameters |
| 2 HR / 1 HR hatch legend | Drawing hatches + manual notes | Weak | No automated rating from model |
| Door schedule | Drawing general table (manual or API) | Partial | Not linked door instances like Revit |
| Keynotes 1–6 | Drawing notes / balloons | Partial | No keynote database |
| Title + rev block | Custom template; DWG/DWT insert to format layers | Partial | Lock Title Block / Border layers |
| Grid bubbles 1–14, A–G | Sketch construction lines + Drawing dimensions | OK | Or import grid from DXF |
| PDU-A/B dashed feeds | 3D curves / sketch overlays shown in drawing | Partial | Symbolic linework easier in AutoCAD |
| Cold/hot aisle arrows | Drawing sketches / notes (not FS) | OK | Annotation lives on Drawing tab |
| Parking + landscaping | FS stall pattern or DXF site plan | Partial | Trees/blocks are DWG territory |
| North arrow / graphic scale | Template blocks or inserted DXF | Partial | Standard in arch templates |
| Sheet A1.0 multi-discipline | Hybrid: Revit/ACAD sheet + Onshape equip xref | Hybrid | Best practical path |
| Full AIA layer discipline set | Onshape layers are limited vs AutoCAD | Weak | Use ARES Kudo on DWG blob |

### Dimensioning approaches

| Method | When |
|--------|------|
| Model-driven Drawing dimensions | Grid spacing, building envelope from 3D/sketches |
| Sketch dimensions in Part Studio | Drive parametric layout; show sketch in drawing view |
| Pure Drawing sketch dimensions | Annotation that should not change the model |
| Import dimensioned DXF | When civil/arch already owns the sheet |

---

## 6. Recommended hybrid workflows

Architectural sheet ownership stays in AEC tools; Onshape owns equipment layout truth and patterning.

### Workflow diagram (conceptual)

```text
Revit / AutoCAD ──► DXF / DWG export ──┐
                                       ├──► Drawing / ARES Kudo ──► PDF / DWG out
Onshape 3D equipment ◄──► FeatureScript ┘
         patterns
```

- Revit/AutoCAD produce the architectural/MEP sheet content (or export DXF/DWG into the drawing environment).
- Onshape 3D equipment + FeatureScript patterns feed mechanical truth into the drawing path.
- FeatureScript ↔ Part Studio is a tight regen loop (patterns drive equipment; equipment params drive patterns).
- Final deliverable: PDF / DWG out of Drawing or ARES.

### Path A — Onshape-centric (equipment study)

Best when the goal is layout studies, not a permit-ready A-sheet.

1. Part Studio: site outline + building shell sketches (or DXF import to sketch).
2. FeatureScript: rack arrays, parking stalls, repeating CRAH placeholders.
3. Assembly: mate equipment; configurations for aisle counts.
4. Drawing: top view, dimensions on grids, manual tables for doors/keynotes.
5. Export PDF/DWG for review — expect rework in AutoCAD for legend density.

### Path B — AEC sheet + Onshape equipment (recommended for A1.0)

1. Revit or AutoCAD owns walls, ratings, doors, schedules, site, title block.
2. Onshape models racks/CRAH/PDU; export footprints DXF or place via coordinates.
3. FeatureScript generates rack grid CSV/points or DXF sketch export for Xref.
4. Optional: store DWG in Onshape; edit with ARES Kudo for collab vaulting.

### Path C — API automation (limited)

REST: create drawing, add general tables (door schedule shell), set titleblock/border. **Cannot** insert DWG blocks by coordinate via API. FeatureScript **cannot** drive Drawing annotations. Use API for release packaging / export, not for fabricating arch sheets.

### What Onshape does well for this project type

- Parametric rack farms
- CRAH / PDU massing
- Live collab on 3D
- Version / branch design options
- Configurations for hall density

---

## 7. Limitations

### Hard limits vs the sample

| Gap | Why it matters |
|-----|----------------|
| Fire-rated wall BIM | No wall types / fire rating parameters; hatches are manual Drawing annotation |
| Linked door schedules | Drawing tables are not Revit-like instance schedules |
| Keynote databases | No keynote system; notes/balloons are manual |
| Dense MEP symbology | Symbolic linework (PDU feeds, airflow arrows, cable trays) is AutoCAD/ARES territory |
| Multi-user Drawing edit | One editor at a time on Drawing tabs |
| AIA layer standards | Onshape layers are limited vs AutoCAD; use ARES Kudo on DWG blob |

### Drawing automation ceiling

FeatureScript automates **3D** (and Part Studio tables). Drawing tabs are a separate application element: views/dimensions/notes are interactive or REST-driven, **not** FeatureScript. Do not plan on "FS generates the A1.0 sheet."

### Domain boundary

Onshape is the wrong primary tool if the deliverable is a multi-discipline architectural presentation sheet. It is the right primary tool if the deliverable is parametric equipment layout with mechanical drawings derived from that truth.

---

## 8. Resources / links

Docs & resources (2024–2026):

| Resource | URL |
|----------|-----|
| FeatureScript intro | https://cad.onshape.com/FsDoc/ |
| Syntax & semantics | https://cad.onshape.com/FsDoc/syntax.html |
| Std library docs | https://cad.onshape.com/FsDoc/library.html |
| Versions & history help | https://cad.onshape.com/help/Content/Document/versions_and_history.htm |
| API architecture | https://onshape-public.github.io/docs/api-intro/architecture/ |
| Drawings API | https://onshape-public.github.io/docs/api-adv/drawings/ |
| Insert DXF/DWG (Drawings) | https://cad.onshape.com/help/Content/Drawing/insert_dxf_or_dwg.htm |
| Custom drawing templates | https://cad.onshape.com/help/Content/Drawing/custom_drawing_templates.htm |
| ARES Kudo + Onshape | https://www.onshape.com/en/blog/how-to-create-and-modify-dwg-drawings |

### Local artifacts

| Artifact | Path |
|----------|------|
| This document (primary) | `docs/onshape-featurescript-cad-drawings.md` |
| Short summary stub | `docs/onshape-featurescript-cad-drawings-summary.md` |
| Interactive canvas | `~/.cursor/projects/.../canvases/onshape-featurescript-cad-drawings.canvas.tsx` |
| Grounding image | Conceptual Data Center Floor Plan (Sheet A1.0) asset |

---

*End of research compilation.*
