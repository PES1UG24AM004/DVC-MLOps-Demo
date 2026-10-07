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

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_dvc_data_version(raw_data_path="data/train.csv"):
    # Computing md5 of raw file since we use dvc pipeline instead of dvc add
    hasher = hashlib.md5()
    with open(raw_data_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def run_experiment(run_name, n_estimators, max_depth, data_path, dvc_version):
    df = pd.read_csv(data_path)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    print(f"\n=======================================================")
    print(f"Starting {run_name}")
    print(f"Tracked DVC Dataset Version (MD5): {dvc_version}")
    print(f"=======================================================")
    
    with mlflow.start_run(run_name=run_name) as run:
        mlflow.log_param("dataset_path", data_path)
        mlflow.log_param("dataset_version", dvc_version)
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted")
        rec = recall_score(y_test, y_pred, average="weighted")
        
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)
        
        # Throw detailed evaluation output into MLflow as an artifact
        from sklearn.metrics import classification_report
        report = classification_report(y_test, y_pred)
        report_path = f"evaluation_report_{run_name}.txt"
        with open(report_path, "w") as f:
            f.write(f"Model Evaluation Report: {run_name}\n")
            f.write("=========================================\n")
            f.write(report)
        mlflow.log_artifact(report_path)
        
        mlflow.sklearn.log_model(
            sk_model=model,
            name="random_forest_model",
            serialization_format="cloudpickle"
        )
        
        print(f"Run ID: {run.info.run_id}")
        print(f"Results -> Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f}")
        return run.info.run_id

if __name__ == "__main__":
    config = load_config()
    
    data_path = config["data"]["output_path"]
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}. Run generate_data.py first.")
        
    dvc_version = get_dvc_data_version(data_path)
    
    mlflow.set_experiment(config["train"]["experiment_name"])
    
    for run_config in config["train"]["runs"]:
        run_experiment(
            run_name=run_config["run_name"],
            n_estimators=run_config["n_estimators"],
            max_depth=run_config["max_depth"],
            data_path=data_path,
            dvc_version=dvc_version
        )
        
    print("\n--- Summary ---")
    print(f"Experiment: {config['train']['experiment_name']}")
    print(f"To launch the MLflow UI and view experiments side-by-side, run:")
    print(f"  mlflow ui --port 5000")
