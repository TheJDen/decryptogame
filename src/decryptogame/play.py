from collections.abc import Iterable, Sequence
from decryptogame.components import Code, Note
from decryptogame.game import Game
from decryptogame.generators import RandomCodes
from decryptogame.teams import Team
from typing import Optional
    
def play_game(teams: Sequence[Team], *, game: Game = None, round_codes: Iterable[Sequence[Code]] = None, round_limit: Optional[int]=None):
    """Play a game of Decrypto.

    Args:
        teams (Sequence[Team]): The pair of teams participating in the game.
        game (Game): The Decrypto game object. If None, a standard game will be generated.
        round_codes (Iterable[Sequence[Code]], optional): Iterable of codes for each round. If None, random codes will be generated.
        round_limit (Optional[int], optional): The maximum number of rounds to play. If None, the game continues until completion.
    """
    game = game if game is not None else Game()
    round_codes = round_codes if round_codes is not None else RandomCodes(game.keyword_cards)
    for rounds_played, codes in enumerate(round_codes):
        if game.game_over() or rounds_played == round_limit:
            return
        play_round(game, teams, codes)


def play_round(game: Game, teams:Sequence[Team], codes: Sequence[Code]):
    """Play a single round of Decrypto.

    Args:
        game (Game): The Decrypto game object.
        teams (Sequence[Team]): The pair of teams participating in the game.
        codes (Sequence[Code]): The codes for the current round.
    """
    # each team's encryptor decides the clues
    clues = {}
    for team_name, code in enumerate(codes):
        clues[team_name] = teams[team_name].encryptor.decide_clues(team_name, game, code)

    # each team attempts to intercept the opposing team's code
    attempted_interception = {}
    for team_name, code in enumerate(codes):
        opponent = not team_name
        attempted_interception[team_name] = teams[team_name].intercepter.intercept_clues(team_name, game, clues[opponent])

    # each team attempts to decipher the clues to their code
    attempted_decipher = {}
    for team_name, code in enumerate(codes):
        attempted_decipher[team_name] = teams[team_name].guesser.decipher_clues(team_name, game, clues[team_name])

    # each team reveals their codes and the notes are processed and added to the notesheet
    notes = [Note(clues=clues[team_name],
                  attempted_interception=attempted_interception[team_name],
                  attempted_decipher=attempted_decipher[team_name],
                  correct_code=code
                  ) 
                  for team_name, code in enumerate(codes)]
    game.process_round_notes(notes)
    game.notesheet.append(notes)