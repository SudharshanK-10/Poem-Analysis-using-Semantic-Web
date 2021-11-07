import ply.lex as lex 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()

# List of token names
tokens = (
    'WORD',
)

# A regular expression rule for words
def t_WORD(t):
    r'[a-zA-Z]+'   
    value = str(t.value)
    t.value = ps.stem(t.value) #stemming the words   
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n,?!"'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# input data
file = open("input.txt","r");
data = file.read()
 
# Give the lexer some input
lexer.input(data)
 
# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok.value)