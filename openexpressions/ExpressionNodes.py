from abc import ABC, abstractmethod

class ExpressionNode(ABC):
    @abstractmethod
    def eval(self):
        pass

class Operand(ExpressionNode):
    @property
    @abstractmethod
    def identifier(self):pass
    
    def __init__(self, v) -> None:
        self.val = v

class Int(Operand):
    identifier = r"\d+(?!\.)"
    def __init__(self, v) -> None:
        super().__init__(int(v))
    def eval(self, context=None):
        return(self.val)

class BoolVal(Operand):
    identifier = r"(0 | 1)"
    def __init__(self, v) -> None:
        super().__init__(int(v))
    def eval(self, context=None):
        return(self.val)

class Float(Operand):
    identifier = r"\d*\.\d+"
    def __init__(self, v) -> None:
        super().__init__(float(v))
    def eval(self, context=None):
        return(self.val)

class Var(Operand):
    negation_inclusive = True
    identifier = r"[a-zA-Z]\w*"
    def __init__(self, v) -> None:
        super().__init__(str(v))
    def eval(self, context=None):
       if(context == None): raise Exception("Attempting to evaluate variable without context")
       if(self.val not in context): raise Exception("Attempting to evaluate variable with no definition in context")
       return(context[self.val])

class BoolVar(Operand):
    identifier = r"[a-zA-Z]\w*"
    def __init__(self, v) -> None:
        super().__init__(str(v))
    def eval(self, context=None):
       if(context == None): raise Exception("Attempting to evaluate variable without context")
       if(self.val not in context): raise Exception("Attempting to evaluate variable with no definition in context")
       val = context[self.val]
       if(int(val) != val): raise Exception("Boolean Var must be 0 or 1")
       val = int(val)
       if(val > 1 or val < 0): raise Exception("Boolean Var must be 0 or 1")
       return(val)

class Operator(ExpressionNode):
    pass

class BinOp(Operator):
    @property
    @abstractmethod
    def identifier(self):pass

    def __init__(self, l, r) -> None:
        self.left, self.right = l, r

class Add(BinOp):
    identifier = r"\+"
    def __init__(self, l, r) -> None:
        super().__init__(l, r)
    def eval(self, context=None):
        return(self.left.eval(context) + self.right.eval(context))

class Sub(BinOp):
    identifier = r"-"
    def __init__(self, l, r) -> None:
        super().__init__(l, r)
    def eval(self, context=None):
        return(self.left.eval(context) - self.right.eval(context))

class Mult(BinOp):
    identifier = r"\*"
    def __init__(self, l, r) -> None:
        super().__init__(l, r)
    def eval(self, context=None):
        return(self.left.eval(context) * self.right.eval(context))

class Div(BinOp):
    identifier = r"/"
    def __init__(self, l, r) -> None:
        super().__init__(l, r)
    def eval(self, context=None):
        return(self.left.eval(context) / self.right.eval(context))

class IntDiv(BinOp):
    identifier = r"//"
    def __init__(self, l, r) -> None:
        super().__init__(l, r)
    def eval(self, context=None):
        return(self.left.eval(context) // self.right.eval(context))

class BitAnd(BinOp):
    identifier = r"&"
    def __init__(self, l, r) -> None:
        super().__init__(l, r)
    def eval(self, context=None):
        return(self.left.eval(context) & self.right.eval(context))

class BitOr(BinOp):
    identifier = r"\|"
    def __init__(self, l, r) -> None:
        super().__init__(l, r)
    def eval(self, context=None):
        return(self.left.eval(context) | self.right.eval(context))

class BitXOr(BinOp):
    identifier = r"\^"
    def __init__(self, l, r) -> None:
        super().__init__(l, r)
    def eval(self, context=None):
        return(self.left.eval(context) ^ self.right.eval(context))
    
class Mod(BinOp):
    identifier = r"%"
    def __init__(self, l, r) -> None:
        super().__init__(l, r)
    def eval(self, context=None):
        return(self.left.eval(context) % self.right.eval(context))

class Pow(BinOp):
    identifier = r"\*\*"
    def __init__(self, l, r) -> None:
        super().__init__(l, r)
    def eval(self, context=None):
        left_val = self.left.eval(context)
        right_val = self.right.eval(context)
        if(hasattr(self.left.__class__, 'negation_inclusive') and self.left.__class__.negation_inclusive): return(left_val ** right_val)
        return(-(abs(left_val) ** right_val) if left_val < 0 else left_val ** right_val)

class UnOp(Operator):
    @property
    @abstractmethod
    def identifier(self):pass

    def __init__(self, e) -> None:
        self.expr = e

class Neg(UnOp):
    identifier = r"-"
    def __init__(self, e) -> None:
        super().__init__(e)
    def eval(self, context=None):
        return(-self.expr.eval(context))

class Not(UnOp):
    identifier = r"~"
    def __init__(self, e) -> None:
        super().__init__(e)
    def eval(self, context):
        return(~self.expr.eval(context))

class WrapOp(Operator):
    @property
    @abstractmethod
    def left_identifier(self):pass

    @property
    @abstractmethod
    def right_identifier(self):pass

    def __init__(self, e) -> None:
        self.expr = e

class Paren(WrapOp):
    negation_inclusive = True
    left_identifier = r"\("
    right_identifier = r"\)"

    def __init__(self, e) -> None:
        super().__init__(e)
    
    def eval(self, context):
        return(self.expr.eval(context))

class Abs(WrapOp):
    negation_inclusive = True
    left_identifier = r"\|"
    right_identifier = r"\|"
    def __init__(self, e) -> None:
        super().__init__(e)
    def eval(self, context):
        return(abs(self.expr.eval(context)))

class PolyOp(Operator):
    @property
    @abstractmethod
    def identifier(self):pass

    @property
    @abstractmethod
    def num_fields(self):pass
    
    def __init__(self, *args) -> None:
        num_fields = self.__class__.num_fields
        if(len(args) != num_fields): raise Exception("Invalid Number of Fields while creating PolyOp: {op}".format(op=self.__class__))
        self.ops = [None] * num_fields
        for i, arg in enumerate(args):
            self.ops[i] = arg

class Sum(PolyOp):
    negation_inclusive = True
    num_fields = 4
    identifier = r"SUM"
    
    def __init__(self, v, l, u, e) -> None:
        super().__init__(v, l, u, e)
    
    def eval(self, context=None):

        if(context == None):
            context = dict()

        if(not isinstance(self.ops[0], Var)): raise Exception("Not a valid variable to define")
        
        lower_bound = self.ops[1].eval(context)
        if(int(lower_bound) != lower_bound): raise Exception("Lower Bound on Sum Operation is not an integer")
        lower_bound = int(lower_bound)
        upper_bound = self.ops[2].eval(context)
        if(int(upper_bound) != upper_bound): raise Exception("Upper Bound on Sum Operation is not an integer")
        upper_bound = int(upper_bound)

        s = 0
        sub_context = context.copy()
        for i in range(lower_bound, upper_bound + 1):
            sub_context[self.ops[0].val] = i
            s += self.ops[3].eval(sub_context)
        return(s)

class Prod(PolyOp):
    negation_inclusive = True
    num_fields = 4
    identifier = r"PROD"
    
    def __init__(self, v, l, u, e) -> None:
        super().__init__(v, l, u, e)
    
    def eval(self, context=None):

        if(context == None):
            context = dict()

        if(not isinstance(self.ops[0], Var)): raise Exception("Not a valid variable to define")
        
        lower_bound = self.ops[1].eval(context)
        if(int(lower_bound) != lower_bound): raise Exception("Lower Bound on Prod Operation is not an integer")
        lower_bound = int(lower_bound)
        upper_bound = self.ops[2].eval(context)
        if(int(upper_bound) != upper_bound): raise Exception("Upper Bound on Prod Operation is not an integer")
        upper_bound = int(upper_bound)

        if(upper_bound < lower_bound): raise Exception("Upper Bound is smaller than Lower Bound on Prod Operation")

        s = 1
        sub_context = context.copy()
        for i in range(lower_bound, upper_bound + 1):
            sub_context[self.ops[0].val] = i
            s *= self.ops[3].eval(sub_context)
        return(s)