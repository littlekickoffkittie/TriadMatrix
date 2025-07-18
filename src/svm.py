import hashlib
import threading
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

class SVM:
    def __init__(self, num_shards=4, gas_limit=1000):
        self.num_shards = num_shards
        self.shards = [{} for _ in range(num_shards)]
        self.locks = [threading.Lock() for _ in range(num_shards)]
        self.gas_limit = gas_limit

    def _get_shard_index(self, key):
        """Determines which shard a key belongs to."""
        hash_bytes = hashlib.sha256(str(key).encode()).digest()
        return int.from_bytes(hash_bytes, 'big') % self.num_shards

    def execute_contract(self, contract_code, contract_input):
        """
        Executes a smart contract in a sandboxed environment with gas limits.
        """
        read_set = {}
        write_set = {}
        gas_used = 0

        def read_state(key):
            nonlocal gas_used
            gas_used += 10 # Cost for reading state
            if gas_used > self.gas_limit:
                raise Exception("Gas limit exceeded")

            shard_index = self._get_shard_index(key)
            with self.locks[shard_index]:
                value = self.shards[shard_index].get(key)
                read_set[key] = value
                return value

        def write_state(key, value):
            nonlocal gas_used
            gas_used += 20 # Cost for writing state
            if gas_used > self.gas_limit:
                raise Exception("Gas limit exceeded")
            write_set[key] = value

        restricted_globals = {
            "__builtins__": safe_builtins,
            "read_state": read_state,
            "write_state": write_state,
            "contract_input": contract_input,
            "output": None,
        }
        restricted_globals.update({
            '_getiter_': iter,
            '_getitem_': lambda obj, key: obj[key],
        })

        try:
            byte_code = compile_restricted(contract_code, '<string>', 'exec')
            exec(byte_code, restricted_globals)
        except Exception as e:
            print(f"Contract execution error: {e}")
            return None

        # Validation and Commit Phase
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

        return restricted_globals.get("output")

    def get_state(self, key):
        shard_index = self._get_shard_index(key)
        with self.locks[shard_index]:
            return self.shards[shard_index].get(key)
