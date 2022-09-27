import random
import json
import pickle
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

# TODO: add functionality for correcting the model
# TODO: perhaps add cli option and use argparse

# create initial lemmatizer object and load the intents into a json object
lemmatizer = WordNetLemmatizer()


def clean_sentence(s):   # function that tokenizes a string into words, and then lemmatizes those words
    s_words = nltk.word_tokenize(s)
    s_words = [lemmatizer.lemmatize(w) for w in s_words]
    return s_words


def input_create(sentence, words):
    s_words = set(clean_sentence(sentence))   # get a set for O(1) search/find time complexity
    bag = []
    for word in words:
        bag.append(1) if word in s_words else bag.append(0)
    return bag


def predict(sentence, classes, model, words):
    input_array = input_create(sentence, words)
    pred = model.predict(np.array([input_array]))[0]
    THRESHOLD = 0.25   # error threshold, if prediction is less than that, then deny it
    results = [[i, percent] for i, percent in enumerate(pred) if percent > THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)   # sort based on [percentage of each class
    return classes[results[0][0]]   # return the class name of the class that was mainly predicted


def get_response(text, json_intents, classes, words, model):
    tag = predict(text, classes, model, words)
    print(tag)
    result = "I am sorry, but I can't understand you..."
    for i in json_intents['intents']:
        if i['tag'] == tag:    # find the category of the pattern
            result = random.choice(i['responses'])    # choose a random response from those available
            break
    return result




