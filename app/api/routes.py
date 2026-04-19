from fastapi import APIRouter
from app.models.schemas import SearchRequest, SearchResponse, Filters
from app.services.parser_service import parser_service
from app.services.similarity_service import similarity_service
from app.utils.validators import validate_filters

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/api/v1/ai/search", response_model=SearchResponse)
async def ai_search(request: SearchRequest):
    query = request.query.strip()

    # 1. Parse query using LLM
    parsed_filters = parser_service.parse_query(query)
    print("parsed_filters", parsed_filters)
    filters_to_validate = parsed_filters.get("filters", {})

    # 2. Validate filters
    validated = validate_filters(filters_to_validate)
    print("validated ", validated)
    # 3. Get similarity terms
    similar_terms = similarity_service.get_similar_terms(query)

    # 4. Generate smarter suggestions
    location = validated.get("location") or "global"
    sector = validated.get("sector")

    suggestions = [
        f"Top {query}",
        f"Best companies in {location}",
    ]

    if sector:
        suggestions.append(f"Top {sector} companies in {location}")

    # 5. Confidence scoring (cleaner logic)
    confidence = 0.4
    if sector:
        confidence += 0.3
    if location:
        confidence += 0.3

    confidence = min(confidence, 1.0)

    return SearchResponse(
        filters=Filters(**validated),
        similarTerms=similar_terms,
        suggestions=suggestions,
        confidence=confidence
    )