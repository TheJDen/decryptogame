import dataclasses

@dataclasses.dataclass(kw_only=True)
class Game:
    scores: list[int] = dataclasses.field(default_factory=lambda:[0,0])
    miscommunications: list[int] = dataclasses.field(default_factory=lambda:[0,0])
    interceptions: list[int] = dataclasses.field(default_factory=lambda:[0,0])