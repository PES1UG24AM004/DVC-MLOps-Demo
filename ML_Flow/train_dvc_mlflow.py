import os
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

import hashlib
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import mlflow
import mlflow.sklearn

def get_dvc_data_version(dvc_pointer_path="data/train.csv.dvc", raw_data_path="data/train.csv"):
    """
    Retrieve the DVC version (MD5 hash) of the dataset.
    Reads from the .dvc pointer file created by 'dvc add',
    falling back to computing MD5 directly if the pointer is missing.
    """
    if os.path.exists(dvc_pointer_path):
        try:
            with open(dvc_pointer_path, "r") as f:
                dvc_meta = yaml.safe_load(f)
                return dvc_meta["outs"][0]["md5"]
        except Exception:
            pass
    # Fallback to computing md5 of raw file
    hasher = hashlib.md5()
    with open(raw_data_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def run_experiment(run_name, n_estimators, max_depth):
    # 1. Load dataset tracked by DVC
    data_path = "data/train.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Tracked data file not found at {data_path}. Ensure 'dvc pull' or generation ran.")
    
    df = pd.read_csv(data_path)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    # 2. Retrieve DVC data version hash
    dvc_version = get_dvc_data_version("data/train.csv.dvc", data_path)
    print(f"\n=======================================================")
    print(f"Starting {run_name}")
    print(f"Tracked DVC Dataset Version (MD5): {dvc_version}")
    print(f"=======================================================")
    
    # 3. Start MLflow Run
    with mlflow.start_run(run_name=run_name) as run:
        # A. Log DVC data lineage
        mlflow.log_param("dataset_path", data_path)
        mlflow.log_param("dataset_version", dvc_version)
        
        # B. Log Hyperparameters
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", 42)
        
        # C. Train Model
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # D. Evaluate Metrics
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted")
        rec = recall_score(y_test, y_pred, average="weighted")
        
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)
        
        # E. Log Model Artifact
        mlflow.sklearn.log_model(
            sk_model=model,
            name="random_forest_model",
            serialization_format="cloudpickle"
        )
        
        print(f"Run ID: {run.info.run_id}")
        print(f"Results -> Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f}")
        print("Model and parameters successfully tracked in MLflow!")
        return run.info.run_id

if __name__ == "__main__":
    mlflow.set_experiment("DVC_MLflow_Pipeline")
    
    # Run 1: Baseline configuration
    run_1_id = run_experiment(run_name="Run_1_Baseline", n_estimators=30, max_depth=2)
    
    # Run 2: Tuned configuration
    run_2_id = run_experiment(run_name="Run_2_Tuned", n_estimators=100, max_depth=5)
    
    print("\n--- Summary ---")
    print(f"Experiment: DVC_MLflow_Pipeline")
    print(f"To launch the MLflow UI and view experiments side-by-side, run:")
    print(f"  mlflow ui --port 5000")
