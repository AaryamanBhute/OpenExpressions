from openexpressions.Parser import Parser
from openexpressions.ExpressionNodes import *
import random

def basic_test(parser, expr):
    assert(parser.parse(expr).eval() == eval(expr))

def context_test(parser, expr, context):
    assert(parser.parse(expr).eval(context) == eval(expr, context))

def test_operations():
    # prepare parser with default settings (math mode)
    parser = Parser()
    basic_test(parser, "1 + 1")
    basic_test(parser, "2 * 2")
    basic_test(parser, "35 - 14")
    basic_test(parser, "24 / 5")
    basic_test(parser, "24 // 5")
    basic_test(parser, "24 % 5")
    basic_test(parser, "2 ** 5")

    basic_test(parser, "-2 ** -5")
    basic_test(parser, "2.5 // 2")
    basic_test(parser, "2.5 // 2.5")
    basic_test(parser, "9 % 2")
    basic_test(parser, "-18//-2")
    basic_test(parser, "18//-2")
    basic_test(parser, "-18//2")

    # prepare parser with boolean settings (boolean mode)
    parser = Parser(mode="boolean")
    basic_test(parser, "0 | 1")
    basic_test(parser, "0 | 0")
    basic_test(parser, "1 | 1")
    basic_test(parser, "0 & 1")
    basic_test(parser, "0 & 0")
    basic_test(parser, "1 & 1")
    basic_test(parser, "0 ^ 1")
    basic_test(parser, "0 ^ 0")
    basic_test(parser, "1 ^ 1")

def test_order_of_operations():
    parser = Parser()
    basic_test(parser, "1 + 1 + 15 + 67")
    basic_test(parser, "1 + 1 * 15 - 67")
    basic_test(parser, "1 + 1 ** 15 - 67")
    basic_test(parser, "2 ** 3 ** 4 + 1 * 15 - 67")
    basic_test(parser, "2 ** 3 ** (4 + 1 )* (15 - 67)")
    basic_test(parser, "(1 * (3 + (2))) ** (2 - (7 - 3))")
    basic_test(parser, "-----1")
    basic_test(parser, "-----1 ** 5")
    basic_test(parser, "-1 ** 5")
    basic_test(parser, "-1 ** 6")
    basic_test(parser, "-1 ** -1")
    basic_test(parser, "-4 ** -1 ** -2 ** -8")
    basic_test(parser, "(-1)**2")
    basic_test(parser, "1 + 8%3**2")

    #SUM and PROD
    assert(parser.parse("SUM (a, 2 ** 3, 2 ** 5, a + 3) * PROD (z, 6 // 2, 6, z ** 2 / 3)").eval() == 920000)

    parser = Parser(mode="boolean")
    basic_test(parser, "1 | 1 & 0 ")
    basic_test(parser, "1 | 1 & 0 ^ 1")
    basic_test(parser, "1 | 1 & 0 ^ 1 & 1 & 1 ^ 1 | 0 | 0 & 0 ^ 0")
    basic_test(parser, "1 | 1 & (0 ^ 1) & 1 & (1 ^ 1 | 0 | 0 & 0) ^ 0")
    basic_test(parser, "1 | (1 & 0 ^ 1 & 1 & 1 ^ 1 | 0 | 0 & 0 ^ 0)")

def test_context():
    parser = Parser()
    context_test(parser, "a + b ** c", {'a' : 1, 'b' : 5, 'c' : 3})
    context_test(parser, "b ** c", {'a' : 1, 'b' : -5, 'c' : 4})
    context_test(parser, "a ** b + b / (c - b + 9 ** 2)", {'a': 12, 'b': 2, 'c': 3})

    #SUM and PROD
    assert(parser.parse("SUM (a, b ** c, b ** 5, a + c) * PROD (z, 6 // b, 6, z ** b / c) + a + z").eval({'b' : 2, 'c': 3, 'a': 5, 'z': 10}) == 920015)

    parser = Parser(mode="boolean")
    context_test(parser, "a | (1 & 0 ^ b & 1 & 1 ^ 1 | c | 0 & d ^ 0)", {'a': 1, 'b':1 , 'c': 0, 'd': 1})

def test_custom_ops():
    class custom_operand_letter(Operand):
        identifier = r"[a-zA-Z]"
        def __init__(self, v) -> None:
            super().__init__(str(v))
        def eval(self, context=None):
            return(self.val)
    class custom_operand_digit(Operand):
        identifier = r"\d"
        def __init__(self, v) -> None:
            super().__init__(int(v))
        def eval(self, context=None):
            return(self.val)
    class custom_unop(UnOp):
        identifier = r"_"
        def __init__(self, e) -> None:
            super().__init__(e)
        def eval(self, context=None):
            return(ord(self.expr.eval()) - ord('a'))
    class custom_binop_mult(BinOp):
        identifier = r"\*"
        def __init__(self, l, r) -> None:
            super().__init__(l, r)
        def eval(self, context=None):
            return(self.left.eval(context) * self.right.eval(context))
    class custom_binop_add(BinOp):
        identifier = r"\+"
        def __init__(self, l, r) -> None:
            super().__init__(l, r)
        def eval(self, context=None):
            return(self.left.eval(context) + self.right.eval(context))
    class custom_wrapop(WrapOp):
        left_identifier = r"\|"
        right_identifier = r"\|"
        def __init__(self, e) -> None:
            super().__init__(e)
        def eval(self, context=None):
            return(len(self.expr.eval(context)))
    class custom_polyop(PolyOp):
        num_fields = 2
        identifier = r"RAND"
        
        def __init__(self, l, u) -> None:
            super().__init__(l, u)
        
        def eval(self, context=None):
            return(random.randint(self.left.eval(context), self.right.eval(context)))

    parser = Parser(mode="empty",
                    custom_operators=((custom_binop_add, 100, False), (custom_binop_mult, 10, False), (custom_unop, 0), custom_wrapop, custom_polyop),
                    custom_operands=(custom_operand_letter, custom_operand_digit))
    
    assert(parser.parse("a * 3 + b * 2").eval() == "aaabb")
    assert(parser.parse("|a * 3 + b * 2|").eval() == 5)
    assert(parser.parse("a * |a * 3 + b * 2|").eval() == "aaaaa")
    assert(parser.parse("a * |a * 3 + b * 2| + b * | b * |a * 5| + b * | b * 3||").eval() == "aaaaabbbbbbbb")