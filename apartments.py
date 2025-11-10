import json

def load(fp):
    with open(fp, 'r') as f:
        return json.load(f)

def group_by_name(washes):
    # Create an overview of the washes for each apartment
    names = {}
    # Loop through all washes
    for wash in washes:
        # Add the address to the dictionary if it is not there already
        if wash['Name'] not in names.keys():
            names[wash['Name']] = {'Items': {}, 'Guests': {}}
            for item, quantity in wash['Items'].items():
                names[wash['Name']]['Items'][item] = quantity
            for item, quantity in wash['Guests'].items():
                names[wash['Name']]['Guests'][item] = quantity
        # If it is there already, add to the total for the apartment
        else:
            for item, quantity in wash['Items'].items():
                if item not in names[wash['Name']]['Items'].keys():
                    names[wash['Name']]['Items'][item] = quantity
                else:
                    names[wash['Name']]['Items'][item] += quantity
            for item, quantity in wash['Guests'].items():
                if item not in names[wash['Name']]['Guests'].keys():
                    names[wash['Name']]['Guests'][item] = quantity
                else:
                    names[wash['Name']]['Guests'][item] += quantity
    return names

def save(data):
    with open('apartments.json', 'w') as f:
        json.dump(data, f, indent = 4)

def main():
    save(group_by_name(load('washes.json')))