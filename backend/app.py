from flask import Flask
from flask_cors import CORS
import json, random


app = Flask(__name__)
CORS(app=app)

@app.get('/test')
def get_random_german_word():
    
    with open("german_words.json", 'r') as file:
        data = json.load(file)

    words = data.get("words", [])
    if words:
        random_word = random.choice(words)
        return json.dumps(random_word)
    else:
        return json.dumps({"error": "No words available"})
