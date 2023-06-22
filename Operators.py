from abc import ABC, abstractmethod

class Operand(ABC):
    @abstractmethod
    def eval(self):
        pass

class Int(Operand):
    identifier = r"\d+"
    def __init__(self, v) -> None:
        self.val = int(v)
    def eval(self, context=None):
        return(self.val)
    def __str__(self) -> str:
        return(str(self.val))

class Float(Operand):
    identifier = r"\d*.\d+"
    def __init__(self, v) -> None:
        self.val = float(v)
    def eval(self, context=None):
        return(self.val)
    def __str__(self) -> str:
        return(str(self.val))

class Var(Operand):
    identifier = r"[a-zA-Z]\w*"
    def __init__(self, i) -> None:
        self.image = str(i)
    def eval(self, context=None):
       if(context == None): raise Exception("Attempting to evaluate variable without context")
       if(self.image not in context): raise Exception("Attempting to evaluate variable with no definition in context")
       return(context[self.image])
    def __str__(self) -> str:
        return(str(self.image))

class Operator(ABC):
    pass

class Binop(Operator):
    @abstractmethod
    def eval(self):
        pass

class Add(Binop):
    identifier = r"\+"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self, context=None):
        return(self.left.eval(context) + self.right.eval(context))

class Sub(Binop):
    identifier = r"-"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self, context=None):
        return(self.left.eval(context) - self.right.eval(context))

class Mult(Binop):
    identifier = r"\*"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self, context=None):
        return(self.left.eval(context) * self.right.eval(context))

class Div(Binop):
    identifier = r"/"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self, context=None):
        return(self.left.eval(context) / self.right.eval(context))

class IntDiv(Binop):
    identifier = r"//"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self, context=None):
        return(self.left.eval(context) // self.right.eval(context))