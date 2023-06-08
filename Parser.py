from ExpressionNodes import *
from collections import defaultdict
import re

class Parser:
    def __init__(self, mode="basic", additional_operators=None, additional_operands=None) -> None:
        
        self.operators = defaultdict(list)
        self.operands = []

        included_operators = set()
        included_operands = set()
        
        #preset configurations
        match(mode):
            case "basic":
                self.operators[1000] += [Add, Sub]
                self.operators[2000] += [Mult, Div, IntDiv]
                included_operators.update((Add, Sub, Mult, Div, IntDiv))

                self.operands += [Var, Number]
                included_operands.update((Var, Number))
            case "void": #omit normal operations
                pass
            case _:
                raise Exception("Invalid Parse Mode")
        
        #add custom operators
        if(additional_operators):
            for priority, type in additional_operators:
                if(not isinstance(type, Operator)):
                    raise Exception("Attempting to treat non-operator class as operator")
                if(type in included_operators): continue
                
                self.operators[priority].append(type)
                included_operators.add(type)
        
        #add custom operators
        if(additional_operands):
            for type in additional_operands:
                if(not isinstance(type, Operand)):
                    raise Exception("Attempting to treat non-operand class as operand")
                if(type in included_operands): continue
                
                self.operands.append(type)
                included_operands.add(type)
        
        #generate operator tokens
        self.operator_tokens = []
        for l in self.operators.values():
            for type in l:
                self.operator_tokens.append(type.identifier)
        
        #regex tokens for operands
        self.operand_patterns = []
        for type in self.operands:
            self.operand_patterns.append(type.pattern)
    
    def parse(self, string : str):
        pass
        
    def __str__(self) -> str:
        return("Operators:" + str(self.operators) + "\n"
               + "Operator Tokens:" + str(self.operator_tokens) + "\n"
               + "Operands:" + str(self.operands) + "\n"
               + "Operand Patterns:" + str(self.operand_patterns))