from utils import load, save

def calculate_total(washes, price_list_items):
    # Loop through all washes
    for wash in washes:
        # Add total cost of items
        if 'Total' not in wash['Items'].keys():
            total = 0
            for item, quantity in wash['Items'].items():
                if item in price_list_items.keys():
                    total += quantity * price_list_items[item]
            wash['Items']['Total'] = total

        # Add total number of guests
        if 'Total' not in wash['Guests'].keys():
            total = 0
            for item, quantity in wash['Guests'].items():
                if item in price_list_items.keys():
                    total += quantity * price_list_items[item]
            wash['Guests']['Total'] = total

    return washes

def main():
    save(calculate_total(load('data/washes.json'), load('data/price_list_items.json')), 'data/washes.json')
