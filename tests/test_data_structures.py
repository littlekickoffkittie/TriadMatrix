import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.triad import Triad
from src.triad_matrix import TriadMatrix

class TestDataStructures(unittest.TestCase):

    def test_triad_creation(self):
        triad = Triad(transactions=["tx1", "tx2"])
        self.assertIsNotNone(triad.hash)
        self.assertIsNotNone(triad.merkle_root)

    def test_triad_matrix_addition(self):
        matrix = TriadMatrix()
        root_hash = matrix.root.hash
        triad1 = matrix.add_triad(transactions=["tx1", "tx2"], parent_hash=root_hash)
        self.assertIn(triad1, matrix.root.children)

        triad2 = matrix.add_triad(transactions=["tx3", "tx4"], parent_hash=triad1.hash)
        self.assertIn(triad2, triad1.children)

    def test_find_paths_to_root(self):
        matrix = TriadMatrix()
        root_hash = matrix.root.hash
        triad1 = matrix.add_triad(transactions=["tx1"], parent_hash=root_hash)
        triad2 = matrix.add_triad(transactions=["tx2"], parent_hash=root_hash)
        triad3 = matrix.add_triad(transactions=["tx3"], parent_hash=triad1.hash)
        triad4 = matrix.add_triad(transactions=["tx4"], parent_hash=triad1.hash)
        triad5 = matrix.add_triad(transactions=["tx5"], parent_hash=triad3.hash)

        paths = matrix.find_paths_to_root(triad5.hash)
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0], [triad5.hash, triad3.hash, triad1.hash, root_hash])

    def test_add_triad_error_handling(self):
        matrix = TriadMatrix()
        root_hash = matrix.root.hash
        # Test adding to a non-existent parent
        with self.assertRaises(ValueError):
            matrix.add_triad(transactions=["tx1"], parent_hash="non_existent_hash")

        # Test adding to a full parent
        matrix.add_triad(transactions=["tx1"], parent_hash=root_hash)
        matrix.add_triad(transactions=["tx2"], parent_hash=root_hash)
        matrix.add_triad(transactions=["tx3"], parent_hash=root_hash)
        with self.assertRaises(Exception):
            matrix.add_triad(transactions=["tx4"], parent_hash=root_hash)

if __name__ == '__main__':
    unittest.main()
