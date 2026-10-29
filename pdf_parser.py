import logging
import re

import pymupdf as fitz
import json

from paths import WASHES_PATH

logger = logging.getLogger(__name__)

CHECKBOX_RE = re.compile(r'☐\s+(.+?)\s+(\d+)\s*$', re.MULTILINE)


def parse_pdf(fp):
    logger.info('Opening the PDF...')
    doc = fitz.open(fp)
    washes = []
    logger.info('Looking through all the pages...')
    for page_count, page in enumerate(doc, start=1):
        text = page.get_text()
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if len(lines) < 3:
            logger.warning(f'Page {page_count} skipped: not enough text found')
            continue

        wash = {}

        # Get text from the page
        wash['Name'] = lines[1]
        wash['Address'] = lines[2]
        task_match = re.search(r'Task Name\s+(.+)', text)
        wash['Task'] = task_match.group(1) if task_match else None
        date_match = re.search(r'Due Date\s+(.+)', text)
        wash['Date'] = date_match.group(1) if date_match else None
        wash['Items'] = {}
        wash['Guests'] = {}
        matches = CHECKBOX_RE.findall(text)
        for item_name, quantity in matches:
            if 'Amount of Guests' in item_name:
                wash['Guests']['Amount of Guests'] = int(quantity)
            else:
                wash['Items'][item_name] = int(quantity)

        washes.append(wash)
        logger.info(f'Finished page {page_count}')
    return washes


def save_pdf(washes, fp=WASHES_PATH):
    logger.info('Saving...')
    with open(fp, 'w') as f:
        json.dump(washes, f, indent=4)
    logger.info('Saved!')


def main(fp=WASHES_PATH):
    save_pdf(parse_pdf(fp), fp)
