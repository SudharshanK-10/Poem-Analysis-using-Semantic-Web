from nltk.featstruct import _trace_unify_identity
from syntaxOntology import syntaxOntology

class PoetryOntology():
    syntaxOntologyObj = syntaxOntology()
    
    def getGenre(self, poemLines, rhymeScheme, totalAlliterations, majorEmotion):
        if self.isSonnet(poemLines):
            return "Shakespearean Sonnet"
        if self.isHaiku(poemLines):
            return "Haiku"
        if self.isLimerick(poemLines, majorEmotion):
            return "Limerick"
        if self.isNarrative(poemLines):
            return "Narrative"
        if self.isArtisticFreeVerse(poemLines, totalAlliterations):
            return "Artistic Free Verse"
        
        return "Free Verse"
        
    def numberOfSyllables(self, line):
        res = 0
        for word in line:
            res += self.syntaxOntologyObj.getNumberOfSyllables(word)
        
        return res
    
    def isSonnet(self, poemLines):
        if len(poemLines) != 14:
            return False
        
        for line in poemLines:
            if self.numberOfSyllables(line) not in range(6, 25):
                return False

        return True
    
    def isHaiku(self, poemLines):
        if len(poemLines) != 3:
            return False

        syllables = [5, 7, 5]
        for index, line in enumerate(poemLines):
            if self.numberOfSyllables(line) != syllables[index]:
                return False
        
        return True

    def isNarrative(self, poemLines):
        return len(poemLines) > 25

    def isArtisticFreeVerse(self, poemLines, totalAlliterations):
        totalWords = 0
        for line in poemLines:
            totalWords += len(line)

        if not (totalAlliterations / float(totalWords) > 0.20):
            return False

        return True

    def isLimerick(self, poemLines, majorEmotion):
        if len(poemLines) > 6 or len(poemLines) < 4:
            return False

        if majorEmotion not in ["Happy", "Surprise"]:
            return False

        return True
