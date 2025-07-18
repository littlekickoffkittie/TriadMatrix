import unittest
from src.svm import SVM

class TestSVM(unittest.TestCase):

    def test_svm_execution(self):
        svm = SVM()

        # A simple smart contract that adds two numbers
        contract_code = """
state['a'] = contract_input['x'] + contract_input['y']
output = state['a']
"""

        result = svm.execute_contract(contract_code, {'x': 10, 'y': 20})

        self.assertEqual(result, 30)
        self.assertEqual(svm.get_state('a'), 30)

    def test_svm_sandboxing(self):
        svm = SVM()

        # An attempt to access a forbidden builtin
        malicious_contract_code = """
import os
os.system('echo "malicious"')
"""

        svm.execute_contract(malicious_contract_code, {})
        # The contract should fail silently, but we can check that no state was modified
        self.assertEqual(svm.state, {})

if __name__ == '__main__':
    unittest.main()
