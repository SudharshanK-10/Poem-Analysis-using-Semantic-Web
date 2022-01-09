import syntaxOntology

class PoetryOntology():
    syntaxOntologyObj = syntaxOntology.syntaxOntology()
    
    def getGenre(self, poemLines, rhymeScheme):
        if self.isSonnet(poemLines, rhymeScheme):
            return "Shakespearean Sonnet"
        if self.isHaiku(poemLines, rhymeScheme):
            return "Haiku"
        
    def numberOfSyllables(self, line):
        res = 0
        for word in line.split():
            res += self.syntaxOntologyObj.getNumberOfSyllables(word)
        
        return res
    
    def isSonnet(self, poemLines, rhymeScheme):
        if len(poemLines) != 14 or rhymeScheme != "ababcdcdefefgg":
            return False
        
        for line in poemLines:
            if self.numberOfSyllables(line) != 10:
                return False

        return True
    
    def isHaiku(self, poemLines, rhymeScheme):
        if len(poemLines) != 3:
            return False

        syllables = [5, 7, 5]
        for index, line in enumerate(poemLines):
            if self.numberOfSyllables(line) != syllables[index]:
                return False
        
        return True

