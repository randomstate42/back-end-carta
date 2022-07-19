from ..exceptions import Empty, GameLimit

class Players:
    """ a circular doubly linked list for 
    managing players' turns and operations"""
    __slots__ = "head", "_last_added", "_size", "_limit"
    
    class _Node:
        __slots__ = "player", "next", "_prev"
        def __init__(self, player, predecessor, successor):
            self.player = player
            self.next = successor
            self._prev = predecessor
            
    def __init__(self, nb_players: int):
        self.head = self._Node(None, None, None)
        self._last_added = self.head
        self._size = 0
        self._limit = nb_players

    def __len__(self):
        return self._size

    def insert(self, player):
        if self._last_added is None:
            raise GameLimit
        elif self._size == 0:
            self.head.player = player
            self._size += 1
        elif self._size == self._limit-1:
            new = self._Node(player, self._last_added, self.head)
            self._last_added.next = new
            self.head._prev = new
            self._size += 1
            self._last_added = None
        else:
            new = self._Node(player, self._last_added, None)
            self._last_added.next = new
            self._last_added = new
            self._size += 1

    async def delete_player(self, node: _Node): 
        if self._size == 0:
            raise Empty
        else :
            predecessor = node._prev
            successor = node.next
            predecessor.next = successor
            successor._prev = predecessor
            self._size -= 1
            node.player = node._prev = node.next = None #garbage collectio


