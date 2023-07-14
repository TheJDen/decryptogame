import abc
from collections import Counter
from decryptogame.game import GameData
from decryptogame.components import TeamName
from typing import Optional

MAX_OFFICIAL_MISCOMMUNICATIONS = 2
MAX_OFFICIAL_INTERCEPTIONS = 2
MAX_OFFICIAL_ROUNDS = 8

class EndCondition(abc.ABC):
    """Interface representing a condition under which a game may end."""

    @abc.abstractmethod
    def game_over(game_data: GameData) -> bool:
        pass
    
    @abc.abstractmethod
    def winner(game_data: GameData) -> Optional[TeamName]:
        pass

    @abc.abstractmethod
    def loser(game_data: GameData) -> Optional[TeamName]:
        pass


class MiscommunicationEndCondition(EndCondition):
    """End condition representing that a game ends if a team has k miscommunication tokens, in which case it loses."""
    
    def __init__(self, k: int = MAX_OFFICIAL_MISCOMMUNICATIONS):
        self.k = k

    def game_over(self, game_data: GameData) -> bool:
        return any(miscommunications == self.k for miscommunications in game_data.miscommunications)
    
    def winner(self, game_data: GameData) -> Optional[TeamName]:
        return None
    
    def loser(self, game_data: GameData) -> Optional[TeamName]:
        # if the game has not finished or multiple players lose, the loser is undecided 
        if not self.game_over(game_data) or Counter(game_data.miscommunications)[self.k] > 1:
            return None
        loser = game_data.miscommunications.index(self.k)
        return TeamName(loser)
        

class InterceptionEndCondition(EndCondition):
    """End condition representing that a game ends if a team has k interception tokens, in which case it wins."""

    def __init__(self, k: int = MAX_OFFICIAL_INTERCEPTIONS):
        self.k = k

    def game_over(self, game_data: GameData) -> bool:
        return any(interceptions == self.k for interceptions in game_data.interceptions)
    
    def winner(self, game_data: GameData) -> Optional[TeamName]:
        # if the game has not finished or multiple players win, the winner is undecided 
        if not self.game_over(game_data) or Counter(game_data.interceptions)[self.k] > 1:
            return None
        winner = game_data.interceptions.index(self.k)
        return TeamName(winner)
    
    def loser(self, game_data: GameData) -> Optional[TeamName]:
        return None


class RoundEndCondition(EndCondition):
    """End condition representing that a game ends if it reaches k rounds, in which case no winner or loser is decided."""

    def __init__(self, k: int = MAX_OFFICIAL_ROUNDS):
        self.k = k

    def game_over(self, game_data: GameData) -> bool:
        return game_data.rounds_played == self.k
    
    def winner(self, game_data: GameData) -> Optional[TeamName]:
        return None
    
    def loser(self, game_data: GameData) -> Optional[TeamName]:
        return None
    
official_end_condition_constructors = [RoundEndCondition, MiscommunicationEndCondition, InterceptionEndCondition]

def interception_miscommunication_diff_tiebreaker(game_data: GameData) -> Optional[TeamName]:
    """Tiebreaker which decides the winner by the greatest difference between the team's number of interception tokens and miscommunication tokens. If this is also a tie, it yields a tie."""
    scores = [interceptions - miscommunications for interceptions, miscommunications in zip(game_data.interceptions, game_data.miscommunications)]
    if scores[0] == scores[1]:
        return None
    return TeamName(scores.index(max(scores)))