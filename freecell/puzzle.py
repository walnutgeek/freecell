''' Generic Puzzle Solving Framework

License:  MIT
Author:   Raymond Hettinger

It was slightly modified to accomodate heustic and get rid 
of inheritace.
'''

from collections import deque
import heapq
from sys import intern
import re

def solve(pos, goal):
    queue = []
    heapq.heappush(queue, pos)
    trail = {intern(pos.canonical()): None}
    solution = deque()
    while pos != goal:
        for m in pos:
            c = m.canonical()
            if c in trail:
                continue
            trail[intern(c)] = pos
            heapq.heappush(queue,m)
        pos = heapq.heappop(queue)

    while pos:
        solution.appendleft(pos)
        pos = trail[pos.canonical()]

    return list(solution)