# A1.0 Detail Fidelity Target — Conceptual Data Center Floor Plan

**Reference:** Detailed Conceptual Data Center Floor Plan (Sheet A1.0 style) — the white-on-black annotated sheet with rooms, parking, legend, keynotes, door schedule, CRAH airflow, and title block.

**Your current Onshape sheet:** Site massing at ~1:4000 with unlabeled boxes. That is **not** this fidelity level.

**Dallas geometry source:**  
`/Users/ankurkulkarni/Documents/Codex/2026-08-12/can/outputs/dallas-data-center-cad-basis.md`

**Related:** [`onshape-chatgpt-chrome-featurescript-playbook.md`](./onshape-chatgpt-chrome-featurescript-playbook.md) (massing path) · [`onshape-featurescript-cad-drawings.md`](./onshape-featurescript-cad-drawings.md) (tool limits)

---

## 1. Verdict (read this first)

| Question | Answer |
|----------|--------|
| Can FeatureScript + one Onshape Drawing get **this** sheet? | **No** — not at this annotation density. |
| What tool produces this look? | **2D AEC CAD / BIM:** AutoCAD, DraftSight, BricsCAD, Revit, or **ARES Kudo** (DWG inside Onshape vault). |
| What is Onshape still good for? | Parametric **3D equipment** (racks, CRAH, UPS) → export footprints to the plan. |
| How do you use ChatGPT Chrome for *this* target? | Drive **AutoCAD / DraftSight / ARES** drawing commands + layer setup + schedule tables — not FeatureScript alone. |

**Recommended path to match the reference:**  
**AutoCAD-class DWG for the sheet** + optional Onshape equipment → DXF into the plan. ChatGPT Chrome coaches layers, blocks, text, and schedules while you draw.

---

## 2. Detail inventory — everything the reference has that you need

Use this as the acceptance checklist. Your Dallas sheet is “done” only when every row is present (adapted to Dallas basis names/coords).

### 2.1 Sheet framework

| # | Element | Reference example | Dallas adaptation |
|---|---------|-------------------|-------------------|
| F1 | Sheet size + border + zone grid (letters/numbers) | A–G / 1–14 style | Size D or Arch D; your grid |
| F2 | Title block filled | Project, date, scale, sheet **A1.0** | Conceptual Dallas Data Center; scale readable for building plan |
| F3 | Revision block | Rev table | At least Rev 0 |
| F4 | North arrow + graphic scale | Bottom-left | Required |
| F5 | Structural / planning grid bubbles | 1–14 / A–G with bay dims | Per Dallas basis grids |
| F6 | Overall building dimensions | Exterior dim strings | 1,000 × 720 ft building (basis) |

### 2.2 Admin / public rooms (must be drawn **and labeled**)

Reference rooms → map to Dallas south band (§11):

| # | Room type | Reference | Dallas basis (building-local) |
|---|-----------|-----------|-------------------------------|
| R1 | Vestibule | 100 | X 455–545, Y 0–18 |
| R2 | Lobby / reception | 110 | X 410–590, Y 18–70 |
| R3 | Security mantrap | 120 | X 455–545, Y 70–110 (split Y 88) |
| R4 | Security ops / NOC | — | Security X 350–430, Y 70–110; NOC X 350–410, Y 0–70 |
| R5 | Private offices | 101–103 | Four offices X 0–120, Y 62–110 |
| R6 | Conference | 104 | X 120–200, Y 62–110 |
| R7 | Break room | 109 | X 0–80, Y 0–50 |
| R8 | Men’s / women’s RR | 107 / 108 | X 80–130 / 130–180, Y 0–50 |
| R9 | Storage / IT | 105 / 106 | Storage + IT closet per §11.1 |
| R10 | Training / lockers / open office | (extra on Dallas) | Lockers, training, open office, etc. |

**Each room needs:** closed wall polyline, **room name + number** text, door swings with marks.

### 2.3 Data hall detail

| # | Element | Required |
|---|---------|----------|
| D1 | Data hall perimeter + room number | Yes (Dallas: multiple halls — one detailed hall sheet + campus key plan) |
| D2 | Every rack row drawn | Yes (pitch from basis) |
| D3 | Cold aisle / hot aisle labels | Yes |
| D4 | Supply (cyan) + return (red) airflow arrows | Yes (symbolic) |
| D5 | CRAH units labeled CRAH-1…n | Yes |
| D6 | Containment doors / “no step aisle” notes | Yes |
| D7 | Sensors optional | Nice-to-have |

### 2.4 Power / support wing

| # | Element | Dallas mapping |
|---|---------|----------------|
| P1 | UPS rooms labeled | East UPS blocks §12.2 |
| P2 | Battery rooms labeled | X 940–1000 bands |
| P3 | Electrical / switchgear | Main electrical + UPS/switchgear |
| P4 | Telecom / meet-me | §11.4 |
| P5 | Staging / loading + large loading door callout | §11.3 + door size from basis |

### 2.5 Parking / site (on same sheet or companion sheet)

Reference puts parking on the **same** A1.0. For Dallas 101-acre site, prefer:

- **A1.0** — building floor plan at readable scale (admin + one hall + support)  
- **C1.0** — site/parking at larger scale  

Still required for “this amount of detail” on the parking sheet:

| # | Element |
|---|---------|
| S1 | Parking boundary |
| S2 | Every stall line (Dallas: **180** stalls) |
| S3 | ADA stalls + ISA symbol (6 accessible) |
| S4 | Drive aisle arrows / one-way entrance text |
| S5 | Landscape tree blocks (symbolic OK) |
| S6 | Pedestrian axis / drop-off callout |

### 2.6 Annotation systems (this is why the reference looks “rich”)

| # | System | Contents |
|---|--------|----------|
| A1 | **Legend** | 2 HR / 1 HR / non-rated walls; door types; exit; FE; sensors; supply/return; cable tray; piping |
| A2 | **Keynotes** 1–6+ | Rack typ., PDU-A, PDU-B, containment door, no-step aisle, fire-rated wall… |
| A3 | **Door schedule** table | Mark, size, material, fire rating for every door |
| A4 | Layer colors | Walls, furniture, HVAC arrows, electrical dashed feeds, landscaping |
| A5 | Dimensions | Grids, rooms, aisles, rack pitch, parking modules |
| A6 | Exit paths | Dashed egress routes |

Without **A1–A6**, the drawing stays “bland” even if walls exist.

---

## 3. Gap vs your current Onshape export

| Reference | Your screenshot | Gap |
|-----------|-----------------|-----|
| Room labels everywhere | None | 100% missing |
| Lobby, offices, RR, break, security | Not identifiable | Geometry and/or labels missing |
| Parking stalls + ADA | Not shown as stalls | Missing module |
| CRAH + hot/cold arrows | None | Missing |
| Legend + keynotes + door schedule | None | Missing |
| Readable plan scale (~3/32"=1'-0") | **1:4000** | Wrong sheet type / scale |
| Filled title / sheet A1.0 | Blank title | Missing |
| Lineweight hierarchy | Flat wireframe | Missing |

---

## 4. How to get this fidelity (practical tool path)

### Path A — Recommended (match the reference)

1. **Draft in AutoCAD / DraftSight / BricsCAD / ARES Kudo** (DWG).  
2. Keep ChatGPT Chrome open; use it for layer lists, block definitions, schedule CSV→table text, and command sequences.  
3. Import Dallas basis coordinates as construction lines / rectangles (ChatGPT can generate a script or step list from the basis MD).  
4. Optional: model racks in Onshape → **export DXF** of top footprints → insert on `I-EQPM` layer.  
5. Build legend, keynotes, door schedule, title block last.  
6. Plot PDF black background or white — style choice.

### Path B — Onshape-only (partial; expect weeks; still weaker)

Use only if you refuse DWG tools:

1. Part Studio: **every** room rectangle + wall extrude + door openings + parking stalls + rack/CRAH solids.  
2. Drawing at **building scale** (not 1:4000) — separate site Drawing.  
3. Hand-place **hundreds** of notes for room names, CRAH IDs, aisle labels.  
4. Manual tables for doors/keynotes.  
5. Fake wall-rating graphics with hatched regions or sketched symbols.

**Limit:** No real AIA wall-type system, weak multi-discipline layers, painful schedule linkage. You will not reach the reference’s polish easily.

### Path C — Hybrid (best of both)

| Own in Onshape | Own in DWG/Revit |
|----------------|------------------|
| Rack arrays, CRAH, UPS massing (FeatureScript) | Walls, rooms, doors, parking, site |
| Config-driven hall options | Legend, keynotes, door schedule, title |
| 3D walkthroughs | Sheet A1.0 / C1.0 packaging |

---

## 5. ChatGPT Chrome prompts aimed at **this** detail level

Paste into ChatGPT while **AutoCAD/DraftSight/ARES** (not Feature Studio) is focused.

### 5.1 Layer standard

```text
I am drafting a conceptual data center floor plan to match A1.0 architectural detail
(legend, keynotes, door schedule, room tags, cold/hot aisle arrows, parking).
Give me an AIA/NCS-inspired layer list with names, colors, and linetypes for:
walls rated/non-rated, doors, room tags, furniture, HVAC supply/return,
electrical PDU feeds, parking, landscape, dimensions, viewport/title.
Then the exact command sequence to create them in AutoCAD.
```

### 5.2 Draw Dallas admin band from basis

```text
Using these Dallas building-local coordinates [paste §11.1–11.2 from dallas-data-center-cad-basis.md],
give AutoCAD steps (or a LISP/script outline) to draw every room polyline on layer A-WALL,
add room tags NAME + number at centroids, and place door arcs with marks at:
vestibule 6ft pairs @ X=500, mantrap 4ft doors, office doors typical 3'-0"x7'-0".
```

### 5.3 Data hall annotation pack

```text
I have rack rows and CRAH footprints drawn. Generate:
1) keynote list matching: 42U rack typ, PDU-A, PDU-B, containment door, no-step aisle, fire-rated wall
2) MTEXT for COLD AISLE / HOT AISLE
3) how to draw cyan supply and red return arrows between CRAH and aisles
AutoCAD commands only.
```

### 5.4 Door schedule table

```text
Build a door schedule table (Mark, Width, Height, Material, Fire Rating, From→To)
for every door in the Dallas admin + mantrap + loading list from this basis excerpt: [paste].
Format as CSV I can import or type into a TABLE.
```

### 5.5 If staying in Onshape Drawing

```text
I have a Part Studio top view in an Onshape Drawing. Scale is wrong (1:4000).
Walk me click-by-click to: set scale so the 1000×720 ft building fills ~60% of a D-size sheet,
add Note labels for each room from this list [paste rooms],
insert a General table for door schedule, and fill the title block for sheet A1.0.
```

---

## 6. Minimum acceptance test (“this amount of detail”)

Print or PDF the sheet and check:

- [ ] Can you find **Lobby**, **Offices**, **Break room**, **Restrooms**, **Security/mantrap** by **reading labels** in under 5 seconds?  
- [ ] Is **parking** drawn as stalls (not one empty rectangle)?  
- [ ] Are **cold/hot aisles** and **CRAH** labeled?  
- [ ] Is there a **legend** + **keynotes** + **door schedule**?  
- [ ] Is the building plan at a **readable scale** (not 1:4000 site postage stamp)?  
- [ ] Is the **title block** filled (project, scale, sheet A1.0)?  

If any box fails, you do not yet have the reference fidelity.

---

## 7. What to do next (ordered)

1. **Stop polishing the 1:4000 Onshape site Drawing** as if it were A1.0 — demote it to **key plan / C-sheet only**.  
2. Pick **Path A or C** (DWG for the annotated plan).  
3. Draw **admin south band rooms + labels** first (instant “not bland” win).  
4. Add **one data hall** with racks + CRAH + aisle arrows.  
5. Add **parking module** (or separate C1.0).  
6. Add **legend + keynotes + door schedule + title**.  
7. Only then bring Onshape FeatureScript racks in as DXF if you still want parametric equipment.

---

*Compiled to answer: “I need this amount of details” against the Conceptual Data Center A1.0 reference.*
