from src.triad import Triad

class TriadMatrix:
    def __init__(self):
        self.root = None
        self.nodes = {}

    def add_triad(self, transactions, parent_hash=None):
        new_triad = Triad(transactions, parent_hash)

        if self.root is None:
            self.root = new_triad

        self.nodes[new_triad.hash] = new_triad

        if parent_hash and parent_hash in self.nodes:
            parent_triad = self.nodes[parent_hash]

            # Find an empty child slot to add the new triad
            for i in range(3):
                if parent_triad.children[i] is None:
                    parent_triad.add_child(new_triad, i)
                    break
            else:
                # If no empty slot is found, this logic will need to be improved
                # based on the specific growth strategy of the Triad Matrix.
                print("Warning: No empty child slot found for parent triad.")

        return new_triad

    def get_triad(self, triad_hash):
        return self.nodes.get(triad_hash)

    def __repr__(self):
        return f"TriadMatrix(root={self.root.hash if self.root else None}, num_triads={len(self.nodes)})"
