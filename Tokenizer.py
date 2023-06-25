import re

class Tokenizer:
    def __init__(self, terminals, op_tokens):
        self.terminals = terminals
        self.op_tokens = op_tokens
    def tokenize(self, content):
        tokens = []
        content = content.rstrip()
        while(content):
            content = content.lstrip()
            found = False
            for pattern, token in sorted(self.terminals, key=lambda a : len(a[0]), reverse=True):
                if((pattern, token) in self.op_tokens): continue
                match_ = re.match((pattern), content)
                if(not match_): continue
                content = content[match_.end():]
                tokens.append((token, match_[0]))
                found = True
                break
            if(found): continue
            for pattern, token in self.op_tokens:
                match_ = re.match((pattern), content)
                if(not match_): continue
                content = content[match_.end():]
                tokens.append((token, match_[0]))
                found = True
                break
            if(not found): raise Exception("Tokenization Error while trying to tokenize: {c}".format(c=content))
        return(tokens)