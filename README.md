# Chatbot-App


![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)


## General
This app is a simple website that utilizes a pretrained chatbot model to offer a more interactive experience to the user.
The purpose of the site, is to demonstrate how a chatbot can be integrated to an official page, and how it may help the
visitors of that page. In this case, the chatbot is a general-purpose bot, that can tell jokes, riddles, give some
information about ferrari, tell the date and time, etc.

## Setting up the environment
This project was created using Python. The packages that were used are [Flask], [nltk] and [tensorflow]. In order to run 
this app, you need to have python 3.9 or higher installed. To download the required packages and start the app for the 
first time, execute the command:
```sh
./setup
```
<b>Note</b>: you need to be inside the chatbot-app/ directory to successfully run the previous script

## Retraining the model
The chatbot model is trained using the [intents.json] file. If you want to retrain the model, you can update the intents
file and then execute the command:
```sh
python3 /chatbot_code/training/model_training.py
```

## Run the app
After all requires packages have been downloaded, you can run the app by simply executing the command:
```sh
python3 app.py
```
The app will start running on localhost on port 5000 (http://127.0.0.1:5000).

## License

MIT

**Free Software**



[intents.json]: https://github.com/Jimlibo/chatbot-app/blob/main/chatbot_code/training/intents.json
[Flask]: https://flask.palletsprojects.com/en/2.2.x/
[nltk]: https://www.nltk.org/
[tensorflow]: https://www.tensorflow.org/?gclid=EAIaIQobChMI1o_StKi8-gIVlZ93Ch1NfQ_cEAAYASAAEgKpkfD_BwE