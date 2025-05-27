# Cables Mapper

A tool for processing diplomatic cables using DataFusion.

## Installation

```bash
pip install -e .
```

## Usage

```bash
cables-cli cables_sample.csv --search "SOVIET"
```

### Options

- `--query`, `-q`: Execute a custom SQL query
- `--search`, `-s`: Search for text in cable content
- `--date-from`: Filter by start date (MM/DD/YYYY)
- `--date-to`: Filter by end date (MM/DD/YYYY)
- `--classification`, `-c`: Filter by classification level
- `--source`: Filter by source
- `--output`, `-o`: Save results to a CSV file
- `--limit`, `-l`: Limit number of results (default: 100)

## Examples

Search for cables containing "SOVIET":
```bash
cables-cli cables_sample.csv --search "SOVIET"
```

Filter by date range:
```bash
cables-cli cables_sample.csv --date-from "01/01/1970" --date-to "12/31/1972"
```

Execute a custom SQL query:
```bash
cables-cli cables_sample.csv --query "SELECT * FROM cables WHERE source LIKE '%TEHRAN%'"
```
