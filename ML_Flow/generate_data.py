import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
import yaml
import os

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def generate_dataset():
    config = load_config()
    data_config = config["data"]
    output_path = data_config["output_path"]
    n_samples = data_config["n_samples"]
    n_features = data_config["n_features"]
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Generate synthetic dataset for classification
    X, y = make_classification(
        n_samples=n_samples, 
        n_features=n_features, 
        n_informative=5, 
        n_redundant=2, 
        random_state=data_config["random_state"]
    )
    
    # Create DataFrame
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(n_features)])
    df["target"] = y
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Dataset generated at {output_path} with {n_samples} samples and {n_features} features.")

if __name__ == "__main__":
    generate_dataset()
