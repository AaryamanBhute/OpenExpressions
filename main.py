from Tokenizer import Tokenizer
from Parser import Parser
from Grammar import Grammar
from enum import Enum

class Token(Enum):
    INTEGER = 1
    FLOAT = 2
    VARIABLE = 3
    PLUS = 4
    MINUS = 5
    TIMES = 6
    DIV = 7
    INTDIV = 8

def dumpAutomaton(automaton):
        visited = []
        def visit(node):
            if(node in visited): return
            visited.append(node)
            print("__________________")
            print(str(id(node)) + ":")
            for rule, cursor, lookahead in node.rules:
                print(rule[:cursor] + (".", ) + rule[cursor:], lookahead)
            for next in node.next:
                if(node.next[next] == True):
                    print(next, "ACCEPT")
                    continue
                print(next, str(id(node.next[next])))
            for child in node.next.values():
                if(child == True): continue
                visit(child)
        visit(automaton)

if __name__ == "__main__":
    #tokenizer = Tokenizer((r"\d+", Token.INTEGER), (r"\d*.\d+", Token.FLOAT), (r"[a-zA-Z]\w*", Token.VARIABLE),
    #                       (r"\+", Token.PLUS), (r"-", Token.MINUS), (r"\*", Token.TIMES), (r"//", Token.INTDIV), (r"/", Token.DIV))
    #print(tokenizer.tokenize("a + b //   15 + 16.2"))

    #parser = Parser()
    """for nt in parser.grammar.grammar:
        for rule in parser.grammar.grammar[nt]:
            l = nt + " -> "
            for e in rule:
                l += str(e) + ", "
            print(l)
    print(parser.tokenize("a + b // 15 + 16.2"))
    print(parser.grammar.firsts)"""
    #parser.dumpAutomaton()
    Tokens = Enum('Tokens', ['id', 'O', 'C', '_plus', '_eof'])
    grammar = Grammar(Tokens, "P", Tokens._eof)
    grammar.addRule("P", ("E",))
    grammar.addRule("E", ("E", Tokens._plus, "T"))
    grammar.addRule("E", ("T",))
    grammar.addRule("T", (Tokens.id, Tokens.O, "E", Tokens.C))
    grammar.addRule("T", (Tokens.id,))

    grammar.genFirsts()

    grammar.buildAutomaton()
    
    grammar.dumpAutomaton()
    