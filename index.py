import ply.lex as lex 
import spacy
import syntaxOntology
import metaphorOntology

nlp = spacy.load("en_core_web_sm")
validTokens = []        #stores the valid tokens/words
lastWords = [] #store the last words in the sentence to determine the rhyme scheme
previousToken = "" #stores the previous token
listOfSentences = [] #stores words in each sentence
singleSentence = [] #stores words in a sentence

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
    singleSentence.append(t.value) 
    return t
    
# Error handling rule
def t_error(t):
    #detect new line character for the purpose of determining the last word in the line
    t.value = str(t.value)
    global previousToken
    global singleSentence

    if t.value[0] == '\n' and previousToken != "":
        lastWords.append(previousToken)
        listOfSentences.append(singleSentence)
        singleSentence = []
        previousToken = ""  #incase of multiple consecutive new lines

    #anyother characters
    t.lexer.skip(1)

def main() :
    # Build the lexer
    lexer = lex.lex()

    # input poem
    noOfPoems = int(input("\nNo of poems : "))
    emotionConveyed = []

    print("-------------------------------------")

    # for each poem analyse the data
    for i in range(1,noOfPoems+1) : 

        #resetting global members
        global validTokens,lastWords,previousToken,listOfSentences,singleSentence
        validTokens = []
        lastWords = []
        previousToken = ""
        listOfSentences = []
        singleSentence = []

        print("\n########## POEM "+str(i)+" ############")

        file = open("Poems/Poem"+str(i)+".txt","r")
        data = file.read()
        
        # Give the lexer some input
        lexer.input(data)
        
        # Tokenize
        while True:
            tok = lexer.token()
            if not tok:
                break
            
        print("-------------------------------------")
        for lemma in validTokens:
            print(lemma.lemma_ + " - " +lemma.pos_+" - "+spacy.explain(lemma.pos_))

        ###################
        # Syntax Ontology #
        ###################
        print("-------------------------------------")
        print("Last words : " + str(lastWords))
        syntaxOntologyObj = syntaxOntology.syntaxOntology()

        # Get rhyming words
        print("Rhyme scheme : " + str(syntaxOntologyObj.getRhymeScheme(lastWords)) + "\n")

        # Get alliterations
        AlliterationWords,totalAllit = syntaxOntologyObj.getAlliterations(listOfSentences)
        print("Number of alliterating words: " + str(totalAllit))
        print("Alliterating words : " + str(AlliterationWords))

        ###################
        # Metaphor Ontology #
        ###################
        print("-------------------------------------")
        metaphorOntologyObj = metaphorOntology.metaphorOntology()
        emotion = metaphorOntologyObj.getPoemEmotion(data)
        print(emotion)

main()