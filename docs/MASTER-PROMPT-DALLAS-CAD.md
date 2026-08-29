# MASTER PROMPT — Dallas Data Center CAD Set

**This is a complete, self-contained work order. Paste the entire document into ChatGPT (Computer Use enabled) or hand it to any coding agent with access to AutoCAD. Do not ask the user for information contained here.**

---

## PART 0 — HOW TO USE THIS DOCUMENT

| If you are… | Do this |
|---|---|
| **ChatGPT with Computer Use + local AutoCAD** | Follow Part 5 (AutoLISP path). This is the primary route. |
| **A coding agent with shell access** | Follow Part 6 (Python/ezdxf path), then hand the DXF to the human for Part 9. |
| **A human** | Read Parts 1–3, then delegate Parts 5–9. |

Work top to bottom. Verify every acceptance check before advancing. Never skip Part 2.

---

## PART 1 — MISSION

Produce a **client-presentable conceptual CAD set** for a 101-acre, 96 MW data center campus in Dallas, Texas.

**Success = nine plotted PDF sheets that a non-technical client immediately reads as professional architectural drawings.**

The benchmark is a detailed A1.0-style architectural sheet containing: poché walls, labeled rooms, furniture and fixtures, door swings, a rack plan with hot/cold aisle annotation, striped parking with landscaping, a legend, keynotes, a door schedule, dimensions, grid bubbles, a north arrow, a graphic scale, a revision block, and a fully filled title block.

### 1.1 Two prior attempts and why they failed

| Attempt | Result | Root cause |
|---|---|---|
| **Onshape + FeatureScript** | Unlabeled boxes at 1:4000 on a mostly empty sheet | FeatureScript generates 3D geometry. It cannot produce architectural sheet annotation. Wrong tool. |
| **AutoCAD Web, first pass** | Correct structure — legend, keynotes, schedule, title block, rooms, parking, halls all present — but it looked flat and unfinished. Client said **"it's just boxes."** | Five specific craft omissions, listed in Part 2. Structure was right; drafting craft was absent. |

**The second attempt was close.** Do not rebuild its structure from scratch — replicate that structure and add the craft.

---

## PART 2 — THE ANTI-"BOXES" CONTRACT (NON-NEGOTIABLE)

These seven rules are the difference between a flat diagram and a real drawing. Any deliverable violating them is rejected.

| # | Requirement | Meaning | Impact |
|---|---|---|---|
| **1** | **Walls have real thickness with solid poché fill** | Never draw a room as a single-line rectangle. Every wall is a filled band of actual thickness (12" exterior/rated, 6" partitions). | **~60% of the visual gap** |
| **2** | **Lineweight hierarchy** | Heavy exterior (0.70mm), medium rated (0.50), lighter partitions (0.35), light equipment (0.13–0.20), hairline grid and dims (0.09). | High |
| **3** | **Furniture and fixtures** | Desks in offices, table in conference, toilets and lavatories in restrooms, seating in lobby, tables in break room, consoles in NOC. | High |
| **4** | **Door swings** | Every door gets a leaf line **and** a 90° arc. Nothing signals "architecture" faster. | High |
| **5** | **Hatches and fills** | Solid-filled server cabinets, asphalt hatch on paving, trees and landscape islands, sidewalks. | High |
| **6** | **No overlapping text, ever** | If labels collide at a scale, move them to an enlargement sheet or use leaders. A smeared label zone is an automatic failure. | Critical |
| **7** | **Real plotted scales** | Never write "MODELSPACE IN FEET." Use true scales such as 1" = 40'-0". | Critical |

### 2.1 Detail inventory — the acceptance checklist

The sheet set is complete only when all of the following exist.

**Sheet framework**

- [ ] Border with zone grid coordinates
- [ ] Title block, every field filled, real sheet number
- [ ] Revision block
- [ ] North arrow and graphic scale on every plan sheet
- [ ] Grid bubbles with bay dimensions
- [ ] Overall building dimension strings

**Rooms — drawn *and* labeled**

- [ ] Vestibule, lobby/reception, security mantrap, security operations, NOC
- [ ] Private offices, conference, open office, IT closet, storage
- [ ] Break room, men's and women's restrooms, lockers, training
- [ ] Receiving/staging, secure storage, spares lab, janitor, waste, service passage
- [ ] Carrier entrance, meet-me/network, main electrical service

**Data hall**

- [ ] Hall perimeter with room number
- [ ] Every rack row drawn, cabinets solid-filled
- [ ] COLD AISLE and HOT AISLE labels
- [ ] Cyan supply arrows and red return arrows
- [ ] CRAH units individually tagged
- [ ] Containment boundaries

**Power and support**

- [ ] UPS rooms, battery rooms, switchgear, telecom, staging/loading with door callouts

**Site and parking**

- [ ] Parking boundary, every stall striped, ADA stalls with ISA symbols
- [ ] Drive aisle arrows, one-way entrance text
- [ ] Landscape trees and islands, sidewalks, drop-off

**Annotation systems**

- [ ] Legend covering every symbol used
- [ ] Keynotes
- [ ] Door schedule table
- [ ] Dimensions on grids, rooms, aisles, rack pitch, parking, roads
- [ ] Egress paths
- [ ] Disclaimer

---

## PART 3 — TOOL REALITY

### 3.1 Why AutoCAD and not Onshape

Onshape is cloud mechanical CAD. FeatureScript builds parametric 3D features — it cannot generate architectural sheet annotation, AIA layers, fire-rated wall types, or linked schedules. It was the wrong tool and is abandoned for this work.

### 3.2 AutoCAD Web vs local

| | Web | Local (full) | LT |
|---|---|---|---|
| AutoLISP | No | **Yes** | **No** |
| `.scr` scripts | No | Yes | Yes |
| VBA / .NET / ActiveX | No | Windows only | Windows only |
| `accoreconsole` headless | No | Windows only | No |
| Hatching, dynamic blocks | Limited | Full | Full |
| Performance with 4,800 objects | Poor | Good | Good |

**Use local full AutoCAD.** Confirm it is not LT — check that `APPLOAD` exists. If it is LT, AutoLISP is unavailable and you must use the Python/ezdxf path in Part 6.

### 3.3 macOS constraints

- AutoLISP **works**. Load with `APPLOAD`.
- **`vl-load-com` and all `vla-*` ActiveX functions do NOT work.** Use `entmake` and `command` only.
- No `accoreconsole`, so all execution is in the GUI.
- On Windows, `accoreconsole.exe /i dallas.dwg /s build.scr` would allow fully headless batch execution including plotting.

### 3.4 Division of labor

| Task | Owner |
|---|---|
| Bulk geometry — 4,800 racks, 180 stalls, 54 rooms | **Generated by code.** Never by clicking. |
| Loading scripts, layouts, viewport scales, plotting | Computer Use or the human |
| Diagnosing what AutoCAD is showing | Screenshots |
| Writing and fixing scripts | The agent |

---

## PART 4 — LAYER STANDARD

Create these before drawing anything. Colors are AutoCAD Color Index; lineweights in mm.

| Layer | Color | LW | Linetype | Contents |
|---|---|---|---|---|
| `00-SITE-CTRL` | 8 | 0.13 | CONTINUOUS | Property boundary |
| `01-CIVIL-RSRV` | 30 | 0.13 | DASHED | Reserve, stormwater, yards |
| `02-ROADS` | 8 | 0.18 | CONTINUOUS | Drives, fire loop, aprons |
| `02-PARK-STALL` | 253 | 0.13 | CONTINUOUS | Stall striping |
| `02-PARK-ADA` | 150 | 0.20 | CONTINUOUS | Accessible stalls, ISA |
| `02-PAVE-HATCH` | 251 | 0.09 | CONTINUOUS | Asphalt fill |
| `02-LANDSCAPE` | 74 | 0.13 | CONTINUOUS | Trees, islands |
| `03-WALL-EXT` | 7 | **0.70** | CONTINUOUS | 12" exterior + poché |
| `03-WALL-FIRE` | 1 | **0.50** | CONTINUOUS | 12" rated barrier + poché |
| `03-WALL-INT` | 7 | **0.35** | CONTINUOUS | 6" partition + poché |
| `04-GRID` | 4 | 0.09 | CENTER | Grid lines, bubbles |
| `05-HALL` | 8 | 0.25 | CONTINUOUS | Hall zones, containment |
| `06-ROOM-TAG` | 7 | 0.13 | CONTINUOUS | Room names, numbers |
| `06-FURN` | 9 | 0.13 | CONTINUOUS | Desks, tables, seating |
| `06-PLUMB` | 9 | 0.13 | CONTINUOUS | Toilets, lavatories |
| `07-DOOR` | 2 | 0.20 | CONTINUOUS | Leaves, swings, marks |
| `08-EQPM-RACK` | 250 | 0.13 | CONTINUOUS | Cabinets (solid filled) |
| `08-EQPM-CRAH` | 3 | 0.20 | CONTINUOUS | Cooling modules |
| `08-EQPM-ELEC` | 6 | 0.20 | CONTINUOUS | UPS, battery, switchgear |
| `09-HVAC-SUP` | 4 | 0.20 | CONTINUOUS | Supply arrows, cold aisle |
| `09-HVAC-RET` | 1 | 0.20 | CONTINUOUS | Return arrows, hot aisle |
| `10-ELEC-A` | 2 | 0.20 | DASHED | A-path distribution |
| `10-ELEC-B` | 6 | 0.20 | DASHED | B-path distribution |
| `11-LIFE-EGRESS` | 3 | 0.25 | DASHED | Exit routes |
| `12-DIM` | 7 | 0.09 | CONTINUOUS | Dimensions |
| `13-ANNO-LEGEND` | 7 | 0.13 | CONTINUOUS | Legend, keynotes, schedules |
| `14-TBLK` | 7 | 0.25 | CONTINUOUS | Title block, borders |

```lisp
(defun c:DALLAYERS ( / lst i)
  (setq lst '(
    ("00-SITE-CTRL" 8 "CONTINUOUS" 0.13) ("01-CIVIL-RSRV" 30 "DASHED" 0.13)
    ("02-ROADS" 8 "CONTINUOUS" 0.18) ("02-PARK-STALL" 253 "CONTINUOUS" 0.13)
    ("02-PARK-ADA" 150 "CONTINUOUS" 0.20) ("02-PAVE-HATCH" 251 "CONTINUOUS" 0.09)
    ("02-LANDSCAPE" 74 "CONTINUOUS" 0.13) ("03-WALL-EXT" 7 "CONTINUOUS" 0.70)
    ("03-WALL-FIRE" 1 "CONTINUOUS" 0.50) ("03-WALL-INT" 7 "CONTINUOUS" 0.35)
    ("04-GRID" 4 "CENTER" 0.09) ("05-HALL" 8 "CONTINUOUS" 0.25)
    ("06-ROOM-TAG" 7 "CONTINUOUS" 0.13) ("06-FURN" 9 "CONTINUOUS" 0.13)
    ("06-PLUMB" 9 "CONTINUOUS" 0.13) ("07-DOOR" 2 "CONTINUOUS" 0.20)
    ("08-EQPM-RACK" 250 "CONTINUOUS" 0.13) ("08-EQPM-CRAH" 3 "CONTINUOUS" 0.20)
    ("08-EQPM-ELEC" 6 "CONTINUOUS" 0.20) ("09-HVAC-SUP" 4 "CONTINUOUS" 0.20)
    ("09-HVAC-RET" 1 "CONTINUOUS" 0.20) ("10-ELEC-A" 2 "DASHED" 0.20)
    ("10-ELEC-B" 6 "DASHED" 0.20) ("11-LIFE-EGRESS" 3 "DASHED" 0.25)
    ("12-DIM" 7 "CONTINUOUS" 0.09) ("13-ANNO-LEGEND" 7 "CONTINUOUS" 0.13)
    ("14-TBLK" 7 "CONTINUOUS" 0.25)))
  (command "_.-LINETYPE" "_L" "DASHED" "" "")
  (command "_.-LINETYPE" "_L" "CENTER" "" "")
  (foreach i lst
    (command "_.-LAYER" "_M" (car i) "_C" (itoa (cadr i)) ""
             "_L" (caddr i) "" "_LW" (rtos (cadddr i) 2 2) "" ""))
  (setvar "FILLMODE" 1) (setvar "LWDISPLAY" 1)
  (princ "\nDallas layers created.") (princ))
```

---

## PART 5 — PROJECT DATA: ALL COORDINATES

All values in **decimal feet**. Site origin (0,0) is the southwest property corner. X is east, Y is north. **Never estimate, round, or invent a coordinate.**

### 5.1 Coordinate systems

| System | Definition |
|---|---|
| Site | Origin at SW property corner |
| Building-local | Building (0,0) = site **(548.756, 688.756)** |
| Parking-local | Parking P(0,0) = site **(892.756, 276.756)** |

```lisp
(setq *BX* 548.756 *BY* 688.756 *PX* 892.756 *PY* 276.756)
(defun b2s (x y) (list (+ *BX* x) (+ *BY* y)))
(defun p2s (x y) (list (+ *PX* x) (+ *PY* y)))
```

### 5.2 Site

| Item | Value |
|---|---|
| Property square | (0,0) to (2097.513, 2097.513) — 101.000 acres |
| Planning reserve | 100 ft inside all boundaries, broken at south drive entrances |
| Substation yard | X 1650–1990, Y 830–1230 (340 × 400) |
| Generator yard | X 600–1498, Y 1510–1810 (898 × 300, 42 positions @ 3 MW) |
| Heat rejection yard | X 600–1498, Y 1810–1990 (898 × 180, 32 cells @ 1000 ton) |
| Stormwater west | X 100–450, Y 700–2000 |
| Stormwater southwest | X 100–300, Y 100–575 |

### 5.3 Roads and fire loop

| Item | Value |
|---|---|
| Fire loop inner edge | X 533.756–1563.756, Y 673.756–1423.756 |
| Fire loop outer edge | X 507.756–1589.756, Y 647.756–1449.756 |
| Public entry drive | X 1033.756–1063.756, Y 0–276.756 (30 ft) |
| Pedestrian walk | X 1042.756–1054.756, Y 588.756–688.756 (12 ft) |
| Service drive | X 1850–1890, Y 0–790 (40 ft) |
| EW connector | X 1589.756–1890, Y 600–640 |
| NS technical spine | X 1590–1630, Y 600–1510 |
| Substation connectors | X 1630–1650 at Y 900–940 and Y 1100–1140 |
| North yard connector | X 1498–1630, Y 1510–1550 |
| Loading apron | X 1198.756–1398.756, Y 600–688.756 |

The fire loop is a **26 ft wide ring**; centerline sits 28 ft from the building face. Keep public and service circulation fully separate.

### 5.4 Parking — exactly 180 spaces (parking-local)

Boundary 312 × 312 from P(0,0) to P(312,312).

| Zone | Local Y |
|---|---|
| South arrival / landscape | 0–60 |
| Stall row 1 | 60–78 |
| Drive aisle 1 | 78–102 |
| Stall row 2 | 102–120 |
| Stall row 3 | 120–138 |
| Drive aisle 2 | 138–162 |
| Stall row 4 | 162–180 |
| Stall row 5 | 180–198 |
| Drive aisle 3 | 198–222 |
| Stall row 6 | 222–240 |
| North pedestrian / drop-off | 240–312 |

- **Rows 1–5:** strip local X 21–291 divided into 30 bays of 9 ft → **150 standard**
- **Row 6:** twelve 9 ft bays at X 15–123, accessible group X 123–189, twelve 9 ft bays at X 189–297 → **24 standard + 6 accessible**

**Accessible group (66 ft, west to east):**

| Element | Local X | Width |
|---|---|---|
| Van space | 123–134 | 11 |
| Access aisle | 134–139 | 5 |
| Accessible car | 139–147 | 8 |
| Accessible car | 147–155 | 8 |
| Shared access aisle | 155–160 | 5 |
| Accessible car | 160–168 | 8 |
| Accessible car | 168–176 | 8 |
| Shared access aisle | 176–181 | 5 |
| Accessible car | 181–189 | 8 |

Drop-off at local Y 252–276 centered on the pedestrian axis. **150 + 24 + 6 = 180.**

### 5.5 Building shell and grid (building-local)

Outside face (0,0) to (1000, 720). Exterior wall 12 in drawn inward. Partitions 6 in; hall/fire barriers 12 in.

- **Grid X:** 0, 120, 295, 315, 490, 510, 685, 705, 880, 1000 → bubbles **1–10**
- **Grid Y:** 0, 110, 350, 370, 610, 720 → bubbles **A–F**

### 5.6 Data halls (building-local)

| Hall | X | Y | Load | Racks |
|---|---|---|---|---|
| H1 | 120–295 | 110–350 | 12 MW | 600 |
| H2 | 315–490 | 110–350 | 12 MW | 600 |
| H3 | 510–685 | 110–350 | 12 MW | 600 |
| H4 | 705–880 | 110–350 | 12 MW | 600 |
| H5 | 120–295 | 370–610 | 12 MW | 600 |
| H6 | 315–490 | 370–610 | 12 MW | 600 |
| H7 | 510–685 | 370–610 | 12 MW | 600 |
| H8 | 705–880 | 370–610 | 12 MW | 600 |

Three north-south spines at X 295–315, 490–510, 685–705 (Y 110–610). East-west cross corridor X 120–880, Y 350–370.

Area check: 336,000 ft² halls + 44,000 ft² corridors = 380,000 ft² = 760 × 500.

### 5.7 Rack module (hall-local, origin at each hall SW corner)

Cabinet footprint **4 ft east-west × 2 ft north-south**. Rows span Y 60–180.

| Row | X range | Orientation |
|---|---|---|
| R1 | 45.5–49.5 | front west |
| R2 | 53.5–57.5 | front east |
| R3 | 63.5–67.5 | front west |
| R4 | 71.5–75.5 | front east |
| R5 | 81.5–85.5 | front west |
| R6 | 89.5–93.5 | front east |
| R7 | 99.5–103.5 | front west |
| R8 | 107.5–111.5 | front east |
| R9 | 117.5–121.5 | front west |
| R10 | 125.5–129.5 | front east |

For row r, cabinet j = 0…59: Y from `60 + 2j` to `62 + 2j`. **600 per hall, 4,800 campus-wide.**

**Aisles:**

| Type | Hall-local X |
|---|---|
| West service zone | 0–39.5 |
| Cold aisle (outer west) | 39.5–45.5 |
| **Hot aisles (contained, 4 ft)** | 49.5–53.5 · 67.5–71.5 · 85.5–89.5 · 103.5–107.5 · 121.5–125.5 |
| **Cold aisles (internal, 6 ft)** | 57.5–63.5 · 75.5–81.5 · 93.5–99.5 · 111.5–117.5 |
| Cold aisle (outer east) | 129.5–135.5 |
| East service zone | 135.5–175 |
| South cross aisle | Y 0–60 |
| North cross aisle | Y 180–240 |

**CRAH / fan wall — 26 per hall:** 13 west at X 10–18, 13 east at X 157–165. For k = 0…12, Y from `12 + 17k` to `24 + 17k`. Footprint 8 × 12 ft.

Rack tag format `Hh-Rrr-Ccc` (e.g. `H3-R07-C42`). **Tag individual racks only on sheet A2.0**, never on the overall plan.

### 5.8 South band rooms (building-local, Y 0–110)

| Room | No. | X0 | Y0 | X1 | Y1 |
|---|---|---|---|---|---|
| BREAK ROOM | 109 | 0 | 0 | 80 | 50 |
| MEN'S RESTROOM | 107 | 80 | 0 | 130 | 50 |
| WOMEN'S RESTROOM | 108 | 130 | 0 | 180 | 50 |
| LOCKERS / WELLNESS | 111 | 180 | 0 | 240 | 50 |
| TRAINING ROOM | 112 | 240 | 0 | 350 | 50 |
| ADMIN CORRIDOR | C01 | 0 | 50 | 350 | 62 |
| OFFICE | 101 | 0 | 62 | 30 | 110 |
| OFFICE | 102 | 30 | 62 | 60 | 110 |
| OFFICE | 103 | 60 | 62 | 90 | 110 |
| OFFICE | 104 | 90 | 62 | 120 | 110 |
| CONFERENCE | 105 | 120 | 62 | 200 | 110 |
| OPEN OFFICE | 106 | 200 | 62 | 300 | 110 |
| IT CLOSET | 113 | 300 | 62 | 350 | 86 |
| OFFICE STORAGE | 114 | 300 | 86 | 350 | 110 |
| NOC | 115 | 350 | 0 | 410 | 70 |
| RECEPTION SUPPORT | 116 | 410 | 0 | 455 | 18 |
| VESTIBULE | 100 | 455 | 0 | 545 | 18 |
| VISITOR SCREENING | 117 | 545 | 0 | 590 | 18 |
| LOBBY / RECEPTION | 110 | 410 | 18 | 590 | 70 |
| FIRE COMMAND | 118 | 590 | 0 | 650 | 70 |
| SECURITY OPERATIONS | 120 | 350 | 70 | 430 | 110 |
| W CONTROLLED PASSAGE | 121 | 430 | 70 | 455 | 110 |
| MANTRAP STAGE 1 | 122 | 455 | 70 | 545 | 88 |
| MANTRAP STAGE 2 | 123 | 455 | 88 | 545 | 110 |
| E CONTROLLED PASSAGE | 124 | 545 | 70 | 570 | 110 |
| BADGE / ADMIN SUPPORT | 125 | 570 | 70 | 650 | 110 |
| RECEIVING / STAGING | 130 | 650 | 0 | 760 | 70 |
| SECURE STORAGE | 131 | 760 | 0 | 850 | 70 |
| SPARES LABORATORY | 132 | 650 | 70 | 730 | 110 |
| JANITOR | 133 | 730 | 70 | 755 | 110 |
| WASTE / PACKAGING | 134 | 755 | 70 | 800 | 110 |
| SERVICE PASSAGE | 135 | 800 | 70 | 850 | 110 |
| CARRIER ENTRANCE | 140 | 850 | 0 | 925 | 55 |
| MEET-ME / NETWORK | 141 | 850 | 55 | 925 | 110 |
| MAIN ELECTRICAL SERVICE | 142 | 925 | 0 | 1000 | 110 |

### 5.9 Technical band rooms (building-local)

| Room | No. | X0 | Y0 | X1 | Y1 |
|---|---|---|---|---|---|
| COOLING / PUMP RM A-S | 201 | 0 | 110 | 120 | 230 |
| COOLING / PUMP RM B-S | 202 | 0 | 230 | 120 | 350 |
| COOLING / PUMP RM A-N | 203 | 0 | 370 | 120 | 490 |
| COOLING / PUMP RM B-N | 204 | 0 | 490 | 120 | 610 |
| UPS / SWITCHGEAR A-S | 210 | 880 | 110 | 940 | 230 |
| BATTERY / ESS A-S | 211 | 940 | 110 | 1000 | 230 |
| UPS / SWITCHGEAR B-S | 212 | 880 | 230 | 940 | 350 |
| BATTERY / ESS B-S | 213 | 940 | 230 | 1000 | 350 |
| UPS / SWITCHGEAR A-N | 214 | 880 | 370 | 940 | 490 |
| BATTERY / ESS A-N | 215 | 940 | 370 | 1000 | 490 |
| UPS / SWITCHGEAR B-N | 216 | 880 | 490 | 940 | 610 |
| BATTERY / ESS B-N | 217 | 940 | 490 | 1000 | 610 |
| WATER TREATMENT / PUMP | 220 | 0 | 610 | 120 | 720 |
| HALL ELECTRICAL E1 | 221 | 120 | 610 | 295 | 720 |
| HALL ELECTRICAL E2 | 222 | 315 | 610 | 490 | 720 |
| HALL ELECTRICAL E3 | 223 | 510 | 610 | 685 | 720 |
| HALL ELECTRICAL E4 | 224 | 705 | 610 | 880 | 720 |
| CENTRAL SWITCHGEAR / CONTROLS | 225 | 880 | 610 | 1000 | 720 |

Draw the X = 940 UPS/battery dividing wall on `03-WALL-FIRE`.

### 5.10 Doors

| Location | Size |
|---|---|
| Vestibule exterior and vestibule-to-lobby | 6 ft double-door pairs centered on building-local X 500 |
| Mantrap (both stages) | 4 ft controlled doors |
| Hall to spine or cross corridor | Two 8 ft equipment doors per hall |
| Loading, south wall | Two 14 ft doors at building-local X 680–694 and X 710–724 |
| All other rooms | 3'-0" × 7'-0" typical |

---

## PART 6 — CORE ROUTINES

These implement the Part 2 contract. Write them first; everything else calls them.

### 6.1 AutoLISP (primary path)

**Wall with poché — Requirement 1**

```lisp
;; Filled wall segment centered on p1->p2
(defun wallseg (p1 p2 th lay / ang dx dy a b c d)
  (setq ang (angle p1 p2)
        dx  (* (/ th 2.0) (cos (+ ang (/ pi 2.0))))
        dy  (* (/ th 2.0) (sin (+ ang (/ pi 2.0))))
        a (list (+ (car p1) dx) (+ (cadr p1) dy))
        b (list (+ (car p2) dx) (+ (cadr p2) dy))
        c (list (- (car p2) dx) (- (cadr p2) dy))
        d (list (- (car p1) dx) (- (cadr p1) dy)))
  (setvar "CLAYER" lay)
  (command "_.PLINE" a b c d "_C")
  (command "_.SOLID" a b d c "")   ; bowtie order for rectangle a-b-c-d
  (princ))

(defun wallrect (x0 y0 x1 y1 th lay)
  (wallseg (list x0 y0) (list x1 y0) th lay)
  (wallseg (list x1 y0) (list x1 y1) th lay)
  (wallseg (list x1 y1) (list x0 y1) th lay)
  (wallseg (list x0 y1) (list x0 y0) th lay)
  (princ))
```

Thicknesses: exterior `1.0` on `03-WALL-EXT`, rated `1.0` on `03-WALL-FIRE`, partition `0.5` on `03-WALL-INT`. **Run `OVERKILL` on wall layers afterward** to clean duplicate shared walls.

**Door with swing — Requirement 4**

```lisp
(defun door (hinge w a0 mk / r p2)
  (setvar "CLAYER" "07-DOOR")
  (setq r  (/ (* a0 pi) 180.0)
        p2 (list (+ (car hinge) (* w (cos r))) (+ (cadr hinge) (* w (sin r)))))
  (command "_.LINE" hinge p2 "")
  (command "_.ARC" "_C" hinge p2 "_A" 90)
  (if mk (command "_.TEXT"
          (list (+ (car hinge) 1.5) (+ (cadr hinge) 1.5)) 2.0 0 mk))
  (princ))
```

**Furniture and fixtures — Requirement 3**

```lisp
(defun frect (x0 y0 x1 y1 lay)
  (setvar "CLAYER" lay)
  (command "_.RECTANGLE" (list x0 y0) (list x1 y1)) (princ))

(defun desk (x y lay)                       ; 5 x 2.5 desk + chair
  (frect x y (+ x 5.0) (+ y 2.5) lay)
  (command "_.CIRCLE" (list (+ x 2.5) (- y 1.5)) 0.9) (princ))

(defun ctable (x0 y0 x1 y1 n lay / i sp)    ; table with n seats per side
  (frect x0 y0 x1 y1 lay)
  (setq sp (/ (- x1 x0) (float (1+ n))) i 1)
  (repeat n
    (command "_.CIRCLE" (list (+ x0 (* i sp)) (- y0 1.5)) 0.9)
    (command "_.CIRCLE" (list (+ x0 (* i sp)) (+ y1 1.5)) 0.9)
    (setq i (1+ i)))
  (princ))

(defun wc (x y lay)                          ; toilet
  (frect x y (+ x 1.5) (+ y 2.5) lay)
  (command "_.CIRCLE" (list (+ x 0.75) (+ y 1.6)) 0.6) (princ))

(defun lav (x y lay) (frect x y (+ x 2.0) (+ y 1.5) lay) (princ))
```

**Minimum furniture plan:**

| Room | Contents |
|---|---|
| Offices 101–104 | 1 desk + chair each |
| Conference 105 | Table, 5 seats per long side |
| Open office 106 | 12 desks in a grid |
| Break room 109 | 6 tables with 4 chairs, counter along one wall |
| Restrooms 107 / 108 | 5 WC + 3 lav each, 5 ft turning circle |
| Lobby 110 | Reception desk + 2 seating clusters |
| Training 112 | 6 rows of tables |
| NOC 115 | Console row + video wall line |

**Solid cabinets, CRAH, landscaping, arrows — Requirement 5**

```lisp
(defun rack (x y)
  (setvar "CLAYER" "08-EQPM-RACK")
  (command "_.RECTANGLE" (list x y) (list (+ x 4.0) (+ y 2.0)))
  (command "_.SOLID" (list x y) (list (+ x 4.0) y)
                     (list x (+ y 2.0)) (list (+ x 4.0) (+ y 2.0)) "")
  (princ))

(defun crah (x y tag)
  (frect x y (+ x 8.0) (+ y 12.0) "08-EQPM-CRAH")
  (command "_.TEXT" "_MC" (list (+ x 4.0) (+ y 6.0)) 2.0 0 tag) (princ))

(defun tree (x y r)
  (setvar "CLAYER" "02-LANDSCAPE")
  (command "_.CIRCLE" (list x y) r)
  (command "_.CIRCLE" (list x y) (* r 0.55)) (princ))

(defun pave (pt)
  (setvar "CLAYER" "02-PAVE-HATCH")
  (command "_.-HATCH" "_P" "ANSI31" 8.0 0 pt "") (princ))

(defun arrow (p1 p2 lay / ang h)
  (setvar "CLAYER" lay)
  (setq ang (angle p1 p2) h 4.0)
  (command "_.LINE" p1 p2 "")
  (command "_.LINE" p2 (polar p2 (+ ang 2.618) h) "")
  (command "_.LINE" p2 (polar p2 (- ang 2.618) h) "") (princ))
```

### 6.2 Python + ezdxf (alternative path)

Use if AutoCAD is LT, if you prefer generating outside the app, or to produce DXF for AutoCAD Web.

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install ezdxf
```

```python
import ezdxf, math
from ezdxf.enums import TextEntityAlignment

BX, BY = 548.756, 688.756
PX, PY = 892.756, 276.756
def b2s(x, y): return (BX + x, BY + y)
def p2s(x, y): return (PX + x, PY + y)

def wallseg(msp, p1, p2, th, lay):
    ang = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
    dx, dy = th/2*math.cos(ang+math.pi/2), th/2*math.sin(ang+math.pi/2)
    pts = [(p1[0]+dx, p1[1]+dy), (p2[0]+dx, p2[1]+dy),
           (p2[0]-dx, p2[1]-dy), (p1[0]-dx, p1[1]-dy)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": lay})
    h = msp.add_hatch(color=7, dxfattribs={"layer": lay})
    h.paths.add_polyline_path(pts, is_closed=True)

def wallrect(msp, x0, y0, x1, y1, th, lay):
    for a, b in (((x0,y0),(x1,y0)), ((x1,y0),(x1,y1)),
                 ((x1,y1),(x0,y1)), ((x0,y1),(x0,y0))):
        wallseg(msp, a, b, th, lay)
```

Split output into `dallas-site.dxf`, `dallas-building.dxf`, `dallas-rack-hall.dxf` to keep files responsive.

### 6.3 Text height rule — Requirements 6 and 7

Model text height = **plotted height (inches) × scale factor**.

| Sheet scale | Factor | 3/32" text | 1/8" text |
|---|---|---|---|
| 1" = 100'-0" | 1200 | 9.4 ft | 12.5 ft |
| 1" = 40'-0" | 480 | 3.75 ft | 5.0 ft |
| 1" = 20'-0" | 240 | 1.9 ft | 2.5 ft |
| 1/16" = 1'-0" | 192 | 1.5 ft | 2.0 ft |
| 1/8" = 1'-0" | 96 | 0.75 ft | 1.0 ft |

**Collision rule — this caused the previous failure.** At 1" = 40', text is 3.75 ft tall. A 30 ft office cannot hold "OFFICE 101" at that height plus furniture. Therefore:

- **A1.0 (1" = 40')** — label major zones only: data halls, band names, LOBBY, PARKING
- **A1.1 (1/8" = 1'-0")** — all individual room names and numbers

Never cram room labels onto the overall plan.

---

## PART 7 — BUILD PHASES

Execute in order. Verify each acceptance check. Save after each phase.

### Phase 1 — Setup · 0.5 hr
Create `~/Documents/DallasCAD/{lisp,dwg,pdf}`. New drawing, units decimal feet. `APPLOAD` the layer file, run `DALLAYERS`. Save `dwg/dallas-master.dwg`.
**Accept:** 27 layers with correct colors and lineweights; `FILLMODE` = 1.

### Phase 2 — Site and civil · 1 hr
Property square, 100 ft reserve, three utility yards, two stormwater reserves. Label each yard with name and size.
**Accept:** property sides measure 2097.513; no yard overlaps.

### Phase 3 — Roads and fire loop · 1.5 hr
All of §5.3. Pave drives. Add `26' FIRE APPARATUS LOOP (TYP.)`, `VEHICLE ENTRANCE — ONE WAY IN`, `SERVICE / TRUCK ENTRANCE`.
**Accept:** continuous 26 ft ring; public and service routes never merge.

### Phase 4 — Parking · 2 hr
All of §5.4. Stripe every stall. ADA stalls on `02-PARK-ADA` with ISA symbols and `VAN` text. Pave the lot. Trees on the perimeter and in islands. Drive-aisle arrows. Note `180 SPACES (174 STANDARD + 6 ACCESSIBLE)`.
**Accept:** stall count is exactly 180; ADA group spans 66 ft; lot hatched; trees present.

### Phase 5 — Shell and grid · 1.5 hr
Exterior wall via `wallrect` at 1.0 ft. Grid lines extended 60 ft beyond the building with 12 ft radius bubbles, 1–10 on X and A–F on Y.
**Accept:** exterior wall reads as a thick filled band; bubbles ring the plan.

### Phase 6 — Halls and circulation · 1 hr
Eight halls via `wallrect` at 1.0 ft on `03-WALL-FIRE`. Spines and cross corridor on `03-WALL-INT`. Label `DATA HALL Hn / 175' x 240' / 12 MW / 600 RACKS`.
**Accept:** 336,000 + 44,000 = 380,000 ft².

### Phase 7 — South band rooms · 2.5 hr
All 36 rooms from §5.8 at 0.5 ft on `03-WALL-INT`. Furniture per §6.1. Doors per §5.10. Room tags at 1.0 ft height for the A1.1 enlargement.
**Accept:** every room has poché walls, name, number, a door with swing, and furniture where listed.

### Phase 8 — Technical bands · 1 hr
All 18 rooms from §5.9. Rated wall at X = 940. Equipment rectangles on `08-EQPM-ELEC` inside UPS, battery, and switchgear rooms.
**Accept:** all labeled; rated walls visibly heavier than partitions.

### Phase 9 — Racks and cooling · 2.5 hr
Per §5.7: 600 cabinets and 26 CRAH per hall. `COLD AISLE` labels on `09-HVAC-SUP`, `HOT AISLE` on `09-HVAC-RET`. Dashed containment over the five hot aisles on `05-HALL`.

**Performance:** build **one hall** completely, verify, then `COPY` to the other seven origins. If AutoCAD bogs down, keep full rack detail in `dwg/dallas-rack-hall.dwg` for sheet A2.0 and show halls as hatched zones on A1.0.

**Accept:** 600 cabinets in one hall, rows at the exact X ranges, cabinets solid black.

### Phase 10 — MEP and life safety · 2 hr
Supply arrows CRAH → every cold aisle. Return arrows from every hot aisle. A-path and B-path dashed routes that never share a corridor. Egress routes from halls to two separated exits.
**Accept:** every cold aisle has supply, every hot aisle has return, A and B physically separate.

### Phase 11 — Dimensions · 1.5 hr
Property sides, building 1000 × 720, grid bays, hall 175 × 240, aisle widths, rack pitch, parking module depths, road widths. Set `DIMSCALE` to match the target sheet.
**Accept:** dimension text legible at plotted scale; arrows visible.

### Phase 12 — Legend, keynotes, schedule · 2.5 hr

Place on the right side on `13-ANNO-LEGEND`.

**Legend:** 2 HR rated wall · 1 HR rated wall · non-rated partition · door with swing · 2 HR door · exit · fire extinguisher · fire pull station · temperature sensor · supply air · return air · cable tray · PDU-A · PDU-B · piping · column.

**Keynotes:**
1. 42U server cabinet, 4' × 2' planning footprint (typ.)
2. PDU-A — fed from UPS A path
3. PDU-B — fed from UPS B path
4. Hot-aisle containment door
5. No-step aisle — maintain clear
6. Fire-rated barrier — see plan
7. 26' fire apparatus loop
8. Two-stage interlocked mantrap

**Door schedule** via the `TABLE` command:

| MARK | SIZE | TYPE | RATING |
|---|---|---|---|
| 100A | 6'-0" × 7'-0" PAIR | H.M. | N.R. |
| 100B | 6'-0" × 7'-0" PAIR | H.M. | N.R. |
| 101–104 | 3'-0" × 7'-0" | H.M. | N.R. |
| 105–114 | 3'-0" × 7'-0" | H.M. | N.R. |
| 122A / 123A | 4'-0" × 7'-0" | H.M. | 1 HR |
| H1–H8 EQ | 8'-0" × 8'-0" | H.M. | 2 HR |
| 211 / 213 / 215 / 217 | 3'-0" × 7'-0" | H.M. | 2 HR |
| LD1 / LD2 | 14'-0" × 14'-0" | COIL | N.R. |

**Accept:** every symbol on the plan appears in the legend; every door mark exists in the schedule.

### Phase 13 — Sheets, title blocks, plotting · 4.5 hr

Paper size **ARCH D (24 × 36)** for all layouts.

| Sheet | Content | Scale |
|---|---|---|
| **C1.0** | Site: property, reserves, roads, fire loop, yards | 1" = 100'-0" |
| **C1.1** | Parking and arrival enlargement | 1" = 20'-0" |
| **A1.0** | Overall floor plan, zone labels only | 1" = 40'-0" |
| **A1.1** | Admin / lobby / security enlargement, all room names | 1/8" = 1'-0" |
| **A2.0** | Typical data hall rack plan (H3) | 1/16" = 1'-0" |
| **M1.0** | Mechanical concept: airflow, CRAH | 1" = 40'-0" |
| **E1.0** | Electrical concept: A/B, UPS, substation | 1" = 40'-0" |
| **LS1.0** | Life safety: egress, ratings | 1" = 40'-0" |
| **S1.0** | Schedules and legend | NTS |

Per sheet: `MVIEW` → set exact scale → **lock the viewport** → per-viewport freeze irrelevant layers (freeze `08-EQPM-RACK` on C1.0, freeze `02-*` on A1.1, and so on).

**Title block on `14-TBLK`, every field filled:**

```
CONCEPTUAL DALLAS DATA CENTER
[SHEET TITLE]

PROJECT:  101-ACRE / 96 MW CAMPUS
LOCATION: DALLAS, TEXAS
DATE:     [today]
SCALE:    [actual, e.g. 1" = 40'-0"]
DRAWN BY: [user]
CHECKED:  --
SHEET:    [A1.0]
```

Add a **north arrow** and **graphic scale bar** to every plan sheet. Plot each layout to PDF in `~/Documents/DallasCAD/pdf/`.

**Accept:** nine PDFs, correct scales, no blank title fields, no text collisions.

### Phase 14 — QA · 2 hr
Run Part 8 and Part 9. Fix everything that fails.

**Total ≈ 26 hr — 3 to 4 focused working days.**

---

## PART 8 — VISUAL QUALITY GATE

Screenshot each sheet and confirm every line before declaring completion.

- [ ] Walls are **thick filled bands**, never single lines
- [ ] Exterior walls visibly heavier than partitions
- [ ] Every door has a leaf **and** a swing arc
- [ ] Offices have desks, conference has a table, restrooms have fixtures, lobby has seating
- [ ] Server cabinets are **solid filled**
- [ ] Parking is paved, striped, landscaped, ADA marked
- [ ] Cold aisles cyan-labeled, hot aisles red-labeled, arrows present
- [ ] Grid bubbles 1–10 and A–F present
- [ ] Legend, keynotes, and door schedule complete
- [ ] Dimensions readable
- [ ] North arrow and graphic scale on every plan sheet
- [ ] **No overlapping or unreadable text anywhere**
- [ ] Title blocks fully filled with real scales
- [ ] Disclaimer on every sheet

**Any failure must be fixed before reporting completion.**

---

## PART 9 — VERIFICATION COUNTS

| Item | Required |
|---|---|
| Parking spaces | 180 (174 standard + 6 accessible, 1 van) |
| Racks per hall | 600 |
| Racks campus-wide | 4,800 |
| CRAH per hall | 26 (13 west + 13 east) |
| Data halls | 8 |
| Hot aisles per hall | 5 |
| Cold aisles per hall | 6 |
| South band rooms | 36 |
| Technical band rooms | 18 |
| Building area | 720,000 ft² |
| Hall area | 336,000 ft² |
| Corridor area | 44,000 ft² |
| Site area | 4,399,560 ft² (101.000 acres) |

---

## PART 10 — FAILURE PROTOCOL

- Same action fails **three times** → stop, screenshot, report what you see and your best hypothesis. Do not loop.
- AutoCAD unresponsive from entity count → split into `dallas-site.dwg`, `dallas-building.dwg`, `dallas-rack-hall.dwg`.
- A LISP function errors → report the command-line text **verbatim**. Do not silently skip a phase.
- Unrecognized dialog → screenshot and ask rather than guessing.
- Missing data → say so explicitly. **Never invent a coordinate.**
- Never delete or modify files outside `~/Documents/DallasCAD/`.

---

## PART 11 — PROJECT FACTS

96 MW IT load · eight 12 MW halls · conventional air-cooled 20 kW racks · 4,800 racks · one-story building · preliminary N+1 block redundancy · PUE 1.25 → 120 MW facility demand → ~150 MVA planning placeholder (not a confirmed Oncor service).

**Reserves:** 42 generator positions at 3 MW (40 duty + 2 redundant) · 32 heat-rejection cells at 1,000 tons (30 duty + 2 redundant) · six 2.5 MW UPS modules per hall block (5 duty + 1 redundant) · 26 CRAH positions per hall (24 duty + 2 standby at 65,000 cfm).

**Cooling math:** one 20 kW rack rejects ~68,243 Btu/h; ~2,528 cfm per rack at 25°F rise; ~1,516,800 cfm per 600-rack hall.

---

## PART 12 — HONEST SCOPE AND LIMITS

- This is **conceptual massing at drafting fidelity**, not a sealed permit set.
- Fire ratings, egress counts, exit travel distances, and accessibility compliance are **placeholders** requiring a licensed architect's code analysis.
- No survey or legal parcel exists; the 101-acre square is an equal-area test geometry.
- The 100 ft planning reserve is an assumption, not a Dallas setback requirement.
- ~150 MVA is unconfirmed with Oncor.
- No finished-floor elevations, grading, or structural engineering.
- CRAH, UPS, generator, and chiller counts are capacity placeholders, not equipment selections.
- No company title-block or AIA layer standard was supplied; the standard in Part 4 is a reasonable default.

### Required disclaimer — place on every sheet

> CONCEPTUAL DESIGN BASIS — NOT FOR CONSTRUCTION, PERMIT, OR BIDDING. This drawing is a dimensionally coordinated planning study. It requires validation by a Dallas-licensed architect and licensed civil, structural, mechanical, electrical, plumbing, fire-protection, security, telecom, and geotechnical engineers against actual survey, zoning, easements, floodplain, utilities, geotechnical data, equipment selections, and adopted codes. Fire ratings, egress counts, accessibility compliance, and utility capacity shown are placeholders.

---

## PART 13 — START HERE

1. Confirm AutoCAD is open and is the **full version, not LT** (verify `APPLOAD` exists). If LT, switch to the Python path in §6.2.
2. Create `~/Documents/DallasCAD/{lisp,dwg,pdf}`.
3. Write `lisp/00-layers.lsp` from Part 4. `APPLOAD` it. Run `DALLAYERS`.
4. Write `lisp/01-core.lsp` from Part 6. `APPLOAD` it.
5. Begin Phase 2 and proceed in order, verifying each acceptance check.
6. Report after each phase with a screenshot.

**Remember: the difference between "just boxes" and a real drawing is wall poché, lineweight hierarchy, furniture, door swings, and hatches. Never skip them to save time.**
