from janome.tokenizer import Tokenizer
t = Tokenizer()
for token in t.tokenize('すももももものうち'):
    print(token)
