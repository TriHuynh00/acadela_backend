# At this point model is a plain Python object graph with instances of
# dynamically created classes and attributes following the grammar.
import colored as colored

from pointmodel.point import Point


def cname(o):
    return o.__class__.__name__

class Interpreter():
    def __init__(self, model):
        self.model = model

    # Let's interpret the model
    def interpret(self):
        case = self.model.case

        if cname(case) == 'Case':
            print('Case Name', case.casename)

        for caseAttr in case.caseAttr:
            if cname(caseAttr) == 'CasePrefix':
                print('Case Prefix =', caseAttr.pattern)
            if cname(caseAttr) == 'Multiplicity':
                print('Multiplicity =', caseAttr.multiplicity)

