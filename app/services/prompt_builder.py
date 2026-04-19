def build_prompt(query: str) -> str:
    return f"""
You are an AI that converts search queries into structured filters.

Return ONLY JSON. No explanation.

Query: "{query}"

Format:
{{
  "filters": {{
    "sector": string | null,
    "location": string | null,
    "tags": string[]
  }},
  "similarTerms": string[],
  "suggestions": string[],
  "confidence": number
}}

Rules:
- Output MUST be valid JSON
- No text outside JSON
- Infer best possible filters

Example:
Query: "Fintech companies in London doing payments"

Output:
{{
  "filters": {{
    "sector": "Fintech",
    "location": "London",
    "tags": ["payments"]
  }},
  "similarTerms": ["banking", "digital payments"],
  "suggestions": ["Try UK fintech", "Explore lending startups"],
  "confidence": 0.9
}}
"""