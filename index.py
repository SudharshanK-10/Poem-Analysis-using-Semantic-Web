import ply.lex as lex 
import spacy
import syntaxOntology

nlp = spacy.load("en_core_web_sm")
validTokens = []        #stores the valid tokens/words
lastWords = [] #store the last words in the sentence to determine the rhyme scheme

previousToken = ""

# List of token names
tokens = (
    'WORD',
)

# A regular expression rule for words
def t_WORD(t):
    r'[a-zA-Z]+'   
    t.value = str(t.value)
    global previousToken
    previousToken = t.value
    validTokens.append(nlp(t.value)[0])     #lemmatize
    return t
    
# Error handling rule
def t_error(t):
    #detect new line character for the purpose of determining the last word in the line
    t.value = str(t.value)
    if t.value[0] == '\n':
        lastWords.append(previousToken)
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

print("-------------------------------")
print(lastWords)

#syntaxOntology class object
syntaxOntologyObj = syntaxOntology.syntaxOntology()
print(syntaxOntologyObj.getRhymeScheme(lastWords))

