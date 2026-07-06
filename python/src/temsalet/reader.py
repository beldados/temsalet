import os
import json
import random
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_proverbs_by_fidel(fidel_letter: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Loads proverbs starting with a specific Amharic letter with pagination.
    - skip: The starting index offset.
    - limit: The maximum number of proverbs to return.
    """
    file_path = os.path.join(DATA_DIR, f"{fidel_letter.strip()}.json")
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                # Apply slicing for pagination
                return data[skip : skip + limit]
            return []
        except json.JSONDecodeError:
            return []

def load_all_proverbs(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Combines and returns paginated proverbs from all JSON files."""
    if not os.path.exists(DATA_DIR):
        return []

    all_proverbs = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".json"):
            file_path = os.path.join(DATA_DIR, file)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_proverbs.extend(data)
                except json.JSONDecodeError:
                    continue

    # Apply slicing for pagination across the unified set
    return all_proverbs[skip : skip + limit]

def get_random_proverb() -> Optional[Dict[str, Any]]:
    """Returns a single random proverb from the complete collection."""
    # We load all proverbs here without slicing to ensure equal random selection
    proverbs = load_all_proverbs(skip=0, limit=100000)
    return random.choice(proverbs) if proverbs else None

def search_proverbs(query: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Searches across all proverbs, limiting the search results size."""
    query = query.lower()
    proverbs = load_all_proverbs(skip=0, limit=100000)
    results = []
    for p in proverbs:
        if (query in p.get("proverb_amharic", "").lower() or
            query in p.get("proverb_english", "").lower() or
            query in p.get("category", "").lower()):
            results.append(p)
            if len(results) >= limit:
                break
    return results
