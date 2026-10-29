import json
import logging

from paths import WASHES_PATH, PRICE_LIST_ITEMS_PATH

logger = logging.getLogger(__name__)


def load(fp=WASHES_PATH):
    with open(fp, 'r') as f:
        return json.load(f)


def calculate_total(washes, price_list_items):
    # Loop through all washes
    for wash in washes:
        # Add total cost of items
        if 'Total' not in wash['Items']:
            total = 0
            for item, quantity in wash['Items'].items():
                if item in price_list_items:
                    total += quantity * price_list_items[item]
            wash['Items']['Total'] = round(total, 2)

        # Add total number of guests
        if 'Total' not in wash['Guests']:
            total = 0
            for item, quantity in wash['Guests'].items():
                if item in price_list_items:
                    total += quantity * price_list_items[item]
            wash['Guests']['Total'] = round(total, 2)

    return washes


def save(data, fp=WASHES_PATH):
    with open(fp, 'w') as f:
        json.dump(data, f, indent=4)


def main(washes_path=WASHES_PATH, price_list_items_path=PRICE_LIST_ITEMS_PATH, out_path=WASHES_PATH):
    save(calculate_total(load(washes_path), load(price_list_items_path)), out_path)
