import ply.lex as lex 
import spacy

nlp = spacy.load("en_core_web_sm")
validTokens = []        #stores the valid tokens/words

# List of token names
tokens = (
    'WORD',
)

# A regular expression rule for words
def t_WORD(t):
    r'[a-zA-Z]+'   
    t.value = str(t.value)
    validTokens.append(nlp(t.value)[0])     #lemmatize
    return t
    
# Error handling rule
def t_error(t):
    #anyother characters
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# input poem
file = open("simplePoem.txt","r")
data = file.read()
 
# Give the lexer some input
lexer.input(data)
 
# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break

for lemma in validTokens:
    print(lemma.lemma_ + " - " + spacy.explain(lemma.pos_))

