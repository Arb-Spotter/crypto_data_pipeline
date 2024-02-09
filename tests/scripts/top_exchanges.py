import unittest
from scripts.top_exchanges import get_top_30_ex
from scripts.top_tokens import get_top_token


class TestTopExchanges(unittest.TestCase):

    def test_get_top_token(self):
        top_30_ex = get_top_30_ex()
        self.assertTrue(len(top_30_ex) == 30)

if __name__ == "__main__":
    unittest.main()
