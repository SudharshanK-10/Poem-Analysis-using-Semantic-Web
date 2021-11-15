# Requirements:
# pip install pronouncing

import pronouncing
import string

lastWords = []

# TODO: Integrate with processing module. Get data from it

file = open("simplePoem.txt","r")
data = file.read()

sentences = data.split('\n')
for sentence in sentences:
    # Clear trailing spaces and punctuations
    temp = sentence.strip().rsplit(' ', 1)[-1]
    if (len(temp) > 0):
        temp = temp.translate(str.maketrans('', '', string.punctuation))
        
        lastWords.append(temp)


curMatch = 'a'
pattern = [None] * len(lastWords)

for i in range(0, len(lastWords)):
    rhymingWords = pronouncing.rhymes(lastWords[i])
    
    if (pattern[i] == None):
        pattern[i] = curMatch
    else:
        continue
        
    for j in range(i + 1, len(lastWords)):
        if (lastWords[j] in rhymingWords):
            pattern[j] = curMatch
        
    curMatch = chr(ord(curMatch) + 1)

pattern = "".join(pattern)
print(pattern)