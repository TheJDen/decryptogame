import pytest
from decryptogame.game import Game, Note

EXAMPLE_KEYWORDS = (
    ("black", "dragonfly", "cocktail", "sombrero"),
    ("antiquity", "bone", "morning", "nightmare")
)

@pytest.fixture()
def default_game():
    return Game(keywords=EXAMPLE_KEYWORDS)

class TestGame:
    def test_default(self, default_game):
        assert default_game.keywords == EXAMPLE_KEYWORDS

        assert default_game.rounds_played == 0

        assert not default_game.notesheet

        assert default_game.miscommunications[0] == 0
        assert default_game.miscommunications[1] == 0

        assert default_game.interceptions[0] == 0
        assert default_game.interceptions[1] == 0

    def test_kw_only(self):
        with pytest.raises(TypeError):
            game = Game(0)
    
    def test_configurable(self):
        # no miscommunications or interceptions
        first_round_notes = [
            Note(attempted_interception=(2, 1, 3), attempted_decipher=(1, 2, 3), correct_code=(1, 2, 3)),
            Note(attempted_interception=(4, 1, 3), attempted_decipher=(3, 1, 4), correct_code=(3, 1, 4))
        ]
        # no miscommunications, one interception of first team by second
        second_round_notes = [
            Note(attempted_interception=(2, 1, 3), attempted_decipher=(2, 1, 3), correct_code=(2, 1, 3)), # interception
            Note(attempted_interception=(2, 4, 3), attempted_decipher=(4, 1, 3), correct_code=(4, 1, 3))
        ]
        # one miscommunication among first team, one interception of second team by first
        third_round_notes = [
            Note(attempted_interception=(2, 3, 1), attempted_decipher=(2, 3, 1), correct_code=(4, 3, 1)),  # miscommunication
            Note(attempted_interception=(2, 1, 3), attempted_decipher=(2, 1, 3), correct_code=(2, 1, 3)) # interception
        ]

        notesheet = [first_round_notes, second_round_notes, third_round_notes]

        rounds_played = len(notesheet)

        game = Game(keywords=EXAMPLE_KEYWORDS, notesheet=notesheet)
        assert game.rounds_played == rounds_played
        assert game.miscommunications[0] == 1
        assert game.miscommunications[1] == 0
        assert game.interceptions[0] == 1
        assert game.interceptions[1] == 1

class TestNote:
    def test_default(self):
        note = Note()
        assert note.clues is None
        assert note.attempted_decipher is None
        assert note.attempted_interception is None
        assert note.correct_code is None

    def test_kw_only(self):
        with pytest.raises(TypeError):
            note = Note(0)