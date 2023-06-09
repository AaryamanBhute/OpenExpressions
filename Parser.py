from ExpressionNodes import *
from collections import defaultdict
import re
from enum import Enum


class Parser:
    class TokenType(Enum):
        OPERATOR = 1
        OPERAND = 2
    
    def __init__(self, mode="basic", additional_operators=None, additional_operands=None) -> None:
        
        self.operators = defaultdict(list)
        self.operands = []

        included_operators = set()
        included_operands = set()

        self.identifier_type = defaultdict(list)
        self.type_priority = defaultdict(int)
        
        #preset configurations
        match(mode):
            case "basic":
                self.operators[1000] += [Add, Sub]
                self.type_priority[Add], self.type_priority[Sub] = 1000, 1000
                self.operators[2000] += [Mult, Div, IntDiv]
                self.type_priority[Mult], self.type_priority[Div], self.type_priority[IntDiv] = 2000, 2000, 2000
                self.operators[3000] += [Pow]
                self.type_priority[Pow] = 3000
                
                included_operators.update((Add, Sub, Mult, Div, IntDiv, Pow))
                for type in (Add, Sub, Mult, Div, IntDiv, Pow):
                    self.identifier_type[type.identifier].append(type)

                self.operands += [Var, Int, Float]
                included_operands.update((Var, Int, Float))
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
                self.operator_tokens.append((type.identifier, type))
        
        self.operator_tokens.sort(key=lambda a : len(a[0]), reverse=True)
        
        #regex tokens for operands
        self.operand_patterns = []
        for type in self.operands:
            self.operand_patterns.append((type.pattern, type))
    
    #TODO - optimize with trie
    def tokenize(self, string : str):
        tokens = []
        
        while(len(string) > 0):
            string = string.lstrip()
            added = False
            for token, type in self.operator_tokens:
                if(string.startswith(token)):
                    string = string[len(token):]
                    tokens.append((token, self.TokenType.OPERATOR))
                    added = True
                    break
            
            if(added):
                continue
            
            for pattern, type in self.operand_patterns:
                m = re.compile(pattern).match(string)
                if(m != None):
                    string = string[m.end():]
                    tokens.append((m.group(0), self.TokenType.OPERAND, type))
                    added = True
                    break
            
            if(not added):
                raise Exception("Could not find match for with remaining string:", string)
        
        return(tokens)

    def parse(self, string : str, context : dict = None):
        tokens = self.tokenize(string)
        
        def build(i, j):
            if(i < 0 or i >= len(tokens) or j < 0 or j >= len(tokens)): raise Exception("Out or range while building", tokens, i, j)
            if(i == j):
                image, token_type, node_type = tokens[i][0], tokens[i][1], tokens[i][2]
                if(token_type == self.TokenType.OPERATOR): raise Exception("Failed to build Parse Tree")
                return(node_type(image))
            #seek bin ops
            weakest_op, op_strength, pos = None, float('inf'), -1
            for k in range(j, i - 1, -1):
                image, token_type = tokens[k][0], tokens[k][1]
                if(token_type == self.TokenType.OPERAND): continue
                if(image not in self.identifier_type): raise Exception("Invalid op in tokens")
                for op in self.identifier_type[image]:
                    if(not issubclass(op, BinaryOperator)): continue
                    if(weakest_op == None):
                        weakest_op = op
                        op_strength = self.type_priority[op]
                        pos = k
                    elif(self.type_priority[op] < op_strength):
                        weakest_op = op
                        op_strength = self.type_priority[op]
                        pos = k
            if(weakest_op == None):
                raise Exception("Failed to parse: no operators remaining with multiple operands")
            return(weakest_op(build(i, pos - 1), build(pos + 1, j)))

        
        return(build(0, len(tokens) - 1))
        
        
    def __str__(self) -> str:
        return("Operators:" + str(self.operators) + "\n"
               + "Operator Tokens:" + str(self.operator_tokens) + "\n"
               + "Operands:" + str(self.operands) + "\n"
               + "Operand Patterns:" + str(self.operand_patterns))