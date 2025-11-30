# Quick Start Guide

## Step-by-Step Setup

### 1. Backend Setup (Terminal 1)

```bash
# Make sure you're in the project root directory
cd /path/to/smart-slides-project

# Install Python dependencies
pip install -r requirements.txt

# Set your OpenAI API key (replace with your actual key)
export OPENAI_API_KEY="sk-your-openai-api-key-here"

# Start the backend server (from project root)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Important:** Make sure you're in the project root directory (where `requirements.txt` is located), not inside the `backend` folder!

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### 2. Frontend Setup (Terminal 2)

```bash
# Install Node.js dependencies
npm install

# Start the frontend development server
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

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

## Troubleshooting

### Backend won't start
- Make sure Python 3.8+ is installed: `python --version`
- Make sure you've set the OPENAI_API_KEY environment variable
- Check if port 8000 is already in use

### Frontend won't start
- Make sure Node.js 16+ is installed: `node --version`
- Try deleting `node_modules` and running `npm install` again
- Check if port 5173 is already in use

### "Failed to generate slides"
- Verify your OpenAI API key is correct
- Check that you have credits in your OpenAI account
- Look at the backend terminal for detailed error messages

### WebSocket not connecting
- Make sure both backend and frontend are running
- Check browser console (F12) for WebSocket errors
- Verify the backend is accessible at http://localhost:8000

## Next Steps

- Try editing slides - changes sync in real-time via WebSocket
- Open multiple browser tabs to see real-time collaboration
- Use the chat feature to communicate with other users

