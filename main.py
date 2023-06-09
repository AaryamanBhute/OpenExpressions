from ExpressionNodes import *
from Parser import Parser

if __name__ == "__main__":
    add = Add(None, None)
    parser = Parser()
    #print(parser)
    string_expr = "4 + apple ** 3"
    #print("  ".join([token[0] for token in parser.tokenize(string_expr)]))
    expr = parser.parse(string_expr)
    printExpr(expr)
    print(expr.eval({"apple" : 2}))
