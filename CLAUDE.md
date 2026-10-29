# CLAUDE.md

## What this repo is

Single-package Python desktop app (flat layout, no monorepo) that parses cleaning-company PDF invoices and generates accountant-ready PDF overviews.

## Commands

- Setup: `pip install -r requirements.txt`
- Run (GUI): `python main.py`
- Run (automatic/CLI): `python main.py --pdf <invoice.pdf> [--out <output.pdf>]` — runs the full pipeline automatically; writes report PDF to `data/apartments.pdf` by default
- Package: `pyinstaller supply-scrubber.spec` → binary at `dist/main`
- Test: `python -m pytest` (from repo root; requires `pip install -r requirements.txt`)

There is no linter, typechecker, or CI configured. Automated verification is the pytest suite plus `python -m py_compile <file>`.

## Architecture

- Entry point: `main.py`. Tkinter/customtkinter GUI; PDF pipeline runs in a background thread fed by a `queue`, GUI polls via `root.after` every 100 ms. With `--pdf`, `main.py` runs the pipeline automatically (see `run_cli`).
- Pipeline order: `pdf_parser.main` → writes `data/washes.json` → `calculate_total.main` (adds `Items`/`Guests` `Total`, rounded to 2 decimals) → `apartment_summary.main` (groups by apartment name) → interactive per-apartment wash counts via GUI spinbox (`wash_summary`) → `pdf_generator.main` → writes `data/apartments.pdf`. Automatic mode derives wash counts from the number of washes parsed per apartment.
- Each pipeline step is its own top-level module with plain functions + `main()`; `main.py` only orchestrates. Flat imports (e.g. `import pdf_parser`), so run from repo root. Default file paths live in `paths.py` (absolute, based on module location).

## Gotchas

- Data file paths are centralized in `paths.py` (absolute); no hardcoded strings remain in modules.
- Final outputs land in `data/`: `washes.json`, `apartments.json`, `apartments.pdf`. Price lists: `data/price_list_items.json`, `data/price_list_apartments.json` (both gitignored; example copies in `example_data/`).
- Parsing depends on exact invoice text layout via regex (`Task Name`, `Due Date`, checkbox lines `☐  <item>  <qty>`, `Name`/`Address` from line positions). Formatting changes in invoices will break parsing — update regexes accordingly.
- Uses PyMuPDF (`import pymupdf as fitz`); switched from pdfplumber due to fitz issues.
- Per-apartment interactive input: arrow keys/Enter on the spinbox; `Return`/`Left`/`Right` key bindings on the root window.
- Automatic mode exits with code 1 and logs a clean error if the invoice PDF or price lists are missing.

## Out of scope for agents

- No linter/typechecker/CI configured.
- Don't add scaffolding or tooling unprompted; keep changes minimal and consistent with the flat-module style.
