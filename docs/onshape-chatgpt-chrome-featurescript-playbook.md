# Onshape + ChatGPT Chrome Extension — Dallas Data Center FeatureScript Playbook

**Purpose:** Practical, end-to-end instructions for using the **ChatGPT Chrome extension** beside **Onshape** in the browser to build a **parametric CAD model** of the Dallas 101-acre data-center concept, with **FeatureScript as the primary build path**, then packaging a Drawing sheet for review export.

**Design basis (source of truth):**  
`/Users/ankurkulkarni/Documents/Codex/2026-08-12/can/outputs/dallas-data-center-cad-basis.md` (CAD Basis of Design v0.1)

**Related research in this workspace:**
- [`onshape-featurescript-cad-drawings.md`](./onshape-featurescript-cad-drawings.md) — capability research
- [`onshape-featurescript-cad-drawings-summary.md`](./onshape-featurescript-cad-drawings-summary.md) — short summary
- [`a10-detail-fidelity-target.md`](./a10-detail-fidelity-target.md) — **match the annotated A1.0 reference** (rooms, parking, legend, door schedule); use this if FeatureScript massing feels too bland
- Canvas (optional): `~/.cursor/projects/.../canvases/onshape-featurescript-cad-drawings.canvas.tsx`

**Status of the basis:** Conceptual / dimensionally coordinated test design — **not** sealed A/E construction documents. Treat all geometry as planning massing until licensed disciplines validate.

---

## Table of contents

1. [Honest capability framing](#1-honest-capability-framing)
2. [Dallas basis → FeatureScript build checklist](#2-dallas-basis--featurescript-build-checklist)
3. [Step-by-step setup](#3-step-by-step-setup)
4. [Onshape document recipe](#4-onshape-document-recipe)
5. [FeatureScript-first build plan (starter skeletons)](#5-featurescript-first-build-plan-starter-skeletons)
6. [ChatGPT Chrome prompt templates](#6-chatgpt-chrome-prompt-templates)
7. [Drawing sheet procedure (after geometry exists)](#7-drawing-sheet-procedure-after-geometry-exists)
8. [End-to-end runbook (zero → export)](#8-end-to-end-runbook-zero--export)
9. [Limitations & failure modes](#9-limitations--failure-modes)
10. [Assumptions & gaps in the Dallas basis](#10-assumptions--gaps-in-the-dallas-basis)

---

## 1. Honest capability framing

### What the ChatGPT Chrome extension actually does here

| Claim | Reality |
|-------|---------|
| “ChatGPT controls Onshape” | **Semi-automation only.** The extension can help you *in the browser UI*: suggest FeatureScript, walk click-paths, fill dialog fields you paste into, and fix regen errors you paste back. It is **not** a native Onshape API integration. |
| API keys | Optional and **separate**. If you later use Onshape REST API for drawing create/export, keep secrets in env/local config — **never paste API keys into ChatGPT**. |
| Side-by-side workflow | Keep Onshape open on `cad.onshape.com`, Feature Studio / Part Studio visible, ChatGPT side panel or popup open. Copy → paste → regenerate → iterate. |

### What FeatureScript builds

| FeatureScript **does** | FeatureScript **does not** |
|------------------------|----------------------------|
| Parametric **3D Part Studio** geometry | Automatically produce a full **A1.0 architectural sheet** |
| Custom features (rack grid, parking, CRAH modules) | Drive Drawing title blocks, door schedules, keynotes, fire-rating hatches |
| Patterns via `opPattern` / sketch loops | Encode BIM wall types or linked Revit-style schedules |
| Variables / configuration-driven counts | Replace AutoCAD/Revit for multi-discipline symbology |

### What Onshape Drawings still require

After geometry exists, you still **manually or semi-manually**:

1. Create a Drawing tab and choose sheet size / template  
2. Insert a **top / named view** of the Part Studio or Assembly  
3. Set scale, add dimensions, notes, north/graphic scale (template or sketch)  
4. Build **tables** (door schedule, rack counts) from CSV or typed rows  
5. Export **PDF** (and optionally DWG/DXF)

ChatGPT can coach the click-path and draft note/table text; it cannot “regen” the sheet from FeatureScript.

### Hybrid path (brief — then ignore for this playbook)

For true AEC sheet fidelity (2 HR / 1 HR walls, keynote databases, full AIA layers): keep walls/schedules in **AutoCAD / Revit / DraftSight / ARES Kudo**, export equipment footprints from Onshape via DXF/DWG. **This playbook focuses on the Onshape-code path you asked for** — FeatureScript massing + Drawing packaging for conceptual review, not permit-ready A-sheets.

---

## 2. Dallas basis → FeatureScript build checklist

Extracted from the Dallas CAD Basis v0.1 and mapped to concrete Onshape / FeatureScript work items.

### 2.1 Project constants (drive Variables + FeatureScript params)

| Item | Value | FS / Variable name suggestion |
|------|-------|-------------------------------|
| Site area | 101 acres = 4,399,560 ft² | `SITE_AREA_FT2` |
| Site square side | 2,097.513 ft | `SITE_SIDE` |
| Building outside face | 1,000 × 720 ft | `BLDG_W`, `BLDG_D` |
| Building SW on site | (548.756, 688.756) | `BLDG_SITE_X0`, `BLDG_SITE_Y0` |
| IT load | 96 MW; 8 × 12 MW halls | `IT_MW`, `HALL_MW` |
| Rack power | 20 kW/rack | `RACK_KW` |
| Total racks | 4,800 (600 × 8) | `RACK_TOTAL`, `RACKS_PER_HALL` |
| Hall size | 175 × 240 ft | `HALL_W`, `HALL_D` |
| Rack footprint | 4 ft (E–W depth) × 2 ft (N–S width) | `RACK_D`, `RACK_W` |
| Rack rows / hall | 10 rows × 60 cabinets | `ROWS`, `COLS` |
| CRAH modules / hall | 26 (13 west + 13 east), 8 × 12 ft | `CRAH_COUNT`, `CRAH_W`, `CRAH_D` |
| Parking | 312 × 312 ft; 180 stalls (174 std + 6 ADA) | `PARK_SIDE`, `STALL_COUNT` |
| Facility demand (PUE 1.25) | 120 MW; ~150 MVA planning placeholder | note only |
| Exterior wall (conceptual) | 12 in inward from outside face | `WALL_EXT` |
| Interior partitions | 6 in ordinary; 12 in major/fire-barrier | `WALL_INT`, `WALL_MAJOR` |

**Coordinate rules (must follow in sketches):**

- Site origin `(0,0)` = SW property corner; +X east, +Y north  
- Building-local `(0,0)` = site `(548.756, 688.756)`  
- Decimal feet for site; feet-inches OK on architectural Drawing annotations  
- **Do not scale from images** — enter every number numerically from the basis

### 2.2 Rooms / zones checklist

#### Site / civil

| Zone | Geometry (basis) | Build item |
|------|------------------|------------|
| Property square | SW–SE–NE–NW at ±2,097.513 | Sketch `00_SITE_CONTROL` |
| 100 ft planning reserve | Inside N/E/W + most of S; break at drives | Offset / sketch |
| Fire-access loop | 26 ft wide; inner 15 ft from bldg face | Extruded slab or sketch bands |
| Parking square | 312×312; SW (892.756, 276.756) | Parking FeatureScript |
| Public entry drive | X 1,033.756–1,063.756, Y 0–276.756 | Sketch roads |
| Service drive | X 1,850–1,890, Y 0–790; 40 ft | Sketch roads |
| Loading apron | X 1,198.756–1,398.756, Y 600–688.756 | Sketch |
| Substation yard | 340×400 at (1650–1990, 830–1230) | Placeholders |
| Generator yard | 898×300 at (600–1498, 1510–1810); 42 gen positions | Pattern placeholders |
| Heat-rejection yard | 898×180 at (600–1498, 1810–1990); 32 cells | Pattern placeholders |
| Stormwater reserves | West + SW rectangles | Sketch only (no basins) |

#### Building shell & grid

| Item | Basis | Build item |
|------|-------|------------|
| Outside-face rectangle | 1,000 × 720 | Floor plate + wall extrude |
| Principal X grid | 0, 120, 295, 315, 490, 510, 685, 705, 880, 1000 | Construction sketch |
| Principal Y grid | 0, 110, 350, 370, 610, 720 | Construction sketch |
| Halls H1–H8 | See §2.3 | Hall rectangles + rack module |
| Spines | X 295–315, 490–510, 685–705; Y 110–610 | Corridor voids / sketches |
| Cross-corridor | X 120–880, Y 350–370 | Corridor |

#### South band Y 0–110 (admin / security / logistics)

| Room / zone | Local X × Y | Notes |
|-------------|-------------|-------|
| Break room | 0–80 × 0–50 | Tag rooms |
| Men’s / women’s RR | 80–130 / 130–180 × 0–50 | 5 ft turning circle note |
| Lockers / wellness | 180–240 × 0–50 | |
| Training | 240–350 × 0–50 | |
| Admin corridor | 0–350 × 50–62 | 12 ft |
| Offices ×4 | 0–120 × 62–110 (30 ft each) | |
| Conference / open office / IT / storage | 120–350 × 62–110 | Split per basis |
| NOC | 350–410 × 0–70 | |
| Vestibule / lobby / mantrap | 410–590 band | Double doors on X=500 |
| Fire command | 590–650 × 0–70 | |
| Receiving / storage / spares / waste | 650–850 | Loading doors at X 680–694 & 710–724 |
| Carrier / MMR / main electrical | 850–1000 | |

#### West / east / north technical bands

| Band | Range | Contents |
|------|-------|----------|
| West mechanical | X 0–120, Y 110–610 | Cooling/pump rooms A/B N&S |
| East electrical | X 880–1000, Y 110–610 | UPS/distro + battery split at X 940 |
| North technical | Y 610–720 | Water treatment, E1–E4, central switchgear |

### 2.3 Halls, racks, HVAC, electrical (equipment counts)

| Hall | Local X | Local Y | Racks | IT |
|------|---------|---------|-------|-----|
| H1 | 120–295 | 110–350 | 600 | 12 MW |
| H2 | 315–490 | 110–350 | 600 | 12 MW |
| H3 | 510–685 | 110–350 | 600 | 12 MW |
| H4 | 705–880 | 110–350 | 600 | 12 MW |
| H5 | 120–295 | 370–610 | 600 | 12 MW |
| H6 | 315–490 | 370–610 | 600 | 12 MW |
| H7 | 510–685 | 370–610 | 600 | 12 MW |
| H8 | 705–880 | 370–610 | 600 | 12 MW |

**Per-hall rack module (do not mirror — translate only):**

- 10 N–S rows; 60 cabinets each; Y `60–180` hall-local  
- Row X ranges (exact): R1 `45.5–49.5` … R10 `125.5–129.5` (see basis §10.1)  
- Hot aisles 4 ft; cold aisles 6 ft; south/north cross aisles Y `0–60` / `180–240`  
- Tags: `Hh-Rrr-Ccc` (e.g. `H3-R07-C42`)  
- CRAH: 13 modules west X `10–18`, 13 east X `157–165`; Y `12+17k` to `24+17k`, k=0…12  
- UPS conceptual: 6 × 2.5 MW modules per hall block (5+1); placeholder boxes in east band  
- Generators campus: 42 × 3 MW positions; chillers: 32 × 1,000-ton cells  

### 2.4 Parking geometry checklist

| Element | Spec |
|---------|------|
| Boundary | 312 × 312; local origin P = site (892.756, 276.756) |
| Stall depth | 18 ft; aisle | 24 ft two-way |
| Rows 1–5 | 30 × 9 ft standard; X strip 21–291 |
| Row 6 | 24 standard + 6 accessible (van + shared aisles per basis §7.2) |
| Total | **180** |

### 2.5 Schedule / sheet needs (Drawing tab — not FeatureScript)

| Schedule / note set | Source in basis | How to produce in Onshape |
|---------------------|-----------------|---------------------------|
| Door schedule | Hall equipment doors (8 ft), vestibule 6 ft pairs, mantrap 4 ft, loading 14 ft ×2 | Drawing general table (manual/CSV) |
| Room list | South band + technical rooms | Table + room tags as notes |
| Rack count verification | 4,800 / 600 | BOM or custom table / note |
| CRAH / UPS / gen / chiller counts | §§10, 14, 15 | Equipment schedule table |
| Keynotes | Cold/hot containment, A/B feeds, fire loop | Drawing notes |
| Title block | Project name, Dallas concept, scale, date, sheet ID | Template / locked layers |

**Sheets suggested by basis §17:** site · architectural plan · rack plan · mechanical concept · electrical concept · life-safety concept · schedules — do **not** dump everything on one unreadable sheet.

---

## 3. Step-by-step setup

### 3.1 Create Onshape account and Dallas document structure

1. Sign up / sign in at [https://cad.onshape.com](https://cad.onshape.com).  
2. **Create Document** → name: `Dallas-101ac-DC-CAD-Basis-v0.1` (or similar).  
3. Optional: create a **Folder** `Dallas Data Center` and keep linked research outside Onshape.  
4. Immediately create a **Version** named `v0-empty-scaffold` after you add the tab recipe in §4 (so you can roll back).  
5. Sharing: start **Private**. If collaborating, share by email with **Edit** only for trusted users; avoid “Anyone with link” for conceptual campus layouts with coordinate data you care about.

### 3.2 Install / configure ChatGPT Chrome extension for Onshape

1. Install the official **ChatGPT** extension from the Chrome Web Store (OpenAI’s listing).  
2. Pin the extension. Sign in to ChatGPT.  
3. Open Onshape (`cad.onshape.com`) in a tab. Open the ChatGPT side panel (or popup — side panel is better for copy/paste).  
4. **Permissions / practical tips:**
   - Allow the extension on `cad.onshape.com` (and `*.onshape.com` if prompted).  
   - Prefer a wide monitor or split window: Onshape ~70% / ChatGPT ~30%.  
   - Keep **Feature Studio** open in one document tab while Part Studio is another — ChatGPT does not hold Onshape tabs for you.  
   - When regenerating features, watch the FeatureScript **notices** flyout; paste errors into ChatGPT verbatim.  
5. **Safety:**
   - Never paste Onshape **OAuth client secrets**, API keys, or personal access tokens into chat.  
   - Do not paste other users’ private document URLs into public ChatGPT shares.  
   - Prefer pasting **FeatureScript code + error text**, not screenshots of credentials.  
   - If you use API automation later, store secrets in a local `.env` ignored by git.

### 3.3 Recommended working loop (extension + Feature Studio)

```text
1. Ask ChatGPT for ONE feature (e.g. rack array for one hall)
2. Paste into Feature Studio → Commit / save
3. Insert feature in Part Studio → set Dallas params
4. If regen fails → copy error → “Fix this FeatureScript…” prompt
5. Version after each stable milestone (site, shell, one hall, all halls, parking)
6. Only then open Drawing tab
```

**Tip:** Ask for **chunks** (one feature type per response). Mega-pastes of 800 lines are hard to debug in Feature Studio.

---

## 4. Onshape document recipe

Create these **tabs/elements** (names are suggestions — keep order):

| # | Element type | Suggested name | Role |
|---|--------------|----------------|------|
| 1 | Feature Studio | `FS_DallasLayout` | Room rectangles, walls, grid helpers |
| 2 | Feature Studio | `FS_DallasRacks` | Rack array + aisle containment boxes |
| 3 | Feature Studio | `FS_DallasMEP` | CRAH modules, UPS/battery placeholders |
| 4 | Feature Studio | `FS_DallasSite` | Parking stalls, fire loop bands, yard pads |
| 5 | Part Studio | `PS_SiteAndBuilding` | Floor plate, rooms, walls, site outlines |
| 6 | Part Studio | `PS_HallModule` | One 600-rack hall prototype (optional isolation) |
| 7 | Assembly | `ASM_Campus` | Instance hall modules H1–H8 + site (if split) |
| 8 | Variable Studio *or* Part Studio Variable table | `VAR_Dallas` | Counts & pitches from §2.1 |
| 9 | Drawing | `DRW_A1_Conceptual_Plan` | Top view packaging |
| 10 | Drawing | `DRW_Rack_Plan_Hall` | One hall at readable scale |
| 11 | Blob (optional) | `door-schedule.csv` | Schedule seed data |

### 4.1 Variables / configuration (Dallas-driven)

Create variables (Variable Studio if available on your plan, else Part Studio variables):

```text
SITE_SIDE = 2097.513 ft
BLDG_W = 1000 ft
BLDG_D = 720 ft
BLDG_SITE_X0 = 548.756 ft
BLDG_SITE_Y0 = 688.756 ft
HALL_W = 175 ft
HALL_D = 240 ft
RACKS_PER_HALL = 600
ROWS = 10
COLS = 60
RACK_D = 4 ft          // east-west depth of cabinet
RACK_W = 2 ft          // north-south width
CRAH_PER_SIDE = 13
PARK_SIDE = 312 ft
STALL_W = 9 ft
STALL_D = 18 ft
AISLE_DRIVE = 24 ft
WALL_EXT = 1 ft
WALL_INT = 0.5 ft
WALL_MAJOR = 1 ft
```

Optional **configuration** on `PS_HallModule`: `rackCount` / `showCRAH` / `showContainment` for design options without rewriting FeatureScript.

### 4.2 Which Feature Studio owns what

| Custom feature | Studio | Inputs from Dallas |
|----------------|--------|--------------------|
| `SiteSquare` | FS_DallasSite | SITE_SIDE |
| `ParkingModule` | FS_DallasSite | P origin, row Y bands, ADA group |
| `BuildingShell` | FS_DallasLayout | 1000×720, wall thickness |
| `PlanningGrid` | FS_DallasLayout | X/Y grid arrays |
| `RoomRectangles` | FS_DallasLayout | room table (south/tech bands) |
| `HallRackArray` | FS_DallasRacks | exact row X ranges + 60×2 ft pitch |
| `CRAHFanWall` | FS_DallasMEP | 13+13 modules |
| `UPSBatteryBlock` | FS_DallasMEP | 120×120 blocks, split at X 940 |

---

## 5. FeatureScript-first build plan (starter skeletons)

> **Important:** Skeletons below are **starters to adapt**. FeatureScript std APIs evolve; if a call fails, paste the error + code into ChatGPT and ask it to align with current [FsDoc](https://cad.onshape.com/FsDoc/). Prefer feet: `* foot` / `* inch`.

### 5.1 Units & Dallas parameter map (module header pattern)

```featurescript
FeatureScript 2295;
import(path : "onshape/std/common.fs", version : "2295.0");

// Starter — bump FeatureScript / std version to match your document's default.

export const DALLAS = {
    "siteSide" : 2097.513 * foot,
    "bldgW" : 1000 * foot,
    "bldgD" : 720 * foot,
    "hallW" : 175 * foot,
    "hallD" : 240 * foot,
    "rackD" : 4 * foot,   // E-W
    "rackW" : 2 * foot,   // N-S
    "rows" : 10,
    "cols" : 60,
    "crahPerSide" : 13,
    "crahW" : 8 * foot,
    "crahD" : 12 * foot
};
```

### 5.2 Rectangular floor / room layout feature (starter)

```featurescript
annotation { "Feature Type Name" : "Dallas Room Rectangles" }
export const dallasRoomRectangles = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Wall height" }
        isLength(definition.wallHeight, { "min" : 0 * inch });
        annotation { "Name" : "Extrude walls", "Default" : true }
        definition.extrudeWalls is boolean;
    }
    {
        // Building-local room table: [name, x0, y0, x1, y1] in feet
        // Starter subset — extend from basis §§11–13
        const rooms = [
            ["BREAK", 0, 0, 80, 50],
            ["RR_M", 80, 0, 130, 50],
            ["RR_W", 130, 0, 180, 50],
            ["LOCKERS", 180, 0, 240, 50],
            ["TRAINING", 240, 0, 350, 50],
            ["NOC", 350, 0, 410, 70],
            ["VESTIBULE", 455, 0, 545, 18],
            ["LOBBY", 410, 18, 590, 70],
            ["MANTRAP", 455, 70, 545, 110],
            ["RECEIVING", 650, 0, 760, 70],
            ["CER", 850, 0, 925, 55],
            ["MMR", 850, 55, 925, 110],
            ["MAIN_ELEC", 925, 0, 1000, 110]
        ];

        const sk = newSketchOnPlane(context, id + "sk", {
            "sketchPlane" : qCreatedBy(makeId("Top"), EntityType.FACE)
        });

        for (var i = 0; i < size(rooms); i += 1)
        {
            const r = rooms[i];
            skRectangle(sk, "rm" ~ i, {
                "firstCorner" : vector(r[1], r[2]) * foot,
                "secondCorner" : vector(r[3], r[4]) * foot
            });
        }
        skSolve(sk);

        if (definition.extrudeWalls)
        {
            // Starter: extrude regions as thin slabs / massing blocks.
            // For true walls, prefer centerline offsets + extrude — ask ChatGPT to refine.
            opExtrude(context, id + "ex", {
                "entities" : qSketchRegion(id + "sk"),
                "endBound" : BoundingType.BLIND,
                "depth" : definition.wallHeight
            });
        }
        println("Dallas rooms sketched: " ~ size(rooms));
    });
```

**Also sketch once (not necessarily FS):** building outside face 0–1000 × 0–720; offset inward 12 in for exterior wall; major partitions 12 in at hall boundaries / spines.

### 5.3 Server rack grid / hot-cold aisle pattern (Dallas-exact starter)

Basis row X mins: `45.5, 53.5, 63.5, 71.5, 81.5, 89.5, 99.5, 107.5, 117.5, 125.5` (each +4 ft depth). Cabinets: Y `60 + 2j` for `j = 0…59`.

```featurescript
annotation { "Feature Type Name" : "Dallas Hall Rack Array" }
export const dallasHallRackArray = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Hall origin X (building-local)" }
        isLength(definition.originX, {});
        annotation { "Name" : "Hall origin Y (building-local)" }
        isLength(definition.originY, {});
        annotation { "Name" : "Rack height" }
        isLength(definition.rackH, { "min" : 0 * inch });
        annotation { "Name" : "Hall index 1-8" }
        isInteger(definition.hallIndex, { "min" : 1, "max" : 8 });
    }
    {
        const rowX0 = [
            45.5, 53.5, 63.5, 71.5, 81.5, 89.5, 99.5, 107.5, 117.5, 125.5
        ]; // feet, hall-local
        const rackD = 4 * foot;
        const rackW = 2 * foot;
        const y0 = 60 * foot;

        // Seed rack at first position, then pattern
        const sk = newSketchOnPlane(context, id + "sk", {
            "sketchPlane" : qCreatedBy(makeId("Top"), EntityType.FACE)
        });
        const xSeed = definition.originX + rowX0[0] * foot;
        const ySeed = definition.originY + y0;
        skRectangle(sk, "rack", {
            "firstCorner" : vector(xSeed, ySeed),
            "secondCorner" : vector(xSeed + rackD, ySeed + rackW)
        });
        skSolve(sk);
        opExtrude(context, id + "ex", {
            "entities" : qSketchRegion(id + "sk"),
            "endBound" : BoundingType.BLIND,
            "depth" : definition.rackH
        });

        var transforms = [];
        var names = [];
        for (var r = 0; r < 10; r += 1)
        {
            for (var c = 0; c < 60; c += 1)
            {
                if (r == 0 && c == 0)
                    continue;
                const dx = (rowX0[r] - rowX0[0]) * foot;
                const dy = (c * 2) * foot;
                transforms = append(transforms,
                    transform(vector(dx, dy, 0 * meter)));
                // Tag style H3-R07-C42
                const rr = (r + 1 < 10) ? "0" ~ (r + 1) : "" ~ (r + 1);
                const cc = (c + 1 < 10) ? "0" ~ (c + 1) : "" ~ (c + 1);
                names = append(names, "H" ~ definition.hallIndex ~ "-R" ~ rr ~ "-C" ~ cc);
            }
        }
        opPattern(context, id + "pat", {
            "entities" : qCreatedBy(id + "ex", EntityType.BODY),
            "transforms" : transforms,
            "instanceNames" : names
        });
        println("Hall H" ~ definition.hallIndex ~ " racks patterned: 600");
        debug(context, qCreatedBy(id + "pat", EntityType.BODY));
    });
```

**Hall origins (building-local SW of each hall rectangle):**

| Hall | originX | originY |
|------|---------|---------|
| H1 | 120 ft | 110 ft |
| H2 | 315 ft | 110 ft |
| H3 | 510 ft | 110 ft |
| H4 | 705 ft | 110 ft |
| H5 | 120 ft | 370 ft |
| H6 | 315 ft | 370 ft |
| H7 | 510 ft | 370 ft |
| H8 | 705 ft | 370 ft |

**Containment:** separate thin boxes or sketches for hot-aisle X bands `49.5–53.5`, `67.5–71.5`, `85.5–89.5`, `103.5–107.5`, `121.5–125.5` (hall-local).

### 5.4 CRAH / UPS / battery placeholders (starter)

```featurescript
annotation { "Feature Type Name" : "Dallas CRAH Modules" }
export const dallasCRAH = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Hall origin X" }
        isLength(definition.originX, {});
        annotation { "Name" : "Hall origin Y" }
        isLength(definition.originY, {});
        annotation { "Name" : "Module height" }
        isLength(definition.height, { "min" : 0 * inch });
    }
    {
        // West X 10–18, East X 157–165; Y: 12+17k .. 24+17k for k=0..12
        const sides = [10, 157]; // feet X starts
        const sk = newSketchOnPlane(context, id + "sk", {
            "sketchPlane" : qCreatedBy(makeId("Top"), EntityType.FACE)
        });
        var n = 0;
        for (var s = 0; s < size(sides); s += 1)
        {
            for (var k = 0; k < 13; k += 1)
            {
                const x0 = definition.originX + sides[s] * foot;
                const y0 = definition.originY + (12 + 17 * k) * foot;
                skRectangle(sk, "c" ~ n, {
                    "firstCorner" : vector(x0, y0),
                    "secondCorner" : vector(x0 + 8 * foot, y0 + 12 * foot)
                });
                n += 1;
            }
        }
        skSolve(sk);
        opExtrude(context, id + "ex", {
            "entities" : qSketchRegion(id + "sk"),
            "endBound" : BoundingType.BLIND,
            "depth" : definition.height
        });
        println("CRAH modules: " ~ n); // expect 26
    });
```

**UPS / battery (east band):** for each 120×120 block (basis §12.2), sketch two regions X `880–940` (UPS/switchgear) and `940–1000` (battery). Six conceptual 2.5 MW modules per hall block = optional 6 boxes inside UPS region — **counts are placeholders**, not vendor selections.

### 5.5 Parking stall pattern (starter — rows 1–5 exact; row 6 ADA detailed)

```featurescript
annotation { "Feature Type Name" : "Dallas Parking Stalls" }
export const dallasParking = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Parking origin site X" }
        isLength(definition.originX, {}); // 892.756 ft
        annotation { "Name" : "Parking origin site Y" }
        isLength(definition.originY, {}); // 276.756 ft
        annotation { "Name" : "Slab thickness" }
        isLength(definition.thickness, { "min" : 0 * inch });
    }
    {
        // Row local-Y bottoms for stall rows 1..6 (18 ft deep): 60,102,120,162,180,222
        const rowY = [60, 102, 120, 162, 180, 222];
        const sk = newSketchOnPlane(context, id + "sk", {
            "sketchPlane" : qCreatedBy(makeId("Top"), EntityType.FACE)
        });
        var n = 0;
        // Rows 1-5: 30 stalls, local X 21–291
        for (var row = 0; row < 5; row += 1)
        {
            for (var i = 0; i < 30; i += 1)
            {
                const x0 = definition.originX + (21 + 9 * i) * foot;
                const y0 = definition.originY + rowY[row] * foot;
                skRectangle(sk, "s" ~ n, {
                    "firstCorner" : vector(x0, y0),
                    "secondCorner" : vector(x0 + 9 * foot, y0 + 18 * foot)
                });
                n += 1;
            }
        }
        // Row 6 standard left 12 + right 12 — ADA group 123–189 drawn separately
        for (var i = 0; i < 12; i += 1)
        {
            const x0 = definition.originX + (15 + 9 * i) * foot;
            const y0 = definition.originY + 222 * foot;
            skRectangle(sk, "s" ~ n, {
                "firstCorner" : vector(x0, y0),
                "secondCorner" : vector(x0 + 9 * foot, y0 + 18 * foot)
            });
            n += 1;
        }
        for (var i = 0; i < 12; i += 1)
        {
            const x0 = definition.originX + (189 + 9 * i) * foot;
            const y0 = definition.originY + 222 * foot;
            skRectangle(sk, "s" ~ n, {
                "firstCorner" : vector(x0, y0),
                "secondCorner" : vector(x0 + 9 * foot, y0 + 18 * foot)
            });
            n += 1;
        }
        // ADA / van / aisles — encode basis §7.2 widths explicitly via ChatGPT refinement
        skSolve(sk);
        opExtrude(context, id + "ex", {
            "entities" : qSketchRegion(id + "sk"),
            "endBound" : BoundingType.BLIND,
            "depth" : definition.thickness
        });
        println("Standard stalls sketched (expect 174 before ADA solids): " ~ n);
    });
```

Ask ChatGPT to add the **exact** ADA rectangles (11 / 5 / 8 / 8 / 5 / 8 / 8 / 5 / 8) so total stalls = **180**.

### 5.6 Debug with `println` / `debug`

| Tool | Use |
|------|-----|
| `println("x: " ~ x)` | FeatureScript notices flyout |
| `debug(context, query)` | Highlights entities while feature dialog open |
| `reportFeatureError(context, id, "msg")` | User-visible failure |
| Rollback bar | Bisect which feature broke regen |

Remove noisy `debug` calls before sharing Versions with stakeholders.

### 5.7 Versioning features with ChatGPT (iteration pattern)

1. **Milestone Version** after: site square → building shell → one hall racks → all 8 halls → parking → yards.  
2. In ChatGPT, keep a short “project card” pinned in the conversation (paste constants from §2.1).  
3. Prefer **diff-style asks**: “Change only the CRAH Y pitch; keep rack array untouched.”  
4. If a feature becomes unmaintainable, **duplicate Feature Studio tab**, rename `FS_DallasRacks_v2`, point Part Studio at the new feature type.

---

## 6. ChatGPT Chrome prompt templates

Paste these while Onshape is open. Replace bracketed fields.

### 6.1 Generate rack FeatureScript from Dallas dims

```text
You are helping me write Onshape FeatureScript for a Dallas data-center Part Studio.
Constraints from CAD basis:
- Hall size 175 ft (X) × 240 ft (Y), hall-local origin at SW.
- 10 rack rows; each cabinet 4 ft deep (X) × 2 ft wide (Y).
- Row X starts (ft): 45.5, 53.5, 63.5, 71.5, 81.5, 89.5, 99.5, 107.5, 117.5, 125.5
- Cabinets: j=0..59 at Y = 60+2j .. 62+2j
- Do NOT equal-space rows; use exact X ranges.
- Pattern with opPattern; instance names Hh-Rrr-Ccc.
Generate a complete defineFeature starter. Use feet. Comment every magic number.
```

### 6.2 Fix FeatureScript error

```text
Onshape FeatureScript regen failed. Fix with minimal diff.
Feature name: [Dallas Hall Rack Array]
Error text (verbatim):
"""
[PASTE ERROR]
"""
Full feature code:
"""
[PASTE CODE]
"""
Explain root cause in one sentence, then give corrected FeatureScript only.
```

### 6.3 Add door openings to wall sketch

```text
I have an Onshape sketch of the building outside-face 1000×720 ft and interior partitions
from the Dallas basis. Add door openings as sketch gaps or separate opening rectangles:
- Two 8 ft equipment doors from each hall H1–H8 to adjacent 20 ft spine/cross-corridor
  (place preliminarily on hall edges mid-bay; mark as PRELIMINARY).
- Vestibule: two 6 ft double-door pairs centered on building X=500
  (exterior/vestibule and vestibule/lobby).
- Mantrap: controlled 4 ft doors.
- Loading: two 14 ft doors on south wall at building-local X 680–694 and 710–724.
Return FeatureScript or explicit skRectangle coordinates I can paste. Units: feet.
```

### 6.4 Room layout feature from south-band list

```text
Generate FeatureScript that sketches these building-local rectangles (feet) as regions
and extrudes [10 ft] massing. Include room name in println summary:
[PASTE TABLE FROM BASIS §11]
Also sketch spines X 295–315, 490–510, 685–705 (Y 110–610) and cross-corridor
X 120–880, Y 350–370.
```

### 6.5 Parking + ADA

```text
Write FeatureScript for Dallas parking:
- Origin site (892.756, 276.756) ft
- Rows/aisles per basis §7.2
- Exactly 174 standard + 6 accessible (include van 11 ft and shared 5 ft aisles)
- println total stall rectangles
Keep as extrudeable sketch regions.
```

### 6.6 CRAH + airflow note text (Drawing helpers)

```text
From Dallas basis: 26 CRAH modules per hall (13 west X10–18, 13 east X157–165,
Y = 12+17k to 24+17k, k=0..12, each 8×12 ft). Give:
1) FeatureScript massing feature
2) Short Drawing note text for cyan supply to cold aisles and red return from
   contained hot aisles — conceptual only, not duct sizes.
```

### 6.7 Door schedule table data

```text
Create a CSV-ready door schedule table (Mark, Width, Height, Type, FireRating, From, To, Notes)
for the Dallas conceptual plan using ONLY stated door sizes from the basis
(8 ft hall equipment, 6 ft vestibule pairs, 4 ft mantrap, 14 ft loading).
Mark unknowns as TBD-RATING. Do not invent fire ratings.
I will paste this into an Onshape Drawing general table.
```

### 6.8 Drawing click-path coach

```text
I am on cad.onshape.com with Part Studio [PS_SiteAndBuilding] complete.
Coach me click-by-click to: create Drawing tab, insert TOP view, set scale for a
1000×720 ft building on [ANSI E / A0 / my sheet], show sketch appearances for grids,
add overall dimensions for building 1000 ft × 720 ft and site 2097.513 ft square,
add a general table for door schedule. Wait after each step for my confirmation.
```

### 6.9 Configuration / variables

```text
Suggest an Onshape Variable Studio list and Part Studio configuration inputs that
encode: SITE_SIDE, BLDG_W/D, RACKS_PER_HALL=600, ROWS=10, COLS=60, CRAH_PER_SIDE=13,
PARK_SIDE=312. Map each to the Dallas basis section number.
```

---

## 7. Drawing sheet procedure (after geometry exists)

ChatGPT helps with **click-path and annotation text**; you still perform UI actions.

### 7.1 Prepare views in 3D

1. In Part Studio or Assembly, orient **Top** (plan).  
2. Create **Named views**: `SITE_PLAN`, `BUILDING_PLAN`, `HALL_H1_RACKS`.  
3. Hide clutter (yard generators when doing admin plan, etc.) via display states if you use them.

### 7.2 Create Drawing

1. Insert new **Drawing** tab → pick template closest to A1.0 / ARCH E / ANSI E (firm standard).  
2. **Insert → View** → select Part Studio/Assembly → **Top** or named view.  
3. Set scale so the 2,097.513 ft site or 1,000×720 building fits with margin (site sheet vs building sheet — **split sheets** per basis §17).  
4. Enable **sketch appearances** / cosmetic outlines as needed for grids and parking lines.

### 7.3 Dimensions & annotation

Dimension numerically from basis (do not scale off PDF):

- Site sides: **2,097.513 ft**; label **101.000 acres**  
- Building: **1,000 ft** E–W × **720 ft** N–S  
- Hall: **175 × 240 ft**  
- Rack pitch: **2 ft** along row; row depths **4 ft**  
- Parking module: **9 × 18 ft** stalls; **24 ft** aisles  
- Fire loop width: **26 ft**

Add notes:

- “Conceptual basis v0.1 — not for construction”  
- Hot aisle containment / cold aisle supply (colors if template allows)  
- A/B dual-cord intent (symbolic dashed lines — expect limited fidelity)

### 7.4 Tables (door / equipment)

1. Insert **General table**.  
2. Paste CSV from prompt §6.7 or type rows.  
3. Separate **equipment count** table: 4,800 racks; 600/hall; 26 CRAH/hall; 42 gens; 32 cells; 180 parking.

Onshape tables are **not** Revit door instances — marks will not auto-update when you move a sketch door.

### 7.5 Title block

Fill: Project `Dallas 101-Acre Data Center — Conceptual CAD Basis v0.1`; Location `Dallas, TX (test assumptions)`; Sheet `A1.0` or `SP-101` / `A-101` per your sheet index; Scale as set; Date; Rev `Conceptual Issue`. North arrow + graphic scale from template or inserted DXF.

### 7.6 Export

- **PDF** for review  
- **DWG/DXF** if handing off to AutoCAD for symbology  
- Optional: store DWG blob + **ARES Kudo** for denser 2D work inside the Onshape document

---

## 8. End-to-end runbook (zero → export)

### Phase A — Account & scaffold

1. [ ] Create Onshape document `Dallas-101ac-DC-CAD-Basis-v0.1`  
2. [ ] Install ChatGPT Chrome extension; verify it works on `cad.onshape.com`  
3. [ ] Create Feature Studios + Part Studio + Variable list (§4)  
4. [ ] Version: `v0-scaffold`

### Phase B — Site & building shell

5. [ ] Sketch property square 2,097.513 ft; constrain fully  
6. [ ] Place building outside face at site (548.756, 688.756), size 1,000×720  
7. [ ] 12 in exterior wall inward; planning grid X/Y from basis §8  
8. [ ] Fire loop inner/outer rectangles; parking boundary 312×312  
9. [ ] Version: `v1-site-shell`

### Phase C — Rooms & halls

10. [ ] South-band rooms (§11) via `Dallas Room Rectangles` or sketches  
11. [ ] West / east / north technical bands (§§12–13)  
12. [ ] Eight hall rectangles H1–H8 + spines + cross-corridor  
13. [ ] Preliminary door openings (§6.3 prompt)  
14. [ ] Version: `v2-rooms-halls`

### Phase D — FeatureScript equipment

15. [ ] Commit `Dallas Hall Rack Array`; apply to H1; verify **600** bodies  
16. [ ] Instance / re-run for H2–H8 with correct origins (total **4,800**)  
17. [ ] Hot-aisle containment sketches/boxes  
18. [ ] CRAH 26/hall; UPS/battery splits; outdoor yard placeholders (42 gen / 32 cells)  
19. [ ] Parking stalls → **180** including ADA group  
20. [ ] Version: `v3-equipment`

### Phase E — Drawing & export

21. [ ] Named views; Drawing tab(s) site + building + rack  
22. [ ] Dimensions + notes + door/equipment tables  
23. [ ] Title block; north; graphic scale; disclaimer  
24. [ ] Export PDF (+ DWG if needed)  
25. [ ] Version: `v4-drawing-export`

### Acceptance criteria vs Dallas basis MD

| Check | Pass condition |
|-------|----------------|
| Site square | Side 2,097.513 ft; closed polyline; area note 101 acres |
| Building | Outside face 1,000×720; SW at site (548.756, 688.756) |
| Grid | All listed X/Y grid lines present |
| Halls | Eight 175×240 rectangles at listed coords |
| Racks | 10×60 per hall; exact row X; Y from 60 with 2 ft pitch; campus 4,800 |
| Aisles | Hot 4 ft / cold 6 ft bands match §10.2 |
| CRAH | 26 modules/hall at specified footprints |
| Parking | 180 stalls; ADA geometry per §7.2 |
| Roads / loop | Entry 30 ft; service 40 ft; fire loop 26 ft clear concept |
| Yards | Substation / gen / heat-rejection rectangles non-overlapping |
| Drawing | Top view(s), key dims, schedules table, conceptual disclaimer |
| Honesty | No claim of fire ratings / sealed engineering |

---

## 9. Limitations & failure modes

| Failure mode | Why | What to do |
|--------------|-----|------------|
| Extension can’t click reliably | Not a native Onshape RPA product; DOM/canvas UI changes | Use ChatGPT for code + coaching; you click |
| FeatureScript ≠ A1.0 sheet | Drawings are a separate app element | Budget manual Drawing time; or hybrid DXF |
| Fire-rated wall symbology | No BIM wall types / HR parameters | Hatch + notes manually, or AutoCAD/Revit |
| Schedule linkage | Tables don’t track sketch doors | Manual/CSV update when doors move |
| 4,800 solid racks slow regen | Heavy Part Studio | One hall Part Studio + Assembly pattern; or sketch-only footprints for campus sheet |
| Equal-spacing mistakes | Easy to “simplify” row pitch in prompts | Refuse equal spacing; paste exact X list every time |
| API secrets in chat | Leakage | Never paste keys; API is optional/separate |
| Drawing single-editor lock | One editor at a time | Coordinate who owns the Drawing tab |
| When to fall back to DXF/AutoCAD | Need AIA layers, Xrefs, keynote DB, permit graphics | Export footprints DWG/DXF; finish sheet in AEC tool / ARES |

---

## 10. Assumptions & gaps in the Dallas basis

The basis is rich on coordinates and counts. Call out what you must **assume** or leave **TBD** in Onshape:

| Topic | In basis? | Playbook assumption |
|-------|-----------|---------------------|
| Exact parcel / survey | No — equal-area square test | Model the square; replace when survey exists |
| Zoning / setbacks | 100 ft reserve is **planning only**, not Dallas code claim | Label as provisional |
| Road on south line | Explicit test assumption | Keep; note on sheet |
| Wall assemblies / fire ratings | Thickness planning only; ratings TBD | Do not invent HR ratings in schedules |
| Door ratings, hardware, exit counts | Preliminary locations only | Mark TBD-RATING; architect to finalize |
| Structural column grid vs planning grid | Planning/grid lines given | Not a engineered structural grid |
| CRAH / UPS / gen / chiller selections | Conceptual counts & footprints | Massing boxes only |
| Duct / pipe sizes | Airflow arrows conceptual | Drawing notes, not sized MEP |
| Floor-to-floor / building height | One-story stated; clear heights not fully specified | Use configurable `wallHeight` / `rackH` (e.g. 10–12 ft massing) |
| Finished floor elevation / grading | Not specified | Flat Z=0 plane |
| Oncor service size | ~150 MVA placeholder | Note only — not drawn as confirmed |
| Landscape / trees / security fence details | Minimal | Omit or schematic only |
| Sheet size / company title block | Not specified | Use your template; label conceptual |
| Layer / AIA color standards | Not specified | Optional Drawing properties; limited vs AutoCAD |

---

## Quick reference links

| Resource | URL / path |
|----------|------------|
| Dallas CAD basis | `/Users/ankurkulkarni/Documents/Codex/2026-08-12/can/outputs/dallas-data-center-cad-basis.md` |
| FeatureScript docs | https://cad.onshape.com/FsDoc/ |
| Onshape drawings help | https://cad.onshape.com/help/Content/Drawing/ |
| Capability research | [`onshape-featurescript-cad-drawings.md`](./onshape-featurescript-cad-drawings.md) |
| This playbook | `docs/onshape-chatgpt-chrome-featurescript-playbook.md` |

---

*Playbook prepared for Onshape-code-first conceptual delivery of the Dallas 101-acre data-center CAD basis, with ChatGPT Chrome as a browser-side co-pilot — not as a native Onshape API controller.*
