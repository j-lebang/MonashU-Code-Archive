import abc

from math import sqrt

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack

class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass


class SimpleStats(Stats):

    def __init__(self, attack, defense, speed, max_hp) -> None:
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_speed(self):
        return self.speed

    def get_max_hp(self):
        return self.max_hp

class ComplexStats(Stats):

    def __init__(
        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula

    def get_attack(self, level: int):
        temp = ArrayStack(len(self.attack_formula))
        for i in range(len(self.attack_formula)): # O(N)
            if self.attack_formula[i] == "+":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a + b)
            elif self.attack_formula[i] == "-":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a - b)
            elif self.attack_formula[i] == "*":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a * b)
            elif self.attack_formula[i] == "/":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a / b)
            elif self.attack_formula[i] == "level":
                temp.push(float(level))
            elif self.attack_formula[i] == "power":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a ** b)
            elif self.attack_formula[i] == "sqrt":
                a = float(temp.pop())
                temp.push(sqrt(a))
            elif self.attack_formula[i] == "middle":
                c = float(temp.pop())
                b = float(temp.pop())
                a = float(temp.pop())
                maxs = max(a, b, c)
                mins = min(a, b, c)
                if not (a == maxs or a == mins):
                    temp.push(a)
                elif not (b == maxs or b == mins):
                    temp.push(b)
                else:
                    temp.push(c)
            else:
                temp.push(float(self.attack_formula[i]))
        
        return int(temp.pop())

        # Final Complexity:
        # Best Case: O(N)
        # Worst Case: O(N)

    def get_defense(self, level: int):
        temp = ArrayStack(len(self.defense_formula))
        for i in range(len(self.defense_formula)): # O(N)
            if self.defense_formula[i] == "+":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a + b)
            elif self.defense_formula[i] == "-":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a - b)
            elif self.defense_formula[i] == "*":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a * b)
            elif self.defense_formula[i] == "/":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a / b)
            elif self.defense_formula[i] == "level":
                temp.push(float(level))
            elif self.defense_formula[i] == "power":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a ** b)
            elif self.defense_formula[i] == "sqrt":
                a = float(temp.pop())
                temp.push(sqrt(a))
            elif self.defense_formula[i] == "middle":
                c = float(temp.pop())
                b = float(temp.pop())
                a = float(temp.pop())
                maxs = max(a, b, c)
                mins = min(a, b, c)
                if not (a == maxs or a == mins):
                    temp.push(a)
                elif not (b == maxs or b == mins):
                    temp.push(b)
                else:
                    temp.push(c)
            else:
                temp.push(float(self.defense_formula[i]))
        
        return int(temp.pop())
    
        # Final Complexity:
        # Best Case: O(N)
        # Worst Case: O(N)

    def get_speed(self, level: int):
        temp = ArrayStack(len(self.speed_formula))
        for i in range(len(self.speed_formula)): # O(N)
            if self.speed_formula[i] == "+":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a + b)
            elif self.speed_formula[i] == "-":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a - b)
            elif self.speed_formula[i] == "*":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a * b)
            elif self.speed_formula[i] == "/":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a / b)
            elif self.speed_formula[i] == "level":
                temp.push(float(level))
            elif self.speed_formula[i] == "power":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a ** b)
            elif self.speed_formula[i] == "sqrt":
                a = float(temp.pop())
                temp.push(sqrt(a))
            elif self.speed_formula[i] == "middle":
                c = float(temp.pop())
                b = float(temp.pop())
                a = float(temp.pop())
                maxs = max(a, b, c)
                mins = min(a, b, c)
                if not (a == maxs or a == mins):
                    temp.push(a)
                elif not (b == maxs or b == mins):
                    temp.push(b)
                else:
                    temp.push(c)
            else:
                temp.push(float(self.speed_formula[i]))
        
        return int(temp.pop())
    
        # Final Complexity:
        # Best Case: O(N)
        # Worst Case: O(N)
    
    def get_max_hp(self, level: int):
        temp = ArrayStack(len(self.max_hp_formula))
        for i in range(len(self.max_hp_formula)): # O(N)
            if self.max_hp_formula[i] == "+":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a + b)
            elif self.max_hp_formula[i] == "-":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a - b)
            elif self.max_hp_formula[i] == "*":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a * b)
            elif self.max_hp_formula[i] == "/":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a / b)
            elif self.max_hp_formula[i] == "level":
                temp.push(float(level))
            elif self.max_hp_formula[i] == "power":
                b = float(temp.pop())
                a = float(temp.pop())
                temp.push(a ** b)
            elif self.max_hp_formula[i] == "sqrt":
                a = float(temp.pop())
                temp.push(sqrt(a))
            elif self.max_hp_formula[i] == "middle":
                c = float(temp.pop())
                b = float(temp.pop())
                a = float(temp.pop())
                maxs = max(a, b, c)
                mins = min(a, b, c)
                if not (a == maxs or a == mins):
                    temp.push(a)
                elif not (b == maxs or b == mins):
                    temp.push(b)
                else:
                    temp.push(c)
            else:
                temp.push(float(self.max_hp_formula[i]))
        
        return int(temp.pop())
    
        # Final Complexity:
        # Best Case: O(N)
        # Worst Case: O(N)
