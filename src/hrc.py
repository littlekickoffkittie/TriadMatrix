import random

class HierarchicalRecursiveConsensus:
    def __init__(self, triad_matrix, fault_tolerance=0.33):
        self.triad_matrix = triad_matrix
        self.fault_tolerance = fault_tolerance

    def _simulate_pbft(self, committee_size):
        """Simulates a PBFT consensus round."""
        # In a real implementation, this would be a complex messaging process.
        # Here, we just simulate the outcome based on fault tolerance.
        num_faulty = int(committee_size * self.fault_tolerance)
        num_honest = committee_size - num_faulty

        # Consensus is reached if honest nodes > 2 * faulty nodes
        return num_honest > 2 * num_faulty

    def achieve_local_consensus(self, triad, committee_size=10):
        """Achieves consensus at the local (leaf) level."""
        print(f"Achieving local consensus for Triad {triad.hash} with committee of {committee_size}...")
        if self._simulate_pbft(committee_size):
            print("Local consensus successful.")
            return True
        else:
            print("Local consensus failed.")
            return False

    def propagate_consensus(self, triad):
        """Propagates consensus results up the Triad Matrix."""
        if not self.achieve_local_consensus(triad):
            return False

        if triad.parent_hash:
            parent_triad = self.triad_matrix.get_triad(triad.parent_hash)
            if parent_triad:
                # In a real system, we'd aggregate cryptographic proofs.
                # Here, we'll just check if all children have reached consensus.
                all_children_have_consensus = all(
                    child is not None and child.pof_data is not None
                    for child in parent_triad.children
                )

                if all_children_have_consensus:
                    print(f"Propagating consensus from children of {parent_triad.hash}...")
                    return self.propagate_consensus(parent_triad)
        else:
            # Root triad
            print(f"Consensus reached at root Triad {triad.hash}.")
            return True

        return False
