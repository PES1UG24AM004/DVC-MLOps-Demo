import os
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris

print("Querying MLflow for latest model in experiment 'DVC_MLflow_Pipeline'...")
client = mlflow.tracking.MlflowClient()
experiment = client.get_experiment_by_name("DVC_MLflow_Pipeline")

if not experiment:
    print("Experiment 'DVC_MLflow_Pipeline' not found. Run train_dvc_mlflow.py first.")
    exit(1)

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time DESC"],
    max_results=1
)

latest_run = runs[0]
run_id = latest_run.info.run_id
print(f"Latest Run Name: {latest_run.data.tags.get('mlflow.runName')}")
print(f"Run ID: {run_id}")
print(f"Dataset Version (DVC MD5): {latest_run.data.params.get('dataset_version')}")
print(f"Logged Accuracy: {latest_run.data.metrics.get('accuracy'):.4f}")

# Load model from MLflow run
model_uri = f"runs:/{run_id}/random_forest_model"
model = mlflow.sklearn.load_model(model_uri)

# Test prediction
iris = load_iris()
sample = [iris.data[0], iris.data[60], iris.data[120]] # One sample from each class
predictions = model.predict(sample)
predicted_classes = [iris.target_names[p] for p in predictions]

print("\n--- Live Inference Test ---")
for i, (feat, pred_name) in enumerate(zip(sample, predicted_classes)):
    print(f"Sample {i+1} Features: {feat} -> Predicted Class: {pred_name}")
print("\nInference successful! Model loaded and executed from MLflow storage.")
