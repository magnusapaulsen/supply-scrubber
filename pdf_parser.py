import fitz, re, json

def parse_pdf(fp):
    print('Opening the PDF...')
    doc = fitz.open(fp)
    washes = []
    print('Looking through all the pages...')
    for page_count, page in enumerate(doc, start=1):
        wash = {}

        # Get text from the page
        text = page.get_text()
        # Turn text into list of lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        # Create new dictionary using RegEx
        wash['Name'] = lines[1]
        wash['Address'] = lines[2]
        task_match = re.search(r'Task Name\s+(.+)', text)
        if task_match:
            wash['Task'] = task_match.group(1)
        date_match = re.search(r'Due Date\s+(.+)', text)
        if date_match:
            wash['Date'] = date_match.group(1)
        wash['Items'] = {}
        wash['Guests'] = {}
        matches = re.findall(r'☐\s+(.+?)\s+(\d+)\s*$', text, re.MULTILINE)
        for item_name, quantity in matches:
            if 'Amount of Guests' in item_name:
                wash['Guests']['Amount of Guests'] = int(quantity)
            else:
                wash['Items'][item_name] = int(quantity)

        washes.append(wash)
        print(f'Finished page {page_count}')
    return washes

def save_pdf(washes):
    print('Saving...')
    with open('data/washes.json', 'w') as f:
        json.dump(washes, f, indent = 4)
    print('Saved!')

def main(fp):
    save_pdf(parse_pdf(fp))
