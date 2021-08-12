import nltk
nltk.download('wordnet')
nltk.download('punkt')
import re
import pandas as pd
import numpy as np


def prep_sentence(sentence):
    words = nltk.word_tokenize(sentence)
    words = [word for word in words if word not in ["'s", ',', ':', "'"]]
    words = [re.sub(r'\'','', word) for word in words]
    #words = [word.lower() for word in words]
    for i in range (len(words)):
        words[i] = words[i].lower()
    prepped_sentence = ' '.join(words)
    #prepped_sentence = clean_sentence(sentence, None)
    return prepped_sentence