from flask import Flask, request, jsonify
from flask_cors import CORS
import json, random

app = Flask(__name__)
CORS(app=app)

@app.get('/test')
def get_random_german_word():
    file_name = request.args.get('file')
    if not file_name:
        return jsonify({"error": "No file specified"}), 400
    
    file_name = file_name.replace(' ', '_')
    try:
        with open(f'./data/{file_name}.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 400

    words = data.get("words", [])
    if words:
        random.shuffle(words)  
        return jsonify(words)
    else:
        return jsonify({"error": "No words available"}), 404

if __name__ == '__main__':
    app.run(debug=True)
