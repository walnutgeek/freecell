from sys import argv
from functools import total_ordering
from freecell import Card, opt_to_str, DECK_SIZE
from freecell.puzzle import solve
import freecell.shuffle as shuffle
from typing import Tuple, Optional, Any

def tuple_set(elems:Tuple[Any], i:int, v:Any, i2:Optional[int]=None, v2:Any=None)->Tuple[Any]:
    stage = list(elems)
    stage[i] = v
    if i2 is not None:
        stage[i2] = v2
    return tuple(stage)

@total_ordering
class Position:
    tableau: Tuple[Tuple[Card]]
    free_cells: Tuple[Optional[Card]] 
    home_cells: Tuple[Optional[Card]] 



    def __init__(self, tableau: Tuple[Tuple[Card]], 
                 free_cells: Tuple[Optional[Card]], 
                 home_cells: Tuple[Optional[Card]]):
        """    
        >>> Position(((),(),(),(),(),(),(),()), (None,None,None,Card(0)), (None,None,None,None))
        Position(((), (), (), (), (), (), (), ()), (Card(0), None, None, None), (None, None, None, None))
        >>> Position(((),(),(),(),(),(),(),()), (Card(3),Card(2),Card(1),Card(0)), (None,None,None,None))
        Position(((), (), (), (), (), (), (), ()), (Card(0), Card(1), Card(2), Card(3)), (None, None, None, None))

        """
        assert len(tableau) == 8
        assert len(free_cells) == 4
        assert len(home_cells) == 4        
        self.tableau = tableau
        self.free_cells = tuple(sorted(free_cells, key=lambda x: (x is None, x)))
        self.home_cells = home_cells
        self._repr = f"Position({tuple(sorted(self.tableau))!r}, {self.free_cells!r}, {self.home_cells!r})"
        value = sum(len(c) for c in self.tableau) + sum(1.1 for _ in filter(None.__ne__, self.free_cells))
        self._key = (value, self._repr)

    @staticmethod
    def deal(seed:int)->"Position":
        cards = shuffle.deal(seed)
        end = len(cards)
        return Position( 
            tuple( tuple( cards[i] for i in range(start, end, 8)) for start in range(8)),
            (None,None,None,None),
            (None,None,None,None))

    def has_free_cell(self):
        """
        >>> Position(((),(),(),(),(),(),(),()), (None,None,None,Card(0)), (None,None,None,None)).has_free_cell()
        True
        >>> Position(((),(),(),(),(),(),(),()), (Card(3),Card(2),Card(1),Card(0)), (None,None,None,None)).has_free_cell()
        False
        """
        return self.free_cells[-1] is None

    def home_move(self, card: Card) -> Tuple[Optional[Card]]:
        suit = card.suit()
        home = self.home_cells[suit]
        home_rank = -1 if home is None else home.rank()
        if card.rank() - 1 == home_rank:
            return tuple_set(self.home_cells, suit, card)

    def tabcolumn_move(self, card: Card, column:int) -> Tuple[Card]:
        tabcolumn = self.tableau[column]
        if tabcolumn:
            last_card = tabcolumn[-1]
            if last_card.color() == card.color() or last_card.rank() - 1 != card.rank():
                return None
        return tabcolumn + (card,)

    

    def __repr__(self):
        """
        >>> Position.deal(11982) # doctest: +NORMALIZE_WHITESPACE
        Position(((Card(0), Card(44), Card(13), Card(28), Card(46), Card(32), Card(11)), 
        (Card(2), Card(9), Card(49), Card(40), Card(20), Card(41), Card(48)), 
        (Card(3), Card(10), Card(22), Card(17), Card(4), Card(25), Card(29)), 
        (Card(5), Card(31), Card(34), Card(33), Card(21), Card(6)), 
        (Card(14), Card(47), Card(19), Card(16), Card(38), Card(30), Card(7)), 
        (Card(23), Card(26), Card(42), Card(37), Card(36), Card(45)), 
        (Card(39), Card(1), Card(35), Card(50), Card(15), Card(12)), 
        (Card(43), Card(51), Card(8), Card(24), Card(27), Card(18))), 
        (None, None, None, None), (None, None, None, None))        
        """
        return self._repr

    def canonical(self):        # returns a string representation after adjusting for symmetry
        return repr(self)

    def __lt__(self,other):
        return self._key < other._key

    def __eq__(self,other):
        return self._key == other._key

    def __ne__(self,other):
        return self._key != other._key

    def __str__(self):
        """
        >>> print(str(GOAL)) # doctest: +NORMALIZE_WHITESPACE
         []  []  []  []       KC  KD  KH  KS
        >>> print(str(Position.deal(11982))) # doctest: +NORMALIZE_WHITESPACE
         []  []  []  []       []  []  []  []
         AH  AS  4H  AC  2D  6S  TS  JS
         3D  3H  QS  QC  8S  7H  AD  KS
         KD  6H  5S  4D  9H  JH  9S  3C
         JC  5D  5C  8C  9D  TD  KH  7C
         6C  2C  TH  QH  6D  TC  4S  7S
         JD  7D  8H  9C  2H  QD  4C  5H
         KC  8D  2S  3S
        >>> print(str(Position.deal(31465))) # doctest: +NORMALIZE_WHITESPACE
         []  []  []  []       []  []  []  []
         4H QH 6D QD 3S 5S 9C 5C
         JH 8C AD AH JC 2H 5H AS
         9H TS JS 8S KH 2C 9S 7C
         JD 4S 7H 4D 2D 7D 4C KD
         TC 7S 6H 5D 8D 3C 6S 8H
         6C KC TD TH AC 2S 3H QS
         KS 3D QC 9D
        """
        s = "".join( opt_to_str(c) for c in self.free_cells) + "     "
        s += "".join( opt_to_str(c) for c in self.home_cells) + "\n\n"
        empty = False
        row = 0
        while not empty:
            data = tuple( self.tableau[col][row] if row < len(self.tableau[col]) else None for col in range(8))
            s += "".join(opt_to_str(n,"  ") for n in data) + "\n"
            empty = not any(data)
            row += 1
        return s

    def __iter__(self):
        #free_cells -> home_cells (4)
        p:Position = self
        for i in range(4):
            c = p.free_cells[i]
            if c is not None:
                new_home = p.home_move(c)
                if new_home is not None:
                    yield Position(p.tableau, tuple_set(p.free_cells, i, None), new_home)
        #tableau -> home_cells (8)
        for i in range(8):
            if p.tableau[i]:
                c = p.tableau[i][-1]
                new_home = p.home_move(c)
                if new_home is not None:
                    yield Position(tuple_set(p.tableau, i, p.tableau[i][:-1]), p.free_cells, new_home)
        #tableau -> free_cells (8)
        if p.has_free_cell():
            for i in range(8):
                if p.tableau[i]:
                    yield Position(tuple_set(p.tableau, i, p.tableau[i][:-1]), 
                                   tuple_set(p.free_cells, -1, p.tableau[i][-1]), p.home_cells)

        #free_cells -> tableau (4*8)
        for cell in range(4):
            card = p.free_cells[cell]
            if card is not None:
                for col in range(8):
                    tabcolumn = p.tabcolumn_move(card, col)
                    if tabcolumn is not None:
                        yield Position(tuple_set(p.tableau, col, tabcolumn), 
                        tuple_set(p.free_cells, cell, None), p.home_cells)

        #tableau -> tableau (8*7)
        for from_col in range(8):
            for to_col in range(8):
                if from_col != to_col and p.tableau[from_col]:
                    card = p.tableau[from_col][-1]
                    tabcolumn = p.tabcolumn_move(card, to_col)
                    if tabcolumn:
                        yield Position(tuple_set(p.tableau, to_col, tabcolumn, from_col, p.tableau[from_col][:-1]),
                            p.free_cells, p.home_cells)


GOAL = Position(((),(),(),(),(),(),(),()), (None,None,None,None), 
            (Card(48),Card(49),Card(50),Card(51)))




if __name__ == "__main__":
        seed = int(argv[1]) if len(argv) == 2 else 11982
        solution = solve(Position.deal(seed), GOAL)
        for step in solution:
            print(str(step))
        print(len(solution))
                

        
    
    
        