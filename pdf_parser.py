import pdfplumber, re, json

def parse_pdf(fp):
    print('Opening the PDF...')
    with pdfplumber.open(fp) as pdf:
        washes = []
        print('Looking through all the pages...')
        page_count = 1
        for page in pdf.pages:
            wash = {}

            # Get text from the page
            text = page.extract_text()
            # Turn text into list of lines
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            
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
            page_count += 1
    return washes

def save_pdf(washes):
    print('Saving...')
    with open('washes.json', 'w') as f:
        json.dump(washes, f, indent = 4)
    print('Saved!')

def main():
    save_pdf(parse_pdf('washes.pdf'))

if __name__ == '__main__':
    main()