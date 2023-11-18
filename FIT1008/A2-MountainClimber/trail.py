from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from data_structures.linked_stack import LinkedStack

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Trail
    bottom: Trail
    following: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.following.store     

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Removing the mountain at the beginning of this series.
        """
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain in series before the current one.
        """
        return TrailSeries(mountain, Trail(self))

    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        """
        return TrailSplit(Trail(None), Trail(None), Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        """
        temp = TrailSeries(mountain, self.following)
        return TrailSeries(self.mountain, Trail(temp))

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        """
        temp = TrailSplit(Trail(None), Trail(None), self.following)
        return TrailSeries(self.mountain, Trail(temp))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain before everything currently in the trail.
        """
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        """
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality.
        
        Complexity Analysis: N is the length of the longest complete path from start to finish 
        Best Case: O(1) when the decision is just a stop
        Worst Case: O(N) when we traverse the longest path from start to finish
        """
        from personality import PersonalityDecision
        
        # use stack to store following and then pop as you go
        stack = LinkedStack()
        stack.push(self)
        while len(stack):
            curr: Trail = stack.pop()
            in_curr: TrailStore = curr.store
            if isinstance(in_curr, TrailSplit):
                stack.push(in_curr.following)
                choice = personality.select_branch(in_curr.top, in_curr.bottom)
                if choice == PersonalityDecision.TOP:
                    stack.push(in_curr.top)
                if choice == PersonalityDecision.BOTTOM:
                    stack.push(in_curr.bottom)
                if choice == PersonalityDecision.STOP:
                    break  
            elif isinstance(in_curr, TrailSeries):
                stack.push(in_curr.following)
                personality.add_mountain(in_curr.mountain)
            else:
                continue
        
    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        if self.store is None:
            return []
        
        result = []
        
        if isinstance(self.store, TrailSeries):
            result += [self.store.mountain]
            result += self.store.following.collect_all_mountains()
        
        if isinstance(self.store, TrailSplit):
            result += self.store.top.collect_all_mountains()
            result += self.store.bottom.collect_all_mountains()
            result += self.store.following.collect_all_mountains()

        return result

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!

        if self.store is None:
            return [[]]
        
        invalid = Mountain("Invalid", -1, -1)
        result = []

        if isinstance(self.store, TrailSeries):
            mountain = self.store.mountain
            if mountain.difficulty_level > max_difficulty:
                return [[invalid]]

            mountains_fol = self.store.following.difficulty_maximum_paths(max_difficulty)
            for mt in mountains_fol:
                result.append([mountain] + mt)

        if isinstance(self.store, TrailSplit):
            mountains_top = self.store.top.difficulty_maximum_paths(max_difficulty)
            mountains_bot = self.store.bottom.difficulty_maximum_paths(max_difficulty)
            mountains_fol = self.store.following.difficulty_maximum_paths(max_difficulty)

            if (mountains_top == [[invalid]] and mountains_bot == [[invalid]]) or mountains_fol == [[invalid]]:
                return [[invalid]]

            if not mountains_top == [[invalid]]:
                for i in mountains_top:
                    for j in mountains_fol:
                        result.append(i + j)

            if not mountains_bot == [[invalid]]:
                for i in mountains_bot:
                    for j in mountains_fol:
                        result.append(i + j)

        return result

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        raise NotImplementedError()
