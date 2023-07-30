from typing import Protocol
import dataclasses
from decryptogame.components import Keywords, Code, Clue, TeamName
from decryptogame.game import Game

@dataclasses.dataclass(kw_only=True)
class TeamContext:
    """Dataclass representing the relevant information a team might consider"""
    team_name: TeamName
    keywords: Keywords
    num_opponent_keywords: int
    game: Game


class Encryptor(Protocol):
    """Interface representing an Encryptor, a teammate who decides clues"""

    def decide_clues(self, code: Code, context: TeamContext) -> Clue:
        """Decide clues for the given code as an Encryptor given the team context and current game state.

        Args:
            code (Code): The code assigned to the Encryptor to decide clues for.
            context (TeamContext): Relevant information the Encryptor's decision may be guided by.

        Returns:
            Clue: The clues decided by the Encryptor for each code number in the provided code.
        """
        ...

class Intercepter(Protocol):
    """Interface representing an Intercepter, a teammate who attempts to decipher the opposing team's clues"""

    def intercept_clues(self, opponent_clues: Clue, context: TeamContext) -> Code:
        """Attempt to decipher the opposing team's clues as an Intercepter given the team context and current game state.

        Args:
            opponent_clues (Clue): The clues provided by the opposing team.
            context (TeamContext): Relevant information the Intercepter's decision may be guided by.

        Returns:
            Code: The intercepter's code numbers guess based on the opposing team's clues.
        """
        ...

class Guesser(Protocol):
    """Interface representing an Guesser, a teammate who attempts to decipher their team's clues"""

    def decipher_clues(self, clues: Clue, context: TeamContext) -> Code:
        """Attempt to decipher the clues provided by the team as a Guesser given the team context and current game state.

        Args:
            clues (Clue): The clues provided by the Guesser's team.
            context (TeamContext): Relevant information the Guesser's decision may be guided by.

        Returns:
            Code: The guessed code numbers based on the team's clues.
        """
        ...
    
@dataclasses.dataclass(kw_only=True)
class Team:
    """Dataclass representing a team for a Decrypto game."""
    keywords: Keywords
    encryptor: Encryptor
    intercepter: Intercepter
    guesser: Guesser



# ship with some built-in players for quick sandboxing and testing


# command line players allow a developer to enter clues or code through the command line

class CommandLineEncryptor(Encryptor):
    """A teammate who decides clues using the command line. """

    def decide_clues(self, code: Code, context: TeamContext) -> Clue:
        """Decide clues for the given code using the command line.

        Args:
            code (Code): The code assigned to the Encryptor to decide clues for.
            context (TeamContext): Relevant information the Encryptor's decision may be guided by.

        Returns:
            Clue: The clues decided by the Encryptor for each code number in the provided code.
        """
        print(f"You are Encryptor on team {TeamName(context.team_name)}")
        print(f"Notesheet: {context.game.notesheet}")
        print(f"Scoresheet: {context.game.data}")
        print(f"Keywords: {context.keywords}")
        print(f"Code : {code}")
        clues = []
        for code_num in code:
            clue = input(f"Clue for number {code_num}: ")
            clues.append(clue)
        return tuple(clues)

class CommandLineIntercepter(Intercepter):
    """A teammate who attempts to decipher the opposing team's clues using the command line. """

    def intercept_clues(self, opponent_clues: Clue, context: TeamContext) -> Code:
        """Attempt to intercept the opposing team's clues using the command line.

        Args:
            opponent_clues (Clue): The clues provided by the opposing team.
            context (TeamContext): Relevant information the Interepter's decision may be guided by.

        Returns:
            Code: The intercepted code numbers based on the opposing team's clues.
        """
        print(f"You are Intercepter on team {TeamName(context.team_name)}")
        print(f"Notesheet: {context.game.notesheet}")
        print(f"Scoresheet: {context.game.data}")
        print(f"Opponent Clues : {opponent_clues}")
        n = context.num_opponent_keywords
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
    """A teammate who attempts to decipher their team's clues using the command line. """

    def decipher_clues(self, clues: Clue, context: TeamContext) -> Code:
        """Attempt to decipher the team's clues using the command line.

        Args:
            clues (Clue): The clues provided by the Guesser's team.
            context (TeamContext): Relevant information the Guesser's decision may be guided by. 

        Returns:
            Code: The guessed code numbers based on the team's clues.
        """
        print(f"You are Guesser on team {TeamName(context.team_name)}")
        print(f"Notesheet: {context.game.notesheet}")
        print(f"Scoresheet: {context.game.data}")
        print(f"Clues : {clues}")
        n = len(context.keywords)
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
                    print(f"Code num must lie in range [0 - {n}).")
                    code_num = None
            code.append(code_num)
        return tuple(code)

CommandLineTeam = lambda keywords: Team(
                                keywords=keywords,
                                encryptor=CommandLineEncryptor(),
                                intercepter=CommandLineIntercepter(),
                                guesser=CommandLineGuesser()
                            )

