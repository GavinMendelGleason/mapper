"""
Visualization utilities for cable embeddings.

This module provides functionality to visualize embeddings using dimensionality
reduction techniques like t-SNE.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from typing import List, Dict, Optional, Union, Tuple
from rich.console import Console

console = Console()


def load_embeddings(embeddings_path: str) -> pd.DataFrame:
    """
    Load embeddings from a pickle file.
    
    Args:
        embeddings_path: Path to the embeddings pickle file
        
    Returns:
        DataFrame containing the embeddings
    """
    if not os.path.exists(embeddings_path):
        raise FileNotFoundError(f"Embeddings file not found: {embeddings_path}")
    
    df = pd.read_pickle(embeddings_path)
    console.print(f"Loaded embeddings for {len(df)} chunks", style="bold green")
    return df


def create_tsne_plot(
    df: pd.DataFrame,
    output_path: Optional[str] = None,
    perplexity: int = 30,
    n_iter: int = 1000,
    random_state: int = 42,
    figsize: Tuple[int, int] = (12, 10),
    title: str = "t-SNE Visualization of Cable Embeddings",
) -> None:
    """
    Create a t-SNE plot of embeddings colored by cable ID.
    
    Args:
        df: DataFrame containing embeddings
        output_path: Path to save the plot (if None, display the plot)
        perplexity: Perplexity parameter for t-SNE
        n_iter: Number of iterations for t-SNE
        random_state: Random state for reproducibility
        figsize: Figure size (width, height) in inches
        title: Plot title
    """
    # Extract embeddings and cable IDs
    embeddings = np.array(df['embedding'].tolist())
    cable_ids = np.array(df['cable_id'].tolist())
    
    # Apply t-SNE for dimensionality reduction
    console.print("Applying t-SNE dimensionality reduction...", style="bold blue")
    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        n_iter=n_iter,
        random_state=random_state
    )
    tsne_result = tsne.fit_transform(embeddings)
    
    # Create a plot
    plt.figure(figsize=figsize)
    ax = sns.scatterplot(
        x=tsne_result[:, 0],
        y=tsne_result[:, 1],
        hue=cable_ids,
        palette="bright",
        s=100,
        alpha=0.7
    )
    
    # Add title and labels
    plt.title(title, fontsize=16)
    plt.xlabel("t-SNE Dimension 1", fontsize=12)
    plt.ylabel("t-SNE Dimension 2", fontsize=12)
    
    # Move legend outside the plot
    sns.move_legend(
        ax, "upper left",
        bbox_to_anchor=(1, 1),
        title="Cable IDs",
        frameon=True
    )
    
    # Adjust layout to make room for the legend
    plt.tight_layout()
    
    # Save or display the plot
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        console.print(f"Plot saved to {output_path}", style="bold green")
    else:
        plt.show()
        console.print("Plot displayed", style="bold green")
