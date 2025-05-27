#!/usr/bin/env python3
"""
CLI tool for working with diplomatic cables data using DataFusion.
"""

import argparse
import os
import sys
from typing import List, Optional

from rich.console import Console

from mapper.context import CablesContext
from mapper.embeddings import EmbeddingModel
from mapper.visualization import load_embeddings, create_tsne_plot

console = Console()


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process diplomatic cables data using DataFusion"
    )
    
    parser.add_argument(
        "csv_file", 
        help="Path to the CSV file containing cables data"
    )
    
    # Query and search options
    query_group = parser.add_argument_group("Query and Search Options")
    query_group.add_argument(
        "--query", "-q",
        help="SQL query to execute against the cables data"
    )
    
    query_group.add_argument(
        "--search", "-s",
        help="Text to search for in cable content"
    )
    
    query_group.add_argument(
        "--date-from",
        help="Start date in format MM/DD/YYYY"
    )
    
    query_group.add_argument(
        "--date-to",
        help="End date in format MM/DD/YYYY"
    )
    
    query_group.add_argument(
        "--classification", "-c",
        help="Classification level to filter by"
    )
    
    query_group.add_argument(
        "--source",
        help="Source of the cable to filter by"
    )
    
    # Chunking and embedding options
    embedding_group = parser.add_argument_group("Chunking and Embedding Options")
    embedding_group.add_argument(
        "--chunk",
        action="store_true",
        help="Chunk the cables for embedding generation"
    )
    
    embedding_group.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Size of each chunk in characters (default: 1000)"
    )
    
    embedding_group.add_argument(
        "--embed",
        action="store_true",
        help="Generate embeddings for the cables"
    )
    
    embedding_group.add_argument(
        "--model",
        default="Alibaba-NLP/gte-Qwen2-7B-instruct",
        help="Model to use for embeddings (default: Alibaba-NLP/gte-Qwen2-7B-instruct)"
    )
    
    embedding_group.add_argument(
        "--batch-size",
        type=int,
        default=8,
        help="Batch size for embedding generation (default: 8)"
    )
    
    # Visualization options
    viz_group = parser.add_argument_group("Visualization Options")
    viz_group.add_argument(
        "--visualize",
        action="store_true",
        help="Visualize embeddings using t-SNE"
    )
    
    viz_group.add_argument(
        "--embeddings-file",
        help="Path to the embeddings pickle file for visualization"
    )
    
    viz_group.add_argument(
        "--perplexity",
        type=int,
        default=30,
        help="Perplexity parameter for t-SNE (default: 30)"
    )
    
    viz_group.add_argument(
        "--iterations",
        type=int,
        default=1000,
        help="Number of iterations for t-SNE (default: 1000)"
    )
    
    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "--output", "-o",
        help="Output file path. For embeddings, this will be a pickle file. For visualization, this will be a PNG file."
    )
    
    output_group.add_argument(
        "--limit", "-l",
        type=int,
        default=100,
        help="Limit the number of results for queries (default: 100)"
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)
    
    try:
        # Handle visualization if requested
        if parsed_args.visualize:
            if not parsed_args.embeddings_file:
                console.print("Error: --embeddings-file is required for visualization", style="bold red")
                return 1
                
            # Load embeddings
            df = load_embeddings(parsed_args.embeddings_file)
            
            # Create t-SNE plot
            create_tsne_plot(
                df=df,
                output_path=parsed_args.output,
                perplexity=parsed_args.perplexity,
                n_iter=parsed_args.iterations,
                title="t-SNE Visualization of Cable Embeddings"
            )
            
            return 0
        
        # Check if the CSV file exists for other operations
        if not os.path.exists(parsed_args.csv_file):
            console.print(f"Error: CSV file '{parsed_args.csv_file}' not found", style="bold red")
            return 1
            
        # Initialize the context with the CSV file
        context = CablesContext(parsed_args.csv_file)
        
        # Handle chunking and embedding if requested
        if parsed_args.chunk or parsed_args.embed:
            # Chunk the cables
            chunks = context.chunk_all_cables(chunk_size=parsed_args.chunk_size)
            
            if parsed_args.embed:
                # Initialize the embedding model
                model = EmbeddingModel(model_name=parsed_args.model)
                
                # Generate embeddings
                embeddings = model.generate_embeddings_for_chunks(
                    chunks=chunks,
                    batch_size=parsed_args.batch_size
                )
                
                # Save embeddings if output path is provided
                if parsed_args.output:
                    model.save_embeddings(embeddings, parsed_args.output)
                else:
                    console.print("Warning: No output path provided for embeddings", style="bold yellow")
            
            return 0
        
        # Execute a custom query if provided
        if parsed_args.query:
            result = context.execute_query(parsed_args.query)
        else:
            # Otherwise, use the search_cables method with the provided filters
            result = context.search_cables(
                text=parsed_args.search,
                date_from=parsed_args.date_from,
                date_to=parsed_args.date_to,
                classification=parsed_args.classification,
                source=parsed_args.source
            )
            
            # Apply limit
            if parsed_args.limit and len(result) > parsed_args.limit:
                result = result.head(parsed_args.limit)
        
        # Output the results
        if parsed_args.output:
            result.to_csv(parsed_args.output, index=False)
            console.print(f"Results saved to {parsed_args.output}", style="bold green")
        else:
            # Print to stdout
            if len(result) > 0:
                console.print(result)
                console.print(f"\nTotal results: {len(result)}", style="bold green")
            else:
                console.print("No results found.", style="bold yellow")
                
        return 0
        
    except Exception as e:
        console.print(f"Error: {str(e)}", style="bold red")
        return 1


if __name__ == "__main__":
    sys.exit(main())
