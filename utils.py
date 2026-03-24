import json
from reportlab.lib import colors
from reportlab.platypus import TableStyle

def load(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def format_currency(value):
    return f"kr {value:,.2f}"

def normalize_price_list(price_list):
    return {key.casefold(): value for key, value in price_list.items()}

def table_style(header_rows=1):
    style_commands = [
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#ffffff')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#111111')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ]

    if header_rows > 0:
        style_commands += [
            ('BACKGROUND', (0, 0), (-1, header_rows - 1), colors.HexColor('#000000')),
            ('FONTNAME', (0, 0), (-1, header_rows - 1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, header_rows), (-1, -2), colors.HexColor('#333333')),
            ('FONTNAME', (0, header_rows), (-1, -1), 'Helvetica'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ff0000')),
        ]
    else:
        style_commands += [
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ff0000')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ]

    return TableStyle(style_commands)
