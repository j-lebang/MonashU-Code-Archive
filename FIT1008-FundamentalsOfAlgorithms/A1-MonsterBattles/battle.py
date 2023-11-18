from __future__ import annotations
from enum import auto
from typing import Optional

from base_enum import BaseEnum
from team import MonsterTeam

# Unless stated otherwise, all methods in this classes are O(1) best/worst case
class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        self.verbosity = verbosity

    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.
        """
        player1 = self.team1.choose_action(self.out1, self.out2)
        player2 = self.team2.choose_action(self.out2, self.out1)

        if player1 == Battle.Action.SWAP:
            self.team1.add_to_team(self.out1) # B: O(1), W: O(N)
            self.out1 = self.team1.retrieve_from_team() # B: O(1), W: O(N)
        if player2 == Battle.Action.SWAP:
            self.team2.add_to_team(self.out2) # B: O(1), W: O(N)
            self.out2 = self.team2.retrieve_from_team() # B: O(1), W: O(N)
        if player1 == Battle.Action.SPECIAL:
            self.team1.special() # B: O(1), W: O(N)
        if player2 == Battle.Action.SPECIAL:
            self.team2.special() # B: O(1), W: O(N)
        if player1 == Battle.Action.ATTACK and player2 == Battle.Action.ATTACK:
            if self.out1.get_speed() > self.out2.get_speed():
                self.out1.attack(self.out2) # O(1)
                if self.out2.get_hp() > 0:
                    self.out2.attack(self.out1) # O(1)
            elif self.out1.get_speed() < self.out2.get_speed():
                self.out2.attack(self.out1) # O(1)
                if self.out1.get_hp() > 0:
                    self.out1.attack(self.out2) # O(1)
            else:
                self.out1.attack(self.out2) # O(1)
                self.out2.attack(self.out1) # O(1)
        elif player1 == Battle.Action.ATTACK:
            self.out1.attack(self.out2) # O(1)
        else:
            self.out2.attack(self.out1) # O(1)

        if self.out1.get_hp() > 0 and self.out2.get_hp() > 0:
            self.out1.set_hp(self.out1.get_hp() - 1) # O(1)
            self.out2.set_hp(self.out2.get_hp() - 1) # O(1)

        if self.out1.get_hp() > 0 and self.out2.get_hp() <= 0:
            self.out1.level_up() # O(1)
            self.out1 = self.out1.evolve() # O(1)
        if self.out2.get_hp() > 0 and self.out1.get_hp() <= 0:
            self.out2.level_up() # O(1)
            self.out2 = self.out2.evolve() # O(1)

        if self.out1.get_hp() <= 0 and len(self.team1) == 0 and self.out2.get_hp() <= 0 and len(self.team2) == 0:
            return Battle.Result.DRAW
        if self.out1.get_hp() <= 0 and len(self.team1) == 0:
            return Battle.Result.TEAM2
        if self.out2.get_hp() <= 0 and len(self.team2) == 0:
            return Battle.Result.TEAM1

        if self.out1.get_hp() <= 0:
            self.out1 = self.team1.retrieve_from_team() # B: O(1), W: O(N)
        if self.out2.get_hp() <= 0:
            self.out2 = self.team2.retrieve_from_team() # B: O(1), W: O(N)

    # Final Complexity:
    # Best Case: O(1)
    # Worst Case: O(N)

    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        # Add any postgame logic here.
        return result

if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
