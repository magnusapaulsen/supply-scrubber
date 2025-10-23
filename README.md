# Supply-Scrubber

A Python program leveraging pdfplumber and RegEx to parse PDF supply sheets, generating an overview of cleaning and restocking tasks for an AirBnB business.

## Features
- Extracts apartment names, addresses, task names, dates, supply quantities and number of guests from PDF files.
- Creates an overview for each wash in a month.
- Creates a monthly overview for each apartment.
- Saves result to JSON-files.

## Installation

1. Clone the repository:
    git clone https://github.com/yourusername/supply-scrubber.git
    cd supply-scrubber

2. Install dependencies:
    pip install -r requirements.txt
    *Note:* Ensure you have Python 3.8+ installed.

## Usage

1. Place your JSON price list (`price_list.json`) in the project directory.
2. Run the script:
    python main.py
    python3 main.py
3. Navigate the GUI to select PDF and run the parsing.
4. View the results in the JSON files (`washes.json`, `apartments.json`)

## Requirements
- `pdfplumber`

List of dependencies is in `requirements.txt`.