class Empty(Exception):
    """raise if the players structure is empty"""
    def __str__(self) -> str:
        return "no player in the game to be removed"

class PlayerNotFound(Exception):
    """raise if the player is not found"""
    def __str__(self) -> str:
        return "player not found"
        
class GameLimit(Exception):
    """raise exception when the nbre of players limit is set"""
    def __str__(self) -> str:
        return "game is full, try another server"

class GameNotStarted(Exception):
    """raise if player starts before others join"""
    def __str__(self) -> str:
        return "others players have not joined yet"

class WrongTurn(Exception):
    """raise when the player tries to player in others' turns"""
    def __str__(self) -> str:
        return "not your turn"