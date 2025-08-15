# Puzzle Scraper

Quick, hacky scripts to scrape puzzle data from the Wheel of Fortune Puzzle Compendium.

- [compendium_scraper.py](./compendium_scraper.py) — scrapes seasons 1–24 by default (adjust the range in the script to include more).
- [messy_parse_scraped.py](./messy_parse_scraped.py) — parses the raw HTML table rows produced by the scraper into CSV rows.

## Requirements
```bash
pip install requests beautifulsoup4
```

## Usage

1) Scrape the compendium HTML and save it to a file:
```bash
python3 compendium_scraper.py > compendium_raw.html
```

2) Parse the scraped HTML into CSV (written to stdout):
```bash
python3 messy_parse_scraped.py compendium_raw.html > years_1_25.csv
```

## Output
- The resulting CSV (e.g., `years_1_25.csv`) contains rows like those included under [data/puzzles](../../data/puzzles/), for example: [years_1_25.csv](../../data/puzzles/years_1_25.csv).

