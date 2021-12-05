# Requirements :
# pip install text2emotion

#Note :
#Inorder to avoid nltk downloading existing packages and displaying it on console,
#Goto .venv/lib64/site-packages/text2emotion/__init__.py
#and remove nltk.download() commands, and fix the syntax warning

import text2emotion

class poetryOntology :
    
    def getPoemEmotion(self,poem) :
        return text2emotion.get_emotion(poem)
