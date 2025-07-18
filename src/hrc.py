import random

class HierarchicalRecursiveConsensus:
    def __init__(self, triad_matrix, fault_tolerance=0.33):
        self.triad_matrix = triad_matrix
        self.fault_tolerance = fault_tolerance

    def _simulate_pbft(self, committee_size):
        """Simulates a PBFT consensus round with pre-prepare, prepare, and commit phases."""
        num_faulty = int(committee_size * self.fault_tolerance)
        num_honest = committee_size - num_faulty

        # A supermajority is required for consensus in PBFT (2/3 of the nodes)
        required_votes = 2 * committee_size // 3 + 1

        # Phase 1: Pre-prepare (Primary sends a proposal)
        # We assume the primary is honest for this simulation.

        # Phase 2: Prepare (Nodes vote on the proposal)
        prepare_votes = sum(1 for _ in range(num_honest) if random.random() > 0.1) # 90% chance of voting
        if prepare_votes < required_votes:
            return False

        # Phase 3: Commit (Nodes commit to the block)
        commit_votes = sum(1 for _ in range(num_honest) if random.random() > 0.1) # 90% chance of voting
        if commit_votes < required_votes:
            return False

        return True

    def achieve_local_consensus(self, triad, committee_size=10):
        """Achieves consensus at the local (leaf) level."""
        return self._simulate_pbft(committee_size)

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
                    for child in parent_triad.children if child is not None
                )

                if all_children_have_consensus:
                    return self.propagate_consensus(parent_triad)
        else:
            # Root triad
            return True

        return False
