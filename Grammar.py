from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from Automata import State
from enum import Enum

@dataclass(unsafe_hash=True)
class StateRule:
    nonterminal : str
    production : tuple
    lookahead : any #value of enum type
    cursor: int

    def __str__(self) -> str:
        line = self.nonterminal + " -> "
        for e in self.production[:self.cursor]:
            line += str(e) + " "
        line += ". "
        for e in self.production[self.cursor:]:
           line += str(e) + " "
        line += ", " + str(self.lookahead)
        return(line)
       

class Grammar:
    def __init__(self, terminals : Enum, start : str, eof: any) -> None:
        self.start_symbol = start
        self.eof = eof
        self.Terminals = terminals
        self.grammar = defaultdict(list)
        self.firsts = defaultdict(set)
        self.nonterminals = set()
        self.automaton = None
        self.states = None
    def dump(self):
        for el in self.grammar:
            print(el, self.grammar[el])
    def addRule(self, nt, rule):
        self.grammar[nt].append(rule)
        self.nonterminals.add(nt)
        for e in rule:
            if(isinstance(e, str)): self.nonterminals.add(e)
    def genFirsts(self):
        self.first.cache_clear()
        self.firsts.clear()
        changed = True
        while(changed):
            changed = False
            for nt in self.nonterminals:
                orig = self.firsts[nt].copy()
                for prod in self.grammar[nt]:
                    for term in prod:
                        if(isinstance(term, str)):
                            self.firsts[nt] |= (self.firsts[term] - set([None]))
                            if(None not in self.firsts[term]): break
                        else:
                            self.firsts[nt].add(term)
                            break
                    else:
                        self.firsts[nt].add(None) #if can reach here it's nullable
                if(self.firsts[nt] != orig):
                    changed = True
    @cache
    def first(self, tokens) -> set:
        ret = set()
        for token in tokens:
            if(isinstance(token, str)):
                ret |= self.firsts[token]
                if(None not in self.firsts[token]): break
            else:
                ret.add(token)
                break
        else:
            ret.add(None)
        return(ret)
    
    def buildAutomaton(self):
        states = []
        def existing(state):
            for s in states:
                if(s == state): 
                    return(s)
            return(None)
        def closure(rules):
            while(True):
                orig = rules.copy()
                new_rules = set()
                for rule in rules:
                    nonterminal, production, lookahead, cursor = rule.nonterminal, rule.production, rule.lookahead, rule.cursor
                    if(cursor >= len(production) or not isinstance(production[cursor], str)): continue
                    new_nonterminal = production[cursor]
                    for new_prod in self.grammar[new_nonterminal]:
                        for next_token in self.first(production[cursor+1:]):
                            if(next_token == None):
                                new_rules.add(StateRule(new_nonterminal, new_prod, lookahead, 0))
                                continue
                            new_rules.add(StateRule(new_nonterminal, new_prod, next_token, 0))
                rules |= new_rules
                if(rules == orig):
                    break
        def build(rules):
            state = State(rules.copy())
            closure(state.rules)
            ex = existing(state)
            if(ex != None):
                return(ex)
            states.append(state)

            #generate state transitions
            nexts = defaultdict(set)
            for rule in state.rules:
                nonterminal, production, lookahead, cursor = rule.nonterminal, rule.production, rule.lookahead, rule.cursor
                if(cursor >= len(production)):
                    if(nonterminal == self.start_symbol):
                        state.addNext(self.eof, "ACCEPT")
                    continue
                nexts[production[cursor]].add(StateRule(nonterminal, production, lookahead, cursor + 1))
            
            #for next in nexts:
            #    print(next)
            #    for state in nexts[next]:
            #        print('\t', str(state))
            
        
            for transition_token in nexts:
                state.addNext(transition_token, build(nexts[transition_token]))
            
            return(state)
        
        self.automaton = build(set([
            StateRule(self.start_symbol, self.grammar[self.start_symbol][0], self.eof, 0)
        ]))

        self.states = states

    
    def dumpAutomaton(self):
        lines = []
        visited = []
        def visit(state):
            if(state in visited): return
            visited.append(state)
            if(state == "ACCEPT"): 
                lines.append("\n\nstate id: " + str(id(state)) + " is ACCEPT \n")
                return
            line = ""
            line += '\n'
            line += ("state id:" + str(id(state)) + "\n")
            line += ("rules:\n")
            r = []
            mappings = defaultdict(set)
            for rule in state.rules:
                mappings[(rule.nonterminal, rule.production, rule.cursor)].add(rule.lookahead)
                #r.append((str(rule) + '\n'))
            for nt, p, c in mappings:
                l = str(nt) + " -> "
                for i, e in enumerate(p):
                    if(i == c):
                        l += ". "
                    l += str(e) + " "
                l += str(mappings[(nt, p, c)])
                r.append(l + '\n')
            line += "".join(sorted(r))
            line += ("___________\n")
            line += "nexts:\n"
            for token in state.next:
                line += str(token) + " -> " + (state if isinstance(state, str) else str(id(state.next[token]))) + ' \n'
            lines.append(line)
            for nex in state.next.values():
                visit(nex)
        visit(self.automaton)
        print("len visited", len(visited), visited)
        print("".join(lines))