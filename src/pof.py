import hashlib
import time

class ProofOfFractal:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty

    def generate_puzzle(self, triad):
        # This is a simplified puzzle for now.
        # A real implementation would involve a more complex self-similar hash pattern.
        prefix = '0' * self.difficulty
        nonce = 0
        while True:
            pof_data = f"{triad.hash}{nonce}"
            hash_attempt = hashlib.sha256(pof_data.encode()).hexdigest()
            if hash_attempt.startswith(prefix):
                triad.pof_data = (nonce, hash_attempt)
                return nonce, hash_attempt
            nonce += 1

    def adjust_difficulty(self, last_triad_time, target_time):
        if time.time() - last_triad_time < target_time:
            self.difficulty += 1
        else:
            self.difficulty = max(1, self.difficulty - 1)
