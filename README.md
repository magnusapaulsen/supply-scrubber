# Supply-Scrubber

A Python program leveraging pdfplumber and RegEx to parse PDF supply sheets, generating an overview of cleaning and restocking tasks for an AirBnB business.

## Features
- Extracts due dates, addresses, task names, and supply quantities from PDF files.
- Aggregates supplies by date and creates a markdown table overview.
- Ignores non-supply data (e.g., "Amount of Guests").
- Outputs results to console and optionally saves to a CSV file.

## Installation

1. Clone the repository:
    git clone https://github.com/yourusername/supply-scrubber.git
    cd supply-scrubber

2. Install dependencies:
    pip install -r requirements.txt
    *Note:* Ensure you have Python 3.8+ installed.

## Usage

1. Place your PDF supply sheets (e.g., `washes.pdf`) in the project directory.
2. Run the script:
    python main.py
3. View the output in the console or check `supplies_overview.csv` for the aggregated data.

## Requirements
- `pdfplumber`
- `re` (built-in Python module)

List of dependencies is in `requirements.txt`.