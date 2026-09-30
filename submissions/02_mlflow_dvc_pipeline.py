"""
PES University - Department of Computer Science
Course: Software Engineering Lab (Sem 5)
Student Name: Aarav Yuval B G | SRN: PES1UG24AM004
Topic: Part 2 - End-to-End MLOps Pipeline (DVC Hash Tracking + MLflow Experiments)
"""

import os
import hashlib
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import mlflow
import mlflow.sklearn

os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

def get_dvc_data_hash(dvc_pointer="ML_Flow/data/train.csv.dvc", raw_file="ML_Flow/data/train.csv"):
    if os.path.exists(dvc_pointer):
        try:
            with open(dvc_pointer) as f:
                return yaml.safe_load(f)["outs"][0]["md5"]
        except Exception:
            pass
    if os.path.exists(raw_file):
        hasher = hashlib.md5()
        with open(raw_file, "rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    return "unknown_hash"

def train_and_track(run_name, n_estimators=100, max_depth=4):
    data_path = "ML_Flow/data/train.csv"
    dvc_hash = get_dvc_data_hash()
    
    df = pd.read_csv(data_path)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    with mlflow.start_run(run_name=run_name) as run:
        # 1. Log DVC Lineage Parameter
        mlflow.log_param("dataset_path", data_path)
        mlflow.log_param("dataset_dvc_hash", dvc_hash)
        
        # 2. Log Model Hyperparameters
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        
        # 3. Fit Model
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)
        
        # 4. Log Evaluation Metrics
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted")
        rec = recall_score(y_test, y_pred, average="weighted")
        
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)
        
        # 5. Log Model Artifact
        mlflow.sklearn.log_model(
            sk_model=model,
            name="random_forest_model",
            serialization_format="cloudpickle"
        )
        
        print(f"[{run_name}] Run ID: {run.info.run_id} | Accuracy: {acc:.4f} | DVC Hash: {dvc_hash}")
        return run.info.run_id

if __name__ == "__main__":
    mlflow.set_experiment("DVC_MLflow_Pipeline")
    print("Executing DVC + MLflow Integrated Runs...")
    r1 = train_and_track("Run_1_Baseline", n_estimators=30, max_depth=2)
    r2 = train_and_track("Run_2_Tuned", n_estimators=120, max_depth=5)
    print("\nExperiments successfully logged to MLflow!")
