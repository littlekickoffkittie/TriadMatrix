import unittest
import time
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.triad import Triad
from src.pof import ProofOfFractal

class TestProofOfFractal(unittest.TestCase):

    def test_pof_puzzle_and_verification(self):
        triad = Triad(transactions=["tx1"])
        pof = ProofOfFractal(difficulty=4, self_similar_depth=1)
        nonce, pof_hash = pof.generate_puzzle(triad)

        self.assertTrue(pof_hash.startswith('00'))
        self.assertTrue(pof.verify_solution(triad, nonce, pof_hash))
        self.assertFalse(pof.verify_solution(triad, nonce + 1, pof_hash))

    def test_difficulty_adjustment(self):
        pof = ProofOfFractal(difficulty=4, adjustment_interval=5, target_time=0.01)

        # Simulate fast triad generation
        for _ in range(5):
            triad = Triad(transactions=[str(time.time())])
            pof.generate_puzzle(triad)
            time.sleep(0.005)

        pof.adjust_difficulty()
        self.assertEqual(pof.difficulty, 5)

        # Simulate slow triad generation
        for _ in range(5):
            triad = Triad(transactions=[str(time.time())])
            pof.generate_puzzle(triad)
            time.sleep(0.015)

        pof.adjust_difficulty()
        self.assertEqual(pof.difficulty, 4)

if __name__ == '__main__':
    unittest.main()
