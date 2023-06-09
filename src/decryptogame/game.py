import dataclasses
from collections.abc import Callable, Sequence
from decryptogame.rules import round_condition, miscommunication_condition, interception_condition


@dataclasses.dataclass(kw_only=True)
class Note:
    clues: Sequence[str] = None
    attempted_decipher: Sequence[int] = None
    attempted_interception: Sequence[int] = None
    correct_code: Sequence[int] = None


@dataclasses.dataclass(kw_only=True)
class GameData:
    rounds_played: int = 0
    miscommunications: Sequence[int] = dataclasses.field(default_factory=lambda: [0, 0])
    interceptions: Sequence[int] = dataclasses.field(default_factory=lambda: [0, 0])


@dataclasses.dataclass(kw_only=True)
class Game:
    keywords: Sequence[Sequence[str]]
    notesheet: list[Sequence[Note]] = dataclasses.field(default_factory=list)
    end_conditions: list[Callable[[GameData], bool]] = dataclasses.field(default_factory=lambda: [round_condition, miscommunication_condition, interception_condition])
    def __post_init__(self):
        self.data = GameData()
        for round_notes in self.notesheet:
            self.process_round_notes(round_notes)
            
    def process_round_notes(self, round_notes):
        for team, note in enumerate(round_notes):
            opponent = not team
            if note.attempted_decipher != note.correct_code:
                self.data.miscommunications[team] += 1
            if note.attempted_interception == note.correct_code:
                self.data.interceptions[opponent] += 1
        self.data.rounds_played += 1

    def game_over(self, game_data=None):
        if game_data is None: # if called without an argument, use internal data
            return self.game_over(self.data)
        return any(end_condition(game_data) for end_condition in self.end_conditions)
