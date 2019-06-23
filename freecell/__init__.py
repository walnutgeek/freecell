
from functools import total_ordering
from typing import List, Union, Optional

DECK_SIZE = 52
RED, BLACK =1, -1

RANKS="A23456789TJQK"
SUITS="CDHS"
N_SUITS = len(SUITS)

@total_ordering
class Card:
    """
    >>> str(Card(5))
    '2D'
    >>> Card('2D') == Card(5)
    True
    >>> c6 = Card(Card(6))
    >>> c6 != Card(5)
    True
    >>> c6 > Card(5)
    True
    >>> c6 <= Card(5)
    False
    >>> Card(5) != Card(5)
    False
    >>> c6.color() == BLACK
    False
    >>> c6.color() == RED
    True
    >>> str(c6)
    '2H'
    >>> Card(-1) == Card(51)
    True
    >>> Card(52)
    Traceback (most recent call last):
     ...
    IndexError: list index out of range
    >>> Card('AA')
    Traceback (most recent call last):
    ...
    ValueError: substring not found
    >>> Card('CC')
    Traceback (most recent call last):
    ...
    ValueError: substring not found
    >>> Card(b'3C')
    Traceback (most recent call last):
    ...
    ValueError: Not sure what to do with: b'3C'
    """
    __all_cards__ :List[Union['Card',None]] = [None for _ in range(DECK_SIZE)]
    idx:int

    def __new__(cls, value):
        if type(value) is cls:
            return value
        if isinstance(value, str) and len(value)==2:
            value = RANKS.index(value[0])*N_SUITS + SUITS.index(value[1]) 
        if isinstance(value, int):
            inst = cls.__all_cards__[value]
            if inst is None:
                inst = super(Card, cls).__new__(cls)
                inst.idx = value + DECK_SIZE if value < 0 else value
                cls.__all_cards__[value] = inst
            return inst
        raise ValueError(f'Not sure what to do with: {value!r}')

    def __lt__(self, other):
        return self.idx < other.idx

    def rank(self):
        return self.idx // N_SUITS
    
    def suit(self):
        return self.idx % N_SUITS

    def color(self):
        return RED if self.suit() in (1,2) else BLACK 

    def __str__(self):
        return RANKS[self.rank()] + SUITS[self.suit()]

    def __repr__(self):
        return f'Card({self.idx})'

def opt_to_str(c: Optional[Card], placeholder="[]"):
    return f" {placeholder if c is None else c} "


    