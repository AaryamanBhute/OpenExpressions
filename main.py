from Parser import Parser
from Operators import *

def print_node(node, num_dashes=0):
    print("-"*num_dashes, node)
    if(issubclass(type(node), Binop)):
        print_node(node.left, num_dashes + 1)
        print_node(node.right, num_dashes + 1)
    elif(issubclass(type(node), WrapOp) or issubclass(type(node), UnOp)):
        print_node(node.expr)

if __name__ == "__main__":
    parser = Parser(mode="empty", custom_operators=(
        (Pow, 70000, False),
        Abs, Paren, Sigma, Pi,
        (Mult, 90000, False),
        (Div, 90000, False),
        (IntDiv, 90000, False),
        (Mod, 90000, False),
        (Add, 100000, False),
        (Sub, 100000, False),
        (Neg, 80000),
    ), custom_operands=(
        Int, Float, Var
    ))
    content = "1 + 1"
    expression = parser.parse(content)
    print(expression.eval({"a" : 2, "b": 2}))