import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

    def test_staking(self):
        token = WacToken()
        token.transfer("genesis", "alice", 200000)
        self.assertTrue(token.stake("alice", 100000))
        self.assertEqual(token.get_balance("alice"), 100000)
        self.assertEqual(token.staked_balances["alice"], 100000)
        self.assertEqual(token.get_total_staked(), 100000)

    def test_max_staking(self):
        token = WacToken(initial_supply=1000000, max_stake_percent=0.05)
        token.transfer("genesis", "alice", 200000)
        self.assertTrue(token.stake("alice", 50000))
        self.assertFalse(token.stake("alice", 1))

    def test_unstaking(self):
        token = WacToken()
        token.transfer("genesis", "alice", 100000)
        token.stake("alice", 50000)
        self.assertTrue(token.unstake("alice", 25000))
        self.assertEqual(token.get_balance("alice"), 75000)
        self.assertEqual(token.staked_balances["alice"], 25000)

if __name__ == '__main__':
    unittest.main()
