"""
PES University - Department of Computer Science
Course: Software Engineering Lab (Sem 5)
Student Name: Aarav Yuval B G | SRN: PES1UG24AM004
Topic: Part 4 - Explicit MLflow Tracking on Wine Dataset
"""

import os
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

mlflow.set_experiment("Wine_Classification_Tracking")

data = load_wine()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.3, random_state=42)

with mlflow.start_run(run_name="Wine_RandomForest_Run") as run:
    n_estimators = 100
    max_depth = 3
    
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    
    # Explicit logging
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)
    
    mlflow.sklearn.log_model(model, name="random_forest_model", serialization_format="cloudpickle")
    
    print(f"Wine Run Completed. Run ID: {run.info.run_id} | Accuracy: {accuracy:.4f}")
