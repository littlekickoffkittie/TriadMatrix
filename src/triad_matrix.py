from src.triad import Triad

class TriadMatrix:
    def __init__(self):
        self.root = Triad(transactions=["genesis"], coordinates=(0,))
        self.nodes = {self.root.hash: self.root}
        self.nodes_by_coordinates = {(0,): self.root}


    def add_triad(self, transactions, parent_hash):
        if parent_hash not in self.nodes:
            raise ValueError(f"Parent triad with hash {parent_hash} not found")

        parent_triad = self.nodes[parent_hash]

        if all(child is not None for child in parent_triad.children):
            raise Exception(f"Parent triad {parent_hash} already has three children.")

        # Find an empty child slot to add the new triad
        for i in range(3):
            if parent_triad.children[i] is None:
                child_coordinates = parent_triad.coordinates + (i,)
                new_triad = Triad(transactions, parent_hash, child_coordinates)
                parent_triad.add_child(new_triad, i)
                self.nodes[new_triad.hash] = new_triad
                self.nodes_by_coordinates[new_triad.coordinates] = new_triad
                return new_triad


    def get_triad(self, triad_hash):
        return self.nodes.get(triad_hash)

    def get_triad_by_coordinates(self, coordinates):
        return self.nodes_by_coordinates.get(coordinates)

    def find_paths_to_root(self, start_triad_hash):
        if start_triad_hash not in self.nodes:
            return []

        start_triad = self.nodes[start_triad_hash]
        paths = []

        def find_path(triad, current_path):
            current_path.append(triad.hash)
            if triad.parent_hash is None:
                paths.append(list(current_path))
                return

            parent_triad = self.nodes.get(triad.parent_hash)
            if parent_triad:
                find_path(parent_triad, list(current_path))

        find_path(start_triad, [])
        return paths

    def __repr__(self):
        return f"TriadMatrix(root={self.root.hash if self.root else None}, num_triads={len(self.nodes)})"
