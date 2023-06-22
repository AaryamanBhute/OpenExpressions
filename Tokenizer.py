import re

class Tokenizer:
    def __init__(self, *nonterminals):
        self.nonterminals = nonterminals
    def tokenize(self, content):
        tokens = []
        while(content):
            content = content.lstrip()
            found = False
            for pattern, token in self.nonterminals:
                match_ = re.match((pattern), content)
                if(not match_): continue
                content = content[match_.end():]
                tokens.append((token, match_[0]))
                found = True
                break
            if(not found): raise Exception("Tokenization Error while trying to tokenize: {c}".format(c=content))
        return(tokens)