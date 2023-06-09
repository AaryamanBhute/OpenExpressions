from abc import ABC, abstractmethod

class ExpressionNode(ABC):
    @abstractmethod
    def eval(self): pass
    @abstractmethod
    def __str__(self) -> str: pass

class Operator(ExpressionNode):
    pass

class Operand(ExpressionNode):
    pass

class Var(Operand):

    pattern = "[a-zA-Z]\w*"

    def __init__(self, i : str):
        self.identifier = i
    def eval(self, context=None):
        if(context == None or not isinstance(context, dict)):
            raise Exception("Attempting to evaluate variable without context")
        if(self.identifier not in context):
            raise Exception("Attempting to evaluate variable not present in context")
        return(context[self.identifier])
    def __str__(self) -> str:
        return(str(self.identifier))

class Int(Operand):
    
    pattern = "\d+"

    def __init__(self, v : str):
        self.val = int(v)
    def eval(self, context=None):
        return(self.val)
    
    def __str__(self) -> str:
        return(str(self.val))

class Float(Operand):

    pattern = "(\d*.d+|\d+.d*)"

    def __init__(self, v : str):
        self.val = float(v)
    def eval(self, context=None):
        return(self.val)
    def __str__(self) -> str:
        return(str(self.val))

class BinaryOperator(Operator):
    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        self.left, self.right = l, r

class UnaryOperator(Operator):
    def __init__(self, e : ExpressionNode):
        self.exp = e
    
    @abstractmethod
    def eval(self): pass

class Add(BinaryOperator):

    identifier = "+"
    
    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self, context=None):
        return(self.left.eval(context) + self.right.eval(context))
    
    def __str__(self) -> str:
        return(Add.identifier)

class Sub(BinaryOperator):

    identifier = "-"

    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self, context=None):
        return(self.left.eval(context) - self.right.eval(context))
    
    def __str__(self) -> str:
        return(Sub.identifier)

class Mult(BinaryOperator):

    identifier = '*'

    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self, context=None):
        return(self.left.eval(context) * self.right.eval(context))
    
    def __str__(self) -> str:
        return(Mult.identifier)
    

class Div(BinaryOperator):

    identifier = "/"

    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self, context=None):
        return(self.left.eval(context) / self.right.eval(context))
    
    def __str__(self, context=None) -> str:
        return(Div.identifier)

class IntDiv(BinaryOperator):

    identifier = "//"

    def __init__(l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self, context=None):
        return(self.left.eval(context) // self.right.eval(context))
    
    def __str__(self) -> str:
        return(IntDiv.identifier)

class Pow(BinaryOperator):

    identifier = "**"

    def __init__(self, l : ExpressionNode, r : ExpressionNode):
        super().__init__(l, r)

    def eval(self, context=None):
        return(self.left.eval(context) ** self.right.eval(context))
    
    def __str__(self) -> str:
        return(Pow.identifier)

def printExpr(expr : ExpressionNode, prefix=""):
    if(isinstance(expr, Operand)):
        print(prefix + str(expr))
    elif(isinstance(expr, BinaryOperator)):
        print(prefix + str(expr))
        printExpr(expr.left, prefix + '\t')
        printExpr(expr.right, prefix + '\t')
    else:
        raise Exception("Invalid Object in Expression", expr.__class__())