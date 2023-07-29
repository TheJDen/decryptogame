from collections.abc import Sequence
from decryptogame.components import Keywords, GameData, Note, TeamName
from decryptogame.end_criteria import EndCondition, OfficialEndConditions
from typing import Optional

def miscommunication_rule(note: Note, data: GameData) -> int:
    return 1 if note.attempted_decipher != note.correct_code else 0

def interception_rule(note: Note, data=GameData, count_first_round=False) -> int:
    if data.rounds_played == 0 and not count_first_round:
        return 0
    return 1 if note.attempted_interception == note.correct_code else 0

def interception_miscommunication_diff_tiebreaker(game_data: GameData) -> Optional[TeamName]:
    """Tiebreaker which decides the winner by the greatest difference between the team's number of interception tokens and miscommunication tokens. If this is also a tie, it yields a tie."""
    scores = [interceptions - miscommunications for interceptions, miscommunications in zip(game_data.interceptions, game_data.miscommunications)]
    if scores[TeamName.WHITE] == scores[TeamName.BLACK]:
        return None
    return TeamName(scores.index(max(scores)))

class Game:        
    def __init__(self, *,
                 keyword_cards: Sequence[Keywords],
                 notesheet: list[Sequence[Note]] = None,
                 end_conditions: list[EndCondition] = None,
                 miscommunication_func = miscommunication_rule,
                 interception_func = interception_rule,
                 tiebreaker_func = interception_miscommunication_diff_tiebreaker
                 ):
        self.keyword_cards = keyword_cards
        self.notesheet = notesheet if notesheet is not None else []
        self.end_conditions = end_conditions if end_conditions is not None else OfficialEndConditions()
        self.miscommunication_func = miscommunication_func
        self.interception_func  = interception_func 
        self.tiebreaker_func = tiebreaker_func
        # initialize game data based on round notes
        self._data = GameData()
        for round_notes in self.notesheet:
            if self.game_over():
                break
            self.process_round_notes(round_notes)


    @property
    def data(self) -> GameData:
        # data shouldn't be altered for simulating plies or viewing round results
        # so accessing yields a copy to minimize unintended side effects
        return self._data.copy()
    

    def process_round_notes(self, round_notes: list[Note]):
        for team_name, note in enumerate(round_notes):
            opponent = not team_name
            self._data.miscommunications[team_name] += self.miscommunication_func(note, self._data)
            self._data.interceptions[opponent] += self.interception_func(note, self._data)
        self._data.rounds_played += 1


    def game_over(self, game_data: GameData = None) -> bool:
        # if called without an argument, use internal data
        game_data = game_data if game_data is not None else self._data
        return any(end_condition.game_over(game_data) for end_condition in self.end_conditions)
    

    def winner(self, game_data: GameData = None) -> Optional[int]:
        # if called without an argument, use internal data
        game_data = game_data if game_data is not None else self._data
        
        # if the game is not over, there is no winner
        if not self.game_over(game_data):
            return None
        
        candidate_winners = [end_condition.winner(game_data) for end_condition in self.end_conditions]
        unique_winners = {candidate for candidate in candidate_winners if candidate is not None}

        losers = [end_condition.loser(game_data) for end_condition in self.end_conditions]
        corresponding_winners = {not loser for loser in losers if loser is not None}
        
        unique_winners.update(corresponding_winners)
        
        # if the game the game ending conditions decide exactly one winner, they are the winner
        if len(unique_winners) == 1:
            return unique_winners.pop()
        
        # otherwise, decide by tiebreaker (can return None to indicate tie anyway)
        return self.tiebreaker_func(game_data)