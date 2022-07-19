import random
from enum import Enum, unique
from typing import List, Union


class GameType(Enum):
    STANDARD, KDOUB, MAKLA, COPIES = (1, 2, 3, 4)

class Card:
    __slots__ = "number", "symbol"
    numbers = (1, 2, 3, 4, 5, 6, 7, 10, 11, 12)

    @unique
    class Symbols(Enum):
        SYOUF, TAJINE, FLOUS, GUAR3A = (1, 2, 3, 4)

    def make(self, symbol: Union[Symbols, str]):
        """this function only for test"""
        if isinstance(symbol, str):
            if symbol == 'SYOUF':
                symbol=self.Symbols.SYOUF
            elif symbol == 'TAJINE':
                symbol=self.Symbols.TAJINE
            elif symbol == 'FLOUS':
                symbol=self.Symbols.FLOUS
            elif symbol == 'GUAR3A':
                symbol=self.Symbols.GUAR3A
            else:
                print("type a correct card")
        else:
            symbol=symbol
        return symbol

    def __init__(self, number: int, symbol: Symbols):
        self.number = number
        self.symbol = self.make(symbol)

    def __str__(self):
        return str(self.number) + " " + str(self.symbol.name)

    def __eq__(self, card):
        return self.number == card.number and self.symbol == card.symbol


class Table:
    __slots__ = "stock", "nb_players", "table_cards", "choice", "PURE_CARDS"

    def __init__(self, nb_players: int):
        self.stock = [Card(n, s) for n in Card.numbers for s in Card.Symbols]
        random.shuffle(self.stock)
        self.table_cards = []
        self.nb_players = nb_players

    def set_table_card(self, game: GameType):
        if game == GameType.STANDARD:
            self.PURE_CARDS = [
                Card(n, s)
                for n in Card.numbers
                for s in Card.Symbols
                if n not in (1, 2, 7)
                ]
            random.shuffle(self.PURE_CARDS)
            self.table_cards.append(self.PURE_CARDS[0])
            self.stock.remove(self.table_cards[0])
        elif game == GameType.KDOUB:
            self.stock.pop()

    def distribute_cards(self, lenghth: int, shares: List[int]):
        n = lenghth // len(shares)
        for i in range(len(shares)):
            shares[i] = n
            if 0 < i <= lenghth % len(shares):
                shares[i - 1] += 1
        return shares
