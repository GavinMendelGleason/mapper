#!/usr/bin/env python3
"""
CLI tool for working with diplomatic cables data using DataFusion.
"""

import argparse
import os
import sys
from typing import List, Optional

from mapper.context import CablesContext


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process diplomatic cables data using DataFusion"
    )
    
    parser.add_argument(
        "csv_file", 
        help="Path to the CSV file containing cables data"
    )
    
    parser.add_argument(
        "--query", "-q",
        help="SQL query to execute against the cables data"
    )
    
    parser.add_argument(
        "--search", "-s",
        help="Text to search for in cable content"
    )
    
    parser.add_argument(
        "--date-from",
        help="Start date in format MM/DD/YYYY"
    )
    
    parser.add_argument(
        "--date-to",
        help="End date in format MM/DD/YYYY"
    )
    
    parser.add_argument(
        "--classification", "-c",
        help="Classification level to filter by"
    )
    
    parser.add_argument(
        "--source",
        help="Source of the cable to filter by"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file path (CSV format). If not specified, prints to stdout."
    )
    
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=100,
        help="Limit the number of results (default: 100)"
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)
    
    # Check if the CSV file exists
    if not os.path.exists(parsed_args.csv_file):
        print(f"Error: CSV file '{parsed_args.csv_file}' not found", file=sys.stderr)
        return 1
    
    try:
        # Initialize the context with the CSV file
        context = CablesContext(parsed_args.csv_file)
        
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
            print(f"Results saved to {parsed_args.output}")
        else:
            # Print to stdout
            if len(result) > 0:
                print(result.to_string())
                print(f"\nTotal results: {len(result)}")
            else:
                print("No results found.")
                
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
