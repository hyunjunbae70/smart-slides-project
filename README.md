# Smart Slides Project

AI-powered PowerPoint generator that creates presentation slides from natural language queries.

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher and npm
- OpenAI API key

## Setup Instructions

### 1. Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your OpenAI API key:**
   
   On Linux/Mac:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   On Windows (PowerShell):
   ```powershell
   $env:OPENAI_API_KEY="your-api-key-here"
   ```
   
   On Windows (Command Prompt):
   ```cmd
   set OPENAI_API_KEY=your-api-key-here
   ```
   
   **Note:** For a permanent setup, add the environment variable to your system settings or use a `.env` file with a package like `python-dotenv`.

3. **Start the FastAPI backend server:**
   
   **Important:** Run this command from the project root directory (where `requirements.txt` is located):
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/api/status`

### 2. Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Start the Vite development server:**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:5173`

### 3. Using the Application

1. **Open your browser** and navigate to `http://localhost:5173`

2. **Generate Slides:**
   - Enter a natural language prompt in the text area (e.g., "Create a presentation about artificial intelligence")
   - Click "Generate Slides" or press Ctrl+Enter (Cmd+Enter on Mac)
   - Wait for the slides to be generated

3. **View and Edit Slides:**
   - Once slides are generated, they will appear in the sidebar
   - Click on a slide to view and edit it
   - Changes are automatically synchronized across all connected clients via WebSocket

4. **Chat (WebSocket):**
   - The chat feature allows real-time communication between users
   - WebSocket connection is established automatically when needed

## Project Structure

```
smart-slides-project/
├── backend/
│   ├── main.py              # FastAPI application with endpoints
│   ├── slide_generator.py   # OpenAI integration for slide generation
│   └── config.py            # Configuration and API key management
├── frontend/
│   ├── src/
│   │   ├── App.svelte       # Main application component
│   │   ├── GenerateSlides.svelte  # Slide generation UI
│   │   ├── SlideList.svelte # Sidebar with slide thumbnails
│   │   ├── SlideEditor.svelte # Slide editing interface
│   │   ├── Chat.svelte       # WebSocket chat component
│   │   ├── api.js           # API service and store management
│   │   ├── websocket.js     # WebSocket service
│   │   └── main.js          # Application entry point
│   └── public/
│       └── index.html       # HTML template
├── requirements.txt         # Python dependencies
├── package.json            # Node.js dependencies
└── README.md               # This file
```

## API Endpoints

- `GET /api/status` - Health check endpoint
- `POST /api/generate-slides` - Generate slides from a prompt
- `WebSocket /ws/chat/{client_id}` - WebSocket endpoint for chat and slide editing

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)

## Troubleshooting

### Backend Issues

1. **"OPENAI_API_KEY environment variable is not set"**
   - Make sure you've set the environment variable before starting the server
   - Verify it's set: `echo $OPENAI_API_KEY` (Linux/Mac) or `echo %OPENAI_API_KEY%` (Windows)

2. **"Failed to connect to OpenAI API"**
   - Check your internet connection
   - Verify your API key is valid
   - Check OpenAI service status

3. **Port 8000 already in use**
   - Change the port: `uvicorn backend.main:app --reload --port 8001`
   - Update the frontend API calls to use the new port

### Frontend Issues

1. **"Cannot connect to API"**
   - Make sure the backend server is running
   - Check that the backend is accessible at `http://localhost:8000`
   - Verify CORS settings if accessing from a different origin

2. **WebSocket connection fails**
   - Ensure the backend is running
   - Check browser console for WebSocket errors
   - Verify the WebSocket URL matches your backend URL

## Development

- Backend uses FastAPI with auto-reload enabled
- Frontend uses Vite with hot module replacement
- Both servers should be running simultaneously for full functionality

## License

See LICENSE file for details.
