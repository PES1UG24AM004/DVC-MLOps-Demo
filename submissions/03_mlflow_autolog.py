"""
PES University - Department of Computer Science
Course: Software Engineering Lab (Sem 5)
Student Name: Aarav Yuval B G | SRN: PES1UG24AM004
Topic: Part 3 - MLflow Autologging with Scikit-Learn
"""

import os
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"
import mlflow
import mlflow.sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# 1. Experiment Setup
mlflow.set_experiment("MLflow_Quickstart")

# 2. Dataset Preparation
X, y = datasets.load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Enable MLflow Autologging
mlflow.sklearn.autolog()

# 4. Train Model (Parameters, Metrics, and Artifacts logged automatically)
with mlflow.start_run() as run:
    lr = LogisticRegression(solver="lbfgs", max_iter=1000)
    lr.fit(X_train, y_train)
    print(f"MLflow Autolog Run Completed. Run ID: {run.info.run_id}")
