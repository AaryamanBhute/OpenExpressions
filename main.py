from Tokenizer import Tokenizer
from enum import Enum

class Token(Enum):
    INTEGER = 1
    FLOAT = 2
    VARIABLE = 3
    PLUS = 4
    MINUS = 5
    TIMES = 6
    DIV = 7
    INTDIV = 8

if __name__ == "__main__":
    tokenizer = Tokenizer((r"\d+", Token.INTEGER), (r"\d*.\d+", Token.FLOAT), (r"[a-zA-Z]\w*", Token.VARIABLE),
                           (r"\+", Token.PLUS), (r"-", Token.MINUS), (r"\*", Token.TIMES), (r"//", Token.INTDIV), (r"/", Token.DIV))
    print(tokenizer.tokenize("a + b // ^ 15 + 16.2"))
    