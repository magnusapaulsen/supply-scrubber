import fitz, re

TASK_PATTERN = re.compile(r'Task Name\s+(.+)')
DATE_PATTERN = re.compile(r'Due Date\s+(.+)')
ITEM_PATTERN = re.compile(r'☐\s+(.+?)\s+(\d+)\s*$', re.MULTILINE)

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
        task_match = TASK_PATTERN.search(text)
        if task_match:
            wash['Task'] = task_match.group(1)
        date_match = DATE_PATTERN.search(text)
        if date_match:
            wash['Date'] = date_match.group(1)
        wash['Items'] = {}
        wash['Guests'] = {}
        for item_name, quantity in ITEM_PATTERN.findall(text):
            if 'Amount of Guests' in item_name:
                wash['Guests']['Amount of Guests'] = int(quantity)
            else:
                wash['Items'][item_name] = int(quantity)

        washes.append(wash)
        print(f'Finished page {page_count}')
    return washes

def main(fp):
    return parse_pdf(fp)
