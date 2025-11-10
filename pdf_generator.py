import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime

def load(fp):
    with open(fp, 'r') as f:
        return json.load(f)

def generate_pdf(data, filename='apartments.pdf'):
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
    date_text = Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", 
                         styles['Normal'])
    elements.append(date_text)
    elements.append(Spacer(1, 1*cm))
    
    # Individual apartment sections
    for apartment, details in data.items():
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
            
            items_data.append(['Total:', f'kr {items_total:,.2f}'])
            
            items_table = Table(items_data, colWidths=[12*cm, 5*cm])
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -2), colors.lightblue),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#AED6F1')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            
            elements.append(items_table)
            elements.append(Spacer(1, 0.3*cm))
        
        # Guests table
        if "Guests" in details:
            guests_data = details["Guests"]
            guest_table_data = [
                ['Number of Guests', 'Total'],
                [str(guests_data.get('Amount of Guests', 0)), f"kr {guests_data.get('Total', 0):,.2f}"]
            ]
            
            guest_table = Table(guest_table_data, colWidths=[12*cm, 5*cm])
            guest_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            
            elements.append(guest_table)
            elements.append(Spacer(1, 0.3*cm))
        
        # Total costs for this apartment
        items_total = details.get("Items", {}).get("Total", 0)
        guests_total = details.get("Guests", {}).get("Total", 0)
        net_cost = items_total + guests_total
        
        total_data = [['Total cost:', f'kr {net_cost:,.2f}']]
        total_table = Table(total_data, colWidths=[12*cm, 5*cm])
        total_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F39C12')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(total_table)
        elements.append(Spacer(1, 0.3*cm))

        # Washes table
        if "Washes" in details:
            washes_data = details["Washes"]
            wash_table_data = [
                ['Number of Washes', 'Price per Wash', 'Total'],
                [
                    str(washes_data.get('Quantity', 0)),
                    f"kr {washes_data.get('Price', 0)}",
                    f"kr {washes_data.get('Total', 0)}"
                ]
            ]

            washes_table = Table(wash_table_data, colWidths=[7*cm, 5*cm, 5*cm])
            washes_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),  # Blue header
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))

            elements.append(washes_table)
            elements.append(Spacer(1, 0.3*cm))
    
    # Build PDF
    doc.build(elements)
    print(f"PDF successfully created: {filename}")

def main():
    data = load('apartments.json')
    generate_pdf(data, 'apartments.pdf')

# Main execution
if __name__ == "__main__":
    data = load('apartments.json')
    generate_pdf(data, 'apartments.pdf')