import json
import logging
from collections import Counter

from paths import WASHES_PATH, APARTMENTS_PATH

logger = logging.getLogger(__name__)


def load(fp=WASHES_PATH):
    with open(fp, 'r') as f:
        return json.load(f)


def group_by_name(washes):
    # Create an overview of the washes for each apartment
    names = {}
    for wash in washes:
        name = wash['Name']
        if name not in names:
            names[name] = {'Items': Counter(), 'Guests': Counter(), 'Washes': {}}
        names[name]['Items'].update(wash['Items'])
        names[name]['Guests'].update(wash['Guests'])
    return names


def save(data, fp=APARTMENTS_PATH):
    with open(fp, 'w') as f:
        json.dump(data, f, indent=4)


def main(washes_path=WASHES_PATH, out_path=APARTMENTS_PATH):
    save(group_by_name(load(washes_path)), out_path)
