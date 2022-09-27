import random
import json
import pickle
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow import keras
from keras import layers

# TODO: convert to object oriented code
# TODO: further research and optimize the training and architecture of the model

# create a lemmatizer object, and load the intents.json file
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())   # read the intents and store them in a json object

# create lists that will be used for the training of the chatbot
words = []    # different words
classes = []  # tags from the intents.json file
documents = []  # pairs of tag and question
ignore_letters = {'?', '!', '.', ','}   # characters to ignore during training and predicting process


# populate the lists created above with the appropriate contents
for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordlist = nltk.word_tokenize(pattern)  # get all words from the sentence
        words.extend(wordlist)

        tag = intent['tag']
        documents.append((wordlist, intent['tag']))   # append the pair of question-tag

        if tag not in classes:
            classes.append(tag)

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]  # get base of all words
words = sorted(set(words))    # remove duplicates and sort the words

classes = sorted(classes)   # sort tags

pickle.dump(words, open('../pickles/words.pkl', 'wb'))   # for encoding the actual input during the prediction process
pickle.dump(classes, open('../pickles/classes.pkl', 'wb'))

# prepare the training features and labels
training = []
output_empty = [0] * len(classes)   # create initial empty output(all zeros) equal to the number of different classes

for doc in documents:   # for each pair of question-tag
    bag = []   # represents the encoded input
    word_patterns = doc[0]   # get only the words
    word_patterns = [lemmatizer.lemmatize(w.lower()) for w in word_patterns if w not in ignore_letters]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1   # go to output, and set the values of the tag of this document to 1
    training.append([bag, output_row])   # append the input array and the output array to the training data

random.shuffle(training)   # randomly shuffle the train dataset
training = np.array(training)  # convert to array

train_x = list(training[:, 0])   # get only the feature arrays
train_y = list(training[:, 1])    # get only the label array


# creating the model and compile it
model = keras.models.Sequential()
model.add(layers.Dense(128, input_shape=(len(train_x[0]),), activation='relu'))    # input layer
model.add(layers.Dropout(0.5))
model.add(layers.Dense(64, activation='relu'))   # hidden layer
model.add(layers.Dropout(0.5))
model.add(layers.Dense(len(train_y[0]), activation='softmax'))    # output layer, neurons = num_of_classes

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# train the  model and save it to a file
history = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=32, verbose=2)
model.save('../models/Nio.h5', history)
print("Model created and saved successfully")






