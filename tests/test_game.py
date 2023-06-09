import pytest
from decryptogame.game import Game, GameData, Note

EXAMPLE_KEYWORDS = (
    ("black", "dragonfly", "cocktail", "sombrero"),
    ("antiquity", "bone", "morning", "nightmare")
)

@pytest.fixture()
def default_game():
    return Game(keywords=EXAMPLE_KEYWORDS)

class TestGame:
    def test_default_values(self, default_game):
        assert default_game.keywords == EXAMPLE_KEYWORDS

        assert default_game.data.rounds_played == 0

        assert not default_game.notesheet

        assert default_game.data.miscommunications[0] == 0
        assert default_game.data.miscommunications[1] == 0

        assert default_game.data.interceptions[0] == 0
        assert default_game.data.interceptions[1] == 0

        assert not default_game.game_over()

    def test_default_end_rounds(self, default_game):
        mid_game_data = GameData(rounds_played=7)
        end_game_data = GameData(rounds_played=8)
        assert not default_game.game_over(mid_game_data)
        assert default_game.game_over(end_game_data)

    def test_default_end_miscommunications(self, default_game):
        mid_game_data = GameData(miscommunications=[1,1], rounds_played=2)
        end_game_data = GameData(miscommunications=[1,2], rounds_played=2)
        assert not default_game.game_over(mid_game_data)
        assert default_game.game_over(end_game_data)

    def test_default_end_interceptions(self, default_game):
        mid_game_data = GameData(interceptions=[1,1], rounds_played=2)
        end_game_data = GameData(interceptions=[1,2], rounds_played=2)
        assert not default_game.game_over(mid_game_data)
        assert default_game.game_over(end_game_data)

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
        

        assert game.data.rounds_played == rounds_played
        assert game.data.miscommunications[0] == 1
        assert game.data.miscommunications[1] == 0
        assert game.data.interceptions[0] == 1
        assert game.data.interceptions[1] == 1

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

class TestGameData:
    # simple game data is stored seorately so plies are tenable
    def test_default(self):
        game_data = GameData()

        assert game_data.miscommunications[0] == 0
        assert game_data.miscommunications[0] == 0

        assert game_data.interceptions[1] == 0
        assert game_data.interceptions[1] == 0

        assert game_data.rounds_played == 0

    def test_kw_only(self):
        with pytest.raises(TypeError):
            game_data = GameData(0)