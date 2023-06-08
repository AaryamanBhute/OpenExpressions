from abc import ABC, abstractmethod
import re

class ExpressionNode(ABC):
    @abstractmethod
    def eval(self): pass

class Operator(ExpressionNode):
    pass

class Operand(ExpressionNode):
    pass

class Var(Operand):

    pattern = re.compile("[a-zA-Z]\w*")

    def __init__(self, i : str):
        self.identifier = i
    def eval(self, context=None):
        if(context == None or not isinstance(context, dict)):
            raise Exception("Attempting to evaluate variable without context")
        if(self.identifier not in context):
            raise Exception("Attempting to evaluate variable not present in context")
        return(context[self.identifier])

class Number(Operand):
    
    pattern = re.compile("(\d+ | \d*.d+ | \d+.d*)")

    def __init__(self, v : int|float):
        self.val = v
    def eval(self):
        return(self.val)

class BinaryOperator(Operator):
    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        self.left, self.right = l, r
    
    @abstractmethod
    def eval(self): pass

class UnaryOperator(Operator):
    def __init__(self, e : ExpressionNode):
        self.exp = e
    
    @abstractmethod
    def eval(self): pass

class Add(BinaryOperator):

    identifier = "+"
    
    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self):
        return(self.l.eval() + self.r.eval())

class Sub(BinaryOperator):

    identifier = "-"

    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self):
        return(self.l.eval() - self.r.eval())

class Mult(BinaryOperator):

    identifier = '*'

    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self):
        return(self.l.eval() * self.r.eval())

class Div(BinaryOperator):

    identifier = "/"

    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self):
        return(self.l.eval() / self.r.eval())

class IntDiv(BinaryOperator):

    identifier = "//"

    def __init__(l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self):
        return(self.l.eval() // self.r.eval())