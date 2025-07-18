class SVM:
    def __init__(self):
        self.state = {}

    def execute_contract(self, contract_code, contract_input):
        # WARNING: Using exec is generally unsafe. This is a simplified implementation
        # for demonstration purposes. A real SVM would require a secure, sandboxed
        # execution environment.

        restricted_globals = {
            "__builtins__": {},
            "state": self.state,
            "contract_input": contract_input,
            "output": None
        }

        try:
            exec(contract_code, restricted_globals)
            return restricted_globals.get("output")
        except Exception as e:
            print(f"Error executing smart contract: {e}")
            return None

    def get_state(self, key):
        return self.state.get(key)
