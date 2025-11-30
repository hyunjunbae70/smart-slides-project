from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List
from backend.slide_generator import generate_slides

app = FastAPI(title="Smart Slides API", version="1.0.0")


class ConnectionManager:
    """
    WebSocket connection manager to handle multiple concurrent connections.
    """
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """
        Accept a new WebSocket connection and add it to the active connections.
        
        Args:
            websocket: The WebSocket connection to add
        """
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection from the active connections.
        
        Args:
            websocket: The WebSocket connection to remove
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        """
        Send a message to all active WebSocket connections.
        
        Args:
            message: The message string to broadcast to all clients
        """
        # Create a list of connections to remove if they fail
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Connection is likely closed, mark for removal
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)


# Create a global connection manager instance
manager = ConnectionManager()


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

