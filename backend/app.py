from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTML client for testing WebSocket
HTML = '''<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <button onclick="sendMessage()">Send Message</button>
        <ul id="messages"></ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                message.appendChild(document.createTextNode(event.data));
                messages.appendChild(message);
            };
            function sendMessage() {
                ws.send("Hello, WebSocket!");
            }
        </script>
    </body>
</html>'''

@app.get("/")
async def get():
    return HTMLResponse(content=HTML)

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

# REST endpoint example
@app.get("/api/message/{msg}")
async def read_message(msg: str):
    return {"message": msg}

# Run the application using: uvicorn backend.app:app --reload
