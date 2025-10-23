import json

def load(fp):
    with open(fp, 'r') as f:
        return json.load(f)

def group_by_address(washes):
    # Create an overview of the washes for each apartment
    addresses = {}
    # Loop through all washes
    for wash in washes:
        # Add the address to the dictionary if it is not there already
        if wash['Address'] not in addresses.keys():
            addresses[wash['Address']] = {'Items': {}, 'Guests': {}}
            for item, quantity in wash['Items'].items():
                addresses[wash['Address']]['Items'][item] = quantity
            for item, quantity in wash['Guests'].items():
                addresses[wash['Address']]['Guests'][item] = quantity
        # If it is there already, add to the total for the apartment
        else:
            for item, quantity in wash['Items'].items():
                if item not in addresses[wash['Address']]['Items'].keys():
                    addresses[wash['Address']]['Items'][item] = quantity
                else:
                    addresses[wash['Address']]['Items'][item] += quantity
            for item, quantity in wash['Guests'].items():
                if item not in addresses[wash['Address']]['Guests'].keys():
                    addresses[wash['Address']]['Guests'][item] = quantity
                else:
                    addresses[wash['Address']]['Guests'][item] += quantity
    return addresses

def save(data):
    with open('apartments.json', 'w') as f:
        json.dump(data, f, indent = 4)

def main():
    save(group_by_address(load('washes.json')))
