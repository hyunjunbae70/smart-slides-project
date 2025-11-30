from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict, Any
import json
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
    
    async def broadcast_to_others(self, message: str, sender: WebSocket):
        """
        Send a message to all active WebSocket connections except the sender.
        
        Args:
            message: The message string to broadcast to all other clients
            sender: The WebSocket connection to exclude from the broadcast
        """
        # Create a list of connections to remove if they fail
        disconnected = []
        
        for connection in self.active_connections:
            if connection != sender:
                try:
                    await connection.send_text(message)
                except Exception:
                    # Connection is likely closed, mark for removal
                    disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
    
    async def broadcast_json(self, payload: Dict[str, Any]):
        """
        Send a JSON payload to all active WebSocket connections.
        
        Args:
            payload: The JSON-serializable dictionary to broadcast to all clients
        """
        # Create a list of connections to remove if they fail
        disconnected = []
        json_message = json.dumps(payload)
        
        for connection in self.active_connections:
            try:
                await connection.send_text(json_message)
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


@app.websocket("/ws/chat/{client_id}")
async def websocket_chat_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for chat functionality and slide editing.
    Accepts connections, receives messages (text or JSON), and broadcasts them to all connected clients.
    
    Handles two types of messages:
    1. Plain text messages: Broadcasts as "client_id: message" for chat
    2. JSON messages with type 'edit': Broadcasts the structured payload for slide edits
    
    Args:
        websocket: The WebSocket connection
        client_id: Unique identifier for the client
    """
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from the client
            data = await websocket.receive_text()
            
            # Try to parse as JSON to check if it's a structured payload
            try:
                payload = json.loads(data)
                
                # Check if it's a slide edit message
                if isinstance(payload, dict) and payload.get('type') == 'edit':
                    # Validate the edit payload structure
                    if 'slide_index' in payload and 'field' in payload and 'value' in payload:
                        # Add client_id to the payload for context
                        edit_payload = {
                            'type': 'edit',
                            'client_id': client_id,
                            'slide_index': payload['slide_index'],
                            'field': payload['field'],
                            'value': payload['value']
                        }
                        # Broadcast the structured JSON payload to all clients
                        await manager.broadcast_json(edit_payload)
                    else:
                        # Invalid edit payload structure
                        await websocket.send_text(json.dumps({
                            'type': 'error',
                            'message': 'Invalid edit payload. Required fields: slide_index, field, value'
                        }))
                else:
                    # JSON message but not an edit type, broadcast as-is
                    await manager.broadcast_json(payload)
                    
            except json.JSONDecodeError:
                # Not JSON, treat as plain text chat message
                # Broadcast the message to all other connected clients
                # Format: "client_id: message"
                message = f"{client_id}: {data}"
                await manager.broadcast_to_others(message, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        # Handle any other exceptions and disconnect
        manager.disconnect(websocket)
        raise

