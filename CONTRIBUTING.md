# Contributing to Temsalet

Thank you for your interest in contributing to Temsalet! We welcome contributions to both our Python codebase and our collection of Ethiopian proverbs.

## How to Contribute Proverbs (No Coding Required)

Our proverbs are stored inside the `src/temsalet/data/` directory, split by their starting Amharic letter (e.g., `ሀ.json`, `ለ.json`).

To add a new proverb:
1. **Fork** this repository.
2. Navigate to `src/temsalet/data/` and open the JSON file corresponding to the starting letter of your proverb (e.g., open `ለ.json` if the proverb starts with 'ለ').
3. Add your proverb to the list using the following format:
   ```json
   {
     "id": "ለ_2",
     "proverb_amharic": "Your proverb in Amharic script",
     "proverb_english": "Literal or closest English translation",
     "meaning_amharic": "Meaning of the proverb in Amharic",
     "meaning_english": "Meaning of the proverb in English",
     "origin": "Traditional",
     "category": "Wisdom"
   }
