from utils import normalize_price_list

def process_washes(washes, price_list_items):
    prices = normalize_price_list(price_list_items)
    apartments = {}

    for wash in washes:
        name = wash['Name']

        # Calculate items total for this wash
        items_total = 0
        for item, quantity in wash['Items'].items():
            key = item.casefold()
            if key in prices:
                items_total += quantity * prices[key]
        items_total = round(items_total, 2)

        # Calculate guests total for this wash
        guests_total = 0
        for guest_key, quantity in wash['Guests'].items():
            key = guest_key.casefold()
            if key in prices:
                guests_total += quantity * prices[key]
        guests_total = round(guests_total, 2)

        # Group by apartment name
        if name not in apartments:
            apartments[name] = {'Items': {}, 'Guests': {}, 'Washes': {}}

        # Accumulate item quantities
        for item, quantity in wash['Items'].items():
            apartments[name]['Items'][item] = apartments[name]['Items'].get(item, 0) + quantity

        # Accumulate guest counts
        for guest_key, quantity in wash['Guests'].items():
            apartments[name]['Guests'][guest_key] = apartments[name]['Guests'].get(guest_key, 0) + quantity

        # Accumulate totals
        apartments[name]['Items']['Total'] = round(
            apartments[name]['Items'].get('Total', 0) + items_total, 2
        )
        apartments[name]['Guests']['Total'] = round(
            apartments[name]['Guests'].get('Total', 0) + guests_total, 2
        )

    return apartments
