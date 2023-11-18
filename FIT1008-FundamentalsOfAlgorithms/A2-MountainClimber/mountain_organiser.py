from __future__ import annotations

from mountain import Mountain
from algorithms.binary_search import *
from algorithms.mergesort import *

class MountainOrganiser:

    def __init__(self) -> None:
        """
        Complexity Analysis:
        Best Case: O(1)
        Worst Case: O(1)
        """
        self.mountains = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        Complexity Analaysis: N is size of self.mountains
        Best Case: O(1) when the item searched is in the middle of self.mountains
        Worst Case: O(log(N)) when item searched is not in self.mountains or at the first or last index
        """
        idx = binary_search(self.mountains, mountain) # O(1) / O(log(N))
        if self.mountains[idx] == mountain:
            return idx
        raise KeyError

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Complexity Analysis: M is size of mountains, N is size of self.mountains
        Best Case: O(Mlog(M) + M + N) = O(Mlog(M) + N) [Because of dominant terms]
        Worst Case: O(Mlog(M) + M + N) = O(Mlog(M) + N) [Because of dominant terms]
        """
        mountains = mergesort(mountains) # O(Mlog(M))
        self.mountains = merge(self.mountains, mountains) # O(N + M)
