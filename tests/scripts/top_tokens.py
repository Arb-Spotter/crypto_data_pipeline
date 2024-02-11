import unittest
from scripts.top_tokens import get_top_token, get_token_symbols


class TestTopTokens(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_get_top_token(self):
        top_30_tokens = get_top_token("mexc", "kucoin", 30)
        self.assertTrue(len(top_30_tokens) == 30)

    def test_get_token_symbols(self):
        symbols = ["BTC", "ETH", "LTC", "LIT", "XRP"]
        metadata = get_token_symbols(symbols)
        print(metadata)
        self.assertTrue(len(metadata) == 5)


if __name__ == "__main__":
    unittest.main()
