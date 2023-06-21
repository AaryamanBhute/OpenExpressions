from enum import Enum
from collections import defaultdict
from functools import cache
from Operators import *
from Grammar import Grammar
from Tokenizer import Tokenizer

class Parser:
    def __init__(self) -> None:
        """
        operators = {
            0 : [Add, Sub],
            1 : [Mult, Div, IntDiv]
        }
        operands = [Int, Float, Var]
        """
        operators = {
            0 : [Add],
            1 : [Mult]
        }
        operands = [Int]
        
        
        tokens = []
        for p in sorted(operators.keys(), reverse=True):
            for op in sorted(operators[p], key=lambda a : len(a.identifier), reverse=True):
                tokens.append(op.identifier)
        
        for op in operands:
            tokens.append(op.identifier)
        
        self.Tokens = Enum('Tokens', ['_{n}'.format(n = i + 1) for i in range(len(tokens))])
        
        token_mappings = {}
        for i, ident in enumerate(tokens):
            token_mappings[ident] = self.Tokens(i + 1)

        prefix, num = "E", 1
        
        start_symbol = "S"

        self.grammar = Grammar(self.Tokens, "S")
        self.grammar.addRule(start_symbol, (prefix + str(num),))
        
        self.rule_mappings = {}
        for p in sorted(operators.keys(), reverse=True):
            cur, nex = prefix + str(num), prefix + str(num + 1)
            for op in operators[p]:
                rule = (cur, token_mappings[op.identifier], nex)
                self.rule_mappings[rule] = op
                self.grammar.addRule(cur, rule)
            self.grammar.addRule(cur, (nex,))
            num += 1
        for op in operands: self.grammar.addRule((prefix + str(num)), (token_mappings[op.identifier],))        
        
        #prepare tokenizer
        self.tokenizer = Tokenizer(*[(ident, token_mappings[ident]) for ident in tokens])
        
        #create automaton
        self.automaton = self.grammar.buildAutomaton()
    
    def tokenize(self, content):
        return(self.tokenizer.tokenize(content))
    
    def dumpAutomaton(self):
        visited = []
        def visit(node):
            if(node in visited): return
            visited.append(node)
            print("__________________")
            print(str(id(node)) + ":")
            mappings = defaultdict(set)
            for rule, cursor, lookahead in node.rules:
                mappings[(rule, cursor,)].add(lookahead)
            for rule, cursor in mappings:
                print(rule[:cursor] + (".", ) + rule[cursor:], lookahead)
            print("nexts:")
            for next in node.next:
                if(node.next[next] == True):
                    print(next, "ACCEPT")
                    continue
                print(next, str(id(node.next[next])))
            for child in node.next.values():
                if(child == True): continue
                visit(child)
        visit(self.automaton)