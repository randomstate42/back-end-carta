from fastapi import APIRouter, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from utils.player import Player
from utils.game import Game
from utils.table import GameType
from game_server import ConnectionManager

app = APIRouter()


manager = ConnectionManager()

"""
the html doc is for test
"""

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="number" id="number" autocomplete="off"/>
            <input type="text" id="symbol" autocomplete="off"/>
            <button>choose</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var username = String
            document.querySelector("#ws-id").textContent = username;
            var ws = new WebSocket(`ws://localhost:8000/ws/${username}`);
            ws.onmessage = function(event) {
                var number = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/{username}")
async def websocket_endpoint(username: str, table, game: GameType=GameType.STANDARD):
    websocket = Player(username, game, table)
    server = await manager.connect(websocket)

    try:
        Game(server, 3, GameType.STANDARD)

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        await manager.broadcast(f"{username} left the server")
