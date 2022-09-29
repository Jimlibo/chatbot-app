"""
Created September 25, 2022
@author: Jimlibo
@Description: A script that uses Flask to connect the different python scripts with the web page contents.
@Usage:
    Run the chatbot application
        python3 app.py
"""

import json
import pickle
from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from chatbot_code.deployment.chatbot import get_response


# initialize the app
app = Flask(__name__)


# create base route
@app.route("/")
@app.route("/home")
def index_page():
    return render_template("index.html")


@app.route("/predict", methods=['POST'])   # use the post method to access this url
def respond():
    words = pickle.load(open('chatbot_code/pickles/words.pkl', 'rb'))
    classes = pickle.load(open('chatbot_code/pickles/classes.pkl', 'rb'))
    model = load_model('chatbot_code/models/NIO.h5')

    user_text = request.get_json().get("message")   # get the message from the user
    intents = json.loads(open('chatbot_code/training/intents.json').read())   # load the intents file
    bot_response = get_response(user_text, intents, classes, words, model)   # get the response from the chatbot
    return_messsage = {"response": bot_response}  # create json object and return it to the user
    return jsonify(return_messsage)


if __name__ == "__main__":
    app.run()
