import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

WASHES_PATH = os.path.join(DATA_DIR, 'washes.json')
APARTMENTS_PATH = os.path.join(DATA_DIR, 'apartments.json')
PRICE_LIST_ITEMS_PATH = os.path.join(DATA_DIR, 'price_list_items.json')
PRICE_LIST_APARTMENTS_PATH = os.path.join(DATA_DIR, 'price_list_apartments.json')
PDF_PATH = os.path.join(DATA_DIR, 'apartments.pdf')
