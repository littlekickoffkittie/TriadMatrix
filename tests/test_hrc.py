import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.triad_matrix import TriadMatrix
from src.hrc import HierarchicalRecursiveConsensus
from src.pof import ProofOfFractal

class TestHierarchicalRecursiveConsensus(unittest.TestCase):

    def test_hrc_propagation(self):
        matrix = TriadMatrix()
        hrc = HierarchicalRecursiveConsensus(matrix, fault_tolerance=0.1) # Low fault tolerance for testing
        pof = ProofOfFractal(difficulty=1)

        # Create a small chain of triads
        root_hash = matrix.root.hash
        matrix.root.pof_data = (0, "dummy_hash") # Assume genesis triad has PoF
        triad1 = matrix.add_triad(transactions=["tx1"], parent_hash=root_hash)
        pof.generate_puzzle(triad1)
        triad2 = matrix.add_triad(transactions=["tx2"], parent_hash=triad1.hash)
        pof.generate_puzzle(triad2)
        triad3 = matrix.add_triad(transactions=["tx3"], parent_hash=triad2.hash)
        pof.generate_puzzle(triad3)


        # Start consensus from the leaf triad
        consensus_reached = hrc.propagate_consensus(triad3)
        self.assertTrue(consensus_reached)

    def test_hrc_failure(self):
        matrix = TriadMatrix()
        hrc = HierarchicalRecursiveConsensus(matrix, fault_tolerance=0.5) # High fault tolerance
        pof = ProofOfFractal(difficulty=1)

        # Create a triad
        root_hash = matrix.root.hash
        triad1 = matrix.add_triad(transactions=["tx1"], parent_hash=root_hash)
        pof.generate_puzzle(triad1)

        # Start consensus, it should fail
        consensus_reached = hrc.propagate_consensus(triad1)
        self.assertFalse(consensus_reached)

if __name__ == '__main__':
    unittest.main()
