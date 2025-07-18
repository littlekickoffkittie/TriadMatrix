import hashlib

class Triad:
    def __init__(self, transactions, parent_hash=None):
        self.transactions = transactions
        self.parent_hash = parent_hash
        self.children = [None, None, None]
        self.merkle_root = self.calculate_merkle_root()
        self.pof_data = None  # To be implemented
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self):
        if not self.transactions:
            return None

        transaction_hashes = [hashlib.sha256(str(tx).encode()).hexdigest() for tx in self.transactions]

        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])

            new_hashes = []
            for i in range(0, len(transaction_hashes), 2):
                combined_hash = hashlib.sha256((transaction_hashes[i] + transaction_hashes[i+1]).encode()).hexdigest()
                new_hashes.append(combined_hash)

            transaction_hashes = new_hashes

        return transaction_hashes[0]

    def calculate_hash(self):
        block_header = str(self.parent_hash) + str(self.merkle_root) + str(self.pof_data)
        return hashlib.sha256(block_header.encode()).hexdigest()

    def add_child(self, child_triad, index):
        if 0 <= index < 3:
            self.children[index] = child_triad
        else:
            raise IndexError("Index out of bounds for children")

    def __repr__(self):
        return f"Triad(hash={self.hash}, parent_hash={self.parent_hash})"
