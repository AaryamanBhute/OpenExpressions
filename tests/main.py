from openexpressions.Parser import Parser
from openexpressions.ExpressionNodes import UnOp, BinOp, PolyOp, WrapOp, Operand, Var, Paren
import math
import re

class Vector(Operand):
    identifier = r"<-?(\d+.\d+|\d+), -?(\d+.\d+|\d+), -?(\d+.\d+|\d+)>"
    def __init__(self, image) -> None:
        super().__init__(tuple(float(i) for i in re.findall(r"-?(\d+.\d+|\d+)", image)))
    def eval(self, context=None):
        return(self.val)

class Negate(UnOp):
    identifier = r"-"
    def __init__(self, expression) -> None:
        super().__init__(expression)
    def eval(self, context=None):
        return(tuple(-i for i in self.expr.eval(context)))

class CrossProduct(BinOp):
    identifier = r"X"
    def __init__(self, left_expression, right_expression) -> None:
        super().__init__(left_expression, right_expression)
    def eval(self, context=None):
        lv = self.left.eval(context)
        rv = self.right.eval(context)
        return((lv[1] * rv[2] - lv[2] * rv[1], lv[2] * rv[0] - lv[0] * rv[2], lv[0] * rv[1] - lv[1] * rv[0]))

class DotProduct(BinOp):
    identifier = r"\."
    def __init__(self, left_expression, right_expression) -> None:
        super().__init__(left_expression, right_expression)
    def eval(self, context=None):
        lv = self.left.eval(context)
        rv = self.right.eval(context)
        s = 0
        for i in range(3):
            s += lv[i] * rv[i]
        return(s)

class Magnitude(WrapOp):
    left_identifier = r"\|"
    right_identifier = r"\|"
    def __init__(self, expression) -> None:
        super().__init__(expression)
    def eval(self, context=None):
        v = self.expr.eval(context)
        s = 0
        for i in range(3):
            s += abs(v[i]) ** 2
        return(math.sqrt(s))

class Select(PolyOp):
    identifier = r"SELECT"
    num_fields = 3

    def __init__(self, one, two, three) -> None:
        super().__init__(one, two, three)
    def eval(self, context=None):
        one = self.ops[0].eval(context)
        two = self.ops[1].eval(context)
        three = self.ops[2].eval(context)
        return((one[0], two[1], three[2]))


if __name__ == "__main__":
    vector_parser = Parser(mode="empty",
                           custom_operands=(Vector, Var),
                           custom_operators=((Negate, 10), (CrossProduct, 20, False), (DotProduct, 20, False), Magnitude, Select, Paren))
    print(vector_parser.parse("-(SELECT(<0, -991, -992>, <-990, 1, -992>, <-990, -991, 2>) X <3, 4, 5>) . a").eval({'a': (-6, 7, -8)}))