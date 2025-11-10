import json

def load(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        return json.load(f)

def summarize_washes(apartments, price_list_apartments):
    for name, data in apartments.items():
        # Ensure 'Washes' exists
        if 'Washes' not in data:
            data['Washes'] = {}

        # Get the price for this apartment
        price = price_list_apartments.get(name, 0)
        data['Washes']['Price'] = price

        # Prompt the user for quantity
        while True:
            try:
                quantity = int(input(f'How many times was {name} washed this month? '))
                data['Washes']['Quantity'] = quantity
            except ValueError:
                print('You have to enter a number...')
            else:
                # Calculate total for this apartment
                data['Washes']['Total'] = price * quantity
                break
    print('That was the last one!')

    return apartments

def save(data, fp):
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def main():
    apartments = load('apartments.json')
    price_list_apartments = load('price_list_apartments.json')
    updated_apartments = summarize_washes(apartments, price_list_apartments)
    save(updated_apartments, 'apartments.json')