# Requirements:
# pip install pronouncing

import pronouncing
import string

class syntaxOntology :

    def getRhymeScheme(self,lastWords) :
        curMatch = 'a'
        pattern = [None] * len(lastWords)

        for i in range(0, len(lastWords)):
            rhymingWords = pronouncing.rhymes(lastWords[i])

            if (pattern[i] == None):
                pattern[i] = curMatch
            else:
                continue
        
            for j in range(i + 1, len(lastWords)):
                if (lastWords[j] in rhymingWords or lastWords[j] == lastWords[i]):
                    pattern[j] = curMatch
        
            curMatch = chr(ord(curMatch) + 1)

        pattern = "".join(pattern)
        return pattern