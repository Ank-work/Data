# Dallas 101-Acre Data Center — AutoCAD Web Phased Build Plan (Code-Driven)

**Goal:** a client-presentable CAD set at the fidelity of the reference A1.0 sheet — labeled rooms, parking stalls, rack plan, hot/cold aisles, CRAH, legend, keynotes, door schedule, dimensions, title block.

**Geometry source of truth:** `/Users/ankurkulkarni/Documents/Codex/2026-08-12/can/outputs/dallas-data-center-cad-basis.md` (CAD Basis v0.1)

**Companion docs:** [`a10-detail-fidelity-target.md`](./a10-detail-fidelity-target.md) (what "detailed" means) · [`onshape-featurescript-cad-drawings.md`](./onshape-featurescript-cad-drawings.md) (why not Onshape)

---

## 0. Read this before Phase 1 — how "code" works with AutoCAD Web

AutoCAD **Web** (`web.autocad.com`) has **no AutoLISP, no scripts, no VBA, no .NET, no CUI macros**. Those are desktop-only. So "build it via code" cannot mean "run code inside AutoCAD Web."

**The working method:**

```
Python + ezdxf  →  dallas-*.dxf  →  upload to AutoCAD Web  →  annotate/plot in browser
   (generates all geometry, layers, blocks, text)     (final polish + PDF)
```

| Task | Where |
|---|---|
| Property, roads, parking stalls, building, grid, rooms, 4,800 racks, CRAH, tags | **Code (ezdxf)** — exact, repeatable, zero mouse errors |
| Layers, colors, linetypes, text styles, blocks | **Code** |
| Room labels, rack tags, keynote text | **Code** (as MTEXT) |
| Dimensions | **Code** for major strings; touch-up in web |
| Legend, door schedule table, title block | **Code** (as line/text) or **paste in web** |
| Viewports, scale, layout sheets, plot to PDF | **AutoCAD Web** (manual, ~20 min/sheet) |

**Why this beats hand-drafting:** the basis has ~4,800 cabinets, 180 stalls, 40+ rooms. Drawing that by hand is weeks. Generating it is minutes, and every coordinate matches the basis exactly.

**If you have desktop AutoCAD too:** same DXF opens there, and you additionally get SCRIPT/LISP. Web-only is fine for this plan.

### 0.1 Browser performance guardrail

4,800 cabinet blocks + full site in one web drawing will be sluggish. **Split the model:**

| File | Contains |
|---|---|
| `dallas-site.dxf` | Property, reserves, roads, fire loop, parking, building footprint |
| `dallas-building.dxf` | Shell, grid, all rooms, doors, tags — halls shown as hatched zones |
| `dallas-rack-hall.dxf` | **One** hall at full rack detail (600 cabinets) + CRAH + aisles |
| `dallas-campus-racks.dxf` | Optional: all 8 halls racked, for the "wow" plot only |

Client sheets reference these separately. Do **not** put 4,800 racks on the A1.0.

---

## 1. Phase 0 — Environment setup

**Build:** working toolchain. No drawing yet.

### Steps

```bash
mkdir -p ~/Arcomurray/cad/dallas && cd ~/Arcomurray/cad/dallas
python3 -m venv .venv && source .venv/bin/activate
pip install ezdxf
```

Create `basis.py` — every number from the basis, one place:

```python
# basis.py — Dallas CAD Basis v0.1 constants (feet, site coords)
SITE_SIDE = 2097.513
BLDG_ORIGIN = (548.756, 688.756)      # building-local (0,0) in site coords
BLDG_W, BLDG_D = 1000.0, 720.0
PARK_ORIGIN = (892.756, 276.756)      # parking-local P
PARK_SIDE = 312.0

def b2s(x, y):
    """building-local -> site coords"""
    return (BLDG_ORIGIN[0] + x, BLDG_ORIGIN[1] + y)

def p2s(x, y):
    """parking-local -> site coords"""
    return (PARK_ORIGIN[0] + x, PARK_ORIGIN[1] + y)
```

**Acceptance:** `python -c "import ezdxf; print(ezdxf.__version__)"` works, and you can sign in at `web.autocad.com`.

**Time:** 15 min.

---

## 2. Phase 1 — Layer standard, styles, template

**Build:** the DXF skeleton every later phase writes into. Get this right or the drawing will never look professional — lineweight and color hierarchy is 80% of why the reference sheet reads well.

### Layer table (AIA/NCS-flavored)

| Layer | Color | Lineweight | Contents |
|---|---|---|---|
| `00-SITE-CTRL` | 8 grey | 0.13 | Property square, control points |
| `01-CIVIL-RSRV` | 30 orange | 0.13 dashed | 100 ft reserve, stormwater |
| `02-ROADS` | 8 | 0.18 | Entrances, service drive, fire loop |
| `02-PARK-STALL` | 253 | 0.13 | Stall lines |
| `02-PARK-ADA` | 150 blue | 0.20 | Accessible stalls + ISA |
| `03-WALL-EXT` | 7 white | **0.50** | Exterior 12" wall |
| `03-WALL-FIRE` | 1 red | **0.50** | Rated hall/fire barrier |
| `03-WALL-INT` | 7 | 0.25 | 6" partitions |
| `04-GRID` | 4 cyan | 0.09 center | Grid lines + bubbles |
| `05-HALL` | 8 | 0.25 | Hall boundaries |
| `06-ROOM-TAG` | 7 | text | Room names/numbers |
| `07-DOOR` | 2 yellow | 0.20 | Leaves + swings |
| `08-EQPM-RACK` | 8 | 0.13 | Cabinets |
| `08-EQPM-CRAH` | 3 green | 0.20 | Cooling modules |
| `08-EQPM-ELEC` | 6 magenta | 0.20 | UPS/battery/switchgear |
| `09-HVAC-SUP` | 4 cyan | 0.20 | Supply arrows |
| `09-HVAC-RET` | 1 red | 0.20 | Return arrows |
| `10-ELEC-A` | 2 | 0.20 dashed | A feed |
| `10-ELEC-B` | 6 | 0.20 dashed | B feed |
| `11-LIFE-EGRESS` | 3 | 0.25 dashed | Exit paths |
| `12-DIM` | 7 | 0.09 | Dimensions |
| `13-ANNO-LEGEND` | 7 | 0.13 | Legend, keynotes, schedule |
| `14-TBLK` | 7 | 0.25 | Title block |

### Code

```python
# phase1_template.py
import ezdxf
from ezdxf.enums import TextEntityAlignment

LAYERS = [
    ("00-SITE-CTRL", 8, "CONTINUOUS"), ("01-CIVIL-RSRV", 30, "DASHED"),
    ("02-ROADS", 8, "CONTINUOUS"), ("02-PARK-STALL", 253, "CONTINUOUS"),
    ("02-PARK-ADA", 150, "CONTINUOUS"), ("03-WALL-EXT", 7, "CONTINUOUS"),
    ("03-WALL-FIRE", 1, "CONTINUOUS"), ("03-WALL-INT", 7, "CONTINUOUS"),
    ("04-GRID", 4, "CENTER"), ("05-HALL", 8, "CONTINUOUS"),
    ("06-ROOM-TAG", 7, "CONTINUOUS"), ("07-DOOR", 2, "CONTINUOUS"),
    ("08-EQPM-RACK", 8, "CONTINUOUS"), ("08-EQPM-CRAH", 3, "CONTINUOUS"),
    ("08-EQPM-ELEC", 6, "CONTINUOUS"), ("09-HVAC-SUP", 4, "CONTINUOUS"),
    ("09-HVAC-RET", 1, "CONTINUOUS"), ("10-ELEC-A", 2, "DASHED"),
    ("10-ELEC-B", 6, "DASHED"), ("11-LIFE-EGRESS", 3, "DASHED"),
    ("12-DIM", 7, "CONTINUOUS"), ("13-ANNO-LEGEND", 7, "CONTINUOUS"),
    ("14-TBLK", 7, "CONTINUOUS"),
]

def new_doc():
    doc = ezdxf.new("R2018", setup=True)   # setup=True loads linetypes + dimstyles
    doc.header["$INSUNITS"] = 2            # feet-ish; we work in decimal feet
    doc.header["$LUNITS"] = 2
    for name, color, lt in LAYERS:
        doc.layers.add(name, color=color, linetype=lt)
    if "ROMANS" not in doc.styles:
        doc.styles.add("ROMANS", font="romans.shx")
    return doc

def save(doc, path):
    doc.saveas(path)
    print("wrote", path)
```

**Acceptance:** open the empty DXF in AutoCAD Web, LAYER palette shows all 23 layers with correct colors.

**Time:** 45 min.

---

## 3. Phase 2 — Site control and civil reserves

**Build:** property square, 100 ft planning reserve, stormwater reserves, three utility yards.

**Basis:** §4 (boundary), §15 (yards), §16 (stormwater).

```python
# phase2_site.py
from basis import SITE_SIDE

def rect(msp, x0, y0, x1, y1, layer):
    return msp.add_lwpolyline(
        [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
        close=True, dxfattribs={"layer": layer})

def build_site(msp):
    rect(msp, 0, 0, SITE_SIDE, SITE_SIDE, "00-SITE-CTRL")          # property
    rect(msp, 100, 100, SITE_SIDE-100, SITE_SIDE-100, "01-CIVIL-RSRV")  # reserve
    # Utility yards (basis §15)
    rect(msp, 1650, 830, 1990, 1230, "01-CIVIL-RSRV")   # substation 340x400
    rect(msp, 600, 1510, 1498, 1810, "01-CIVIL-RSRV")   # generator  898x300
    rect(msp, 600, 1810, 1498, 1990, "01-CIVIL-RSRV")   # heat rejection 898x180
    # Stormwater (basis §16)
    rect(msp, 100, 700, 450, 2000, "01-CIVIL-RSRV")
    rect(msp, 100, 100, 300, 575, "01-CIVIL-RSRV")
    for x, y, t in [(1820, 1030, "SUBSTATION YARD\n340'x400'"),
                    (1049, 1660, "GENERATOR YARD\n898'x300' (42 POS @ 3MW)"),
                    (1049, 1900, "HEAT REJECTION YARD\n898'x180' (32 CELLS)"),
                    (275, 1350, "STORMWATER RESERVE")]:
        msp.add_mtext(t, dxfattribs={"layer": "06-ROOM-TAG", "char_height": 24}
                      ).set_location((x, y), attachment_point=5)
```

**Acceptance:** property side measures 2,097.513 ft; yards do not overlap; area label reads 101.000 acres.

**Time:** 1 hr.

---

## 4. Phase 3 — Roads, fire loop, entries

**Build:** public entry drive, service entrance and spine, connectors, loading apron, 26 ft fire-access loop.

**Basis:** §6, §7.3, §7.4.

```python
def build_roads(msp):
    # Fire loop: 26 ft ring between inner and outer rectangles (basis §6)
    rect(msp, 533.756, 673.756, 1563.756, 1423.756, "02-ROADS")   # inner edge
    rect(msp, 507.756, 647.756, 1589.756, 1449.756, "02-ROADS")   # outer edge
    # Public entry drive 30 ft (basis §7.3)
    rect(msp, 1033.756, 0, 1063.756, 276.756, "02-ROADS")
    # Pedestrian walk 12 ft on axis X=1048.756
    rect(msp, 1042.756, 588.756, 1054.756, 688.756, "02-ROADS")
    # Service drive 40 ft + spine (basis §7.4)
    rect(msp, 1850, 0, 1890, 790, "02-ROADS")
    rect(msp, 1589.756, 600, 1890, 640, "02-ROADS")
    rect(msp, 1590, 600, 1630, 1510, "02-ROADS")
    rect(msp, 1498, 1510, 1630, 1550, "02-ROADS")
    rect(msp, 1630, 900, 1650, 940, "02-ROADS")
    rect(msp, 1630, 1100, 1650, 1140, "02-ROADS")
    # Loading apron
    rect(msp, 1198.756, 600, 1398.756, 688.756, "02-ROADS")
```

Add text: `VEHICLE ENTRANCE — ONE WAY IN`, `SERVICE / TRUCK ENTRANCE`, `26' FIRE APPARATUS LOOP (TYP.)`.

**Acceptance:** loop is a continuous 26 ft ring; public and service circulation never merge.

**Time:** 1.5 hr.

---

## 5. Phase 4 — Parking: 180 stalls with ADA

**Build:** the thing most obviously missing from your Onshape sheet. 150 standard + 24 standard + 6 accessible.

**Basis:** §7.1, §7.2.

```python
from basis import p2s, PARK_SIDE

ROWS = [(60,78), (102,120), (120,138), (162,180), (180,198), (222,240)]

def build_parking(msp):
    x0, y0 = p2s(0, 0); x1, y1 = p2s(PARK_SIDE, PARK_SIDE)
    rect(msp, x0, y0, x1, y1, "02-ROADS")

    # Rows 1-5: 30 bays of 9 ft across local X 21-291
    for (ylo, yhi) in ROWS[:5]:
        for j in range(31):                       # 31 lines = 30 bays
            lx = 21 + 9*j
            msp.add_line(p2s(lx, ylo), p2s(lx, yhi), dxfattribs={"layer": "02-PARK-STALL"})
        msp.add_line(p2s(21, ylo), p2s(291, ylo), dxfattribs={"layer": "02-PARK-STALL"})
        msp.add_line(p2s(21, yhi), p2s(291, yhi), dxfattribs={"layer": "02-PARK-STALL"})

    # Row 6: 12 std | ADA group | 12 std   (basis §7.2)
    ylo, yhi = ROWS[5]
    for start in (15, 189):
        for j in range(13):
            lx = start + 9*j
            msp.add_line(p2s(lx, ylo), p2s(lx, yhi), dxfattribs={"layer": "02-PARK-STALL"})
    ada = [(123,134,"VAN"), (134,139,"AISLE"), (139,147,"ADA"), (147,155,"ADA"),
           (155,160,"AISLE"), (160,168,"ADA"), (168,176,"ADA"),
           (176,181,"AISLE"), (181,189,"ADA")]
    for (a, b, kind) in ada:
        lay = "02-PARK-ADA" if kind != "AISLE" else "02-PARK-STALL"
        p0 = p2s(a, ylo); p1 = p2s(b, yhi)
        rect(msp, p0[0], p0[1], p1[0], p1[1], lay)
        if kind in ("ADA", "VAN"):
            cx, cy = p2s((a+b)/2, (ylo+yhi)/2)
            msp.add_text(kind, height=3,
                         dxfattribs={"layer": "02-PARK-ADA"}
                         ).set_placement((cx, cy), align=TextEntityAlignment.MIDDLE_CENTER)
```

Add drive-aisle direction arrows (local Y 78–102, 138–162, 198–222), drop-off callout at local Y 252–276, and a `180 SPACES (174 STD + 6 ACCESSIBLE)` note.

**Acceptance:** count stalls = 180. ADA group totals 66 ft. Van space is 11 ft.

**Time:** 2 hr.

---

## 6. Phase 5 — Building shell and planning grid

**Build:** 1,000 × 720 outside face, 12" wall offset inward, grid lines + bubbles.

**Basis:** §5, §8.

```python
from basis import b2s, BLDG_W, BLDG_D

GRID_X = [0,120,295,315,490,510,685,705,880,1000]
GRID_Y = [0,110,350,370,610,720]

def build_shell(msp):
    o = b2s(0,0); e = b2s(BLDG_W, BLDG_D)
    rect(msp, o[0], o[1], e[0], e[1], "03-WALL-EXT")           # outside face
    i0 = b2s(1,1); i1 = b2s(BLDG_W-1, BLDG_D-1)
    rect(msp, i0[0], i0[1], i1[0], i1[1], "03-WALL-EXT")       # 12" inner face

def build_grid(msp):
    for n, gx in enumerate(GRID_X, start=1):
        a = b2s(gx, -60); b = b2s(gx, BLDG_D+60)
        msp.add_line(a, b, dxfattribs={"layer": "04-GRID"})
        msp.add_circle(b, 12, dxfattribs={"layer": "04-GRID"})
        msp.add_text(str(n), height=10, dxfattribs={"layer": "04-GRID"}
                     ).set_placement(b, align=TextEntityAlignment.MIDDLE_CENTER)
    for n, gy in enumerate(GRID_Y):
        letter = "ABCDEF"[n]
        a = b2s(-60, gy); b = b2s(BLDG_W+60, gy)
        msp.add_line(a, b, dxfattribs={"layer": "04-GRID"})
        msp.add_circle(a, 12, dxfattribs={"layer": "04-GRID"})
        msp.add_text(letter, height=10, dxfattribs={"layer": "04-GRID"}
                     ).set_placement(a, align=TextEntityAlignment.MIDDLE_CENTER)
```

**Acceptance:** grid bubbles 1–10 and A–F ring the plan like the reference sheet.

**Time:** 1.5 hr.

---

## 7. Phase 6 — Halls, spines, cross-corridor

**Build:** 8 hall rectangles, 3 north-south spines, east-west secure corridor.

**Basis:** §8, §9.

```python
HALLS = {
 "H1":(120,295,110,350), "H2":(315,490,110,350), "H3":(510,685,110,350), "H4":(705,880,110,350),
 "H5":(120,295,370,610), "H6":(315,490,370,610), "H7":(510,685,370,610), "H8":(705,880,370,610)}

def build_halls(msp):
    for name,(x0,x1,y0,y1) in HALLS.items():
        a = b2s(x0,y0); b = b2s(x1,y1)
        rect(msp, a[0], a[1], b[0], b[1], "03-WALL-FIRE")
        c = b2s((x0+x1)/2, (y0+y1)/2)
        msp.add_mtext(f"DATA HALL {name}\n175' x 240' | 12 MW | 600 RACKS",
                      dxfattribs={"layer":"06-ROOM-TAG","char_height":14}
                      ).set_location(c, attachment_point=5)
    for (sx0,sx1) in [(295,315),(490,510),(685,705)]:
        a=b2s(sx0,110); b=b2s(sx1,610); rect(msp,a[0],a[1],b[0],b[1],"03-WALL-INT")
    a=b2s(120,350); b=b2s(880,370); rect(msp,a[0],a[1],b[0],b[1],"03-WALL-INT")
```

**Acceptance:** 336,000 ft² halls + 44,000 ft² corridors = 380,000 ft² central block.

**Time:** 1 hr.

---

## 8. Phase 7 — South band: admin, lobby, security, logistics, telecom

**Build:** the rooms your client actually looks for. This is the single biggest "not bland" win.

**Basis:** §11.1–§11.4. Coordinates are building-local.

```python
SOUTH_ROOMS = [
 # (name, number, x0,y0,x1,y1)
 ("BREAK ROOM","109",0,0,80,50), ("MEN'S RESTROOM","107",80,0,130,50),
 ("WOMEN'S RESTROOM","108",130,0,180,50), ("LOCKERS / WELLNESS","111",180,0,240,50),
 ("TRAINING ROOM","112",240,0,350,50), ("ADMIN CORRIDOR","C01",0,50,350,62),
 ("OFFICE","101",0,62,30,110), ("OFFICE","102",30,62,60,110),
 ("OFFICE","103",60,62,90,110), ("OFFICE","104",90,62,120,110),
 ("CONFERENCE","105",120,62,200,110), ("OPEN OFFICE","106",200,62,300,110),
 ("IT CLOSET","113",300,62,350,86), ("OFFICE STORAGE","114",300,86,350,110),
 ("NOC","115",350,0,410,70), ("RECEPTION SUPPORT","116",410,0,455,18),
 ("VESTIBULE","100",455,0,545,18), ("VISITOR SCREENING","117",545,0,590,18),
 ("LOBBY / RECEPTION","110",410,18,590,70),
 ("FIRE COMMAND","118",590,0,650,70), ("SECURITY OPERATIONS","120",350,70,430,110),
 ("W CONTROLLED PASSAGE","121",430,70,455,110),
 ("MANTRAP STAGE 1","122",455,70,545,88), ("MANTRAP STAGE 2","123",455,88,545,110),
 ("E CONTROLLED PASSAGE","124",545,70,570,110), ("BADGE / ADMIN SUPPORT","125",570,70,650,110),
 ("RECEIVING / STAGING","130",650,0,760,70), ("SECURE STORAGE","131",760,0,850,70),
 ("SPARES LABORATORY","132",650,70,730,110), ("JANITOR","133",730,70,755,110),
 ("WASTE / PACKAGING","134",755,70,800,110), ("SERVICE PASSAGE","135",800,70,850,110),
 ("CARRIER ENTRANCE","140",850,0,925,55), ("MEET-ME / NETWORK","141",850,55,925,110),
 ("MAIN ELECTRICAL SERVICE","142",925,0,1000,110),
]

def build_rooms(msp, rooms, layer="03-WALL-INT"):
    for (name, num, x0,y0,x1,y1) in rooms:
        a=b2s(x0,y0); b=b2s(x1,y1)
        rect(msp, a[0],a[1],b[0],b[1], layer)
        c=b2s((x0+x1)/2,(y0+y1)/2)
        msp.add_mtext(f"{name}\\P{num}",
                      dxfattribs={"layer":"06-ROOM-TAG","char_height":6}
                      ).set_location(c, attachment_point=5)
```

**Acceptance:** you can find LOBBY, OFFICE 101–104, BREAK ROOM, restrooms, MANTRAP by reading the plan.

**Time:** 2 hr.

---

## 9. Phase 8 — West, east, north technical bands

**Build:** cooling/pump rooms, UPS + battery blocks, hall electrical modules, central switchgear.

**Basis:** §12, §13.

```python
TECH_ROOMS = [
 ("COOLING / PUMP RM A (S)","201",0,110,120,230), ("COOLING / PUMP RM B (S)","202",0,230,120,350),
 ("COOLING / PUMP RM A (N)","203",0,370,120,490), ("COOLING / PUMP RM B (N)","204",0,490,120,610),
 ("UPS / SWITCHGEAR A-S","210",880,110,940,230), ("BATTERY / ESS A-S","211",940,110,1000,230),
 ("UPS / SWITCHGEAR B-S","212",880,230,940,350), ("BATTERY / ESS B-S","213",940,230,1000,350),
 ("UPS / SWITCHGEAR A-N","214",880,370,940,490), ("BATTERY / ESS A-N","215",940,370,1000,490),
 ("UPS / SWITCHGEAR B-N","216",880,490,940,610), ("BATTERY / ESS B-N","217",940,490,1000,610),
 ("WATER TREATMENT / PUMP","220",0,610,120,720),
 ("HALL ELECTRICAL E1","221",120,610,295,720), ("HALL ELECTRICAL E2","222",315,610,490,720),
 ("HALL ELECTRICAL E3","223",510,610,685,720), ("HALL ELECTRICAL E4","224",705,610,880,720),
 ("CENTRAL SWITCHGEAR / CONTROLS","225",880,610,1000,720),
]
# build_rooms(msp, TECH_ROOMS, layer="03-WALL-FIRE")
```

Battery rooms get `03-WALL-FIRE` separation per basis §12.2 note.

**Acceptance:** every band room labeled; UPS/battery split at X 940 is visible.

**Time:** 1 hr.

---

## 10. Phase 9 — Rack module (the money shot)

**Build:** one cabinet block → one 60-cabinet row → 10 rows → one 600-rack hall → replicate.

**Basis:** §10.1–§10.3.

```python
ROW_X = [(45.5,49.5),(53.5,57.5),(63.5,67.5),(71.5,75.5),(81.5,85.5),
         (89.5,93.5),(99.5,103.5),(107.5,111.5),(117.5,121.5),(125.5,129.5)]

def define_rack_block(doc):
    blk = doc.blocks.new(name="RACK_4x2")
    blk.add_lwpolyline([(0,0),(4,0),(4,2),(0,2)], close=True,
                       dxfattribs={"layer":"08-EQPM-RACK"})
    return blk

def build_hall_racks(msp, hall_x0, hall_y0, hall_no):
    """hall_x0/y0 = hall SW corner in BUILDING-local coords"""
    for r,(xa,xb) in enumerate(ROW_X, start=1):
        for j in range(60):
            hx = hall_x0 + xa
            hy = hall_y0 + 60 + 2*j
            msp.add_blockref("RACK_4x2", b2s(hx, hy),
                             dxfattribs={"layer":"08-EQPM-RACK"})
    # aisle labels (basis §10.2)
    cold = [(39.5,45.5),(57.5,63.5),(75.5,81.5),(93.5,99.5),(111.5,117.5),(129.5,135.5)]
    hot  = [(49.5,53.5),(67.5,71.5),(85.5,89.5),(103.5,107.5),(121.5,125.5)]
    for (a,b) in cold:
        c = b2s(hall_x0+(a+b)/2, hall_y0+120)
        msp.add_text("COLD AISLE", height=3, dxfattribs={"layer":"09-HVAC-SUP"}
                     ).set_placement(c, align=TextEntityAlignment.MIDDLE_CENTER)
    for (a,b) in hot:
        c = b2s(hall_x0+(a+b)/2, hall_y0+120)
        msp.add_text("HOT AISLE", height=3, dxfattribs={"layer":"09-HVAC-RET"}
                     ).set_placement(c, align=TextEntityAlignment.MIDDLE_CENTER)

def build_crah(msp, hall_x0, hall_y0):
    """26 modules: 13 west at X 10-18, 13 east at X 157-165 (basis §10.4)"""
    for side, (xa, xb) in (("W",(10,18)), ("E",(157,165))):
        for k in range(13):
            ya, yb = 12 + 17*k, 24 + 17*k
            a = b2s(hall_x0+xa, hall_y0+ya); b = b2s(hall_x0+xb, hall_y0+yb)
            rect(msp, a[0],a[1],b[0],b[1], "08-EQPM-CRAH")
            c = b2s(hall_x0+(xa+xb)/2, hall_y0+(ya+yb)/2)
            msp.add_text(f"CRAH-{side}{k+1}", height=2.5,
                         dxfattribs={"layer":"08-EQPM-CRAH"}
                         ).set_placement(c, align=TextEntityAlignment.MIDDLE_CENTER)
```

**Rack tags** (`H3-R07-C42`): generate only on the **rack plan sheet**, not the A1.0 — 600 tags per hall is unreadable at plan scale. Tag row ends instead.

**Acceptance:** 600 blockrefs per hall; row X ranges match the basis table exactly; 4,800 total campus-wide.

**Time:** 2.5 hr.

---

## 11. Phase 10 — MEP + life-safety annotation

**Build:** the symbolic layer that makes the reference sheet look engineered.

| Item | Layer | How |
|---|---|---|
| Supply arrows CRAH → cold aisles | `09-HVAC-SUP` | Cyan arrow polylines, one per cold aisle |
| Return arrows hot aisle → plenum | `09-HVAC-RET` | Red arrows |
| Hot-aisle containment boundary | `05-HALL` | Dashed rectangle over each hot aisle |
| A feed / B feed routes | `10-ELEC-A/B` | Dashed polylines from east band + spine (basis §14) |
| Egress paths | `11-LIFE-EGRESS` | Dashed routes to two separated exits |
| Cable tray | `10-ELEC-A` | Long-dash overhead runs in spines |

```python
def arrow(msp, p0, p1, layer, head=3.0):
    msp.add_line(p0, p1, dxfattribs={"layer": layer})
    import math
    ang = math.atan2(p1[1]-p0[1], p1[0]-p0[0])
    for s in (+1,-1):
        a = ang + s*math.radians(150)
        msp.add_line(p1, (p1[0]+head*math.cos(a), p1[1]+head*math.sin(a)),
                     dxfattribs={"layer": layer})
```

**Acceptance:** every cold aisle has a supply arrow; every hot aisle has a return arrow and containment outline; A and B never share a route.

**Time:** 2 hr.

---

## 12. Phase 11 — Doors and door schedule

**Build:** door leaves + 90° swing arcs + marks, then the schedule table.

**Basis:** §9 (two 8 ft equipment doors per hall), §11.2 (6 ft vestibule pairs at X 500, 4 ft mantrap), §7.4 (two 14 ft loading doors at X 680–694, 710–724).

```python
def door(msp, hinge, width, start_deg, mark):
    import math
    msp.add_arc(center=hinge, radius=width, start_angle=start_deg,
                end_angle=start_deg+90, dxfattribs={"layer":"07-DOOR"})
    a = math.radians(start_deg)
    msp.add_line(hinge, (hinge[0]+width*math.cos(a), hinge[1]+width*math.sin(a)),
                 dxfattribs={"layer":"07-DOOR"})
    msp.add_text(mark, height=2.5, dxfattribs={"layer":"07-DOOR"}
                 ).set_placement((hinge[0]+2, hinge[1]+2))
```

Schedule rows (MARK / SIZE / TYPE / RATING) — build as text grid on `13-ANNO-LEGEND`, or type into an AutoCAD Web TABLE:

| MARK | SIZE | TYPE | RATING |
|---|---|---|---|
| 100A | 6'-0" × 7'-0" PAIR | H.M. | N.R. |
| 101–104 | 3'-0" × 7'-0" | H.M. | N.R. |
| 120A/B | 4'-0" × 7'-0" | H.M. | 1 HR |
| H1–H8 EQ | 8'-0" × 8'-0" | H.M. | 2 HR |
| LD1/LD2 | 14'-0" × 14'-0" | COIL | N.R. |

**Acceptance:** every door on the plan has a mark that exists in the schedule.

**Time:** 2 hr.

---

## 13. Phase 12 — Dimensions, legend, keynotes

**Build:** dimension strings + the three annotation blocks that frame the reference sheet.

```python
def dim_h(msp, x0, x1, y, offset=40):
    msp.add_linear_dim(base=(x0, y+offset), p1=(x0,y), p2=(x1,y),
                       dxfattribs={"layer":"12-DIM"}).render()
```

**Dimension:** property sides, building 1,000 × 720, grid bays, hall 175 × 240, rack pitch 8 ft typ., aisle widths 6 ft / 4 ft, parking module 18/24, road widths.

**Legend** (`13-ANNO-LEGEND`, top-right): rated wall types, door types, exit, extinguisher, temp sensor, supply/return, cable tray, PDU-A / PDU-B, column.

**Keynotes:**
1. 42U server rack, 4' × 2' planning footprint (typ.)
2. PDU-A — fed from UPS A path
3. PDU-B — fed from UPS B path
4. Hot-aisle containment door
5. No-step aisle — maintain clear
6. Fire-rated barrier — see plan
7. 26' fire apparatus loop
8. Two-stage interlocked mantrap

**Acceptance:** a reviewer can decode every line type from the legend alone.

**Time:** 2.5 hr.

---

## 14. Phase 13 — Sheets, title block, plotting (in AutoCAD Web)

**Build:** the actual client deliverable. This part is manual in the browser.

### Sheet list

| Sheet | Content | Suggested scale (ARCH D 24×36) |
|---|---|---|
| **C1.0** | Site plan: property, reserves, roads, fire loop, yards | 1" = 100'-0" |
| **C1.1** | Parking + arrival enlargement, 180 stalls, ADA | 1" = 20'-0" |
| **A1.0** | Overall floor plan, all rooms labeled, halls as zones | 1" = 40'-0" |
| **A1.1** | Admin / lobby / security enlargement | 1/8" = 1'-0" |
| **A2.0** | Typical data hall rack plan (H3), CRAH, aisles | 1/16" = 1'-0" |
| **M1.0** | Mechanical concept: airflow, CRAH schedule | 1" = 40'-0" |
| **E1.0** | Electrical concept: A/B, UPS, substation | 1" = 40'-0" |
| **LS1.0** | Life safety: egress, ratings, extinguishers | 1" = 40'-0" |
| **S1.0** | Schedules: door, room, equipment | NTS |

### Browser steps per sheet

1. Upload DXF → open in AutoCAD Web.
2. Switch to a **Layout** tab → set paper size ARCH D.
3. `MVIEW` a viewport → `ZOOM` → set viewport scale from the table.
4. Lock the viewport.
5. `LAYFRZ` per-viewport the layers not belonging to that discipline (e.g. freeze `08-EQPM-RACK` on C1.0).
6. Insert/draw the title block on `14-TBLK`: project name, Dallas TX, date, scale, drawn by, sheet number, revision table, north arrow, graphic scale.
7. `PLOT` → PDF.

**Acceptance:** all nine PDFs plot with correct scale, readable text, filled title blocks.

**Time:** 4–5 hr.

---

## 15. Phase 14 — QA audit before showing the client

Run the basis §17.16 audit plus a presentation check.

| Check | Pass condition |
|---|---|
| Geometry vs basis | Every coordinate traceable to a basis section |
| Duplicates | `OVERKILL` removes nothing significant |
| Open loops | All room polylines closed |
| Counts | 180 stalls · 600 racks/hall · 4,800 campus · 26 CRAH/hall · 8 halls |
| Areas | Halls 336,000 ft²; corridors 44,000 ft²; building 720,000 ft² |
| Labels | No unlabeled enclosed room |
| Legend | Every symbol used appears in legend |
| Doors | Every mark exists in schedule |
| Title blocks | No blank fields, no "TITLE" placeholder |
| Text size | Legible at plotted scale, not model scale |
| Disclaimer | Conceptual/not-for-construction note present |

**Mandatory client-facing note** (basis §1 and §18):

> CONCEPTUAL DESIGN BASIS — NOT FOR CONSTRUCTION, PERMIT, OR BIDDING. Requires validation by a Dallas-licensed architect and licensed civil, structural, MEP, fire-protection, security, telecom, and geotechnical engineers against actual survey, zoning, utilities, and adopted codes.

**Time:** 2 hr.

---

## 16. Master script assembly

```python
# build_all.py
from phase1_template import new_doc, save
import phase2_site, phase3_roads, phase4_parking, phase5_shell, \
       phase6_halls, phase7_rooms, phase9_racks

def site_file():
    doc = new_doc(); msp = doc.modelspace()
    phase2_site.build_site(msp); phase3_roads.build_roads(msp)
    phase4_parking.build_parking(msp); phase5_shell.build_shell(msp)
    save(doc, "dallas-site.dxf")

def building_file():
    doc = new_doc(); msp = doc.modelspace()
    phase5_shell.build_shell(msp); phase5_shell.build_grid(msp)
    phase6_halls.build_halls(msp)
    phase7_rooms.build_rooms(msp, phase7_rooms.SOUTH_ROOMS)
    phase7_rooms.build_rooms(msp, phase7_rooms.TECH_ROOMS, "03-WALL-FIRE")
    save(doc, "dallas-building.dxf")

def rack_hall_file():
    doc = new_doc(); msp = doc.modelspace()
    phase9_racks.define_rack_block(doc)
    phase9_racks.build_hall_racks(msp, 510, 110, 3)    # H3
    phase9_racks.build_crah(msp, 510, 110)
    save(doc, "dallas-rack-hall.dxf")

if __name__ == "__main__":
    site_file(); building_file(); rack_hall_file()
```

Rebuild is one command — change a basis number, regenerate, re-upload. That is the payoff of the code path.

---

## 17. Schedule summary

| Phase | Deliverable | Time |
|---|---|---|
| 0 | Toolchain + basis.py | 0.25 hr |
| 1 | Layers/styles template | 0.75 hr |
| 2 | Site + civil reserves | 1 hr |
| 3 | Roads + fire loop | 1.5 hr |
| 4 | Parking 180 stalls | 2 hr |
| 5 | Shell + grid | 1.5 hr |
| 6 | Halls + corridors | 1 hr |
| 7 | South band rooms | 2 hr |
| 8 | Technical bands | 1 hr |
| 9 | Racks + CRAH | 2.5 hr |
| 10 | MEP/life-safety annotation | 2 hr |
| 11 | Doors + schedule | 2 hr |
| 12 | Dims + legend + keynotes | 2.5 hr |
| 13 | Sheets + title + PDF | 4.5 hr |
| 14 | QA audit | 2 hr |
| | **Total** | **~26 hr** |

Roughly **3–4 focused working days** to a client-presentable nine-sheet conceptual set.

---

## 18. Where ChatGPT Chrome helps

| Use it for | Prompt shape |
|---|---|
| Writing/fixing a phase script | "Write ezdxf code that draws these rooms from this coordinate list: [paste basis §11.1]" |
| Debugging | "This ezdxf script throws [error]. Here is the function: [paste]" |
| Command lookup in AutoCAD Web | "In AutoCAD Web, how do I set viewport scale to 1"=40' and lock it?" |
| Schedule text | "Turn this door list into a CSV with MARK, SIZE, TYPE, RATING" |
| Keynote/legend wording | "Write 8 keynotes for a conceptual data center plan covering racks, PDU A/B, containment, rated walls" |

Never paste credentials or license keys.

---

## 19. Honest limits

- This is **conceptual massing at drafting fidelity**, not a sealed permit set.
- Fire ratings, egress counts, and ADA compliance in the basis are placeholders — a licensed architect must set them.
- ezdxf writes DXF; AutoCAD Web is fine with it, but very large drawings (4,800 blocks + site) will lag in browser. Keep the split from §0.1.
- Hatch patterns and complex dynamic blocks are limited in Web vs desktop; if you need heavy hatching, do it on desktop AutoCAD or accept simpler fills.
- No xrefs workflow in Web — plan on separate files per sheet group rather than an xref tree.

---

*Build plan generated against Dallas CAD Basis of Design v0.1.*
