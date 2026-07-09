import os
import json
import random
# This mapping groups all 7 variations into one "Base" letter
FIDEL_GROUPS = {
    # 'ሀ' family
    'ሀ': 'ሀ', 'ሁ': 'ሀ', 'ሂ': 'ሀ', 'ሃ': 'ሀ', 'ሄ': 'ሀ', 'ህ': 'ሀ', 'ሆ': 'ሀ',
    # 'ለ' family
    'ለ': 'ለ', 'ሉ': 'ለ', 'ሊ': 'ለ', 'ላ': 'ለ', 'ሌ': 'ለ', 'ል': 'ለ', 'ሎ': 'ለ',
    # 'ሐ' family
    'ሐ': 'ሐ', 'ሑ': 'ሐ', 'ሒ': 'ሐ', 'ሓ': 'ሐ', 'ሔ': 'ሐ', 'ሕ': 'ሐ', 'ሖ': 'ሐ',
    # 'መ' family
    'መ': 'መ', 'ሙ': 'መ', 'ሚ': 'መ', 'ማ': 'መ', 'ሜ': 'መ', 'ም': 'መ', 'ሞ': 'መ',
    # 'ሠ' family
    'ሠ': 'ሠ', 'ሡ': 'ሠ', 'ሢ': 'ሠ', 'ሣ': 'ሠ', 'ሤ': 'ሠ', 'ሥ': 'ሠ', 'ሦ': 'ሠ',
    # 'ረ' family
    'ረ': 'ረ', 'ሩ': 'ረ', 'ሪ': 'ረ', 'ራ': 'ረ', 'ሬ': 'ረ', 'ር': 'ረ', 'ሮ': 'ረ',
    # 'ሰ' family
    'ሰ': 'ሰ', 'ሱ': 'ሰ', 'ሲ': 'ሰ', 'ሳ': 'ሰ', 'ሴ': 'ሰ', 'ስ': 'ሰ', 'ሶ': 'ሰ',
    # 'ሸ' family
    'ሸ': 'ሸ', 'ሹ': 'ሸ', 'ሺ': 'ሸ', 'ሻ': 'ሸ', 'ሼ': 'ሸ', 'ሽ': 'ሸ', 'ሾ': 'ሸ',
}
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
    """Searches across all proverbs using the Fidel grouping logic."""
    query = query.lower()
    
    # If someone searches 'ም', we treat it as 'መ'
    base_query = FIDEL_GROUPS.get(query, query) 

    proverbs = load_all_proverbs(skip=0, limit=100000)
    results = []
    
    for p in proverbs:
        amharic_text = p.get("proverb_amharic", "")
        # Get the first letter of the proverb
        first_char = amharic_text[0] if amharic_text else ""
        # Convert that first letter to its "Base" family (e.g. 'ም' -> 'መ')
        base_first_char = FIDEL_GROUPS.get(first_char, first_char)

        # Logic: Match if the query is in the text 
        # OR if the first letter belongs to the family being searched
        if (query in amharic_text.lower() or 
            query in p.get("proverb_english", "").lower() or
            base_query == base_first_char):
            
            results.append(p)
            if len(results) >= limit:
                break
                
    return results