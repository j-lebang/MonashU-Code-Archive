from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR

from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.sorted_list_adt import ListItem
from data_structures.array_sorted_list import ArraySortedList

if TYPE_CHECKING:
    from battle import Battle

# Unless stated otherwise, all methods in this classes are O(1) best/worst case
class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, sort_key: SortMode = SortMode.HP, team_limit = 6, **kwargs) -> None:
        self.TEAM_LIMIT = team_limit
        
        if team_mode.value == 1:
            self.array = ArrayStack(self.TEAM_LIMIT)
        if team_mode.value == 2:
            self.array = CircularQueue(self.TEAM_LIMIT)
        if team_mode.value == 3:
            self.array = ArraySortedList(self.TEAM_LIMIT)
            self.sortBy = sort_key.value
            self.reversed = 0
        # Add any preinit logic here.
        self.team_mode = team_mode.value
        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly(**kwargs)
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually(**kwargs)
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(**kwargs)
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")

    def add_to_team(self, monster: MonsterBase):
        if self.team_mode == 1:
            self.array.push(monster) # O(1)
        if self.team_mode == 2:
            self.array.append(monster) # O(1)
        if self.team_mode == 3:
            if self.sortBy == 1: # HP
                self.array.add(ListItem(monster, monster.get_hp())) # B: O(log N), W: O(N)
            if self.sortBy == 2: # ATTACK
                self.array.add(ListItem(monster, monster.get_attack())) # B: O(log N), W: O(N)
            if self.sortBy == 3: # DEFENSE
                self.array.add(ListItem(monster, monster.get_defense())) # B: O(log N), W: O(N)
            if self.sortBy == 4: # SPEED
                self.array.add(ListItem(monster, monster.get_speed())) # B: O(log N), W: O(N)
            if self.sortBy == 5: # LEVEL
                self.array.add(ListItem(monster, monster.get_level())) # B: O(log N), W: O(N)

        # Final Complexity:
        # Best Case: O(1)
        # Worst Case: O(N)

    def retrieve_from_team(self) -> MonsterBase:
        if self.team_mode == 1:
            return self.array.pop() # O(1)
        if self.team_mode == 2:
            return self.array.serve() # O(1)
        if self.team_mode == 3:
            if not self.reversed:
                return self.array.delete_at_index(len(self.array) - 1).value # O(log N)
            return self.array.delete_at_index(0).value # O(N)
        
        # Final Complexity:
        # Best Case: O(1)
        # Worst Case: O(N)

    def special(self) -> None:
        if self.team_mode == 1:
            temp = ArrayR(self.TEAM_LIMIT)
            n = min(len(self.array), 3)
            for i in range(n): # O(1)
                temp[i] = self.array.pop() # O(1)
            for i in range(n): # O(1)
                self.array.push(temp[i]) # O(1)

        if self.team_mode == 2:
            n = len(self.array)
            tempQueue = CircularQueue(n // 2)
            tempStack = ArrayStack((n + 1) // 2)
            for i in range(n // 2): # O(N)
                tempQueue.append(self.array.serve()) # O(1)
            while len(self.array): # O(N)
                tempStack.push(self.array.serve()) # O(1)
            
            while len(tempStack): # O(N)
                self.array.append(tempStack.pop()) # O(1)
            while len(tempQueue): # O(N)
                self.array.append(tempQueue.serve()) # O(1)

        if self.team_mode == 3:
            self.reversed = 1 - self.reversed # O(1)

        # Final Complexity:
        # Best Case: O(1)
        # Worst Case: O(N)


    def regenerate_team(self) -> None:
        while len(self.array): # O(N)
            self.retrieve_from_team() # B: O(1), W: O(N)
        temp = CircularQueue(len(self.initial))
        while len(self.initial): # O(N)
            front = self.initial.serve() # O(1)
            self.add_to_team(front) # B: O(1), W: O(N)
            temp.append(front) # O(1)
        self.initial = temp
        self.reversed = 0

        # Final Complexity:
        # Best Case: O(N)
        # Worst Case: O(N^2)

    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        self.initial = CircularQueue(team_size)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.initial.append(monsters[x]())
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        """
        monsters = get_all_monsters()

        team_size = -1
        while team_size == -1 or team_size > self.TEAM_LIMIT:
            team_size = int(input("How many monsters are there?"))
            if (team_size > self.TEAM_LIMIT):
                team_size = -1
                continue
            
        self.initial = CircularQueue(team_size)
        
        cnt = 1
        while cnt <= team_size: # O(N)
            print(f"MONSTERS Are:")
            num = 1
            for monster in monsters:
                print(f"{num}: {monster.get_name()} [{'❌' if monster.can_be_spawned() else '✔️'}]")
                num += 1

            inp = int(input("Which monster are you spawning?"))
            while not monsters[inp - 1].can_be_spawned():
                print(f"This monster cannot be spawned.")
                inp = int(input("Which monster are you spawning?"))
            
            self.initial.append(monsters[inp - 1]())
            self.add_to_team(monsters[inp - 1]())
            cnt += 1

        # Final Complexity:
        # Best Case: O(N)
        # Worst Case: O(N)
            

    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        """
        if len(provided_monsters) > self.TEAM_LIMIT:
            raise ValueError

        self.initial = CircularQueue(len(provided_monsters))
        for i in provided_monsters: # O(N)
            if not i.can_be_spawned():
                raise ValueError
            self.initial.append(i()) # O(1)
            self.add_to_team(i()) # B: O(1), W: O(N)

        # Final Complexity:
        # Best Case: O(N)
        # Worst Case: O(N^2)

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP
    
    def __len__(self):
        return len(self.array)

if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())
