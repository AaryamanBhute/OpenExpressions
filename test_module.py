from Parser import Parser
from Operators import *

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
    class custom_unop():
        pass
    class custom_binop(BinOp):
        pass
    class custom_wrapop(WrapOp):
        pass
    class custom_polyop(PolyOp):
        pass