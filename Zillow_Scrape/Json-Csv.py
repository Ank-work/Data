import pandas as pd
import json
import os
from datetime import datetime, timedelta

# Define data folders
data_folders = {
    "rent": "data/rent",

}

# Function to convert timestamp (milliseconds since epoch) to human-readable date
def convert_timestamp(timestamp):
    if isinstance(timestamp, (int, float)) and timestamp > 0:
        return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return "N/A"

# Function to calculate estimated listing date from days on Zillow
def calculate_listing_date(days_on_zillow):
    if isinstance(days_on_zillow, (int, float)) and days_on_zillow > 0:
        return (datetime.utcnow() - timedelta(days=days_on_zillow)).strftime('%Y-%m-%d')
    return "N/A"

# Loop through each category folder
for category, folder_path in data_folders.items():
    all_data = []  # Store data from all JSON files in the category

    if not os.path.exists(folder_path):  # Skip if folder does not exist
        print(f"WARNING: Folder '{folder_path}' not found, skipping...")
        continue

    # Loop through JSON files in the category folder
    for json_file in os.listdir(folder_path):
        if not json_file.endswith(".json"):
            continue

        json_path = os.path.join(folder_path, json_file)
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Determine where the list of properties lives
            if isinstance(data, list):
                properties = data
            elif isinstance(data, dict):
                if "listResults" in data:
                    properties = data["listResults"]
                elif "mapResults" in data:
                    properties = data["mapResults"]
                else:
                    # fallback: first list value in the dict
                    props = next((v for v in data.values() if isinstance(v, list)), [])
                    properties = props
            else:
                properties = []

            if not properties:
                print(f"WARNING: No property array found in {json_file}, skipping...")
                continue

            # Normalize JSON data into a DataFrame
            df = pd.json_normalize(properties, sep='_')

            # Convert timestamp fields
            for col in df.columns:
                if 'date' in col.lower() or 'timeonzillow' in col.lower():
                    df[col] = df[col].apply(convert_timestamp)

            # Calculate listing date for rent and sale properties
            days_col = 'hdpData_homeInfo_daysOnZillow'
            if category in ["rent", "sale"] and days_col in df.columns:
                df['Estimated_Listing_Date'] = df[days_col].apply(calculate_listing_date)

            all_data.append(df)
            print(f"Processed {json_file}: {len(df)} records")

        except Exception as e:
            print(f"ERROR processing {json_file}: {e}")

    # Merge all data into a single CSV file per category
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        os.makedirs("data", exist_ok=True)
        csv_filename = f"data/{category}.csv"
        final_df.to_csv(csv_filename, index=False, encoding='utf-8')
        print(f"CSV created: {csv_filename} ({len(final_df)} total rows)")
    else:
        print(f"WARNING: No valid data to save for {category}. CSV not created.")
