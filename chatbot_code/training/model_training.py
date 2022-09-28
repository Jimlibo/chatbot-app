import os
import random
import json
import pickle
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow import keras
from keras import layers
from datetime import datetime

# TODO: further research and optimize the training and architecture of the model


def print_error(msg):   # print formatted error message and exit with code 1
    print("[ERROR]:", msg)
    exit(1)


def print_info(msg):   # print formatted info message
    print("[INFO]:", msg)


class BotTrainer:
    def __init__(self, intents_file=None):
        # check if intents file has been given or if it does not exist
        if intents_file is None:
            print_error("Intents file is required!")
        elif not os.path.exists(intents_file):
            print_error("File {} could not be found".format(intents_file))

        self.intents = json.loads(open(intents_file).read())
        self.words = []    # list with all words from intents file
        self.classes = []    # list with all the different classes (tags) from intents file
        self.documents = []  # pairs of (pattern, class)
        self.ignore_letters = {'?', '!', '.', ','}   # characters to be ignored
        self.lemmatizer = WordNetLemmatizer()    # object to lemmatize the words
        self.dataset = None   # dataset with features and labels for training
        self.model = None   # the chatbot model
        self.history = None  # history from the training of the model

    def get_intents(self):
        print_info("Loading intents")

        for intent in self.intents['intents']:   # transverse the json object with the intents
            for pattern in intent['patterns']:
                wordlist = nltk.word_tokenize(pattern)  # get all words from the sentence
                self.words.extend(wordlist)  # add them to the words' list

                tag = intent['tag']
                self.documents.append((wordlist, intent['tag']))  # append the pair of question-tag to the documents

                if tag not in self.classes:   # append tag to classes if it does not already exist
                    self.classes.append(tag)

        self.words = [self.lemmatizer.lemmatize(word) for word in self.words if word not in self.ignore_letters]
        self.words = sorted(set(self.words))  # remove duplicates and sort the words
        self.classes = sorted(self.classes)  # sort tags

        return self

    def store_word_classes(self):
        print_info("Saving words and classes to pickle files")

        pickle.dump(self.words, open('../pickles/words.pkl', 'wb'))   # store words and classes for predictions
        pickle.dump(self.classes, open('../pickles/classes.pkl', 'wb'))

        return self

    def prepare_dataset(self):
        training = []
        output_empty = [0] * len(self.classes)  # create initial empty output(all zeros)

        for doc in self.documents:  # for each pair of question-tag
            bag = []  # represents the encoded input
            word_patterns = doc[0]  # get only the words
            word_patterns = [   # use the lemmatizer object to get the base words of all words of this document
                self.lemmatizer.lemmatize(w.lower()) for w in word_patterns if w not in self.ignore_letters
            ]
            for word in self.words:
                bag.append(1) if word in word_patterns else bag.append(0)

            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1  # set value n of the specific class to 1 in the output array
            training.append([bag, output_row])  # append the input array and the output array to the training data

        random.shuffle(training)  # randomly shuffle the train dataset
        self.dataset = np.array(training)  # convert to array and store to dataset variable

        return self

    def train_model(self):
        print_info("Creating and training the model")

        train_x = list(self.dataset[:, 0])  # get only the feature arrays
        train_y = list(self.dataset[:, 1])  # get only the label array

        # creating the model architecture
        self.model = keras.models.Sequential()
        self.model.add(layers.Dense(128, input_shape=(len(train_x[0]),), activation='relu'))  # input layer
        self.model.add(layers.Dropout(0.5))
        self.model.add(layers.Dense(64, activation='relu'))  # hidden layer
        self.model.add(layers.Dropout(0.5))
        self.model.add(layers.Dense(len(train_y[0]), activation='softmax'))  # output layer, neurons = num_of_classes

        # compiling and training the model
        self.model.compile(    # compiling the model
            optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        self.history = self.model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=32, verbose=2)

        return self

    def save_model(self):
        print_info("Saving the model")
        self.model.save('../models/Nio.h5', self.history)

        return self

    def pipeline(self):  # method that calls all the previous methods in a sequential way
        self.get_intents().store_word_classes().prepare_dataset().train_model().save_model()


def main():
    start = datetime.now()

    trainer = BotTrainer("intents.json")
    trainer.pipeline()

    print("\nScript Execution Time: " + str(datetime.now() - start))


if __name__ == '__main__':
    main()
