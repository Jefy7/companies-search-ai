from difflib import get_close_matches

VALID_SECTORS = [
    "Fintech", "Healthcare", "SaaS", "EdTech", "Gaming",
    "IoT", "Logistics", "Cybersecurity", "AI", "E-commerce"
]

SECTOR_MAP = {
    "fintech": "Fintech",
    "finance": "Fintech",
    "banking": "Fintech",
    "payments": "Fintech",

    "healthcare": "Healthcare",
    "health": "Healthcare",
    "medical": "Healthcare",

    "saas": "SaaS",
    "software": "SaaS",

    "education": "EdTech",
    "edtech": "EdTech",

    "gaming": "Gaming",
    "games": "Gaming",

    "iot": "IoT",
    "internet of things": "IoT",

    "logistics": "Logistics",
    "supply chain": "Logistics",

    "cybersecurity": "Cybersecurity",
    "security": "Cybersecurity",

    "ai": "AI",
    "artificial intelligence": "AI",
    "ml": "AI",

    "ecommerce": "E-commerce",
    "e-commerce": "E-commerce",
    "online shopping": "E-commerce",
}

LOCATION_MAP = {
    "london": "London",
    "nyc": "New York",
    "new york": "New York",
    "bangalore": "Bangalore",
    "bengaluru": "Bangalore",
    "singapore": "Singapore",
    "dubai": "Dubai",
    "san francisco": "San Francisco",
    "sf": "San Francisco",
    "berlin": "Berlin",
    "sydney": "Sydney",
    "tokyo": "Tokyo",
    "paris": "Paris",
}
VALID_SUBSECTORS = {
    "Fintech": [
        "Payments", "Lending", "InsurTech", "WealthTech", "Blockchain"
    ],
    "Healthcare": [
        "Telemedicine", "PharmaTech", "HealthTech", "Medical Devices", "Wellness"
    ],
    "SaaS": [
        "CRM", "ERP", "HRTech", "MarketingTech", "DevTools"
    ],
    "EdTech": [
        "K-12", "Higher Education", "Upskilling", "Test Prep"
    ],
    "Gaming": [
        "Mobile Gaming", "PC Gaming", "Esports", "Game Development"
    ],
    "IoT": [
        "Smart Home", "Industrial IoT", "Wearables", "Connected Devices"
    ],
    "Logistics": [
        "Supply Chain", "Last Mile Delivery", "Fleet Management", "Warehouse Tech"
    ],
    "Cybersecurity": [
        "Network Security", "Cloud Security", "Identity & Access", "Threat Intelligence"
    ],
    "AI": [
        "Machine Learning", "NLP", "Computer Vision", "Generative AI"
    ],
    "E-commerce": [
        "Marketplaces", "D2C", "Social Commerce", "RetailTech"
    ]
}
SUBSECTOR_MAP = {
    # Fintech
    "payments": ("Fintech", "Payments"),
    "lending": ("Fintech", "Lending"),
    "insurance": ("Fintech", "InsurTech"),
    "wealth": ("Fintech", "WealthTech"),
    "crypto": ("Fintech", "Blockchain"),
    "blockchain": ("Fintech", "Blockchain"),

    # Healthcare
    "telemedicine": ("Healthcare", "Telemedicine"),
    "pharma": ("Healthcare", "PharmaTech"),
    "wellness": ("Healthcare", "Wellness"),

    # SaaS
    "crm": ("SaaS", "CRM"),
    "erp": ("SaaS", "ERP"),
    "hr": ("SaaS", "HRTech"),

    # AI
    "ml": ("AI", "Machine Learning"),
    "nlp": ("AI", "NLP"),
    "cv": ("AI", "Computer Vision"),
    "genai": ("AI", "Generative AI"),

    # E-commerce
    "marketplace": ("E-commerce", "Marketplaces"),
    "d2c": ("E-commerce", "D2C"),
}

# ----------------------------
# Core Matching Logic
# ----------------------------
def match_from_query(query: str, mapping: dict):
    query_lower = query.lower()

    # 1. Direct keyword match
    for key, value in mapping.items():
        if key in query_lower:
            return value

    return None


def fuzzy_match(value: str, valid_list: list[str]):
    if not value:
        return None

    matches = get_close_matches(value, valid_list, n=1, cutoff=0.6)
    return matches[0] if matches else None

def extract_subsector(query: str, sector: str | None):
    if not query:
        return None

    q = query.lower()

    # 1. Try direct mapping
    for key, (mapped_sector, sub) in SUBSECTOR_MAP.items():
        if key in q:
            return sub if not sector or sector == mapped_sector else None

    # 2. Try matching inside VALID_SUBSECTORS
    if sector and sector in VALID_SUBSECTORS:
        for sub in VALID_SUBSECTORS[sector]:
            if sub.lower() in q:
                return sub

    return None

# ----------------------------
# Main Validator (UPDATED)
# ----------------------------
def validate_filters(filters: dict, query: str):
    """
    Smart validation:
    1. Try LLM output
    2. Fallback to query keyword match
    3. Fallback to fuzzy match
    """

    query_lower = query.lower()

    # ---- SECTOR ----
    sector = None

    # 1. From LLM
    if filters.get("sector"):
        sector = SECTOR_MAP.get(filters["sector"].lower())

    # 2. From query (strong fallback)
    if not sector:
        sector = match_from_query(query_lower, SECTOR_MAP)

    # 3. Fuzzy fallback
    if not sector and filters.get("sector"):
        sector = fuzzy_match(filters["sector"], VALID_SECTORS)

    # ---- LOCATION ----
    location = None

    # 1. From LLM
    if filters.get("location"):
        location = LOCATION_MAP.get(filters["location"].lower())

    # 2. From query
    if not location:
        location = match_from_query(query_lower, LOCATION_MAP)

    sub_sector = extract_subsector(query, sector)

    # ---- TAGS ----
    tags = filters.get("tags", [])

    # keep only meaningful tags (present in query)
    tags = [tag for tag in tags if tag.lower() in query_lower]

    return {
        "sector": sector,
        "sub_sector": sub_sector,
        "location": location,
        "tags": tags,
    }