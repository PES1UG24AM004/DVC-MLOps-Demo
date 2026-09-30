"""
PES University - Department of Computer Science
Course: Software Engineering Lab (Sem 5)
Student Name: Aarav Yuval B G | SRN: PES1UG24AM004
Topic: Part 5 - Loading Logged Model from MLflow Artifact Store for Inference
"""

import os
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris

client = mlflow.tracking.MlflowClient()
exp = client.get_experiment_by_name("DVC_MLflow_Pipeline")

if not exp:
    print("Experiment 'DVC_MLflow_Pipeline' not found. Run 02_mlflow_dvc_pipeline.py first.")
    exit(1)

runs = client.search_runs(experiment_ids=[exp.experiment_id], order_by=["start_time DESC"], max_results=1)
latest_run_id = runs[0].info.run_id
print(f"Loading Model from MLflow Run ID: {latest_run_id}")

model_uri = f"runs:/{latest_run_id}/random_forest_model"
model = mlflow.sklearn.load_model(model_uri)

# Test with 3 sample vectors
iris = load_iris()
sample_inputs = [iris.data[0], iris.data[55], iris.data[110]]
preds = model.predict(sample_inputs)
pred_labels = [iris.target_names[p] for p in preds]

print("\n--- Live Inference Results ---")
for i, (sample, pred) in enumerate(zip(sample_inputs, pred_labels)):
    print(f"Sample {i+1} {sample} -> Prediction: {pred}")

print("\n[SUCCESS] Model successfully restored and served from MLflow artifacts.")
