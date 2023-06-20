class Node:
    def __init__(self) -> None:
        self.next = {}
        self.rules = set()
    
    def addRule(self, rule, pos, lookahead):
        self.rules.add((rule, pos, lookahead))
    
    def addNext(self, el, state):
        self.next[el] = state
    
    def __eq__(self, other: object) -> bool:
        if(isinstance(other, Node)):
            return(self.rules == other.rules)
        return(False)
    
    def __str__(self) -> str:
        ret = str(id(self)) + '\n'
        for rule in self.rules:
            ret += str(rule) + '\n'
        ret += str(self.next) + '\n'
        return(ret)