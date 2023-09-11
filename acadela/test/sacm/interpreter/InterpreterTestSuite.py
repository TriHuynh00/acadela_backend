import unittest
from acadela.test.sacm.interpreter.field.SyntacticFieldTest import SyntacticFieldTest
import sys
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class InterpreterTestSuite(unittest.TestSuite):

    def test_all(self):
        self.addTest(SyntacticFieldTest())

if __name__ == "__main__":
    unittest.main()