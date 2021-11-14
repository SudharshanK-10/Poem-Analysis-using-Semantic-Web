# Requirements:
# pip install pronouncing

import pronouncing

lastWords = []

# TODO: Integrate with processing module. Get data from it

file = open("input.txt","r")
data = file.read()

sentences = data.split('\n')
for sentence in sentences:
    # Clear trailing spaces and get last word
    lastWords.append(sentence.strip().rsplit(' ', 1)[-1])
    
for word in lastWords:
    rhymingWords = pronouncing.rhymes(word)
    print(rhymingWords)

