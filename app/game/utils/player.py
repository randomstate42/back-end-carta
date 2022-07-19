from typing import Union, List, Optional

from .table import Card, GameType
from fastapi import WebSocket


class Player(WebSocket):
    #__slots__ = "username", "_table", "_game", "cards"

    def __init__(self, username: str, game: GameType, table, place: Optional[int]):
        self.username = username
        self._table = table
        self._game = game
        cards_share = self._table.distribute_cards(
            len(self._table.stock), [0*table.nb_players]
            )
        if game in (GameType.STANDARD, GameType.MAKLA, GameType.COPIES):
            self.cards = self._table.stock[:4]
            self._table.stock = self._table.stock[4:]
        elif game == GameType.KDOUB:
            self.cards = self._table.stock[: cards_share[place]]
            self._table.stock = self._table.stock[cards_share[place]:]

    async def take_card(self, n=1):
        cards = self._table.stock[-n:]
        self._table.stock = self._table.stock[:-n]
        if n == 1:
            self.cards.append(cards)
        else:
            self.cards.extend(cards)

    async def put_card(self, cards: Union[Card, List[Card]], n: int=1):
        if n == 1:
            self._table.table_cards.append(cards)
            self.cards.remove(cards)
        else:
            self._table.table_cards.extend(cards)
            for card in cards:
                self.cards.remove(card)

    async def card_is_allowed(self, card, table_card, game, helper: int):
        if game == GameType.STANDARD:
            if table_card.number == 2 and helper > 0:
                return (
                    True
                    if (card.symbol == table_card.symbol or card.number == 2)
                    else False
                    )
            elif table_card.number == 2:
                return True if card.number == 2 else False
            elif table_card.number == 7:
                return (
                    True
                    if (card.number == 7 or card.symbol == self._table.choice)
                    else False
                    )
            elif (
                card.symbol == table_card.symbol
                or card.number == table_card.number
                    ):
                return True
            return False
        else:
            pass

    async def allowed_cards(self, helper: int):
        """allowed_cards = [
            card
            for card in self.cards
            if self.card_is_allowed(
                card, self._table.table_cards[-1], self._game, helper)
            ]"""
        allowed_cards = []
        for card in self.cards:
            cond = await self.card_is_allowed(
                card, self._table.table_cards[-1], 
                self._game, helper
                )
            if cond:
                allowed_cards.append(card)
        return allowed_cards

    async def allowed_to_move(self, helper: int):
        """for card in self.cards:
            cond = await self.card_is_allowed(card, table_card, self._game, helper)
            if cond:
                return True"""
        cond = await self.allowed_cards(helper)
        if cond:
            return True
        return False
