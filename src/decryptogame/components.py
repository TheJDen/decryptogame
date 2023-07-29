import dataclasses
from copy import deepcopy
from collections.abc import Sequence
from enum import IntEnum

Keywords = Sequence[str]
Code = tuple[int]
Clue = tuple[str]

class TeamName(IntEnum):
    WHITE = 0
    BLACK = 1

    def __format__(self, spec):
        return f"<{self.name}: {self.value}>"

@dataclasses.dataclass(kw_only=True)
class GameData:
    rounds_played: int = 0
    miscommunications: Sequence[int] = dataclasses.field(default_factory=lambda: [0, 0])
    interceptions: Sequence[int] = dataclasses.field(default_factory=lambda: [0, 0])

    def copy(self):
        return deepcopy(self)

@dataclasses.dataclass(kw_only=True)
class Note:
    clues: Clue = None
    attempted_decipher: Code = None
    attempted_interception: Code = None
    correct_code: Code = None
