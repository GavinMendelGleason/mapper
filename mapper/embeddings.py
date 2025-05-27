"""
Embedding utilities for cable text processing.

This module provides functionality to generate embeddings for cable chunks
using the gte-Qwen2-7B-instruct model.
"""

import os
import torch
import pandas as pd
from typing import List, Dict, Any, Optional, Union
from sentence_transformers import SentenceTransformer
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

from mapper.chunking import CableChunk

console = Console()


class EmbeddingModel:
    """Wrapper for the embedding model."""
    
    def __init__(self, model_name: str = "Alibaba-NLP/gte-Qwen2-7B-instruct"):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Name of the model to use for embeddings
        """
        console.print(f"Initializing embedding model: {model_name}...", style="bold green")
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
        self.model_name = model_name
        console.print("Model initialized successfully!", style="bold green")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for a single text.
        
        Args:
            text: The text to embed
            
        Returns:
            List of embedding values
        """
        with torch.no_grad():
            embedding = self.model.encode(text)
            return embedding.tolist()
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        with torch.no_grad():
            embeddings = self.model.encode(texts)
            return embeddings.tolist()
    
    def generate_embeddings_for_chunks(
        self, chunks: List[CableChunk], batch_size: int = 8
    ) -> Dict[str, List[float]]:
        """
        Generate embeddings for a list of cable chunks.
        
        Args:
            chunks: List of CableChunk objects
            batch_size: Number of chunks to process at once
            
        Returns:
            Dictionary mapping chunk IDs to embeddings
        """
        results = {}
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Generating embeddings...", total=len(chunks))
            
            # Process in batches
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i+batch_size]
                texts = [chunk.text for chunk in batch]
                
                # Generate embeddings for the batch
                batch_embeddings = self.generate_embeddings(texts)
                
                # Store results
                for j, chunk in enumerate(batch):
                    chunk_id = f"{chunk.cable_id}_{chunk.chunk_id}"
                    results[chunk_id] = batch_embeddings[j]
                
                progress.update(task, advance=len(batch))
        
        return results
    
    def save_embeddings(
        self, embeddings: Dict[str, List[float]], output_path: str
    ) -> None:
        """
        Save embeddings to a file.
        
        Args:
            embeddings: Dictionary mapping chunk IDs to embeddings
            output_path: Path to save the embeddings
        """
        # Convert to DataFrame
        data = []
        for chunk_id, embedding in embeddings.items():
            cable_id, chunk_id_num = chunk_id.split('_')
            data.append({
                'cable_id': cable_id,
                'chunk_id': int(chunk_id_num),
                'embedding': embedding
            })
        
        df = pd.DataFrame(data)
        
        # Save to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_pickle(output_path)
        console.print(f"Embeddings saved to {output_path}", style="bold green")
