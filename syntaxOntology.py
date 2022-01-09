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

            if(curMatch != 'z'):        
                curMatch = chr(ord(curMatch) + 1)
            else :
                curMatch = 'A'
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
    
    def getNumberOfSyllables(self, word):
        word = word.lower()
        if word in self.phonemeDict:
            return len(self.phonemeDict[word])
        else:
            return 0

    def getAlliterations(self,sentences) :

        # List of lists containing all alliterations in the poem
        allAlliterations = []

        # List containing all alliterations in a single line
        allitInLine =[]

        totalWords = 0
        totalAllitCount = 0

        for sentence in sentences:
            #proximity - Allowed number of gaps between alliterating words
            #depends on the no of words in each sentence
            proximity = len(sentence)   #[0,len(sentence)-1]
            pos = 0

            proximalPhonemes = [None] * proximity

            numOfAlliterations = 0

            for word in sentence:
                totalWords += 1

                firstSyllable = self.getPhonemes(word)[0]
                if firstSyllable in proximalPhonemes:
                    numOfAlliterations += 1

                    i = proximalPhonemes.index(firstSyllable)
                    prevAllitWord = sentence[i]

                    if prevAllitWord not in allitInLine :
                        allitInLine.append(prevAllitWord)

                    allitInLine.append(word)

                proximalPhonemes[pos] = firstSyllable
                pos = (pos + 1) if (pos + 1) < proximity else 0

            if numOfAlliterations > 0:
                totalAllitCount += numOfAlliterations + 1
                
            if allitInLine:
                allAlliterations.append(allitInLine.copy())

            allitInLine.clear()
        
        return allAlliterations,totalAllitCount
