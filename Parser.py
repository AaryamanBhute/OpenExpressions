from enum import Enum
from Operators import *
from Grammar import Grammar
from Tokenizer import Tokenizer
from ParseTable import ParseTable, Reduce, Shift

class Parser:
    def __init__(self, empty=False, rev=None) -> None:
        operators = {}
        operands = []
        rev = set()

        if(not empty):
            operators = { #based on order
                -1 : [Paren, Abs, Sigma, Pi], #wrapops and PolyOps
                70000 : [Pow],
                80000 : [Neg],
                90000 : [Mult, Div, IntDiv],
                100000 : [Add, Sub],
                
            }
            operands = [Int, Float, Var]
            rev = set([Pow])

        #add custom operands
        
        if(len(operands) == 0): raise Exception("Parser must be created with at least 1 operand")

        tokens = set()

        for p in operators:
            for op in operators[p]:
                if(issubclass(op, Binop)):
                    tokens.add(op.identifier)
                if(issubclass(op, WrapOp)):
                    tokens.add(op.left_ident)
                    tokens.add(op.right_ident)
                if(issubclass(op, UnOp)):
                    tokens.add(op.identifier)
                if(issubclass(op, PolyOp)):
                    tokens.add(r"\(")
                    tokens.add(r"\)")
                    tokens.add(r",")
                    tokens.add(op.identifier)
        tokens = list(tokens)
        tokens.sort(key=lambda a : len(a), reverse=True) #ensure that operators like ** are not interpreted as *, *
        
        operand_tokens = set()
        for op in operands:
            tokens.append(op.identifier)
            operand_tokens.add(op.identifier)
                
        self.Tokens = Enum('Tokens', ['_{n}'.format(n = i + 1) for i in range(len(tokens))] + ['_eof'])
        
        token_mappings = {}
        for i, ident in enumerate(tokens):
            token_mappings[ident] = self.Tokens(i + 1)
        
        prefix, num = "E", 1
        first_rule = (prefix + str(num))
        start_symbol = "S"
        
        self.eof_token = self.Tokens._eof

        self.grammar = Grammar(self.Tokens, start_symbol, self.eof_token)
        self.grammar.addRule(start_symbol, (prefix + str(num),))
        
        self.rule_mappings = {}
        for p in sorted(operators.keys(), reverse=True):
            cur, nex = prefix + str(num), prefix + str(num + 1)
            for op in operators[p]:
                rule = None
                if(issubclass(op, Binop)):
                    #allows for reverse binops
                    rule = (cur, token_mappings[op.identifier], nex) if op not in rev else (nex, token_mappings[op.identifier], cur)
                elif(issubclass(op, WrapOp)):
                    rule = (token_mappings[op.left_ident], first_rule, token_mappings[op.right_ident])
                elif(issubclass(op, UnOp)):
                    rule = (token_mappings[op.identifier], cur)
                elif(issubclass(op, PolyOp)):
                    rule = (token_mappings[op.identifier], token_mappings[r"\("])
                    for i in range(op.num_ops):
                        if(i > 0):
                            rule += (token_mappings[r","],)
                        rule += (first_rule,)
                    rule += (token_mappings[r"\)"],)
                if(rule == None): raise Exception("Attempting to add null rule to grammer")
                self.rule_mappings[(cur, rule)] = op #stores production to operation in form: (nt, (prod)) -> op
                self.grammar.addRule(cur, rule)
            rule = (nex,)
            self.grammar.addRule(cur, rule)
            self.rule_mappings[(cur, rule)] = None #no new op created
            num += 1
        for op in operands:
            cur = prefix + str(num)
            rule = (token_mappings[op.identifier],)
            self.grammar.addRule(cur, rule)
            self.rule_mappings[(cur, rule)] = op
        
        #prepare tokenizer
        self.tokenizer = Tokenizer([(ident, token_mappings[ident]) for ident in tokens], [(ident, token_mappings[ident]) for ident in operand_tokens])
        
        #create automaton
        self.grammar.buildAutomaton()
        #print(self.grammar.dump())

        #create parsetable
        self.table = ParseTable(self.grammar.states, start_symbol, self.eof_token)
    
    def tokenize(self, content):
        return(self.tokenizer.tokenize(content))
    
    def parse(self, content):
        if(content == ""): raise Exception("Cannot Parse Empty String")
        tokens = self.tokenizer.tokenize(content)
        state_stack = [0] # initial state
        used = []
        expression_nodes = []
        for token, image in tokens: #eat one token each iteration
            while((token in self.table.action[state_stack[-1]]) and (isinstance(self.table.action[state_stack[-1]][token], Reduce))):
                rule = self.table.action[state_stack[-1]][token].rule
                
                nt, prod = rule.nonterminal, rule.production
                prod_len = len(prod)

                if((nt, prod) not in self.rule_mappings): raise Exception("Op not found for rule during reduction")

                op = self.rule_mappings[(nt, prod)]
                
                #manage expression nodes being used in reduction
                expression_nodes, eaten_nodes = expression_nodes[:len(expression_nodes) - prod_len], expression_nodes[len(expression_nodes) - prod_len:]
                #manage state change
                state_stack = state_stack[:len(state_stack) - prod_len]
                
                if(op == None): #no change required to expression_nodes
                    expression_nodes += eaten_nodes
                elif(issubclass(op, Operand)):
                    expression_nodes.append(op(eaten_nodes[0])) # 0(raw value -> int, float, var...)
                elif(issubclass(op, Binop)): #eats 3 things
                    #manage expression composition
                    expression_nodes.append(op(eaten_nodes[0], eaten_nodes[2])) # 0(left) 1(op) 2(right)
                elif(issubclass(op, WrapOp)):
                    expression_nodes.append(op(eaten_nodes[1])) #0(left_ident) 1(expr) 2(right_ident)
                elif(issubclass(op, UnOp)):
                    expression_nodes.append(op(eaten_nodes[1])) #0(ident) 1(expr)
                elif(issubclass(op, PolyOp)):
                    #0(ident) #1(open paren) #2(param 1) #3(,) #4(param2) ...
                    params = []
                    for i in range(2, len(eaten_nodes), 2):
                        params.append(eaten_nodes[i])
                    expression_nodes.append(op(*params))
                else:
                    raise Exception("Unkown operator type")
                
                state_stack.append(self.table.goto[state_stack[-1]][nt]) #goto state from production
            
            
            if(token not in self.table.action[state_stack[-1]]): raise Exception("Parse Error, given expression is invalid")

            #shift
            action = self.table.action[state_stack[-1]][token]
            if(not isinstance(action, Shift)): raise Exception("Attempting to shift without correct shift action")

            expression_nodes.append(image)
            used.append(image)
            state_stack.append(action.next)

        #feed eof

        #reduce with eof
        token = self.eof_token
        while((token in self.table.action[state_stack[-1]]) and (isinstance(self.table.action[state_stack[-1]][token], Reduce))):
            rule = self.table.action[state_stack[-1]][token].rule
                
            nt, prod = rule.nonterminal, rule.production
            prod_len = len(prod)

            if((nt, prod) not in self.rule_mappings): raise Exception("Op not found for rule during reduction")
                
            op = self.rule_mappings[(nt, prod)]
                
            #manage expression nodes being used in reduction
            expression_nodes, eaten_nodes = expression_nodes[:len(expression_nodes) - prod_len], expression_nodes[len(expression_nodes) - prod_len:]
            #manage state change
            state_stack = state_stack[:len(state_stack) - prod_len]
            
            if(op == None): #no change required to expression_nodes
                expression_nodes += eaten_nodes
            elif(issubclass(op, Operand)):
                expression_nodes.append(op(eaten_nodes[0])) # 0(raw value -> int, float, var...)
            elif(issubclass(op, Binop)): #eats 3 things
                #manage expression composition
                expression_nodes.append(op(eaten_nodes[0], eaten_nodes[2])) # 0(left) 1(op) 2(right)
            elif(issubclass(op, WrapOp)):
                expression_nodes.append(op(eaten_nodes[1])) #0(left_ident) 1(expr) 2(right_ident)
            elif(issubclass(op, UnOp)):
                expression_nodes.append(op(eaten_nodes[1])) #0(ident) 1(expr)
            elif(issubclass(op, PolyOp)):
                #0(ident) #1(open paren) #2(param 1) #3(,) #4(param2) ...
                params = []
                for i in range(2, len(eaten_nodes), 2):
                    params.append(eaten_nodes[i])
                expression_nodes.append(op(*params))
            else:
                raise Exception("Unkown operator type")
                
            state_stack.append(self.table.goto[state_stack[-1]][nt]) #goto state from production

        if(self.eof_token not in self.table.action[state_stack[-1]]): raise Exception("Parse Error, unexpected or early EOF")

        if(self.table.action[state_stack[-1]][self.eof_token] != "ACCEPT"): raise Exception("Parse Error, unexpected or early EOF")

        #at this point, expression nodes should be compiled into a single root node at expression_nodes[0]

        return(expression_nodes[0])