import hashlib
import time

class ProofOfFractal:
    def __init__(self, difficulty=4, self_similar_depth=2):
        self.difficulty = difficulty
        self.self_similar_depth = self_similar_depth

    def _is_self_similar(self, hash_hex, depth):
        if depth == 0:
            return True

        prefix = '0' * (self.difficulty // (2**depth))
        if not hash_hex.startswith(prefix):
            return False

        half_len = len(hash_hex) // 2
        return self._is_self_similar(hash_hex[half_len:], depth - 1)


    def generate_puzzle(self, triad):
        nonce = 0
        while True:
            pof_data = f"{triad.hash}{nonce}"
            hash_attempt = hashlib.sha256(pof_data.encode()).hexdigest()

            if self._is_self_similar(hash_attempt, self.self_similar_depth):
                triad.pof_data = (nonce, hash_attempt)
                return nonce, hash_attempt
            nonce += 1

    def adjust_difficulty(self, last_triad_time, target_time):
        if time.time() - last_triad_time < target_time:
            self.difficulty += 1
        else:
            self.difficulty = max(1, self.difficulty - 1)
        if time.time() - last_triad_time < target_time:
            self.difficulty += 1
        else:
            self.difficulty = max(1, self.difficulty - 1)
