from Parser import Parser

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