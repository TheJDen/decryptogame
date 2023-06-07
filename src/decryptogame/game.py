import dataclasses
from collections.abc import Sequence

@dataclasses.dataclass(kw_only=True)
class Note:
    clues: Sequence[str] = None
    attempted_decipher: Sequence[int] = None
    attempted_interception: Sequence[int] = None
    correct_code: Sequence[int] = None


@dataclasses.dataclass(kw_only=True)
class Game:
    keywords: Sequence[Sequence[str]]
    notesheet: list[Sequence[Note]] = dataclasses.field(default_factory=list)
     
    def __post_init__(self):
        self.rounds_played = len(self.notesheet)
        self.miscommunications = [0, 0]
        self.interceptions = [0, 0]
        for round_notes in self.notesheet:
            self.process_round_notes(round_notes)
            
    def process_round_notes(self, round_notes):
        for team, note in enumerate(round_notes):
            opponent = not team
            if note.attempted_decipher != note.correct_code:
                self.miscommunications[team] += 1
            if note.attempted_interception == note.correct_code:
                self.interceptions[opponent] += 1

