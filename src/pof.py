import hashlib
import time
import collections

class ProofOfFractal:
    def __init__(self, difficulty=4, self_similar_depth=2, adjustment_interval=10, target_time=10):
        self.difficulty = difficulty
        self.self_similar_depth = self_similar_depth
        self.adjustment_interval = adjustment_interval
        self.target_time = target_time
        self.triad_times = collections.deque(maxlen=adjustment_interval)

    def _is_self_similar(self, hash_hex, depth):
        prefix = '0' * (self.difficulty // (2**depth))
        return hash_hex.startswith(prefix)

    def generate_puzzle(self, triad):
        nonce = 0
        while True:
            pof_data = f"{triad.hash}{nonce}"
            hash_attempt = hashlib.sha256(pof_data.encode()).hexdigest()

            if self._is_self_similar(hash_attempt, self.self_similar_depth):
                triad.pof_data = (nonce, hash_attempt)
                self.triad_times.append(time.time())
                return nonce, hash_attempt
            nonce += 1

    def verify_solution(self, triad, nonce, pof_hash):
        pof_data = f"{triad.hash}{nonce}"
        hash_attempt = hashlib.sha256(pof_data.encode()).hexdigest()
        if hash_attempt != pof_hash:
            return False
        return self._is_self_similar(hash_attempt, self.self_similar_depth)

    def adjust_difficulty(self):
        if len(self.triad_times) < self.adjustment_interval:
            return

        total_time = self.triad_times[-1] - self.triad_times[0]
        average_time = total_time / (len(self.triad_times) - 1)

        if average_time < self.target_time * 0.9:
            self.difficulty += 1
        elif average_time > self.target_time * 1.1:
            self.difficulty = max(1, self.difficulty - 1)
