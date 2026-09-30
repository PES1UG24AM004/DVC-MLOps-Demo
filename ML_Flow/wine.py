import os
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# 1. Initialize experiment
mlflow.set_experiment("Wine_Classification_Tracking")

# 2. Load dataset
data = load_wine()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 3. Model training with explicit MLflow tracking
with mlflow.start_run(run_name="RandomForest_Wine_Run") as run:
    n_estimators = 100
    max_depth = 3
    
    # Train
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    
    # Log hyperparameters
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("dataset", "Wine (178 samples, 13 features)")
    
    # Predict and log metrics
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model artifact with cloudpickle serialization
    mlflow.sklearn.log_model(
        sk_model=model,
        name="random_forest_model",
        serialization_format="cloudpickle"
    )
    
    print(f"Run ID: {run.info.run_id}")
    print(f"Model trained with accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=data.target_names))
