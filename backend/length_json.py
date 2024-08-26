import json
from datetime import datetime
from math import ceil

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

print(f"No. of words known: {number_of_words_learned}")
print(f"Rate of learning: {number_of_words_learned/delta}/day")
