import abc
import dataclasses
import random
from decryptogame.components import Code, Clue, TeamName
from decryptogame.game import Game

class Encryptor(abc.ABC):
    """Interface representing an Encryptor, a teammate who decides clues"""

    @abc.abstractmethod
    def decide_clues(team_name: TeamName, game: Game, code: Code) -> Clue:
        pass

class Intercepter(abc.ABC):
    """Interface representing an Intercepter, a teammate who attempts to decipher the opposing team's clues"""

    @abc.abstractmethod
    def intercept_clues(team_name: TeamName, game: Game, opponent_clues: Clue) -> Code:
        pass

class Guesser(abc.ABC):
    """Interface representing an Guesser, a teammate who attempts to decipher their team's clues"""

    @abc.abstractmethod
    def decipher_clues(team_name: TeamName, game: Game, clues: Clue) -> Code:
        pass
    
@dataclasses.dataclass(kw_only=True)
class Team:
    encryptor: Encryptor
    intercepter: Intercepter
    guesser: Guesser



# ship with some built-in players for quick sandboxing and testing


# command line players allow a developer to enter clues or code through the command line

class CommandLineEncryptor(Encryptor):
    """Interface representing an Encryptor, a teammate who decides clues"""

    def decide_clues(team_name: TeamName, game: Game, code: Code) -> Clue:
        print(f"You are Encryptor on team {TeamName(team_name)}")
        print(f"Notesheet: {game.notesheet}")
        print(f"Scoresheet: {game.data}")
        print(f"Keywords: {game.keywords[team_name]}")
        print(f"Code : {code}")
        clues = []
        for code_num in code:
            clue = input(f"Clue for number {code_num}: ")
            clues.append(clue)
        return tuple(clues)

class CommandLineIntercepter(Intercepter):
    """Interface representing an Intercepter, a teammate who attempts to decipher the opposing team's clues"""

    def intercept_clues(team_name: TeamName, game: Game, opponent_clues: Clue) -> Code:
        print(f"You are Intercepter on team {TeamName(team_name)}")
        print(f"Notesheet: {game.notesheet}")
        print(f"Scoresheet: {game.data}")
        print(f"Opponent Clues : {opponent_clues}")
        opponent = not team_name
        n = len(game.keywords[opponent])
        print(f"Number of Opponent Keywords: {n}")
        code = []
        for clue in opponent_clues:
            code_num = None
            while code_num is None:
                try:
                    code_num = int(input(f"Code number for clue {clue}: "))
                except ValueError:
                    pass
                if code_num is None or code_num not in range(n):
                    print(f"Code num must lie in range [0 - {n}).")
                    code_num = None
            code.append(code_num)
        return tuple(code)

class CommandLineGuesser(Guesser):
    """Interface representing an Guesser, a teammate who attempts to decipher their team's clues"""

    def decipher_clues(team_name: TeamName, game: Game, clues: Clue) -> Code:
        print(f"You are Guesser on team {TeamName(team_name)}")
        print(f"Notesheet: {game.notesheet}")
        print(f"Scoresheet: {game.data}")
        print(f"Clues : {clues}")
        n = len(game.keywords[team_name])
        print(f"Number of Keywords: {n}")
        code = []
        for clue in clues:
            code_num = None
            while code_num is None:
                try:
                    code_num = int(input(f"Code number for clue {clue}: "))
                except ValueError:
                    pass
                if code_num is None or code_num not in range(n + 1):
                    print(f"Code num must lie in range [0 - {n}].")
                    code_num = None
            code.append(code_num)
        return tuple(code)



# random players choose clues and codes randomly

class RandomEncryptor(Encryptor):
    """Interface representing an Encryptor, a teammate who decides clues"""

    def decide_clues(team_name: TeamName, game: Game, code: Code) -> Clue:
        pass

class RandomIntercepter(Intercepter):
    """Interface representing an Intercepter, a teammate who attempts to decipher the opposing team's clues"""

    def intercept_clues(team_name: TeamName, game: Game, opponent_clues: Clue) -> Code:
        pass

class RandomGuesser(Guesser):
    """Interface representing an Guesser, a teammate who attempts to decipher their team's clues"""

    def decipher_clues(team_name: TeamName, game: Game, clues: Clue) -> Code:
        pass