from typing import Optional
from exceptions import GameNotStarted
from exceptions import Empty
from exceptions import GameLimit
from utils.players import Players
from utils.player import Player



class ConnectionManager:
    def __init__(self, nb_players: int=3):
        self.active_connections = Players(nb_players)

    async def connect(self, player: Player):
        try :
            await player.accept()
            self.active_connections.insert(player)
            player.place = len(self.active_connections)
        except GameLimit as g:
            self.broadcast(g)

    def disconnect(self, player: Player):
        try:
            self.active_connections.delete_player(player)
        except Empty as e:
            print(e)

    async def _send(self, message: str, player: Player):
        if len(self.active_connections) < self.nb_players:
            raise GameNotStarted
        else:
            await player.send_text(message)

    async def _recieve(self, message: str):
        if len(self.active_connections) < self.nb_players:
            raise GameNotStarted
        else : 
            for connection in self.active_connections:
                await connection.send_text(message)

    async def communicate(self, prefix: str, message: str, prefix2: str):
        try:
            self._send(prefix+message)
            self._recieve(prefix2+message)
        except GameNotStarted as g:
            print(g)      

    async def broadcast(self, message: str, player: Optional[Player]):
        try:
            if player:
                await player.send_text(message)
            else:
                self._recieve(message)
        except GameNotStarted as g:
            print(g)

