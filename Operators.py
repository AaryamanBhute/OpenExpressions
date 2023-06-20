from abc import ABC, abstractmethod

class Operand(ABC):
    @abstractmethod
    def eval(self):
        pass

class Int(Operand):
    identifier = r"\d+"
    def __init__(self, v) -> None:
        self.val = v
    def eval(self, context=None):
        return(self.val)

class Float(Operand):
    identifier = r"\d*.\d+"
    def __init__(self, v) -> None:
        self.val = v
    def eval(self, context=None):
        return(self.val)

class Var(Operand):
    identifier = r"[a-zA-Z]\w*"
    def __init__(self, i) -> None:
        self.image = i
    def eval(self, context=None):
       if(context == None): raise Exception("Attempting to evaluate variable without context")
       if(self.image not in context): raise Exception("Attempting to evaluate variable with no definition in context")
       return(context[self.image])
        

class Binop(ABC):
    @abstractmethod
    def eval(self):
        pass

class Add(Binop):
    identifier = r"\+"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self):
        return(self.left.eval() + self.right.eval())

class Sub(Binop):
    identifier = r"-"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self):
        return(self.left.eval() - self.right.eval())

class Mult(Binop):
    identifier = r"\*"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self):
        return(self.left.eval() * self.right.eval())

class Div(Binop):
    identifier = r"/"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self):
        return(self.left.eval() / self.right.eval())

class IntDiv(Binop):
    identifier = r"//"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self):
        return(self.left.eval() // self.right.eval())