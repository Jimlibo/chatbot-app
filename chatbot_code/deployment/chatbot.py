import random
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

# TODO: add functionality for correcting the model
# TODO: perhaps add cli option and use argparse


def clean_sentence(s):
    """
    A function that takes as input a string, and uses tokenize() and lemmatize() to get the root words
    of that string
    :param s: a string containing many words, spaces or other special characters
    :return: a list containing the root words of the sentence s
    """
    lemmatizer = WordNetLemmatizer()   # lemmatizer object to extract the root words from the sentence
    s_words = nltk.word_tokenize(s)
    s_words = [lemmatizer.lemmatize(w) for w in s_words]
    return s_words


def input_create(sentence, words):
    """
    A function that takes as input a string, uses clean_sentence to get its root words, and compares them
    with the param list words, to create a list of 0 and 1
    :param sentence: a string containing words, spaces, and other characters
    :param words: a list of root words, that were used to train a chatbot
    :return: a list of 0 and 1, with length = len(words)
    """
    s_words = set(clean_sentence(sentence))   # get a set for O(1) search/find time complexity
    bag = []
    for word in words:
        bag.append(1) if word in s_words else bag.append(0)  # 1 if word is in sentence's root words, else 0
    return bag


def predict(sentence, classes, model, words):
    """
    A function that deploys a pretrained model to predict the class that the param sentence belongs to.
    :param sentence: a string containing words, spaces and other special characters
    :param classes: a list with the possible categories that the sentence can belong to
    :param model: a pretrained neural network model, to predict the class of the sentence
    :param words: a list with all the root words that the model was trained with
    :return: a string, representing the class that the sentence belongs to
    """
    input_array = input_create(sentence, words)
    pred = model.predict(np.array([input_array]))[0]
    THRESHOLD = 0.25   # error threshold, if prediction is less than that, then deny it
    results = [[i, percent] for i, percent in enumerate(pred) if percent > THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)   # sort based on [percentage of each class
    return classes[results[0][0]] if results[0] is not None else None   # return the class that was mainly predicted


def get_response(text, json_intents, classes, words, model):
    """
    A function that deploys a pretrained model to predict the category of the string given, and then return
    a response from those found in json_intents .
    :param text: a string containing many words, spaces or other characters
    :param json_intents: a json object with (tag, pattern, response) contents
    :param classes: a list with all possible classes that the text can belong to
    :param words: a list with all the words that were used to train a neural network model
    :param model: a pretrained neural network model
    :return: a string, representing the response to the parameter text
    """
    tag = predict(text, classes, model, words)
    print(tag)
    result = "I am sorry, but I can't understand you..."
    for i in json_intents['intents']:
        if i['tag'] == tag:    # find the category of the pattern
            result = random.choice(i['responses'])    # choose a random response from those available
            break
    return result
