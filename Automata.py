class State:
    def __init__(self, rules=None) -> None:
        self.next = {}
        self.rules = set() if rules == None else rules
    
    def addRule(self, rule, pos, lookahead):
        self.rules.add((rule, pos, lookahead))
    
    def addNext(self, el, state):
        self.next[el] = state
    
    def __eq__(self, other: object) -> bool:
        if(not isinstance(other, State)):
            return(False)
        return(self.rules == other.rules)
    
    def __str__(self) -> str:
        ret = str(id(self)) + '\n'
        for rule in self.rules:
            ret += str(rule) + '\n'
        ret += str(self.next) + '\n'
        return(ret)