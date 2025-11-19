import json

def load(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def prepare_data(apartments):
    # Make list of all apartments
    apts = []
    for apt in apartments.keys():
        apts.append(apt)
    return apts

def finalize_data(apartments, summary, price_list_apartments):
    for apt, quantity in summary.items():
        if apt not in apartments:
            continue

        if 'Washes' not in apartments[apt]:
            apartments[apt]['Washes'] = {}

        apartments[apt]['Washes']['Price'] = price_list_apartments[apt]
        apartments[apt]['Washes']['Quantity'] = quantity
        apartments[apt]['Washes']['Total'] = quantity * apartments[apt]['Washes']['Price']
    
    return apartments

def create_summary():
    # I don't use this since I don't run this file from main()
    pass

def save(data, fp):
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def main():
    apartments = load('apartments.json')
    prepare_data(apartments)
    finalized_data = finalize_data(apartments, create_summary(apartments), load('price_list_apartments.json'))
    save(finalized_data, 'apartments.json')