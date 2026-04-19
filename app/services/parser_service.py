import json
import re
from app.services.llm_service import llm_service


class ParserService:
    def parse_query(self, query: str):
        print("query", query)
        prompt = self._build_prompt(query)
        print("prompt", prompt)

        raw_response = llm_service.generate(prompt)
        print("raw_response", raw_response)

        if not raw_response:
            return self._fallback()

        parsed = self._extract_json(raw_response)
        print("parsed ", parsed)
        if not parsed:
            return self._fallback()

        return self._normalize(parsed)

    # ----------------------------
    # Prompt Builder
    # ----------------------------
    def _build_prompt(self, query: str) -> str:
        return f"""
    You extract structured filters from company search queries.

    Sectors: Fintech, Healthcare, SaaS, EdTech, Gaming, IoT, Logistics, Cybersecurity, AI, E-commerce
    Locations: London, New York, Bangalore, San Francisco, Berlin, Singapore, Dubai, Sydney, Tokyo, Paris

    RULES:
    - If query matches a sector or partial word matches to sector, return it
    - If query contains a city or partial word matches to city name or shorthand of city name, return location
    - If query has any important keywords other than sector and location, return it in tags
    - Be Case Insensitive
    - Be STRICT but SMART
    - Return ONLY JSON

    EXAMPLES:

    Query: Fintech
    Output:
    {{"sector":"Fintech","location":null,"tags":[]}}

    Query: SaaS companies in London
    Output:
    {{"sector":"SaaS","location":"London","tags":[]}}

    Query: Healthcare startups
    Output:
    {{"sector":"Healthcare","location":null,"tags":["startups"]}}

    Query: AI
    Output:
    {{"sector":"AI","location":null,"tags":[]}}

    Query: New York 
    Output:
    {{"sector":null,"location":"New York","tags":[]}}

    Query: New Y
    Output:
    {{"sector":null,"location":"New York","tags":[]}}

    Query: Lo
    Output:
    {{"sector":Logistics,"location":"London","tags":[]}}

    Query: AI startups in New York 
    Output:
    {{"sector":AI,"location":"New York","tags":[startups]}}

    NOW DO THIS:

    Query: "{query}"
    Output:
    """

    # ----------------------------
    # Extract JSON safely
    # ----------------------------
    def _extract_json(self, text: str):
        try:
            # 1. Try normal JSON first
            return json.loads(text)
        except:
            pass

        try:
            # 2. Try wrapping in braces (fix your exact case)
            wrapped = "{" + text.strip().strip(",") + "}"
            return json.loads(wrapped)
        except:
            pass

        try:
            # 3. Regex fallback (safe extraction)
            match = re.search(r'"sector".*', text)
            if not match:
                return None

            cleaned = "{" + match.group(0) + "}"
            return json.loads(cleaned)
        except:
            return None

    # ----------------------------
    # Normalize Output
    # ----------------------------
    def _normalize(self, data: dict):
        return {
            "filters": {
                "sector": data.get("sector"),
                "location": data.get("location"),
                "tags": data.get("tags", []),
            },
            "similarTerms": [],
            "suggestions": [],
            "confidence": 0.6,  # base confidence
        }

    # ----------------------------
    # Fallback
    # ----------------------------
    def _fallback(self):
        return {
            "filters": {},
            "similarTerms": [],
            "suggestions": [],
            "confidence": 0,
        }


parser_service = ParserService()