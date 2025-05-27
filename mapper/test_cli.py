#!/usr/bin/env python3
"""
Test script for the cables CLI.
"""

import os
import sys
from mapper.cli import main

def test_cli():
    """Run a simple test of the CLI with the sample data."""
    # Get the path to the sample CSV file
    sample_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cables_sample.csv")
    
    if not os.path.exists(sample_path):
        print(f"Error: Sample file not found at {sample_path}")
        return 1
    
    # Test basic loading
    print("Testing basic CSV loading...")
    args = [sample_path]
    result = main(args)
    
    if result != 0:
        print("Basic loading test failed")
        return 1
    
    # Test with a search term
    print("\nTesting search functionality...")
    args = [sample_path, "--search", "SOVIET"]
    result = main(args)
    
    if result != 0:
        print("Search test failed")
        return 1
    
    print("\nAll tests passed!")
    return 0

if __name__ == "__main__":
    sys.exit(test_cli())
