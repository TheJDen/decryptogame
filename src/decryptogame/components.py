import dataclasses
from copy import deepcopy
from collections.abc import Sequence
from enum import IntEnum

class TeamName(IntEnum):
    WHITE = 0
    BLACK = 1

@dataclasses.dataclass(kw_only=True)
class GameData:
    rounds_played: int = 0
    miscommunications: Sequence[int] = dataclasses.field(default_factory=lambda: [0, 0])
    interceptions: Sequence[int] = dataclasses.field(default_factory=lambda: [0, 0])

    def copy(self):
        return deepcopy(self)

@dataclasses.dataclass(kw_only=True)
class Note:
    clues: Sequence[tuple[str]] = None
    attempted_decipher: Sequence[int] = None
    attempted_interception: Sequence[int] = None
    correct_code: Sequence[int] = None
