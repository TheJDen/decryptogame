# Tutorials

Decryptogame is meant for fast prototyping of Decrypto gameplay with AI or simulation agents. Let's spin up our first game of Decrypto in decryptogame.

In a game of Decrypto, each team is assigned a keyword card containing a sequence of words.
You may provide your own keyword cards as a tuple of strings to each team, but we will use a generator to provide a random keyword cards from the official wordset

```python
>>> import decryptogame as dg

>>> keywords_generator = dg.generators.RandomKeywordCards()
>>> keyword_cards = next(keywords_generator)
>>> keyword_cards
[('COFFEE', 'VAMPIRE', 'GUITAR', 'CAT'), ('ORCHESTRA', 'FOREST', 'ATTACK', 'EXIT')]
```

Great, now we have a pair of keyword cards for each team. Let's form our teams. In decryptogame, each team has a keyword card, and an encryptor, intercepter, and guesser, who each follow their protocol outlined in the teams module. Decryptogame ships with a CommandLineTeam for easy interaction straght out the gate. Let's make teams using the CommandLineTeam.

```python
>>> teams = [dg.teams.CommandLineTeam(keywords) for keywords in keyword_cards]
```

Now, we are ready to play a game of Decrypto! To play a game, we use the play_game procedure. It is highly configurable; we may pass in a game with custom rules an argument, an iterable of code pairs for each round to reproduce games, or a number of rounds to play before stopping to check out how things are going. For now, we are jut going to play a default game, which plays by the official rules, generates random code pairs, and plays the game to completion.

The play_game procedure will alter the update the Game object after each round, and return it after play.

```python
>>> result_game = dg.play_game(teams)
```

You will be able to play the game using the CommandLineTeam teammates. We can use the game object to retrieve data about our game after play. Let's check out the winner; it might be None if the game ended as a tie.

```python
>>> print(result_game.winner())
<TeamName.WHITE: 0>
```

Let's check out the data, like the number of rounds played, or the number of miscommunications for each team. In decryptogame, the white team is index 0, and the black team is index 1, as implied in the previous code block.


```python
>>> result_game.data
GameData(rounds_played=3, miscommunications=[1, 2], interceptions=[2, 0])
```

You've played your first game of Decrypto on decryptogame!


