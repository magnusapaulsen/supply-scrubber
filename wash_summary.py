def finalize_data(apartments, summary, price_list_apartments):
    for apt, quantity in summary.items():
        if apt not in apartments:
            continue

        apartments[apt]['Washes'] = {
            'Price': price_list_apartments[apt],
            'Quantity': quantity,
            'Total': quantity * price_list_apartments[apt]
        }

    return apartments
