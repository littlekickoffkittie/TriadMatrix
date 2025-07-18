import unittest
from src.triad import Triad
from src.triad_matrix import TriadMatrix

class TestDataStructures(unittest.TestCase):

    def test_triad_creation(self):
        triad = Triad(transactions=["tx1", "tx2"])
        self.assertIsNotNone(triad.hash)
        self.assertIsNotNone(triad.merkle_root)

    def test_triad_matrix_addition(self):
        matrix = TriadMatrix()
        triad1 = matrix.add_triad(transactions=["tx1", "tx2"])
        self.assertEqual(matrix.root, triad1)

        triad2 = matrix.add_triad(transactions=["tx3", "tx4"], parent_hash=triad1.hash)
        self.assertIn(triad2, triad1.children)

if __name__ == '__main__':
    unittest.main()
