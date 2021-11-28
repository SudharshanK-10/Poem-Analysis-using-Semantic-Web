# Requirements:
# pip install pronouncing

import pronouncing
import nltk
import re

nltk.download('cmudict')
nltk.download('stopwords')

class syntaxOntology :

    phonemeDict = nltk.corpus.cmudict.dict()
    stopwords = nltk.corpus.stopwords.words("english")
    removePunctuation = lambda x: re.sub(r'[^\w\s]', '', x)

    def getRhymeScheme(self, lastWords) :
        curMatch = 'a'
        pattern = [None] * len(lastWords)

        for i in range(0, len(lastWords)):
            # Get all rhyming words for ith last word
            rhymingWords = pronouncing.rhymes(lastWords[i])

            if (pattern[i] == None):
                pattern[i] = curMatch
            else:
                continue
            
            # If a rhyming word is used in poem, update rhyme scheme
            for j in range(i + 1, len(lastWords)):
                if (lastWords[j] in rhymingWords or lastWords[j] == lastWords[i]):
                    pattern[j] = curMatch
        
            curMatch = chr(ord(curMatch) + 1)

        pattern = "".join(pattern)
        return pattern

    # Returns the first syllable of a word in dictionary
    def getPhonemes(self, word) :
        if word in self.phonemeDict:
            return self.phonemeDict[word][0]

        # Handling words without a dictionary entry
        else:
            return ["NONE"]

    def getAlliterations(self, sentences) :

        # List of lists containing all alliterations in the poem
        allAlliterations = []

        # List containing all alliterations in a single line
        allitInLine =[]

        print("Alliterations:")
        print(sentences)
