class categorizationModule :
    rhymeScore = 0
    allitScore = 0
    totalScore = 0

    def calculateRhymeScore(self, rhymeScheme, numOfLines):
        numOfLetters = len(set(rhymeScheme))
        self.rhymeScore = numOfLetters / float(numOfLines)
        self.rhymeScore = 1 - self.rhymeScore

    def calculateAllitScore(self, totalAllit, AlliterationWords, listOfSentences):
        totalWords = 0
        avgSentenceLength = 0
        maxSentenceLength = 0
        for sentence in listOfSentences:
            length = len(sentence)
            totalWords += length

            if (length > maxSentenceLength):
                maxSentenceLength = length

            avgSentenceLength += length / len(listOfSentences)

        baseAllitScore = totalAllit / totalWords

        maxAllitLength = 0
        for Alliteration in AlliterationWords:
            if len(Alliteration) > maxAllitLength:
                maxAllitLength = len(Alliteration)

        longestAllitScore = maxAllitLength / avgSentenceLength
        if (longestAllitScore > 1):
            diff = longestAllitScore - 1
            if (diff >= 1):
                longestAllitScore = 1
            else:
                longestAllitScore = 1
                longestAllitScore -= ((1 - diff)/10)
        else:
            diff = 1 - longestAllitScore


        self.allitScore = (baseAllitScore + longestAllitScore) / 2

    def computeEmotion(self, emotion):
        majorEmotion = max(emotion, key=emotion.get)
        revEmotion = sorted(((v , k) for k, v in emotion.items()))

        minorEmotion1 = revEmotion[-2][1]
        minorEmotion2 = revEmotion[-3][1]

        minorEmotions = minorEmotion1 + ", " + minorEmotion2

        return majorEmotion, minorEmotions


    def calculateFinalScore(self):
        self.totalScore = self.rhymeScore + self.allitScore
        self.totalScore /= 2

        self.totalScore *= 10
        self.totalScore = round(self.totalScore, 2)
        return self.totalScore