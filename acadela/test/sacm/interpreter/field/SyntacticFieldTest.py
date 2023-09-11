import unittest
from acadela.test.sacm.interpreter.TestParam import baseCodeWithoutField
import acadela.sacm.interpreter.stage as stageIntrprtr
from acadela.sacm.interpreter.case_template import CaseInterpreter

from os.path import join, dirname
import sys
from textx import metamodel_from_file, TextXSyntaxError

sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela')

class SyntacticFieldTest(unittest.TestCase):

    def setUp(self):
        self.baseCode = baseCodeWithoutField
        self.mm = metamodel_from_file(\
            join('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela',
                 'AcadelaGrammar.tx'), classes=None, ignore_case=True)

    def test_field_mandatory_attr(self):
        self.baseCode += '''
            Form 
                field Height
                    #number(0-150) #exactlyOne
                    description = 'Height of patient in cm'    
                    
                field Weight
                    #number(0-300) #exactlyOne
                    description = 'Weight of patient in kg'                        
        '''

        model = self.mm.model_from_str(self.baseCode)
        caseInterpreter = CaseInterpreter(self.mm, model)
        caseInterpreter.interpret()
        self.assertEqual(len(caseInterpreter.stageList), 1)

    if __name__ == "main":
        unittest.main()