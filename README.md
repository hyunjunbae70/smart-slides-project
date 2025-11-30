# Smart Slides Project

AI-powered PowerPoint generator that creates presentation slides from natural language queries.

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher and npm
- OpenAI API key

## Setup Instructions

### 1. Backend Setup (Terminal 1)

1. **Create and activate a Python virtual environment:**
   
   On Linux/Mac:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   
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

4. **Start the FastAPI backend server:**
   
   **Important:** Run this command from the project root directory (where `requirements.txt` is located), not inside the `backend` folder:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

   You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     Application startup complete.
   ```

   The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/api/status`

### 2. Frontend Setup (Terminal 2)

**Important:** You need a separate terminal window/tab for the frontend. Keep the backend running in Terminal 1.

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Start the Vite development server:**
   ```bash
   npm run dev
   ```
   
   You should see:
   ```
   VITE v5.x.x  ready in xxx ms

   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ```
   
   The frontend will be available at `http://localhost:5173`

### 3. Open in Browser

Navigate to: **http://localhost:5173**

### 4. Generate Your First Slides

1. Enter a prompt like: "Create a presentation about artificial intelligence"
2. Click "Generate Slides" or press Ctrl+Enter
3. Wait a few seconds for the slides to be generated
4. Once generated, you'll see:
   - **Left sidebar**: List of all slides
   - **Center**: Slide editor (click a slide to edit)
   - **Right panel**: Chat interface

5. **Additional Features:**
   - Try editing slides - changes sync in real-time via WebSocket
   - Open multiple browser tabs to see real-time collaboration
   - Use the chat feature to communicate with other users

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

### Backend won't start
- Make sure Python 3.8+ is installed: `python --version`
- Make sure you've created and activated a Python virtual environment
- Make sure you've set the OPENAI_API_KEY environment variable
- Check if port 8000 is already in use

### Frontend won't start
- Make sure Node.js 16+ is installed: `node --version`
- Make sure you're using a separate terminal window/tab (keep backend running in Terminal 1)
- Try deleting `node_modules` and running `npm install` again
- Check if port 5173 is already in use

### "Failed to generate slides"
- Verify your OpenAI API key is correct
- Check that you have credits in your OpenAI account
- Look at the backend terminal for detailed error messages

### WebSocket not connecting
- Make sure both backend and frontend are running (in separate terminals)
- Check browser console (F12) for WebSocket errors
- Verify the backend is accessible at http://localhost:8000

### Other Backend Issues

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

### Other Frontend Issues

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
