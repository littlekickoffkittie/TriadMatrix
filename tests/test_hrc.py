import unittest
from src.triad_matrix import TriadMatrix
from src.hrc import HierarchicalRecursiveConsensus

class TestHierarchicalRecursiveConsensus(unittest.TestCase):

    def test_hrc_propagation(self):
        matrix = TriadMatrix()
        hrc = HierarchicalRecursiveConsensus(matrix)

        # Create a small chain of triads
        triad1 = matrix.add_triad(transactions=["tx1"])
        triad2 = matrix.add_triad(transactions=["tx2"], parent_hash=triad1.hash)
        triad3 = matrix.add_triad(transactions=["tx3"], parent_hash=triad2.hash)

        # Start consensus from the leaf triad
        consensus_reached = hrc.propagate_consensus(triad3)
        self.assertTrue(consensus_reached)

if __name__ == '__main__':
    unittest.main()
