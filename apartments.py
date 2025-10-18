import json

def load(fp):
    with open(fp, 'r') as f:
        return json.load(f)

def group_by_address(washes):
    addresses = {}
    for wash in washes:
        if wash['Address'] not in addresses.keys():
            addresses[wash['Address']] = {'Items': {}, 'Guests': {}}
            for item, quantity in wash['Items'].items():
                addresses[wash['Address']]['Items'][item] = quantity
            for item, quantity in wash['Guests'].items():
                addresses[wash['Address']]['Guests'][item] = quantity
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

save(group_by_address(load('washes.json')))