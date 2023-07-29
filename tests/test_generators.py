import pytest
from decryptogame.generators import RandomKeywordCards, RandomCodes

@pytest.fixture
def default_random_code_generator():
    keyword_cards = [("a", "b", "c", "d"), ("e", "f", "g", "h")]
    return RandomCodes(keyword_cards)
    
class TestRandomKeywordCards:
    def test_default(self):
        card_generator = RandomKeywordCards()
        card1, card2 = next(card_generator)

        assert len(card1) == 4
        assert len(card2) == 4

        assert len(set(card1)) == 4
        assert len(set(card2)) == 4

class TestRandomCodes:
    def test_default(self, default_random_code_generator):
        code1, code2 = next(default_random_code_generator)

        assert len(code1) == 3
        assert len(code2) == 3

        assert len(set(code1)) == 3
        assert len(set(code2)) == 3

        assert all(code_num in range(4) for code_num in code1)
        assert all(code_num in range(4) for code_num in code2)


        