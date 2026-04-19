from sentence_transformers import SentenceTransformer, util

class SimilarityService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def get_similar_terms(self, query: str):
        base_terms = [
            "fintech", "payments", "saas", "healthcare",
            "ai", "machine learning", "cloud", "security"
        ]

        query_emb = self.model.encode(query, convert_to_tensor=True)
        base_emb = self.model.encode(base_terms, convert_to_tensor=True)

        scores = util.cos_sim(query_emb, base_emb)[0]

        results = [
            base_terms[i]
            for i, score in enumerate(scores)
            if score > 0.4
        ]

        return results

similarity_service = SimilarityService()