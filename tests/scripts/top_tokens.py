import unittest
from scripts.top_tokens import get_top_token


class TestTopTokens(unittest.TestCase):

    def test_get_top_token(self):
        top_30_tokens = get_top_token("binance","kucoin",30)
        self.assertTrue(len(top_30_tokens) == 30)


if __name__ == "__main__":
    unittest.main()
