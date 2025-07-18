import unittest
import time
from src.triad import Triad
from src.pof import ProofOfFractal

class TestProofOfFractal(unittest.TestCase):

    def test_pof_puzzle(self):
        triad = Triad(transactions=["tx1"])
        pof = ProofOfFractal(difficulty=3)
        nonce, pof_hash = pof.generate_puzzle(triad)

        self.assertTrue(pof_hash.startswith('000'))
        self.assertIsNotNone(nonce)

    def test_difficulty_adjustment(self):
        pof = ProofOfFractal(difficulty=4)

        # Simulate fast block time
        pof.adjust_difficulty(time.time() - 5, 10)
        self.assertEqual(pof.difficulty, 5)

        # Simulate slow block time
        pof.adjust_difficulty(time.time() - 15, 10)
        self.assertEqual(pof.difficulty, 4)

if __name__ == '__main__':
    unittest.main()
