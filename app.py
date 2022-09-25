"""
Created September 25, 2022
@author: Jimlibo

@Description: A script that uses Flask to connect the different python scripts with the web page contents.
"""


from flask import Flask, render_template, request, jsonify

# initialize the app
app = Flask(__name__)


# create base route
@app.route("/")
@app.route("/home")
def index_page():
    return render_template("index.html")


@app.route("/predict", methods=['POST'])   # use the post method to access this url
def respond():
    user_text = request.get_json().get("message")   # get the message from the user
    #bot_response = get_response(user_text)   # get the response from the chatbot
    #return_messsage = {"response": bot_response}  # create json object and return it to the user
    #return jsonify(return_messsage)
    return jsonify({'response': "Sorry, i am not yet trained..."})


if __name__ == "__main__":
    app.run(debug=True)
