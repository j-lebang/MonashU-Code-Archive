from __future__ import annotations
from mountain import Mountain

from mountain_organiser import *
from algorithms.binary_search import *
from algorithms.mergesort import *

class MountainManager(MountainOrganiser):

    def __init__(self) -> None:
        """
        * Declaring an empty list
        Complexity Analysis:
        Best Case: O(1)
        Worst Case: O(1)
        - For more details, look to `mountain_organiser.py`
        """
        super().__init__()

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Complexity Analysis: N is size of self.mountains
        Since we are adding one mountain at a time
        Best Case: O(N + 1) = O(N) since we are only adding one mountain at a time
        Worst Case: O(N + 1) = O(N) since we are only adding one mountain at a time
        - For more details, look to `mountain_organiser.py`
        """
        super().add_mountains([mountain]) # O(1log(1) + N) = O(N)

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Complexity Analaysis: N is size of self.mountains
        Best Case: O(N) due to list slicing
        Worst Case: O(N) due to list slicing
        """
        idx = super().cur_position(mountain) # O(1) / O(log(N))
        self.mountains = self.mountains[:idx] + self.mountains[idx + 1:] # O(N)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        """
        Complexity Analaysis: N is size of self.mountains
        Best Case: O(1) when the item searched is in the middle of self.mountains
        Worst Case: O(log(N)) when item searched is not in self.mountains or at the first or last index
        """
        idx = super().cur_position(old) # O(1) / O(log(N))
        self.mountains[idx] = new

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        """
        * Binary search left and right index to find left and right border
        Complexity Analysis: N is length of self.mountains
        Best Case: O(log(N)) * 2 = O(log(N)) due to binary search. This complexity
                   is achieved when (r_idx - l_idx + 1) < log(N) or when l_idx and
                   r_idx is -1
        Worst Case: O(N) When all difficulty is the same so the result 
                    list is just the original list (due to slicing)
        """
        l_idx, r_idx = -1, -1

        l, r = 0, len(self.mountains) - 1
        while l <= r: # O(log(N))
            mid = l + r >> 1
            if self.mountains[mid].difficulty_level == diff:
                l_idx = mid
                r = mid - 1
            elif self.mountains[mid].difficulty_level > diff:
                r = mid - 1
            else:
                l = mid + 1

        l, r = 0, len(self.mountains) - 1
        while l <= r: # O(log(N))
            mid = l + r >> 1
            if self.mountains[mid].difficulty_level == diff:
                r_idx = mid
                l = mid + 1
            elif self.mountains[mid].difficulty_level > diff:
                r = mid - 1
            else:
                l = mid + 1

        if l_idx == -1 or r_idx == -1:
            return [] # O(1)
        return self.mountains[l_idx : r_idx + 1] # O(N)

    def group_by_difficulty(self) -> list[list[Mountain]]:
        """
        * Use two pointer
        Complexity Analysis: N is size of self.mountains
        Best Case: O(N)
        Worst Case: O(N)
        """
        result = []
        l, r = 0, 0
        for i in range(len(self.mountains)): # O(N)
            if self.mountains[i].difficulty_level == self.mountains[l].difficulty_level:
                r += 1
            else:
                result.append(self.mountains[l : r])
                l = r
                r += 1
        result.append(self.mountains[l : r])
        # The sum of all (r - l) when appending to result will be N

        return result