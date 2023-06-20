from collections import defaultdict
from functools import cache
from Automata import Node

class EOF:
    def __str__(self) -> str:
        return("$")

class Grammar:
    def __init__(self, tokens, start) -> None:
        self.end = EOF()
        self.start_symbol = start
        self.Tokens = tokens
        self.grammar = defaultdict(list)
        self.firsts = None
    def addRule(self, nt, rule):
        self.grammar[nt].append(rule)
    def genFirsts(self):
        self.firsts = {}
        for nonterminal in self.grammar:
            self.firsts[nonterminal] = self.first(nonterminal)
    @cache
    def first(self, t):
        if(t == None):
            return(set([None]))
        if(isinstance(t, self.Tokens)):
           return(set([t]))
        first = set()
        rules = self.grammar[t]
        nullable = False
        if([] in rules):
            first.add(None)
            nullable = True
        for rule in rules:
            if(rule == []): continue
            for el in rule:
                if(el == t and nullable): continue
                if(el == t and not nullable): break
                conts = self.first(el)
                first = first.union(conts)
                if(None not in conts):
                    break
        return(first)
    
    @cache
    def firstList(self, l):
        first = set()
        for e in l:
            if(e == self.end):
                first.add(self.end)
                return(first)
            cur = self.first(e)
            first = first.union(cur)
            if(None not in cur): break
        return(first)

    def buildAutomaton(self):
        states = []
        def existing(state):
            for s in states:
                if(state == s): return(s)
            return(None)
        
        def closure(rules):
            new_rules = set()
            for rule, cursor, looakahead in rules:
                if(cursor >= len(rule) or not isinstance(rule[cursor], str)): #if cursor at end or next is a terminal
                    continue
                for production in self.grammar[rule[cursor]]:
                    #print("prod", production)
                    #print("rule", rule , cursor,rule[cursor + 1:] + (looakahead,))
                    #print(rule[cursor + 1:] + (looakahead,), self.firstList(rule[cursor + 1:] + (looakahead,)))
                    for token in self.firstList(rule[cursor + 1:] + (looakahead,)):
                        new_rules.add(((rule[cursor],) + production, 1, token))
            for new_rule in new_rules: rules.add(new_rule)
        
        #state0 = set()
        #state0.add(((self.start_symbol,) + self.grammar[self.start_symbol][0], 1, self.end)) #setup initial state
        #closure(state0)
        #for rule in state0:
        #    print(rule)

        def buildState(rules):
            #rules -> [(rule, cursor_pos, lookahead)]
            cur_state = Node()
            for rule, cursor_pos, lookahead in rules:
                cur_state.addRule(rule, cursor_pos, lookahead)
            closure(cur_state.rules) #perform closure on the rules
            ex = existing(cur_state)
            if(ex): return(ex)
            
            #compute nexts
            transitions = defaultdict(set)
            for rule, cursor_pos, lookahead in cur_state.rules:
                if(cursor_pos >= len(rule)): continue
                transitions[rule[cursor_pos]].add((rule, cursor_pos + 1, lookahead))
            
            for token in transitions:
                cur_state.addNext(token, buildState(transitions[token]))
            
            return(cur_state)
        
        initial_state = buildState(set([((self.start_symbol,) + self.grammar[self.start_symbol][0], 1, self.end)]))
        print(initial_state)