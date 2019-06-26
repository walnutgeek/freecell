from sys import argv
from typing import List

from freecell import DECK_SIZE, Card


def randomGenerator(seed=1):
    max_int32 = (1 << 31) - 1
    seed = seed & max_int32
    while True:
        seed = (seed * 214013 + 2531011) & max_int32
        yield seed >> 16


def deal(seed) -> List[Card]:
    """
    >>> sorted(deal(11982)[:6])
    [Card(0), Card(2), Card(3), Card(5), Card(14), Card(23)]
    """
    cards = list(map(Card, range(DECK_SIZE - 1, -1, -1)))
    rnd = randomGenerator(seed)
    for i, r in zip(range(DECK_SIZE), rnd):
        j = (DECK_SIZE - 1) - r % (DECK_SIZE - i)
        cards[i], cards[j] = cards[j], cards[i]
    return cards


def show(cards):
    l = [str(c) for c in cards]
    for i in range(0, len(cards), 8):
        print(" ", " ".join(l[i : i + 8]))


if __name__ == "__main__":
    seed = int(argv[1]) if len(argv) == 2 else 11982
    print("Hand", seed)
    deck = deal(seed)
    show(deck)
