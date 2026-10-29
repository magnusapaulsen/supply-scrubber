import json
import logging

from paths import APARTMENTS_PATH, PRICE_LIST_APARTMENTS_PATH

logger = logging.getLogger(__name__)


def load(fp=APARTMENTS_PATH):
    with open(fp, 'r') as f:
        return json.load(f)


def prepare_data(apartments):
    return list(apartments)


def finalize_data(apartments, summary, price_list_apartments):
    for apt, quantity in summary.items():
        if apt not in apartments:
            continue

        if 'Washes' not in apartments[apt]:
            apartments[apt]['Washes'] = {}

        if apt not in price_list_apartments:
            continue

        apartments[apt]['Washes']['Price'] = price_list_apartments[apt]
        apartments[apt]['Washes']['Quantity'] = quantity
        apartments[apt]['Washes']['Total'] = round(quantity * apartments[apt]['Washes']['Price'], 2)

    return apartments


def save(data, fp=APARTMENTS_PATH):
    with open(fp, 'w') as f:
        json.dump(data, f, indent=4)


def main(summary, price_list_apartments, apartments_path=APARTMENTS_PATH, out_path=APARTMENTS_PATH):
    apartments = load(apartments_path)
    finalized_data = finalize_data(apartments, summary, price_list_apartments)
    save(finalized_data, out_path)
