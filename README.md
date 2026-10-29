# supply-scrubber

**A desktop tool that automates monthly cost reporting for an Airbnb business by parsing custom cleaning-company PDF invoices and generating structured, accountant-ready PDF overviews.**

## Features
- Parses PDF invoices using **PyMuPDF** + **regex**
- Extracts per-apartment restocking quantities, guest counts, and dates
- Combines data with:
  - Per-apartment number of cleanings entered by the user
  - Per-apartment price lists (cleaning fees + individual supply items)
- Calculates exact costs per stay and per month
- Saves structured overviews as JSON (`washes.json`, `apartments.json`)
- Generates a clean, multi-page PDF report (one page per apartment) ready for the accountant
- Two run modes:
  - **GUI** (`python main.py`): interactive per-apartment cleaning counts via spinbox
  - **Automatic** (`python main.py --pdf <invoice.pdf>`): zero-interaction pipeline, ideal for LLM agents
- Testable pipeline with a pytest suite

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
    Place your JSON price lists (`price_list_items.json` & `price_list_apartments`) inside the data folder of the project directory.
    (Example files are included)

4. Run the script:
    ```bash
    python main.py
    ```
    
5. Navigate the GUI:
    Select PDF.
    Run parsing.
    Fill in number of cleanings (arrow keys and enter work too).
    Click 'Generate PDF' once it appears.

### Automatic mode (no GUI)

To run the full pipeline on an invoice and produce the final report PDF directly:

```bash
python main.py --pdf /path/to/invoice.pdf --out /path/to/output.pdf
```

This parses the PDF, calculates totals, groups apartments, assigns one wash per parsed wash, and writes the finished PDF (default: `data/apartments.pdf`, override with `--out`). No interactive input is required. This is the mode an LLM agent would use to fulfill a request like "take this invoice and use supply-scrubber to generate a PDF for my accountant."

## Testing

```bash
python -m pytest
```

The test suite covers the calculation, grouping, and finalize logic, plus PDF generation. All tests run without the GUI or a display server.
     
## Packaging (PyInstaller)

To build a standalone executable (no Python install needed on the target machine):

```bash
pyinstaller supply-scrubber.spec
```

Produces a binary at `dist/main`. The `data/` folder (icons, theme, price lists) is bundled at build time.

## Requirements
- `CTkSpinbox`
- `customtkinter`
- `pymupdf`
- `reportlab`
- `pytest` (for running the test suite)
- `pyinstaller` (for building the standalone executable)

List of dependencies is in `requirements.txt`.
