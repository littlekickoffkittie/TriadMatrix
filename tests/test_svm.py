import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.svm import SVM

class TestSVM(unittest.TestCase):

    def test_svm_execution(self):
        svm = SVM()

        # A simple smart contract that adds two numbers
        contract_code = """
a = contract_input['x'] + contract_input['y']
write_state('a', a)
output = a
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

        result = svm.execute_contract(malicious_contract_code, {})
        self.assertIsNone(result)

    def test_gas_limit(self):
        svm = SVM(gas_limit=50)

        # A contract that will exceed the gas limit
        contract_code = """
for i in range(10):
    write_state('key' + str(i), i)
"""
        result = svm.execute_contract(contract_code, {})
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
