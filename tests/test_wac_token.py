import unittest
from src.wac_token import WacToken

class TestWacToken(unittest.TestCase):

    def test_initial_supply(self):
        token = WacToken(initial_supply=5000)
        self.assertEqual(token.get_balance("genesis"), 5000)

    def test_transfer(self):
        token = WacToken()
        token.transfer("genesis", "alice", 100)
        self.assertEqual(token.get_balance("genesis"), 999900)
        self.assertEqual(token.get_balance("alice"), 100)

    def test_insufficient_funds(self):
        token = WacToken()
        self.assertFalse(token.transfer("alice", "bob", 50))

    def test_minting(self):
        token = WacToken()
        token.mint("bob", 250)
        self.assertEqual(token.get_balance("bob"), 250)
        self.assertEqual(token.total_supply, 1000250)

if __name__ == '__main__':
    unittest.main()
