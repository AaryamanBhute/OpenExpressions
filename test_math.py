from Parser import Parser

def test_operations():
    parser = Parser()
    assert(parser.parse("1 + 1").eval() == 2)
    assert(parser.parse("2 * 2").eval() == 4)
    assert(parser.parse("35 - 14").eval() == 21)
    assert(parser.parse("24 / 5").eval() == 4.8)