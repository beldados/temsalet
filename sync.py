import os
import shutil
import json

# Define Paths
ROOT_DATA_DIR = "data"
PY_DATA_DIR = os.path.join("python", "src", "temsalet", "data")
JS_DATA_DIR = os.path.join("javascript", "data")
WEB_DATA_FILE = os.path.join("website", "proverbs.json")

def sync_data():
    if not os.path.exists(ROOT_DATA_DIR):
        print(f"Error: Master data directory '{ROOT_DATA_DIR}' not found.")
        return

    # 1. Sync to Python package data folder
    if os.path.exists(PY_DATA_DIR):
        shutil.rmtree(PY_DATA_DIR)
    shutil.copytree(ROOT_DATA_DIR, PY_DATA_DIR)
    print("✓ Synced data to Python package.")

    # 2. Sync to JavaScript package data folder
    if os.path.exists(JS_DATA_DIR):
        shutil.rmtree(JS_DATA_DIR)
    shutil.copytree(ROOT_DATA_DIR, JS_DATA_DIR)
    print("✓ Synced data to JavaScript package.")

    # 3. Consolidate separate JSON files into a single proverbs.json for the static website
    consolidated_proverbs = []
    for file in os.listdir(ROOT_DATA_DIR):
        if file.endswith(".json"):
            file_path = os.path.join(ROOT_DATA_DIR, file)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        consolidated_proverbs.extend(data)
                except json.JSONDecodeError:
                    print(f"Warning: Failed to parse {file}")
                    continue

    # Write consolidated data to the website folder
    os.makedirs(os.path.dirname(WEB_DATA_FILE), exist_ok=True)
    with open(WEB_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(consolidated_proverbs, f, ensure_ascii=False, indent=2)
    print("✓ Synced and consolidated data to website.")

if __name__ == "__main__":
    sync_data()
