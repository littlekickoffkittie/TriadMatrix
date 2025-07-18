import hashlib
import threading

class SVM:
    def __init__(self, num_shards=4):
        self.num_shards = num_shards
        self.shards = [{} for _ in range(num_shards)]
        self.locks = [threading.Lock() for _ in range(num_shards)]

    def _get_shard_index(self, key):
        """Determines which shard a key belongs to."""
        hash_bytes = hashlib.sha256(str(key).encode()).digest()
        return int.from_bytes(hash_bytes, 'big') % self.num_shards

    def execute_contract(self, contract_code, contract_input):
        """
        Executes a smart contract with optimistic concurrency control.
        WARNING: Uses exec(), which is unsafe for production.
        """
        read_set = {}
        write_set = {}

        # 1. Execution Phase (Optimistic)
        temp_state = {}

        def read_state(key):
            shard_index = self._get_shard_index(key)
            with self.locks[shard_index]:
                value = self.shards[shard_index].get(key)
                temp_state[key] = value
                read_set[key] = value
                return value

        def write_state(key, value):
            write_set[key] = value

        restricted_globals = {
            "__builtins__": {},
            "read_state": read_state,
            "write_state": write_state,
            "contract_input": contract_input,
            "output": None,
        }

        try:
            exec(contract_code, restricted_globals)
        except Exception as e:
            print(f"Contract execution error: {e}")
            return None

        # 2. Validation and Commit Phase
        for key, value in read_set.items():
            shard_index = self._get_shard_index(key)
            with self.locks[shard_index]:
                if self.shards[shard_index].get(key) != value:
                    print("Transaction conflict detected. Aborting.")
                    return None # Abort

        for key, value in write_set.items():
            shard_index = self._get_shard_index(key)
            with self.locks[shard_index]:
                self.shards[shard_index][key] = value

        print("Transaction committed successfully.")
        return restricted_globals.get("output")

    def get_state(self, key):
        shard_index = self._get_shard_index(key)
        with self.locks[shard_index]:
            return self.shards[shard_index].get(key)
