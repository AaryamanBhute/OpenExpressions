from dataclasses import dataclass
from Grammar import StateRule
from Automata import State
from collections import defaultdict

@dataclass
class Reduce:
    rule : StateRule

@dataclass
class Shift:
    next : int

class ParseTable:
    def __init__(self, states, start_symbol, eof_token) -> None:
        self.states = states
        self.count = len(states)
        state_num = {}
        for i, state in enumerate(states):
            state_num[id(state)] = i
        self.action = [dict() for i in range(self.count)]
        self.goto = [dict() for i in range(self.count)]
        for i, state in enumerate(states):
            actions = self.action[i]
            gotos = self.goto[i]
            #actions
            for rule in state.rules:
                if(rule.cursor == len(rule.production) and rule.nonterminal == start_symbol):
                    actions[eof_token] = "ACCEPT" #accept
                elif(rule.cursor == len(rule.production)):
                    if(rule.lookahead in actions): raise Exception("Conflict in Parse Table")
                    actions[rule.lookahead] = Reduce(rule)
                elif(not isinstance(rule.production[rule.cursor], str)): #if next if a terminal
                    next_terminal = rule.production[rule.cursor]
                    if(next_terminal not in state.next): raise Exception("Automaton does not contain necessary shift transition")
                    actions[next_terminal] = Shift(state_num[id(state.next[next_terminal])])
            #goto
            for transitions in state.next:
                if(not isinstance(transitions, str)): #if terminal
                    continue
                if(transitions not in state.next): raise Exception("Automaton does not contain necessary goto")
                gotos[transitions] = state_num[id(state.next[transitions])]
    def dump(self):
        for i in range(self.count):
            print(i)
            print('\t', self.action[i])
            print('\t', self.goto[i])