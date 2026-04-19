VALID_SECTORS = [
    "Fintech", "Healthcare", "SaaS", "EdTech", "Gaming", "IoT", "Logistics", "Cybersecurity", "AI"
]
SECTOR_MAP = {
    "fintech": "Fintech",
    "finance": "Fintech",
    "banking": "Fintech",
    "healthcare": "Healthcare",
    "health": "Healthcare",
    "logistics": "Logistics",
    "saas": "SaaS",
    "education": "EdTech",
    "gaming": "Gaming",
    "iot": "IoT",
    "cybersecurity": "Cybersecurity",
    "ai": "AI",
    "e-commerce": "E-commerce"
}
LOCATION_MAP = {
    "london": "London",
    "nyc": "New York",
    "new york": "New York",
    "bangalore": "Bangalore",
    "singapore": "Singapore",
    "Dubai": "Dubai",
    "san francisco": "San Francisco", 
    "berlin": "Berlin", 
    "singapore": "Singapore", 
    "dubai": "Dubai", 
    "sydney":"Sydney", 
    "tokyo":"Tokyo", 
    "paris":"Paris"
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