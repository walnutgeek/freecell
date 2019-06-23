# FREECELL

Curing my addiction to freecell, by solving them all.

## Run
```
python -m freecell.game 169 > solution.txt
```
## Inspirations

### Raymond Hettinger talk on US Pycon 2019

[Slides](https://rhettinger.github.io/index.html)

[Video](https://www.youtube.com/watch?v=_GP9OpZPUYc)

Breadth-first search was not be able to cut it because because search space become too big at the end of te game. Sightly modified to add heuristic.


### Microsoft Shuffle Algorithm

Ported from leagcy python sourced form: 
[rosettacode.org: Deal cards for FreeCell](https://rosettacode.org/wiki/Deal_cards_for_FreeCell#Python)

Usage:
```
> python -m freecell.shuffle
Hand 11982
  AH AS 4H AC 2D 6S TS JS
  3D 3H QS QC 8S 7H AD KS
  KD 6H 5S 4D 9H JH 9S 3C
  JC 5D 5C 8C 9D TD KH 7C
  6C 2C TH QH 6D TC 4S 7S
  JD 7D 8H 9C 2H QD 4C 5H
  KC 8D 2S 3S
> python -m freecell.shuffle 31465
Hand 31465
  4H QH 6D QD 3S 5S 9C 5C
  JH 8C AD AH JC 2H 5H AS
  9H TS JS 8S KH 2C 9S 7C
  JD 4S 7H 4D 2D 7D 4C KD
  TC 7S 6H 5D 8D 3C 6S 8H
  6C KC TD TH AC 2S 3H QS
  KS 3D QC 9D
>
```