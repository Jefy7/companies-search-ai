from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str

class Filters(BaseModel):
    sector: Optional[str] = None
    location: Optional[str] = None
    tags: List[str] = []

class SearchResponse(BaseModel):
    filters: Filters
    similarTerms: List[str]
    suggestions: List[str]
    confidence: float