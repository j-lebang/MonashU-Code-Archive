from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.referential_array import ArrayR
from data_structures.queue_adt import CircularQueue
from data_structures.bset import BSet

# Unless stated otherwise, all methods in this classes are O(1) best/worst case
class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        self.battle = battle or Battle(verbosity=0)
        # self.elms = BSet()
        self.own_elements = False

    def set_my_team(self, team: MonsterTeam) -> None:
        # Generate the team lives here too.
        self.my_team = team
        self.my_lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)

        # self.my_elements = team

    def generate_teams(self, n: int) -> None:
        self.opponents_team = CircularQueue(n) 
        self.opponents_lives = CircularQueue(n)
        for i in range(n): # O(N)
            self.opponents_team.append(MonsterTeam(
                team_mode = MonsterTeam.TeamMode.BACK,
                selection_mode = MonsterTeam.SelectionMode.RANDOM
            )) # O(1)
            self.opponents_lives.append(RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)) # O(1)
        
        # Final Complexity:
        # Best Case: O(N)
        # Worst Case: O(N)

    def battles_remaining(self) -> bool:
        return len(self.opponents_team) > 0 and self.my_lives > 0 # O(1)

        # Final Complexity:
        # Best Case: O(1)
        # Worst Case: O(1)

    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        # if not self.own_elements:
        #     while len(self.my_elements):
        #         print(f"self.my_elements = {len(self.my_elements)}")
        #         a = self.my_elements.retrieve_from_team()
        #         print("= A =", a.get_name(), "|", a.get_element())
        #         self.elms.add(Element.from_string(a.get_element()).value)
        #     self.own_elements = True

        enemy_team: MonsterTeam = self.opponents_team.serve() # O(1)
        enemy_lives = self.opponents_lives.serve() # O(1)

        # self.my_elements.regenerate_team()
        self.my_team.regenerate_team() # B: O(N), W: O(N^2)
        enemy_team.regenerate_team() # B: O(N), W: O(N^2)

        # enemy_elements = CircularQueue(len(enemy_team))
        # temp = CircularQueue(len(enemy_team))
        # while len(enemy_team):
        #     var = enemy_team.retrieve_from_team()
        #     temp.append(var)
        #     enemy_elements.append(var)
        # enemy_team.array = temp

        # while len(enemy_elements):
        #     b = enemy_elements.serve()
        #     print("= B =", b.get_name(), "|", b.get_element())
        #     self.elms.add(Element.from_string(b.get_element()).value)

        results = self.battle.battle(self.my_team, enemy_team)
        if results == Battle.Result.TEAM1:
            enemy_lives -= 1
        elif results == Battle.Result.TEAM2:
            self.my_lives -= 1
        else:
            self.my_lives -= 1
            enemy_lives -= 1
        
        if enemy_lives > 0:
            self.opponents_team.append(enemy_team) # O(1)
            self.opponents_lives.append(enemy_lives) # O(1)

        return (results, self.my_team, enemy_team, self.my_lives, enemy_lives)
    
        # Final Complexity:
        # Best Case: O(N)
        # Worst Case: O(N^2)

    def out_of_meta(self) -> ArrayR[Element]:
        # next_enemy: MonsterTeam = self.opponents_team.peek()

        # elements = BSet()
        # while len(next_enemy):
        #     c = next_enemy.retrieve_from_team()
        #     print("= C =", c.get_name(), "|", c.get_element())
        #     elements.add(Element.from_string(c.get_element()).value)

        # res = self.elms.difference(elements)

        # ret = ArrayR(len(res))
        # x = 0
        # for element in Element:
        #     if element.value in res:
        #         ret[x] = element
        #         x += 1

        # return ret
        raise NotImplementedError

    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError

def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError

if __name__ == "__main__":

    RandomGen.set_seed(129371)

    bt = BattleTower(Battle(verbosity=3))
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    bt.generate_teams(3)

    for result, my_team, tower_team, player_lives, tower_lives in bt:
        print(result, my_team, tower_team, player_lives, tower_lives)
