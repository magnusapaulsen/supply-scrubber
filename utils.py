import json

def load(fp):
    with open(fp, 'r') as f:
        return json.load(f)
    
def save(data, fp):
    with open(fp, 'w') as f:
        json.dump(data, f, indent = 4)