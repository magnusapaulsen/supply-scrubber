import json

def load(fp):
    with open(fp, 'r') as f:
        return json.load(f)

def calculate_total(washes, price_list):
    for wash in washes:
        if 'Total' not in wash['Items'].keys():
            total = 0
            for item, quantity in wash['Items'].items():
                if item in price_list.keys():
                    total += quantity * price_list[item]
            wash['Items']['Total'] = total
            print('Saved total of items...')
        else:
            print('Already calculated...')
        if 'Total' not in wash['Guests'].keys():
            total = 0
            for item, quantity in wash['Guests'].items():
                if item in price_list.keys():
                    total += quantity * price_list[item]
            wash['Guests']['Total'] = total
            print('Saved total of guests...')
        else:
            print('Already calculated...')

    return washes

def save(data, fp):
    with open(fp, 'w') as f:
        json.dump(data, f, indent = 4)

save(calculate_total(load('washes.json'), load('price_list.json')), 'washes.json')