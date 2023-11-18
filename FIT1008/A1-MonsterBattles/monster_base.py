from __future__ import annotations
import abc

from math import ceil

from stats import Stats

from elements import Element, EffectivenessCalculator

class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level:int=1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        """
        self.level = level

        if simple_mode:
            self.stats = self.get_simple_stats()
        else:
            self.stats = self.get_complex_stats()
        
        self.max_hp = self.get_max_hp()
        self.atk = self.get_attack()
        self.defense = self.get_defense()
        self.speed = self.get_speed()

        self.hp = self.max_hp
        self.element = self.get_element()
        self.name = self.get_name()
        self.desc = self.get_description()
        self.evo = self.get_evolution()
        self.level_change = 0

    def get_level(self):
        """The current level of this monster instance"""
        return self.level

    def level_up(self):
        """Increase the level of this monster instance by 1"""
        self.level += 1
        self.level_change += 1

    def get_hp(self):
        """Get the current HP of this monster instance"""
        self.hp = self.hp - self.max_hp + self.get_max_hp()
        return self.hp

    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        self.hp = val

    def get_attack(self):
        """Get the attack of this monster instance"""
        return self.stats.get_attack()

    def get_defense(self):
        """Get the defense of this monster instance"""
        return self.stats.get_defense()

    def get_speed(self):
        """Get the speed of this monster instance"""
        return self.stats.get_speed()

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        return self.stats.get_max_hp()

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        return self.hp > 0

    def attack(self, other: MonsterBase):
        """Attack another monster instance"""
        # Step 1: Compute attack stat vs. defense stat
        # Step 2: Apply type effectiveness
        # Step 3: Ceil to int
        # Step 4: Lose HP
        attack = self.get_attack()
        defense = other.get_defense()

        if defense < attack / 2:
            damage = attack - defense
        elif defense < attack:
            damage = attack * 5 / 8 - defense / 4
        else:
            damage = attack / 4

        element1 = self.get_element()
        element2 = other.get_element()

        my_element = Element.from_string(element1)
        other_element = Element.from_string(element2)

        damage *= EffectivenessCalculator.get_effectiveness(my_element, other_element)
        other.set_hp(other.get_hp() - ceil(damage))

    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        return bool(self.level_change)

    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        if self.ready_to_evolve() and not self.evo == None:
            monster = self.evo()
            monster.set_hp(monster.max_hp + self.hp - self.max_hp)
            while monster.get_level() < self.get_level():
                monster.level_up()
            return monster
        return self
    
    def __str__(self):
        return f"LV.{self.level} {self.name}, {self.get_hp()}/{self.max_hp} HP"

    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass
