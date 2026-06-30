from fastapi import FastAPI

from app.api.upload import router as upload_router

app = FastAPI()

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}

app.include_router(upload_router)