import os
import threading
from typing import List

from sentence_transformers import SentenceTransformer, util  # type: ignore


class SimilarityService:
    _instance = None
    _lock = threading.Lock()

    _model = None
    _base_terms = [
        "fintech", "payments", "saas", "healthcare",
        "ai", "machine learning", "cloud", "security"
    ]
    _base_embeddings = None

    def __new__(cls):
        """Thread-safe Singleton"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def _load_model(self):
        """Lazy load model (only when needed)"""
        if self.__class__._model is None:
            os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "60")

            # Optional: force offline mode if needed
            # os.environ["HF_HUB_OFFLINE"] = "1"

            self.__class__._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

            # Precompute base embeddings once
            self.__class__._base_embeddings = self._model.encode(
                self._base_terms,
                convert_to_tensor=True,
                normalize_embeddings=True
            )

    def get_similar_terms(
        self,
        query: str,
        threshold: float = 0.5,
        top_k: int = 3
    ) -> List[str]:
        if not query or not query.strip():
            return []

        self._load_model()

        query_embedding = self._model.encode(
            query,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        scores = util.cos_sim(query_embedding, self._base_embeddings)[0]

        # Get terms above threshold
        results = [
            self._base_terms[i]
            for i, score in enumerate(scores)
            if float(score) >= threshold
        ]

        # 🔁 Smart fallback → return top_k instead of just 1
        if not results:
            top_indices = scores.topk(k=top_k).indices.tolist()
            results = [self._base_terms[i] for i in top_indices]

        return results


# ✅ Global instance
similarity_service = SimilarityService()