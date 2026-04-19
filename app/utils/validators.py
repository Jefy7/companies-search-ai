VALID_SECTORS = [
    "Fintech", "Healthcare", "SaaS", "EdTech", "Gaming"
]
SECTOR_MAP = {
    "fintech": "Fintech",
    "finance": "Fintech",
    "banking": "Fintech",
    "health": "Healthcare",
    "saas": "SaaS",
    "education": "EdTech",
    "gaming": "Gaming"
}
LOCATION_MAP = {
    "london": "London",
    "nyc": "New York",
    "new york": "New York",
    "bangalore": "Bangalore",
    "singapore": "Singapore",
    "Dubai": "Dubai"
}

def normalize(value, mapping):
    if not value:
        return None
    return mapping.get(value.lower(), None)


def validate_filters(filters: dict):
    return {
        "sector": normalize(filters.get("sector"), SECTOR_MAP),
        "location": normalize(filters.get("location"), LOCATION_MAP),
        "tags": filters.get("tags", []),
    }