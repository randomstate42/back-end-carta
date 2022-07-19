import random
import cgi
import cgitb
cgitb.enable()

from .table import Table, Card, GameType
from ..game_server import ConnectionManager


class Game:
    __slots__ = "_nb_players", "_type", "_table", "_players", "server"

    def __init__(self, server: ConnectionManager, nb_players: int, type: str):
        self._nb_players = nb_players
        self._type = type
        self._table = Table(self._nb_players)
        self._table.set_table_card(self._type)
        #self._players = Players(self._nb_players)
        self.server = server
        self._players = self.server.active_connections

    async def play(self):
        form = cgi.FieldStorage()
        if self._type == GameType.STANDARD:
            special_case = False
            nbre_of_twos = 0
            node = self._players.head
            current_player = node.player
            while len(self._players) > 1:
                table_card = self._table.table_cards[-1]
                self.server.broadcast(f"table card {table_card}")
                cond = await current_player.allowed_to_move(table_card, nbre_of_twos)
                if cond:
                    #print("{} ur cards ".format(current_player.username))
                    self.server(f"{current_player.username} ur cards", current_player)
                    for card in current_player.cards:
                        self.server(card)
                    #number, symbol = int(input("choose a number")), input("choose a symbol")
                    number = form["number"]
                    symbol = form["symbol"]
                    card = Card(number, symbol)
                    allowed = await current_player.allowed_cards(nbre_of_twos)
                    if (
                        table_card.number == 2
                        and card not in allowed
                            ):
                        await current_player.take_card(2)
                    elif table_card.number == card.number == 2:
                        await current_player.put_card(card)
                        nbre_of_twos += 1
                        if special_case:
                            special_case = False
                    else:
                        mask = await current_player.card_is_allowed(
                            card, table_card, 
                            self._type, nbre_of_twos
                            )
                        while not mask:
                            self.server.broadcast("choose an allowed one", current_player)
                            number = form["number"]
                            symbol = form["symbol"]
                            card = Card(number, symbol)
                            mask = await current_player.card_is_allowed(
                                card, table_card, 
                                self._type, nbre_of_twos
                                )
                        if card.number == 7:
                            self._table.choice = form["symbol"]
                        elif card.number == 2 and len(self._players) == 2:
                            special_case = True
                            nbre_of_twos += 1
                        await current_player.put_card(card)
                elif table_card.number == 2 and not special_case:
                    await current_player.take_card(nbre_of_twos)
                    special_case = False
                    nbre_of_twos = 0
                    self.server.broadcast(f"{current_player.username} ur cards ", current_player)
                    for card in self.cards:
                        print(card)
                else:
                    await current_player.take_card()
                    special_case = False
                    if nbre_of_twos > 0:
                        nbre_of_twos = 0
                    self.server.broadcast(f"{current_player.username} ur cards ", current_player)
                    for c in current_player.cards:
                        print(c)
                node = node.next.next if card.number == 1 else node.next
                next_player = node.player
                if len(current_player.cards) == 0:
                    self._players.delete_player(current_player)
                current_player = next_player
                if len(self._table.stock) == 8:
                    self._table.stock[8:] = self._table.table_cards[:-1]
                    self._table.table_cards = self._table.table_cards[-1:]
                    random.shuffle(self._table.stock)
        else:
            pass


