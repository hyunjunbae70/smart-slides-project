from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.slide_generator import generate_slides

app = FastAPI(title="Smart Slides API", version="1.0.0")


class GenerateSlidesRequest(BaseModel):
    query: str


@app.get("/api/status")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "message": "API is running"}


@app.post("/api/generate-slides")
async def generate_slides_endpoint(request: GenerateSlidesRequest):
    """
    Generate slides based on a user query.
    
    Args:
        request: Request body containing the query string
        
    Returns:
        JSON object containing a list of slides with title, content, and theme
        
    Raises:
        HTTPException: If slide generation fails
    """
    try:
        slides_data = generate_slides(request.query)
        return slides_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating slides: {str(e)}")

