import pyzill
import csv
import os
import time
import random

# LA County bounding box from user-provided coordinates
# Points:
# Northwest: 35.00, -119.0000
# Northeast: 35.00, -117.55000
# Southeast: 33.6700, -117.55000
# Southwest: 33.6700, -119.0000
BOUNDING_BOX = {
    "ne_lat": 35.00,      # Northern boundary (max latitude)
    "ne_long": -117.5500, # Eastern boundary (min longitude is more negative)
    "sw_lat": 33.6700,    # Southern boundary (min latitude)
    "sw_long": -119.0000, # Western boundary (max longitude is more negative)
}

THRESHOLD = 400
ZOOM_VALUE = 10
PROXY = pyzill.parse_proxy("eu.decodo.com", "10000", "spxa9xe020", "aklkVUlqzP69~1t6kJ")
DATA_TYPES = ["rent", "sale", "sold"]
SEARCH_FUNCS = {
    "rent": pyzill.for_rent,
    "sale": pyzill.for_sale,
    "sold": pyzill.sold,
}
DATA_FOLDER = "data"

os.makedirs(DATA_FOLDER, exist_ok=True)


def random_delay():
    delay = random.randint(4,6)
    print(f"Waiting {delay} seconds...")
    time.sleep(delay)


def _extract_map_results(raw):
    if isinstance(raw, dict) and "mapResults" in raw:
        return raw["mapResults"]
    elif isinstance(raw, list):
        return raw
    else:
        return []


def scrape_cell(func, search_value, ne_lat, ne_long, sw_lat, sw_long):
    random_delay()
    try:
        if func == pyzill.for_rent:
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
                is_entire_place=None,
                is_room=False
            )
        else:
            raw = func(
                pagination=1,
                search_value=search_value,
                min_beds=None, max_beds=None,
                min_bathrooms=None, max_bathrooms=None,
                min_price=None, max_price=None,
                ne_lat=ne_lat, ne_long=ne_long,
                sw_lat=sw_lat, sw_long=sw_long,
                zoom_value=ZOOM_VALUE,
                proxy_url=PROXY
            )
        return _extract_map_results(raw)
    except Exception as e:
        print(f"Warning: Error scraping cell {ne_lat, ne_long, sw_lat, sw_long}: {e}")
        return []


def recursive_scrape(func, search_value, ne_lat, ne_long, sw_lat, sw_long, threshold):
    items = scrape_cell(func, search_value, ne_lat, ne_long, sw_lat, sw_long)
    if len(items) > threshold:
        print(f"Threshold hit ({len(items)}) for box {ne_lat, ne_long, sw_lat, sw_long} → splitting…")
        mid_lat = (ne_lat + sw_lat) / 2
        mid_long = (ne_long + sw_long) / 2
        quadrants = [
            (mid_lat, ne_long, sw_lat, mid_long),  # SE
            (ne_lat, ne_long, mid_lat, mid_long),  # NE
            (mid_lat, mid_long, sw_lat, sw_long),  # SW
            (ne_lat, mid_long, mid_lat, sw_long),  # NW
        ]
        all_items = []
        for q_ne_lat, q_ne_long, q_sw_lat, q_sw_long in quadrants:
            all_items.extend(
                recursive_scrape(func, search_value, q_ne_lat, q_ne_long, q_sw_lat, q_sw_long, threshold)
            )
        return all_items
    return items


def deduplicate(records):
    seen = set()
    unique = []
    for rec in records:
        zpid = rec.get("zpid")
        if not zpid:
            continue
        if zpid not in seen:
            seen.add(zpid)
            unique.append(rec)
    return unique


def save_to_csv(data_type, records):
    if not records:
        print(f"No records to save for {data_type}")
        return
    keys = set()
    for rec in records:
        keys.update(rec.keys())
    keys = sorted(keys)
    out_path = os.path.join(DATA_FOLDER, f"zillow_{data_type}_la_county.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for rec in records:
            writer.writerow(rec)
    print(f"Saved {len(records)} unique {data_type} records to {out_path}")


def main():
    for dtype in DATA_TYPES:
        print(f"\nScraping {dtype.upper()}...")
        func = SEARCH_FUNCS[dtype]
        print(f"Starting with bounding box: {BOUNDING_BOX}")
        records = recursive_scrape(
            func,
            "Los Angeles County, CA",
            BOUNDING_BOX["ne_lat"], BOUNDING_BOX["ne_long"],
            BOUNDING_BOX["sw_lat"], BOUNDING_BOX["sw_long"],
            THRESHOLD
        )
        unique_records = deduplicate(records)
        save_to_csv(dtype, unique_records)

if __name__ == "__main__":
    main() 