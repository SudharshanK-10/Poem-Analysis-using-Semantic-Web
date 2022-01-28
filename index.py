import ply.lex as lex
from pronouncing import rhymes 
import spacy
from PoetryOntology import PoetryOntology
from categorizationModule import categorizationModule
import syntaxOntology
import metaphorOntology
from tabulate import tabulate

nlp = spacy.load("en_core_web_sm")

validTokens = []        #stores the valid tokens/words
lastWords = [] #store the last words in the sentence to determine the rhyme scheme
previousToken = "" #stores the previous token
listOfSentences = [] #stores words in each sentence
singleSentence = [] #stores words in a sentence
analysis=[] #holds the overall analysis where each element is the result of the respective module

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
    # noOfPoems = int(input("\nNo of poems : "))
    noOfPoems = 17
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

        print("Processing Poem " + str(i) +"....")
        #print("\n########## POEM "+str(i)+" ############")

        file = open("Poems/Poem"+str(i)+".txt","r")
        data = file.read()
        
        # Give the lexer some input
        lexer.input(data)
        
        # Tokenize
        while True:
            tok = lexer.token()
            if not tok:
                break

        '''   
        print("-------------------------------------")
        for lemma in validTokens:
            print(lemma.lemma_ + " - " +lemma.pos_+" - "+spacy.explain(lemma.pos_))
        '''

        ###################
        # Syntax Ontology #
        ###################
        '''
        print("-------------------------------------")
        print("Last words : " + str(lastWords))
        '''
        syntaxOntologyObj = syntaxOntology.syntaxOntology()
        

        # Get rhyming words
        rhymeScheme = str(syntaxOntologyObj.getRhymeScheme(lastWords));
        #print("Rhyme scheme : " + rhymeScheme + "\n")

        # Get alliterations
        AlliterationWords,totalAllit = syntaxOntologyObj.getAlliterations(listOfSentences)
        #print("Number of alliterating words: " + str(totalAllit))
        #print("Alliterating words : " + str(AlliterationWords))


        #####################
        # Metaphor Ontology #
        #####################
        #print("-------------------------------------")
        metaphorOntologyObj = metaphorOntology.metaphorOntology()
        emotion = metaphorOntologyObj.getPoemEmotion(data)
        #print(emotion)
    

        ##################
        # Categorization #
        ##################
        categorizationObj = categorizationModule()
        categorizationObj.calculateRhymeScore(rhymeScheme, len(listOfSentences))
        categorizationObj.calculateAllitScore(totalAllit, AlliterationWords, listOfSentences)
        majorEmotion, minorEmotions = categorizationObj.computeEmotion(emotion)


        ###################
        # Poetry Ontology #
        ###################
        poetryOntologyObj = PoetryOntology()
        genre = poetryOntologyObj.getGenre(listOfSentences, rhymeScheme, totalAllit, majorEmotion)
        #print(genre)


        ################
        # Final Output #
        ################
        finalScore = categorizationObj.calculateFinalScore()
        #print("Major Emotion: " + majorEmotion)
        #print("Minor Emotions: " + minorEmotions)
        #print("Creativity Score: " + str(finalScore))


        outFile = open("Result/Poem"+str(i)+".txt", "w")
        poemAnalysis = []


        outFile.write("------------FINAL RESULT----------------\n\n")
        l = [["Rhyme Scheme",rhymeScheme],["Number of Alliterations",str(totalAllit)],["Genre",genre]
        ,["Major Emotion",majorEmotion],["Minor Emotion",minorEmotions]
        ]

        finalResultTable = tabulate(l)
        outFile.write(finalResultTable)
        outFile.write("\nCREATIVITY SCORE         " + str(finalScore) + "\n")
        outFile.write("----------------------   ------------------\n\n")

         #for overall analysis table
        poemAnalysis.append("Poem"+str(i))
        poemAnalysis.append(rhymeScheme)
        poemAnalysis.append(str(totalAllit))
        poemAnalysis.append(genre)
        poemAnalysis.append(majorEmotion)
        poemAnalysis.append(minorEmotions)
        poemAnalysis.append(str(finalScore))
        analysis.append(poemAnalysis)

        outFile.write("-------MODULE-WISE RESULTS---------\n\n")
        #preprocessing module
        outFile.write("------------------------------------\n")
        outFile.write("------PRE PROCESSING MODULE-------\n")
        outFile.write("------------------------------------\n\n")
        l = []
        for lemma in validTokens:
            l.append([lemma.lemma_,lemma.pos_,spacy.explain(lemma.pos_)])
        preProcessingModuleResult = tabulate(l,headers=["Lemma","POS Tag","Explanation"])
        outFile.write(preProcessingModuleResult)

        #syntax ontology module
        outFile.write("\n\n------------------------------------\n")
        outFile.write("-----SYNTAX ONTOLOGY MODULE-------\n")
        outFile.write("------------------------------------\n\n")
        outFile.write("Last words - " + str(lastWords) + "\n\n")
        outFile.write("Rhyme scheme - " + rhymeScheme + "\n\n")
        outFile.write("Alliterating words - " + str(AlliterationWords) + "\n\n")
        outFile.write("Number of alliterating words - " + str(totalAllit) + "\n\n")
        
        #poetry ontology module
        outFile.write("------------------------------------\n")
        outFile.write("-----POETRY ONTOLOGY MODULE-------\n")
        outFile.write("------------------------------------\n\n")
        outFile.write("Genre - " + genre + "\n\n")

        #metaphor ontology module
        outFile.write("------------------------------------\n")
        outFile.write("-----METAPHOR ONTOLOGY MODULE-------\n")
        outFile.write("------------------------------------\n\n")
        outFile.write(str(emotion) + "\n\n")

        #categorisation module
        outFile.write("------------------------------------\n")
        outFile.write("-----CATEGORISATION MODULE-----------\n")
        outFile.write("------------------------------------\n\n")
        outFile.write("Major Emotion - " + majorEmotion + "\n")
        outFile.write("Minor Emotions - " + minorEmotions + "\n")
        outFile.write("Creativity Score - " + str(finalScore) + "\n")

    overAllAnalysisTable = tabulate(analysis,headers=["Poem Name","Rhyme Scheme","Number of Alliterations",
    "Genre","Major Emotion","Minor Emotions", "Creativity Score"])

    outFile = open("Result/Analysis.txt","w")
    outFile.write(overAllAnalysisTable)

main()