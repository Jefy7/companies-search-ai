from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI Search Service")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "AI Service Running"}