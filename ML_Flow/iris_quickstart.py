import mlflow
import mlflow.sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# 1. Initialize experiment
mlflow.set_experiment("MLflow_Quickstart")

# 2. Prepare Data
X, y = datasets.load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Define hyperparameters
params = {"solver": "lbfgs", "max_iter": 1000}
lr = LogisticRegression(**params)

# 4. Track with MLflow Autologging
mlflow.sklearn.autolog()

with mlflow.start_run() as run:
    lr.fit(X_train, y_train)
    run_id = run.info.run_id
    print(f"Run ID: {run_id}")
    print("Model and metrics logged automatically!")

# 5. Load the Model back for Inference
print("\nLoading model from MLflow artifact store for inference test...")
model_uri = f"runs:/{run_id}/model"
loaded_model = mlflow.sklearn.load_model(model_uri)
sample_predictions = loaded_model.predict(X_test[:5])
print(f"Predictions on 5 test samples: {sample_predictions}")
print(f"Actual labels for 5 test samples: {y_test[:5]}")
