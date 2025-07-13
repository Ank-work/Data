import pyzill
import json
import os
import random
import time

# —————— Configuration ——————
PROXY       = pyzill.parse_proxy("gb.decodo.com", "30000", "spxa9xe020", "Nc4d2BqZz4wp8_Zclv")
ZOOM_VALUE  = 10
MAX_RESULTS = 500   # Zillow's hard cap per map query
DATA_FOLDERS = {"rent": "data/rent", "sale": "data/sale", "sold": "data/sold"}
SEARCH_FUNCS = {
    "rent": pyzill.for_rent,
    "sale": pyzill.for_sale,
    "sold": pyzill.sold,
}

# LA County bounding box coordinates - More precise coordinates
AREAS = [
    {
        "id":           "la_county",
        "search_value": "Los Angeles County, CA",
        "ne_lat":       34.8235,  # Northern boundary
        "ne_long":     -117.6441, # Eastern boundary  
        "sw_lat":       32.7967,  # Southern boundary
        "sw_long":    -118.9535,  # Western boundary
    },
]

# ensure output folders exist
for folder in DATA_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

def random_delay():
    delay = random.randint(2, 4)  # Reduced delay for faster scraping
    print(f"⏱ Waiting {delay}s…")
    time.sleep(delay)

def save_data(data_type, region_id, records):
    fn   = f"zillow_{data_type}_{region_id}.json"
    path = os.path.join(DATA_FOLDERS[data_type], fn)
    with open(path, "w") as f:
        json.dump(records, f, indent=2)
    print(f"✔ Saved {len(records)} unique {data_type} records to {path}")

def _extract_map_results(raw):
    if isinstance(raw, dict) and "mapResults" in raw:
        return raw["mapResults"]
    if isinstance(raw, list):
        return raw
    return []

def scrape_recursive(func, search_value, ne_lat, ne_long, sw_lat, sw_long, depth=0):
    """Recursive scraping with improved bounding box splitting"""
    if depth > 6:  # Prevent infinite recursion
        print(f"⚠️  Max depth reached for box {ne_lat,ne_long,sw_lat,sw_long}")
        return []
    
    random_delay()
    try:
        # More inclusive parameters for rental scraping
        raw = func(
            pagination=1,
            search_value=search_value,
            min_beds=None, max_beds=None,
            min_bathrooms=None, max_bathrooms=None,
            min_price=None, max_price=None,
            ne_lat=ne_lat, ne_long=ne_long,
            sw_lat=sw_lat, sw_long=sw_long,
            zoom_value=ZOOM_VALUE,
            proxy_url=PROXY,
            is_entire_place=None,  # Include both entire places and rooms
            is_room=None           # Include both rooms and entire places
        )
    except Exception as e:
        print(f"⚠️  Error fetching {ne_lat,ne_long,sw_lat,sw_long}: {e}")
        return []

    items = _extract_map_results(raw)
    print(f"📍 Box {depth}: Got {len(items)} results")

    if len(items) >= MAX_RESULTS:
        print(f"⚠️  Cap hit ({len(items)}) on box {ne_lat,ne_long,sw_lat,sw_long}, splitting…")
        mid_lat  = (ne_lat + sw_lat) / 2
        mid_long = (ne_long + sw_long) / 2
        
        # Create 4 quadrants
        quadrants = [
            ( mid_lat,  ne_long, sw_lat,  mid_long),  # SE
            ( ne_lat,   ne_long, mid_lat, mid_long),  # NE
            ( mid_lat,  mid_long, sw_lat, sw_long),   # SW
            ( ne_lat,   mid_long, mid_lat, sw_long),  # NW
        ]
        
        all_items = []
        for i, (q_ne_lat, q_ne_long, q_sw_lat, q_sw_long) in enumerate(quadrants):
            print(f"  📍 Scraping quadrant {i+1}/4...")
            quadrant_items = scrape_recursive(func, search_value,
                                           q_ne_lat, q_ne_long, q_sw_lat, q_sw_long, depth + 1)
            all_items.extend(quadrant_items)
        
        return all_items

    return items

if __name__ == "__main__":
    for area in AREAS:
        region_id   = area["id"]
        search_val  = area["search_value"]
        ne_lat, ne_long = area["ne_lat"], area["ne_long"]
        sw_lat, sw_long = area["sw_lat"], area["sw_long"]

        # Only scrape rental data
        dtype = "rent"
        func = SEARCH_FUNCS[dtype]
        
        print(f"\n📍 Scraping {dtype.upper()} for {region_id} (LA County)…")
        print(f"📍 Bounding box: NE({ne_lat}, {ne_long}) SW({sw_lat}, {sw_long})")
        
        raw_list = scrape_recursive(func, search_val, ne_lat, ne_long, sw_lat, sw_long)

        print(f"📍 Total raw results: {len(raw_list)}")

        # filter out bad records & dedupe
        seen, unique = set(), []
        missing_count = 0
        for idx, rec in enumerate(raw_list):
            z = rec.get("zpid")
            if z:
                if z not in seen:
                    seen.add(z)
                    unique.append(rec)
            else:
                # Assign a synthetic zpid and add region_id for context
                rec["zpid"] = f"missing_zpid_{region_id}_{missing_count}"
                rec["region_id"] = region_id
                unique.append(rec)
                missing_count += 1
        if missing_count > 0:
            print(f"⚠️  {missing_count} records missing zpid; assigned synthetic IDs and included them.")

        print(f"📍 After deduplication: {len(unique)} records")

        # Remove property type filtering to capture ALL listings
        # ALLOWED_TYPES = {"SINGLE_FAMILY", "APARTMENT", "CONDO", "CO_OP", "TOWNHOUSE"}
        # filtered = [rec for rec in unique if rec.get("propertyType") in ALLOWED_TYPES]
        # print(f"✔ Filtered to {len(filtered)} records with allowed home types.")
        
        # Use all records without filtering
        filtered = unique
        print(f"✔ Using all {len(filtered)} records (no property type filtering)")

        save_data(dtype, region_id, filtered)
