from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    def __eq__(self, other: Mountain) -> bool:
        return (
            self.name == other.name and
            self.difficulty_level == other.difficulty_level and
            self.length == other.length
        )

    def __lt__(self, other: Mountain) -> bool:
        if self.difficulty_level == other.difficulty_level:
            return self.name < other.name
        return self.difficulty_level < other.difficulty_level
    
    def __gt__(self, other: Mountain) -> bool:
        if self.difficulty_level == other.difficulty_level:
            return self.name > other.name
        return self.difficulty_level > other.difficulty_level
    
    def __le__(self, other: Mountain) -> bool:
        return self < other or self == other
    
    def __ge__(self, other: Mountain) -> bool:
        return self > other or self == other