import abc
from collections import Counter
from decryptogame.game import GameData

MAX_OFFICIAL_MISCOMMUNICATIONS = 2
MAX_OFFICIAL_INTERCEPTIONS = 2
MAX_OFFICIAL_ROUNDS = 8

class EndCondition(abc.ABC):
    @abc.abstractmethod
    def game_over(game_data: GameData) -> bool:
        pass
    @abc.abstractmethod
    def winner(game_data: GameData) -> int:
        pass


# game ends if a team has k miscommunication tokens, in which case it loses
class MiscommunicationEndCondition(EndCondition):
    def __init__(self, k: int = MAX_OFFICIAL_MISCOMMUNICATIONS):
        self.k = k

    def game_over(self, game_data: GameData) -> bool:
        return any(miscommunications == self.k for miscommunications in game_data.miscommunications)
    
    def winner(self, game_data: GameData) -> int:
        if not self.game_over(game_data) or Counter(game_data.miscommunications)[self.k] > 1:
            return None
        loser = game_data.miscommunications.index(self.k)
        return not loser
        
# game ends if a team has k interception tokens, in which case it wins
class InterceptionEndCondition(EndCondition):
    def __init__(self, k: int = MAX_OFFICIAL_INTERCEPTIONS):
        self.k = k

    def game_over(self, game_data: GameData) -> bool:
        return any(interceptions == self.k for interceptions in game_data.interceptions)
    
    def winner(self, game_data: GameData) -> int:
        if not self.game_over(game_data) or Counter(game_data.interceptions)[self.k] > 1:
            return None
        winner = game_data.interceptions.index(self.k)
        return winner

# game ends if a team has k miscommunication tokens, in which case it loses
class RoundEndCondition(EndCondition):
    def __init__(self, k: int = MAX_OFFICIAL_ROUNDS):
        self.k = k

    def game_over(self, game_data: GameData) -> bool:
        return game_data.rounds_played == self.k
    
    def winner(self, game_data: GameData) -> int:
        return None
    
official_end_condition_constructors = [RoundEndCondition, MiscommunicationEndCondition, InterceptionEndCondition]

def interception_miscommunication_diff_tiebreaker(game_data: GameData):
    scores = [interceptions - miscommunications for interceptions, miscommunications in zip(game_data.interceptions, game_data.miscommunications)]
    if scores[0] == scores[1]:
        return None
    return scores.index(max(scores))