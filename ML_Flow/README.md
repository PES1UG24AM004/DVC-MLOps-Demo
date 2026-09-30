# MLflow & DVC Integration Demo

## Overview
This directory demonstrates the end-to-end MLOps lifecycle combining **DVC** (data versioning) and **MLflow** (experiment tracking, model packaging, and inference).

### Core Synergy
- **DVC (Data Version Control):** Manages the physical dataset (`data/train.csv`) without cluttering Git. Creates lightweight pointer `train.csv.dvc`.
- **MLflow:** Acts as the experiment notebook, tracking parameters (including the DVC dataset MD5 hash), metrics (accuracy, precision, recall), and serializing trained model artifacts.

---

## Directory Structure
- `data/train.csv`: Training dataset (ignored by Git, tracked by DVC).
- `data/train.csv.dvc`: Lightweight DVC metadata pointer (tracked by Git).
- `train_dvc_mlflow.py`: Main integration script linking DVC data MD5 hash to MLflow runs.
- `iris_quickstart.py`: Implements MLflow autologging (`mlflow.sklearn.autolog()`).
- `wine.py`: Implements explicit metric, parameter, and model artifact logging.
- `test_inference.py`: Demonstrates loading a trained model from MLflow storage by run ID and running live predictions.

---

## Quickstart Commands

1. **Run DVC + MLflow Pipeline:**
   ```powershell
   python train_dvc_mlflow.py
   ```

2. **Run Autologging Demo:**
   ```powershell
   python iris_quickstart.py
   ```

3. **Run Wine Classifier Demo:**
   ```powershell
   python wine.py
   ```

4. **Test Live Inference from Stored Model:**
   ```powershell
   python test_inference.py
   ```

5. **Launch MLflow UI (Web Dashboard):**
   ```powershell
   mlflow ui --port 5000
   ```
   Open `http://localhost:5000` in your web browser.
