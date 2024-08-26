from flask import Flask, request, jsonify
from flask_cors import CORS
import json, random
from datetime import datetime

app = Flask(__name__)
CORS(app=app)

@app.get('/')
def get_learn_data():
    with open("./data/A1_Nouns.json", 'r') as noun_file:
        nouns = json.load(noun_file)

    with open("./data/A1_Verbs.json", 'r') as verb_file:
            verbs = json.load(verb_file)

    with open("./data/A1_Adjectives.json", 'r') as adjective_file:
            adjectives = json.load(adjective_file)

    with open('./data/A1_Others.json', 'r') as other_file:
            others = json.load(other_file)
    
    number_of_words_learned = (len(nouns['words']) + len(verbs['words']) + len(adjectives['words']) + len(others['words'])) 
    delta = (datetime.now() - datetime(2024, 8, 21)).days + 1

    return { "home_data": [number_of_words_learned, delta]}
    


@app.get('/test')
def get_random_german_word():
    file_name = request.args.get('file')
    if not file_name:
        return jsonify({"error": "No file specified"}), 400
    
    file_name = file_name.replace(' ', '_')
    try:
        with open(f'./data/{file_name}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 400

    words = data.get("words", [])
    if words:
        random.shuffle(words)
        response = jsonify(words)
        response.headers.add('Content-Type', 'application/json; charset=utf-8')
        return response
    else:
        return jsonify({"error": "No words available"}), 404

if __name__ == '__main__':
    app.run(debug=True)
