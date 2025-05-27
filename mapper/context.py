from datafusion import SessionContext, ColumnType, Column
from datafusion.expr import lit, col
import pandas as pd
import os
from typing import List, Dict, Any, Optional

class CablesContext:
    """Context for working with diplomatic cables data using DataFusion."""
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the cables context.
        
        Args:
            data_path: Path to the CSV file containing cables data.
                       If None, no data will be loaded initially.
        """
        self.ctx = SessionContext()
        self.data_path = data_path
        
        # Define the schema for cables
        self.schema = {
            "id": ColumnType.Utf8,
            "date": ColumnType.Utf8,
            "reference_number": ColumnType.Utf8,
            "source": ColumnType.Utf8,
            "classification": ColumnType.Utf8,
            "references": ColumnType.Utf8,
            "header": ColumnType.Utf8,
            "content": ColumnType.Utf8
        }
        
        if data_path and os.path.exists(data_path):
            self.load_data(data_path)
    
    def load_data(self, path: str) -> None:
        """
        Load cables data from a CSV file.
        
        Args:
            path: Path to the CSV file containing cables data.
        """
        self.data_path = path
        
        # Read the CSV file using pandas
        df = pd.read_csv(path, header=None)
        
        # Rename columns to match our schema
        if len(df.columns) >= 8:
            df.columns = ["id", "date", "reference_number", "source", 
                          "classification", "references", "header", "content"]
            
            # Register the dataframe with DataFusion
            self.ctx.register_dataframe("cables", df)
            print(f"Loaded {len(df)} cables from {path}")
        else:
            raise ValueError(f"CSV file {path} does not have the expected number of columns")
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query against the cables data.
        
        Args:
            query: SQL query to execute.
            
        Returns:
            DataFrame containing the query results.
        """
        return self.ctx.sql(query).collect().to_pandas()
    
    def search_cables(self, 
                     text: Optional[str] = None,
                     date_from: Optional[str] = None,
                     date_to: Optional[str] = None,
                     classification: Optional[str] = None,
                     source: Optional[str] = None) -> pd.DataFrame:
        """
        Search cables based on various criteria.
        
        Args:
            text: Text to search for in the content.
            date_from: Start date in format MM/DD/YYYY.
            date_to: End date in format MM/DD/YYYY.
            classification: Classification level.
            source: Source of the cable.
            
        Returns:
            DataFrame containing matching cables.
        """
        conditions = []
        
        if text:
            conditions.append(f"content LIKE '%{text}%'")
        
        if date_from:
            conditions.append(f"date >= '{date_from}'")
        
        if date_to:
            conditions.append(f"date <= '{date_to}'")
        
        if classification:
            conditions.append(f"classification = '{classification}'")
        
        if source:
            conditions.append(f"source LIKE '%{source}%'")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = f"""
        SELECT id, date, reference_number, source, classification, content
        FROM cables
        WHERE {where_clause}
        ORDER BY date
        """
        
        return self.execute_query(query)
    
    def get_cable_by_id(self, cable_id: str) -> pd.DataFrame:
        """
        Retrieve a specific cable by its ID.
        
        Args:
            cable_id: The ID of the cable to retrieve.
            
        Returns:
            DataFrame containing the requested cable.
        """
        query = f"""
        SELECT *
        FROM cables
        WHERE id = '{cable_id}'
        """
        
        return self.execute_query(query)
