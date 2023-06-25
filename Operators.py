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
class BoolVal(Operand):
    identifier = r"(0 | 1)"
    def __init__(self, v) -> None:
        self.val = int(v)
    def eval(self, context=None):
        return(self.val)
    def __str__(self) -> str:
        return(str(self.val))

class Float(Operand):
    identifier = r"\d*\.\d+"
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

class BoolVar(Operand):
    identifier = r"[a-zA-Z]\w*"
    def __init__(self, i) -> None:
        self.image = str(i)
    def eval(self, context=None):
       if(context == None): raise Exception("Attempting to evaluate variable without context")
       if(self.image not in context): raise Exception("Attempting to evaluate variable with no definition in context")
       val = context[self.image]
       if(int(val) != val): raise Exception("Boolean Var must be 0 or 1")
       val = int(val)
       if(val > 1 or val < 0): raise Exception("Boolean Var must be 0 or 1")
       return(val)
    def __str__(self) -> str:
        return(str(self.image))

class Operator(ABC):
    @abstractmethod
    def eval(self):
        pass

class Binop(Operator):
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

class BitAnd(Binop):
    identifier = r"&"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self, context=None):
        return(self.left.eval(context) & self.right.eval(context))

class BitOr(Binop):
    identifier = r"\|"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self, context=None):
        return(self.left.eval(context) | self.right.eval(context))

class BitXOr(Binop):
    identifier = r"\^"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self, context=None):
        return(self.left.eval(context) ^ self.right.eval(context))
    
class Mod(Binop):
    identifier = r"%"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self, context=None):
        return(self.left.eval(context) % self.right.eval(context))

class Pow(Binop):
    identifier = r"\*\*"
    def __init__(self, l, r) -> None:
        self.left, self.right = l, r
    def eval(self, context):
        return(self.left.eval(context) ** self.right.eval(context))

class UnOp(Operator):
    pass

class Neg(UnOp):
    identifier = r"-"
    def __init__(self, e) -> None:
        self.expr = e
    def eval(self, context):
        return(-self.expr.eval(context))

class BitInv(UnOp):
    identifier = r"~"
    def __init__(self, e) -> None:
        self.expr = e
    def eval(self, context):
        return(~self.expr.eval(context))

class WrapOp(Operator):
    pass

class Paren(WrapOp):
    left_ident = r"\("
    right_ident = r"\)"
    def __init__(self, e) -> None:
        self.expr = e
    def eval(self, context):
        return(self.expr.eval(context))

class Abs(WrapOp):
    left_ident = r"\|"
    right_ident = r"\|"
    def __init__(self, e) -> None:
        self.expr = e
    def eval(self, context):
        return(abs(self.expr.eval(context)))

class PolyOp(Operator):
    pass

class Sigma(PolyOp):
    num_ops = 4
    identifier = r"SUM"
    
    def __init__(self, v, l, u, e) -> None:
        self.var = v
        self.lower = l
        self.upper = u
        self.expr = e
    
    def eval(self, context):

        if(not isinstance(self.var, Var)): raise Exception("Not a valid variable to define")
        
        lower_bound = self.lower.eval(context)
        if(int(lower_bound) != lower_bound): raise Exception("Lower Bound on SIGMA Operation is not an integer")
        lower_bound = int(lower_bound)
        upper_bound = self.upper.eval(context)
        if(int(upper_bound) != upper_bound): raise Exception("Upper Bound on SIGMA Operation is not an integer")
        upper_bound = int(upper_bound)

        s = 0
        sub_context = context.copy()
        for i in range(lower_bound, upper_bound + 1):
            sub_context[self.var.image] = i
            s += self.expr.eval(sub_context)
        return(s)

class Pi(PolyOp):
    num_ops = 4
    identifier = r"PROD"
    
    def __init__(self, v, l, u, e) -> None:
        self.var = v
        self.lower = l
        self.upper = u
        self.expr = e
    
    def eval(self, context):

        if(not isinstance(self.var, Var)): raise Exception("Not a valid variable to define")
        
        lower_bound = self.lower.eval(context)
        if(int(lower_bound) != lower_bound): raise Exception("Lower Bound on PI Operation is not an integer")
        lower_bound = int(lower_bound)
        upper_bound = self.upper.eval(context)
        if(int(upper_bound) != upper_bound): raise Exception("Upper Bound on PI Operation is not an integer")
        upper_bound = int(upper_bound)

        if(upper_bound < lower_bound): raise Exception("Upper Bound is smaller than Lower Bound on PI Operation")

        s = 1
        sub_context = context.copy()
        for i in range(lower_bound, upper_bound + 1):
            sub_context[self.var.image] = i
            s *= self.expr.eval(sub_context)
        return(s)