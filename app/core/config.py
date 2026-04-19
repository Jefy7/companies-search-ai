import os

class Settings:
    MODEL_NAME = os.getenv("MODEL_NAME", "google/flan-t5-base")
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    MAX_TOKENS = 256
    CONFIDENCE_THRESHOLD = 0.5

settings = Settings()