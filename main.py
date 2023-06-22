from Parser import Parser

def print_node(node, num_dashes=0):
    print('-' * num_dashes, node)

    try:
        print_node(node.left, num_dashes + 1)
        print_node(node.right, num_dashes + 1)
    except:
        pass

if __name__ == "__main__":
    parser = Parser()
    content = "a + b // 3 / 2"
    expression = parser.parse(content)
    print_node(expression)