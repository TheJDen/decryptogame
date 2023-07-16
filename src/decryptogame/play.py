from collections.abc import Iterable, Sequence
from decryptogame.components import Code, Note
from decryptogame.game import Game
from decryptogame.generators import RandomCodes
from decryptogame.teams import Team
from typing import Optional
    
def play_game(game: Game, teams: Sequence[Team], *, round_codes: Iterable[Sequence[Code]] = None, round_limit: Optional[int]=None):
    round_codes = round_codes if round_codes is not None else RandomCodes(game.keyword_cards)
    for rounds_played, codes in enumerate(round_codes):
        if game.game_over() or rounds_played == round_limit:
            return
        play_round(game, teams, codes)


def play_round(game: Game, teams:Sequence[Team], codes: Sequence[Code]):

    notes = [Note(), Note()]

    # each team's encryptor decides the clues and they are written on their team's note
    for team_name, code in enumerate(codes):
        notes[team_name].clues = teams[team_name].encryptor.decide_clues(team_name, game, code)

    # each team attempts to intercept the opposing team's code
    for team, code in enumerate(codes):
        opponent = not team
        notes[team].attempted_interception = teams[team].intercepter.intercept_clues(team_name, game, notes[opponent].clues)

    # each team attempts to decipher the clues to their code
    for team, code in enumerate(codes):
        notes[team].attempted_decipher = teams[team].guesser.decipher_clues(team_name, game, notes[team].clues)

    # each team reveals their codes
    for team, code in enumerate(codes):
        notes[team].correct_code = codes[team]

    # the notes are processed and added to the notesheet
    game.process_round_notes(notes)
    game.notesheet.append(notes)