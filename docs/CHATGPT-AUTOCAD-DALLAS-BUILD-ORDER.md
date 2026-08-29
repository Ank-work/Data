# BUILD ORDER FOR CHATGPT — Dallas Data Center CAD Set (Local AutoCAD, macOS)

**Paste this entire document into ChatGPT with Computer Use enabled. It is your complete instruction set. Do not ask the user for information that is already in this document.**

---

## 0. YOUR ROLE AND MISSION

You are operating **local AutoCAD on macOS** via Computer Use to produce a **client-presentable conceptual CAD set** for a 101-acre Dallas data center.

**Success = a 9-sheet PDF set that a non-technical client immediately reads as professional architectural drawings.**

The benchmark is a reference sheet with: poché walls, labeled rooms, furniture, door swings, a full rack plan with hot/cold aisles, parking with striped stalls and landscaping, a legend, keynotes, a door schedule, dimensions, a north arrow, a graphic scale, and a filled title block.

### 0.1 The failure you must avoid

A previous attempt produced correct *structure* but it looked flat and unfinished. The client's words were "it's just boxes." The cause was five specific omissions. **These are your highest priority and are non-negotiable:**

| # | Requirement | Meaning |
|---|---|---|
| **1** | **Walls have real thickness with solid fill (poché)** | Never draw a room as a single-line rectangle. Every wall is a filled band of actual thickness. This is ~60% of the visual difference. |
| **2** | **Lineweight hierarchy** | Heavy exterior walls, medium partitions, light equipment, hairline dimensions and grids. |
| **3** | **Furniture and fixtures** | Desks in offices, table in conference, toilets/lavs in restrooms, seating in lobby, tables in break room. |
| **4** | **Door swings** | Every door gets a leaf line plus a 90° arc. Nothing reads as "architecture" faster. |
| **5** | **Hatches and fills** | Solid-filled server cabinets, asphalt on parking, landscaping/trees, sidewalks. |

Plus two readability rules:

- **6** — **No overlapping text.** If labels collide at a given scale, move them to an enlargement sheet or use leaders. Never ship a smeared label zone.
- **7** — **Real plotted scales.** Never write "MODELSPACE IN FEET" in a title block. Use a true scale such as 1" = 40'-0".

### 0.2 Hard rules

1. **Every coordinate comes from Section 3 of this document.** Do not estimate, round, or invent geometry.
2. **Work in decimal feet, model space, 1:1.** Scale is applied only in paper-space viewports.
3. **Generate geometry with code, not clicking.** Clicking is for loading scripts, viewports, and plotting only.
4. **Never delete or overwrite the user's files** outside `~/Documents/DallasCAD/`.
5. **Every sheet carries the disclaimer** in Section 9.3. This is conceptual work, not a permit set.
6. **Stop and report** if you fail the same action three times. Do not loop.

---

## 1. ENVIRONMENT AND METHOD

### 1.1 What you have

- **AutoCAD full version on macOS** (not LT — LT has no AutoLISP)
- **AutoLISP works.** Load `.lsp` files with `APPLOAD`, or run `.scr` with `SCRIPT`.
- **VBA, ActiveX, and `.NET` do NOT work on Mac AutoCAD.** Never use `vl-load-com` or any `vla-*` function. Use `entmake` and `command` only.
- **`accoreconsole` does not exist on macOS.** All execution happens in the GUI.

### 1.2 Working directory

Create and use:

```
~/Documents/DallasCAD/
├── lisp/          # your .lsp files
├── dwg/           # drawings
└── pdf/           # plotted output
```

### 1.3 The execution loop

```
1. Write a .lsp file to ~/Documents/DallasCAD/lisp/
2. In AutoCAD: APPLOAD → select file → Load
3. Type the command name at the AutoCAD prompt
4. ZOOM Extents, screenshot, verify against the phase acceptance check
5. Fix and reload if wrong
```

Write files using a text editor or Terminal. Verify each phase visually before starting the next.

### 1.4 AutoLISP conventions for this project

- Prefix all commands with `_.` for locale safety: `(command "_.LINE" ...)`
- Set `FILLMODE` to 1 so solids display filled
- Use `SOLID` for wall poché — it is faster and more reliable than hatch boundary detection
- Point order for `SOLID` on rectangle corners a→b→c→d is **a b d c** (bowtie order)

---

## 2. LAYER STANDARD

Create these first. Colors are AutoCAD Color Index. Lineweight is in mm.

| Layer | Color | Lineweight | Linetype | Contents |
|---|---|---|---|---|
| `00-SITE-CTRL` | 8 | 0.13 | CONTINUOUS | Property boundary, control |
| `01-CIVIL-RSRV` | 30 | 0.13 | DASHED | Planning reserve, stormwater, yards |
| `02-ROADS` | 8 | 0.18 | CONTINUOUS | Drives, fire loop, aprons |
| `02-PARK-STALL` | 253 | 0.13 | CONTINUOUS | Stall striping |
| `02-PARK-ADA` | 150 | 0.20 | CONTINUOUS | Accessible stalls, ISA symbol |
| `02-PAVE-HATCH` | 251 | 0.09 | CONTINUOUS | Asphalt fill |
| `02-LANDSCAPE` | 74 | 0.13 | CONTINUOUS | Trees, islands, lawn |
| `03-WALL-EXT` | 7 | **0.70** | CONTINUOUS | 12" exterior wall + poché |
| `03-WALL-FIRE` | 1 | **0.50** | CONTINUOUS | 12" rated barrier + poché |
| `03-WALL-INT` | 7 | **0.35** | CONTINUOUS | 6" partition + poché |
| `04-GRID` | 4 | 0.09 | CENTER | Grid lines and bubbles |
| `05-HALL` | 8 | 0.25 | CONTINUOUS | Hall zone outlines, containment |
| `06-ROOM-TAG` | 7 | 0.13 | CONTINUOUS | Room names and numbers |
| `06-FURN` | 9 | 0.13 | CONTINUOUS | Desks, tables, seating |
| `06-PLUMB` | 9 | 0.13 | CONTINUOUS | Toilets, lavatories |
| `07-DOOR` | 2 | 0.20 | CONTINUOUS | Leaves, swings, marks |
| `08-EQPM-RACK` | 250 | 0.13 | CONTINUOUS | Server cabinets (solid filled) |
| `08-EQPM-CRAH` | 3 | 0.20 | CONTINUOUS | Cooling modules |
| `08-EQPM-ELEC` | 6 | 0.20 | CONTINUOUS | UPS, battery, switchgear |
| `09-HVAC-SUP` | 4 | 0.20 | CONTINUOUS | Supply air arrows, cold aisle |
| `09-HVAC-RET` | 1 | 0.20 | CONTINUOUS | Return air arrows, hot aisle |
| `10-ELEC-A` | 2 | 0.20 | DASHED | A-path distribution |
| `10-ELEC-B` | 6 | 0.20 | DASHED | B-path distribution |
| `11-LIFE-EGRESS` | 3 | 0.25 | DASHED | Exit routes |
| `12-DIM` | 7 | 0.09 | CONTINUOUS | Dimensions |
| `13-ANNO-LEGEND` | 7 | 0.13 | CONTINUOUS | Legend, keynotes, schedules |
| `14-TBLK` | 7 | 0.25 | CONTINUOUS | Title block, borders |

### 2.1 Layer creation LISP

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
  (setvar "FILLMODE" 1)
  (setvar "LWDISPLAY" 1)
  (princ "\nDallas layers created.")
  (princ))
```

---

## 3. PROJECT DATA — ALL COORDINATES

**All values in decimal feet.** Site origin (0,0) is the southwest property corner. X is east, Y is north.

### 3.1 Coordinate systems

| System | Definition |
|---|---|
| **Site** | Origin at SW property corner |
| **Building-local** | Building (0,0) = site **(548.756, 688.756)** |
| **Parking-local** | Parking P(0,0) = site **(892.756, 276.756)** |

Conversion helpers:

```lisp
(setq *BX* 548.756 *BY* 688.756 *PX* 892.756 *PY* 276.756)
(defun b2s (x y) (list (+ *BX* x) (+ *BY* y)))   ; building -> site
(defun p2s (x y) (list (+ *PX* x) (+ *PY* y)))   ; parking  -> site
```

### 3.2 Site

| Item | Value |
|---|---|
| Property square | (0,0) to (2097.513, 2097.513) — 101.000 acres |
| Planning reserve | 100 ft inside all boundaries; break at south drive entrances |
| Substation yard | X 1650–1990, Y 830–1230 (340 × 400) |
| Generator yard | X 600–1498, Y 1510–1810 (898 × 300, 42 positions @ 3 MW) |
| Heat rejection yard | X 600–1498, Y 1810–1990 (898 × 180, 32 cells @ 1000 ton) |
| Stormwater west | X 100–450, Y 700–2000 |
| Stormwater southwest | X 100–300, Y 100–575 |

### 3.3 Roads and fire loop

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

### 3.4 Parking — 180 spaces (parking-local coordinates)

Boundary: 312 × 312 from P(0,0) to P(312,312).

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

- **Rows 1–5:** 30 stalls each. Strip local X 21–291, divided into 30 bays of 9 ft. = **150 standard**
- **Row 6:** twelve 9 ft bays at X 15–123, accessible group X 123–189, twelve 9 ft bays at X 189–297. = **24 standard + 6 accessible**

**Accessible group breakdown (66 ft, west to east):**

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

Drop-off: local Y 252–276, centered on the pedestrian axis. **Total = 150 + 24 + 6 = 180.**

### 3.5 Building shell and grid (building-local)

- Outside face rectangle: (0,0) to (1000, 720)
- Exterior wall: 12 in, drawn inward from the outside face
- Interior partitions: 6 in ordinary, 12 in for hall/fire barriers

**Grid X:** 0, 120, 295, 315, 490, 510, 685, 705, 880, 1000 → bubbles **1–10**
**Grid Y:** 0, 110, 350, 370, 610, 720 → bubbles **A–F**

### 3.6 Data halls (building-local)

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

**Circulation:** three north-south spines at X 295–315, 490–510, 685–705 (all Y 110–610). East-west cross corridor X 120–880, Y 350–370.

### 3.7 Rack module (hall-local, origin at each hall SW corner)

Cabinet footprint: **4 ft east-west × 2 ft north-south**. Rows run Y 60–180.

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

For row r and cabinet j = 0…59: Y from `60 + 2j` to `62 + 2j`. **10 × 60 = 600 per hall, 4,800 campus-wide.**

**Aisles:**

| Type | Hall-local X |
|---|---|
| West service zone | 0–39.5 |
| Cold aisle (outer W) | 39.5–45.5 |
| **Hot aisles (contained)** | 49.5–53.5, 67.5–71.5, 85.5–89.5, 103.5–107.5, 121.5–125.5 |
| **Cold aisles (internal)** | 57.5–63.5, 75.5–81.5, 93.5–99.5, 111.5–117.5 |
| Cold aisle (outer E) | 129.5–135.5 |
| East service zone | 135.5–175 |
| South cross aisle | Y 0–60 |
| North cross aisle | Y 180–240 |

**CRAH / fan wall — 26 per hall:** 13 west at X 10–18, 13 east at X 157–165. For k = 0…12, Y from `12 + 17k` to `24 + 17k`. Footprint 8 × 12 ft.

Rack tag format: `Hh-Rrr-Ccc` (example `H3-R07-C42`). **Only tag individual racks on the enlarged rack plan sheet A2.0** — never on the overall plan.

### 3.8 South band rooms (building-local, Y 0–110)

| Room | Number | X0 | Y0 | X1 | Y1 |
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

### 3.9 Technical band rooms (building-local)

| Room | Number | X0 | Y0 | X1 | Y1 |
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

Battery rooms use rated separation from UPS rooms — draw the X=940 wall on `03-WALL-FIRE`.

---

## 4. CORE DRAWING ROUTINES — WRITE THESE FIRST

These functions solve the five craft requirements. Everything else calls them.

### 4.1 Wall with thickness and poché — REQUIREMENT 1

```lisp
;; Draw a filled wall segment centered on p1->p2
(defun wallseg (p1 p2 th lay / ang dx dy a b c d)
  (setq ang (angle p1 p2)
        dx  (* (/ th 2.0) (cos (+ ang (/ pi 2.0))))
        dy  (* (/ th 2.0) (sin (+ ang (/ pi 2.0))))
        a (list (+ (car p1) dx) (+ (cadr p1) dy))
        b (list (+ (car p2) dx) (+ (cadr p2) dy))
        c (list (- (car p2) dx) (- (cadr p2) dy))
        d (list (- (car p1) dx) (- (cadr p1) dy)))
  (setvar "CLAYER" lay)
  ;; outline
  (command "_.PLINE" a b c d "_C")
  ;; poché fill  (SOLID bowtie order: a b d c)
  (command "_.SOLID" a b d c "")
  (princ))

;; Draw all four walls of a rectangular room
(defun wallrect (x0 y0 x1 y1 th lay)
  (wallseg (list x0 y0) (list x1 y0) th lay)
  (wallseg (list x1 y0) (list x1 y1) th lay)
  (wallseg (list x1 y1) (list x0 y1) th lay)
  (wallseg (list x0 y1) (list x0 y0) th lay)
  (princ))
```

**Wall thicknesses:** exterior `1.0` ft on `03-WALL-EXT`, hall/fire barrier `1.0` ft on `03-WALL-FIRE`, interior partition `0.5` ft on `03-WALL-INT`.

**After drawing all rooms, run `OVERKILL`** on the wall layers to remove duplicate segments where rooms share walls.

### 4.2 Door with swing — REQUIREMENT 4

```lisp
;; hinge = point, w = leaf width, a0 = start angle in degrees, mk = mark text
(defun door (hinge w a0 mk / r p2)
  (setvar "CLAYER" "07-DOOR")
  (setq r (/ (* a0 pi) 180.0)
        p2 (list (+ (car hinge) (* w (cos r))) (+ (cadr hinge) (* w (sin r)))))
  (command "_.LINE" hinge p2 "")
  (command "_.ARC" "_C" hinge p2 "_A" 90)
  (if mk (progn
    (setvar "CLAYER" "07-DOOR")
    (command "_.TEXT" (list (+ (car hinge) 1.5) (+ (cadr hinge) 1.5)) 2.0 0 mk)))
  (princ))
```

Place doors on: every office, conference, break room, restroom, training, lockers, IT, storage, NOC, fire command, security ops, badge, spares, janitor, waste, carrier, meet-me, electrical; both mantrap stages; the vestibule and lobby 6 ft pairs centered on building-local X 500; two 8 ft equipment doors from each hall to an adjacent spine or the cross corridor; two 14 ft loading doors on the south wall at building-local X 680–694 and X 710–724.

### 4.3 Furniture and fixtures — REQUIREMENT 3

```lisp
(defun frect (x0 y0 x1 y1 lay)
  (setvar "CLAYER" lay)
  (command "_.RECTANGLE" (list x0 y0) (list x1 y1))
  (princ))

;; Desk 5x2.5 with chair
(defun desk (x y lay)
  (frect x y (+ x 5.0) (+ y 2.5) lay)
  (setvar "CLAYER" lay)
  (command "_.CIRCLE" (list (+ x 2.5) (- y 1.5)) 0.9)
  (princ))

;; Conference table with n seats per long side
(defun ctable (x0 y0 x1 y1 n lay / i sp)
  (frect x0 y0 x1 y1 lay)
  (setq sp (/ (- x1 x0) (float (1+ n))) i 1)
  (repeat n
    (command "_.CIRCLE" (list (+ x0 (* i sp)) (- y0 1.5)) 0.9)
    (command "_.CIRCLE" (list (+ x0 (* i sp)) (+ y1 1.5)) 0.9)
    (setq i (1+ i)))
  (princ))

;; Toilet 1.5x2.5
(defun wc (x y lay)
  (frect x y (+ x 1.5) (+ y 2.5) lay)
  (command "_.CIRCLE" (list (+ x 0.75) (+ y 1.6)) 0.6)
  (princ))

;; Lavatory 2x1.5
(defun lav (x y lay) (frect x y (+ x 2.0) (+ y 1.5) lay) (princ))
```

**Minimum furniture plan:**

| Room | Contents |
|---|---|
| Offices 101–104 | 1 desk + chair each |
| Conference 105 | Table with 5 seats per side |
| Open office 106 | 12 desks in a grid |
| Break room 109 | 6 tables with 4 chairs each, counter along one wall |
| Restrooms 107/108 | 5 WC + 3 lav each, 5 ft turning circle |
| Lobby 110 | Reception desk + 2 seating clusters |
| Training 112 | 6 rows of tables |
| NOC 115 | Console row + video wall line |

### 4.4 Solid-filled cabinet and CRAH — REQUIREMENT 5

```lisp
;; Server cabinet 4x2, solid filled
(defun rack (x y)
  (setvar "CLAYER" "08-EQPM-RACK")
  (command "_.RECTANGLE" (list x y) (list (+ x 4.0) (+ y 2.0)))
  (command "_.SOLID" (list x y) (list (+ x 4.0) y)
                     (list x (+ y 2.0)) (list (+ x 4.0) (+ y 2.0)) "")
  (princ))

(defun crah (x y tag)
  (frect x y (+ x 8.0) (+ y 12.0) "08-EQPM-CRAH")
  (setvar "CLAYER" "08-EQPM-CRAH")
  (command "_.TEXT" "_MC" (list (+ x 4.0) (+ y 6.0)) 2.0 0 tag)
  (princ))
```

### 4.5 Landscaping, paving, arrows — REQUIREMENT 5

```lisp
;; Tree symbol
(defun tree (x y r)
  (setvar "CLAYER" "02-LANDSCAPE")
  (command "_.CIRCLE" (list x y) r)
  (command "_.CIRCLE" (list x y) (* r 0.55))
  (princ))

;; Asphalt hatch inside last-drawn closed boundary
(defun pave (pt)
  (setvar "CLAYER" "02-PAVE-HATCH")
  (command "_.-HATCH" "_P" "ANSI31" 8.0 0 pt "")
  (princ))

;; Directional arrow
(defun arrow (p1 p2 lay / ang h)
  (setvar "CLAYER" lay)
  (setq ang (angle p1 p2) h 4.0)
  (command "_.LINE" p1 p2 "")
  (command "_.LINE" p2 (polar p2 (+ ang 2.618) h) "")
  (command "_.LINE" p2 (polar p2 (- ang 2.618) h) "")
  (princ))
```

Place trees along the parking perimeter and in the arrival zone (local Y 0–60), plus landscape islands between stall rows. Pave the parking square and drive aisles.

### 4.6 Text height rule — REQUIREMENT 6 and 7

Model-space text height = **plotted height (inches) × drawing scale factor**.

| Sheet scale | Scale factor | 3/32" text | 1/8" text |
|---|---|---|---|
| 1" = 100'-0" | 1200 | 9.4 ft | 12.5 ft |
| 1" = 40'-0" | 480 | 3.75 ft | 5.0 ft |
| 1" = 20'-0" | 240 | 1.9 ft | 2.5 ft |
| 1/8" = 1'-0" | 96 | 0.75 ft | 1.0 ft |
| 1/16" = 1'-0" | 192 | 1.5 ft | 2.0 ft |

**Collision rule:** on the overall plan (1" = 40'), text is 3.75 ft tall. A 30 ft wide office cannot hold "OFFICE 101" at that height plus furniture. **Therefore: on sheet A1.0 label only major zones** (data halls, band names, LOBBY, PARKING). Put individual room names on enlargement sheet A1.1 at 1/8" = 1'-0". Do not cram them onto A1.0.

---

## 5. BUILD PHASES

Execute in order. Verify each acceptance check before continuing. Save after each phase.

### Phase 1 — Setup
Create `~/Documents/DallasCAD/`. Start a new drawing, `UNITS` → Architectural or Decimal feet. Load and run `DALLAYERS`. Save as `dwg/dallas-master.dwg`.
**Accept:** 27 layers exist with correct colors and lineweights; `FILLMODE` = 1.

### Phase 2 — Site and civil
Property square, 100 ft reserve, three utility yards, two stormwater reserves. Label each yard with name and size.
**Accept:** property sides measure 2097.513; yards do not overlap.

### Phase 3 — Roads and fire loop
All items in Section 3.3. Pave the drives. Add text `26' FIRE APPARATUS LOOP (TYP.)`, `VEHICLE ENTRANCE — ONE WAY IN`, `SERVICE / TRUCK ENTRANCE`.
**Accept:** fire loop is a continuous 26 ft ring; public and service routes never merge.

### Phase 4 — Parking
All of Section 3.4. Stripe every stall. Fill ADA stalls on `02-PARK-ADA` and add an ISA symbol plus `VAN` text on the van space. Pave the lot. Add trees along the perimeter and islands. Add drive-aisle arrows and a `180 SPACES (174 STANDARD + 6 ACCESSIBLE)` note.
**Accept:** count stalls — exactly 180. ADA group spans 66 ft. Lot is hatched, trees present.

### Phase 5 — Building shell and grid
Exterior wall via `wallrect` at 1.0 ft on `03-WALL-EXT`. Grid lines extended 60 ft past the building with 12 ft radius bubbles: numbers 1–10 on X, letters A–F on Y.
**Accept:** exterior wall reads as a thick filled band. Bubbles ring the plan.

### Phase 6 — Halls and circulation
Eight hall rectangles with `wallrect` at 1.0 ft on `03-WALL-FIRE`. Three spines and the cross corridor on `03-WALL-INT`. Label each hall `DATA HALL Hn / 175' x 240' / 12 MW / 600 RACKS`.
**Accept:** 336,000 ft² of halls + 44,000 ft² of corridor = 380,000 ft².

### Phase 7 — South band rooms
All 36 rooms from Section 3.8 using `wallrect` at 0.5 ft on `03-WALL-INT`. Add furniture per Section 4.3. Add doors per Section 4.2. Room tags at 1.0 ft height (for the A1.1 enlargement).
**Accept:** every room has walls with poché, a name, a number, a door with a swing, and furniture where listed.

### Phase 8 — Technical bands
All 18 rooms from Section 3.9. Battery/UPS dividing wall at X=940 on `03-WALL-FIRE`. Add equipment rectangles on `08-EQPM-ELEC` inside UPS, battery, and switchgear rooms.
**Accept:** all labeled; rated wall visibly heavier than partitions.

### Phase 9 — Racks and cooling
For each of the 8 halls, place 600 cabinets per Section 3.7 and 26 CRAH units. Label aisles `COLD AISLE` on `09-HVAC-SUP` and `HOT AISLE` on `09-HVAC-RET`. Draw dashed containment boundaries over the five hot aisles on `05-HALL`.

**Performance note:** 4,800 solid-filled cabinets will slow AutoCAD. Build **one hall** completely, verify it, then `COPY` the hall contents to the other seven hall origins. If it becomes unworkable, keep full rack detail in a separate drawing `dwg/dallas-rack-hall.dwg` for sheet A2.0 and show halls as hatched zones on A1.0.

**Accept:** 600 cabinets in one hall, rows at the exact X ranges in the table, cabinets solid black.

### Phase 10 — MEP and life safety
Supply arrows from CRAH to every cold aisle on `09-HVAC-SUP`. Return arrows from every hot aisle on `09-HVAC-RET`. A-path and B-path dashed routes on `10-ELEC-A` / `10-ELEC-B` — they must never share a route. Egress routes on `11-LIFE-EGRESS` from halls to two separated exits.
**Accept:** every cold aisle has supply, every hot aisle has return, A and B are physically separate.

### Phase 11 — Dimensions
Dimension: property sides, building 1000 × 720, grid bays, hall 175 × 240, aisle widths, rack pitch, parking module depths (18/24), road widths. Use `DIMSCALE` matching the target sheet.
**Accept:** dimension text is legible at plotted scale, arrows are visible.

### Phase 12 — Legend, keynotes, schedules
Place on the right side of the sheet on `13-ANNO-LEGEND`.

**Legend:** 2 HR rated wall · 1 HR rated wall · non-rated partition · door with swing · 2 HR door · exit · fire extinguisher · fire pull · temperature sensor · supply air · return air · cable tray · PDU-A · PDU-B · piping · column.

**Keynotes:**
1. 42U server cabinet, 4' × 2' planning footprint (typ.)
2. PDU-A — fed from UPS A path
3. PDU-B — fed from UPS B path
4. Hot-aisle containment door
5. No-step aisle — maintain clear
6. Fire-rated barrier — see plan
7. 26' fire apparatus loop
8. Two-stage interlocked mantrap

**Door schedule** — build with the `TABLE` command, columns MARK / SIZE / TYPE / RATING:

| MARK | SIZE | TYPE | RATING |
|---|---|---|---|
| 100A | 6'-0" × 7'-0" PAIR | H.M. | N.R. |
| 100B | 6'-0" × 7'-0" PAIR | H.M. | N.R. |
| 101–104 | 3'-0" × 7'-0" | H.M. | N.R. |
| 105–114 | 3'-0" × 7'-0" | H.M. | N.R. |
| 122A/123A | 4'-0" × 7'-0" | H.M. | 1 HR |
| H1–H8 EQ | 8'-0" × 8'-0" | H.M. | 2 HR |
| 211/213/215/217 | 3'-0" × 7'-0" | H.M. | 2 HR |
| LD1 / LD2 | 14'-0" × 14'-0" | COIL | N.R. |

**Accept:** every symbol used on the plan appears in the legend; every door mark on the plan exists in the schedule.

### Phase 13 — Sheets, title blocks, plotting

Create these layouts. Set paper size **ARCH D (24 × 36)** for each.

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

**Per sheet:** `MVIEW` a viewport → set the exact scale → **lock the viewport** → use `VPLAYER` or per-viewport freeze to hide layers from other disciplines (freeze `08-EQPM-RACK` on C1.0, freeze `02-*` on A1.1, and so on).

**Title block on `14-TBLK`** — every field filled:

```
CONCEPTUAL DALLAS DATA CENTER
[SHEET TITLE]

PROJECT:  101-ACRE / 96 MW CAMPUS
LOCATION: DALLAS, TEXAS
DATE:     [today]
SCALE:    [actual scale, e.g. 1" = 40'-0"]
DRAWN BY: [user]
CHECKED:  --
SHEET:    [A1.0]
```

Also place a **north arrow** and **graphic scale bar** on every plan sheet.

Plot each layout to PDF in `~/Documents/DallasCAD/pdf/`.

**Accept:** nine PDFs, correct scales, no blank title-block fields, no text collisions.

---

## 6. VISUAL QUALITY GATE

Before declaring completion, screenshot each sheet and confirm every line:

- [ ] Walls are **thick filled bands**, never single lines
- [ ] Exterior walls visibly heavier than partitions
- [ ] Every door has a leaf **and** a swing arc
- [ ] Offices have desks; conference has a table; restrooms have fixtures; lobby has seating
- [ ] Server cabinets are **solid filled**
- [ ] Parking is paved, striped, has trees, ADA stalls are marked
- [ ] Cold aisles are cyan-labeled, hot aisles red-labeled, arrows present
- [ ] Grid bubbles 1–10 and A–F present
- [ ] Legend, keynotes, and door schedule present and complete
- [ ] Dimensions readable
- [ ] North arrow and graphic scale on every plan sheet
- [ ] **No overlapping or unreadable text anywhere**
- [ ] Title blocks fully filled with real scales
- [ ] Disclaimer present on every sheet

**If any box fails, fix it before reporting completion.**

---

## 7. VERIFICATION COUNTS

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

---

## 8. FAILURE PROTOCOL

- Same action fails **3 times** → stop, screenshot, report what you see and your best hypothesis. Do not keep retrying.
- AutoCAD becomes unresponsive from entity count → split into `dallas-site.dwg`, `dallas-building.dwg`, `dallas-rack-hall.dwg` and produce sheets from separate files.
- A LISP function errors → report the exact command-line text verbatim. Do not silently skip the phase.
- A dialog you don't recognize appears → screenshot it and ask, rather than guessing.
- Never accept a "close enough" coordinate. If data seems missing, say so explicitly rather than inventing it.

---

## 9. PROJECT FACTS AND DISCLAIMER

### 9.1 Design basis

96 MW IT load · eight 12 MW halls · conventional air-cooled 20 kW racks · 4,800 racks · one-story building · preliminary N+1 block redundancy · PUE 1.25 → 120 MW facility demand → ~150 MVA planning placeholder.

### 9.2 Reserves

42 generator positions at 3 MW (40 duty + 2 redundant) · 32 heat-rejection cells at 1,000 tons (30 duty + 2 redundant) · six 2.5 MW UPS modules per hall block (5 duty + 1 redundant) · 26 CRAH positions per hall (24 duty + 2 standby at 65,000 cfm).

### 9.3 Required disclaimer — place on every sheet

> CONCEPTUAL DESIGN BASIS — NOT FOR CONSTRUCTION, PERMIT, OR BIDDING. This drawing is a dimensionally coordinated planning study. It requires validation by a Dallas-licensed architect and licensed civil, structural, mechanical, electrical, plumbing, fire-protection, security, telecom, and geotechnical engineers against actual survey, zoning, easements, floodplain, utilities, geotechnical data, equipment selections, and adopted codes. Fire ratings, egress counts, accessibility compliance, and utility capacity shown are placeholders.

---

## 10. START HERE

1. Confirm AutoCAD is open and it is the **full version, not LT** (check that `APPLOAD` exists).
2. Create `~/Documents/DallasCAD/{lisp,dwg,pdf}`.
3. Write `lisp/00-layers.lsp` from Section 2.1, `APPLOAD` it, run `DALLAYERS`.
4. Write `lisp/01-core.lsp` from Section 4 (all core routines), `APPLOAD` it.
5. Begin Phase 2 and proceed in order, verifying each acceptance check.
6. Report progress after each phase with a screenshot.

**Remember: the difference between "just boxes" and a real drawing is walls with poché, lineweights, furniture, door swings, and hatches. Never skip them to save time.**
