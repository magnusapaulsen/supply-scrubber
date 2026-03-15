import json
from collections import Counter

def load(fp):
    with open(fp, 'r') as f:
        return json.load(f)

def group_by_name(washes):
    # Create an overview of the washes for each apartment
    names = {}
    for wash in washes:
        name = wash['Name']
        if name not in names:
            names[name] = {'Items': Counter(), 'Guests': Counter(), 'Washes': {}}
        names[name]['Items'].update(wash['Items'])
        names[name]['Guests'].update(wash['Guests'])
    return names

def save(data):
    with open('data/apartments.json', 'w') as f:
        json.dump(data, f, indent = 4)

def main():
    save(group_by_name(load('data/washes.json')))