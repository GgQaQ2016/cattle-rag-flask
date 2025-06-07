"""Utility functions for loading knowledge data files."""

import json
from pathlib import Path
from typing import List, Dict

DATA_DIR = Path(__file__).resolve().parent
OFFICIAL_FILE = DATA_DIR / "official_knowledge.json"
USER_DATA_DIR = DATA_DIR / "user_data"


def load_official_knowledge() -> List[Dict]:
    """Load official knowledge entries from JSON file."""
    if not OFFICIAL_FILE.exists():
        return []
    with open(OFFICIAL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_user_knowledge(user_id: str) -> List[Dict]:
    """Load knowledge entries for a specific user."""
    user_file = USER_DATA_DIR / f"{user_id}.json"
    if not user_file.exists():
        return []
    with open(user_file, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    # Demo: print number of entries for quick verification
    print("Official knowledge entries:", len(load_official_knowledge()))
    print("Sample user entries:", len(load_user_knowledge("sample_user")))
