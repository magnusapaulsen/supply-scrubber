# supply-scrubber

**A desktop tool that automates monthly cost reporting for an Airbnb business by parsing custom cleaning-company PDF invoices and generating structured, accountant-ready PDF overviews.**

## Features
- Parses PDF invoices using **PyMuPDF** + **regex**
- Extracts per-apartment restocking quantities, guest counts, and dates
- Combines data with:
  - Per-apartment number of cleanings entered by the user
  - Per-apartment price lists (cleaning fees + individual supply items)
- Calculates exact costs per stay and per month
- Saves structured overviews as JSON (`apartments.json`)
- Generates a clean, multi-page PDF report (one page per apartment) ready for the accountant

## Screenshots
<div>
  <img src="screenshots/screenshot1.png" width="45%"/>
  <img src="screenshots/screenshot2.png" width="45%"/>
</div>
<div>
  <img src="screenshots/screenshot3.png" width="45%"/>
  <img src="screenshots/screenshot4.png" width="45%"/>
</div>
<div>
  <img src="screenshots/screenshot5.png" width="45%"/>
  <img src="screenshots/screenshot6.png" width="45%"/>
</div>

## Get started

1. Clone the repository:
	```bash
	git clone https://github.com/magnusapaulsen/supply-scrubber.git
 	cd supply-scrubber
 	```
  
2. Install dependencies:
	```bash
	pip install -r requirements.txt
 	```
 
    *Note:* Ensure you have Python 3.8+ installed.

3. Get price lists:
    Place your JSON price lists (`price_list_items.json` & `price_list_apartments.json`) inside the data folder of the project directory.
    (Example files are included)

4. Run the app:
    ```bash
    python main.py
    ```

5. Navigate the GUI:
    Select PDF.
    Run parsing.
    Fill in number of cleanings per apartment.
    Click Generate PDF.

## Requirements
- `CTkSpinbox`
- `customtkinter`
- `pymupdf`
- `reportlab`

List of dependencies is in `requirements.txt`.
