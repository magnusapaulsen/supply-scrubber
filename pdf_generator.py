from utils import load, format_currency, table_style
from paths import get_data_path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from datetime import datetime

def generate_pdf(data, filename='data/apartments.pdf'):
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)

    # Container for PDF elements
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#000000'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#000000'),
        spaceAfter=12,
        spaceBefore=12
    )

    # Title
    title = Paragraph(f"Expense Report", title_style)
    elements.append(title)

    # Date
    date_text = Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal'])
    elements.append(date_text)
    elements.append(Spacer(1, 1*cm))

    # Individual apartment sections
    for i, (apartment, details) in enumerate(data.items()):

        if i > 0:
            elements.append(PageBreak())

        # Apartment heading
        apt_heading = Paragraph(f"<b>{apartment}</b>", heading_style)
        elements.append(apt_heading)

        # Items table
        if "Items" in details:
            items_data = [['Item', 'Quantity']]
            items = details["Items"].copy()
            items_total = items.pop("Total", 0)

            for item, qty in items.items():
                items_data.append([item, str(qty)])

            items_data.append(['Total:', format_currency(items_total)])

            items_table = Table(items_data, colWidths=[14*cm, 3*cm])
            items_table.setStyle(table_style(header_rows=1))

            elements.append(items_table)
            elements.append(Spacer(1, 0.5*cm))

        # Guests table
        if "Guests" in details:
            guests_data = details["Guests"]
            guest_table_data = [
                ['Number of Guests', 'Total'],
                [str(guests_data.get('Amount of Guests', 0)), format_currency(guests_data.get('Total', 0))]
            ]

            guest_table = Table(guest_table_data, colWidths=[14*cm, 3*cm])
            guest_table.setStyle(table_style(header_rows=1))

            elements.append(guest_table)
            elements.append(Spacer(1, 0.5*cm))

        # Total costs for this apartment
        items_total = details.get("Items", {}).get("Total", 0)
        guests_total = details.get("Guests", {}).get("Total", 0)
        total = items_total + guests_total

        total_data = [['Total cost:', format_currency(total)]]
        total_table = Table(total_data, colWidths=[14*cm, 3*cm])
        total_table.setStyle(table_style(header_rows=0))

        elements.append(total_table)
        elements.append(Spacer(1, 0.3*cm))

        # Washes table
        if "Washes" in details:
            washes_data = details["Washes"]
            wash_table_data = [
                ['Number of Washes', 'Price per Wash', 'Total'],
                [
                    str(washes_data.get('Quantity', 0)),
                    format_currency(washes_data.get('Price', 0)),
                    format_currency(washes_data.get('Total', 0))
                ]
            ]

            washes_table = Table(wash_table_data, colWidths=[7*cm, 7*cm, 3*cm])
            washes_table.setStyle(table_style(header_rows=1))

            elements.append(washes_table)
            elements.append(Spacer(1, 1*cm))

    # Build PDF
    doc.build(elements)
    print(f"PDF successfully created: {filename}")

def main():
    data = load(get_data_path('data/apartments.json'))
    generate_pdf(data, get_data_path('data/apartments.pdf'))

# Main execution
if __name__ == "__main__":
    data = load(get_data_path('data/apartments.json'))
    generate_pdf(data, get_data_path('data/apartments.pdf'))
