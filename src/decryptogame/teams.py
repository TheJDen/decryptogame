import abc
import dataclasses
from decryptogame.game import Game

class Encryptor(abc.ABC):
    """Interface representing an Encryptor, a teammate who decides clues"""

    @abc.abstractmethod
    def decide_clues(game: Game, code: tuple[str]) -> bool:
        pass

class Intercepter(abc.ABC):
    """Interface representing an Intercepter, a teammate who attempts to decipher the opposing team's clues"""

    @abc.abstractmethod
    def intercept_clues(game: Game, clues: tuple[str]) -> bool:
        pass

class Guesser(abc.ABC):
    """Interface representing an Guesser, a teammate who attempts to decipher their team's clues"""

    @abc.abstractmethod
    def decipher_clues(game: Game, code: tuple[str]) -> bool:
        pass
    
@dataclasses.dataclass(kw_only=True)
class Team:
    encryptor: Encryptor
    intercepter: Intercepter
    guesser: Guesser