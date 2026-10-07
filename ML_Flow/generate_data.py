import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
import os

def generate_dataset(output_path="data/train.csv", n_samples=1000):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Generate synthetic dataset for classification
    X, y = make_classification(
        n_samples=n_samples, 
        n_features=10, 
        n_informative=5, 
        n_redundant=2, 
        random_state=42
    )
    
    # Create DataFrame
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
    df["target"] = y
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Dataset generated at {output_path} with {n_samples} samples.")

if __name__ == "__main__":
    generate_dataset()
