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

#### Query and Search Options
- `--query`, `-q`: Execute a custom SQL query
- `--search`, `-s`: Search for text in cable content
- `--date-from`: Filter by start date (MM/DD/YYYY)
- `--date-to`: Filter by end date (MM/DD/YYYY)
- `--classification`, `-c`: Filter by classification level
- `--source`: Filter by source

#### Chunking and Embedding Options
- `--chunk`: Chunk the cables for embedding generation
- `--chunk-size`: Size of each chunk in characters (default: 1000)
- `--embed`: Generate embeddings for the cables
- `--model`: Model to use for embeddings (default: Alibaba-NLP/gte-Qwen2-7B-instruct)
- `--batch-size`: Batch size for embedding generation (default: 8)

#### Visualization Options
- `--visualize`: Visualize embeddings using t-SNE
- `--embeddings-file`: Path to the embeddings pickle file for visualization
- `--perplexity`: Perplexity parameter for t-SNE (default: 30)
- `--iterations`: Number of iterations for t-SNE (default: 1000)

#### Output Options
- `--output`, `-o`: Output file path (CSV for queries, pickle for embeddings, PNG for visualization)
- `--limit`, `-l`: Limit number of results for queries (default: 100)

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

Generate embeddings:
```bash
cables-cli cables_sample.csv --chunk --embed --output embeddings.pkl
```

Visualize embeddings:
```bash
cables-cli cables_sample.csv --visualize --embeddings-file embeddings.pkl --output visualization.png
```
