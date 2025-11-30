from fastapi import FastAPI

app = FastAPI(title="Smart Slides API", version="1.0.0")


@app.get("/api/status")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "message": "API is running"}

