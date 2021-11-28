# Requirements:
# pip install pronouncing

import pronouncing
import string

from nltk.corpus import cmudict
from nltk.corpus import stopwords

class syntaxOntology :

    phonemeDict = cmudict.dict()
    stopwords = stopwords.words("english")

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
        word = word.lower()
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

        # TODO: Find a way to dynamically determine the allowed proximity based on 
        #       number of words per line
        # Allowed number of gaps between alliterating words
        proximity = 3
        index = 0

        totalWords = 0
        totalAllitCount = 0

        for sentence in sentences:
            proximalPhonemes = [None] * proximity

            numOfAlliterations = 0

            for word in sentence.split(sep=" "):
                # Remove punctuations
                word = word.translate(str.maketrans('', '', string.punctuation))
                totalWords += 1

                firstSyllable = self.getPhonemes(word)[0]
                if firstSyllable in proximalPhonemes:
                    numOfAlliterations += 1
                    allitInLine.append(word)

                proximalPhonemes[index] = firstSyllable
                index = (index + 1) if (index + 1) < proximity else 0

            if numOfAlliterations > 0:
                totalAllitCount += numOfAlliterations + 1
                
            if allitInLine:
                allAlliterations.append(allitInLine.copy())

            allitInLine.clear()

        # TODO: Print alliterating words

        return totalAllitCount
