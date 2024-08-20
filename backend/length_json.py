import json

with open("german_words.json", 'r') as file:
        data = json.load(file)

print(len(data['words']))