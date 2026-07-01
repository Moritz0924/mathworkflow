"""
Q1 Solution Script
Problem: Student Score Prediction (placeholder, must match actual problem)
Model: Multiple Linear Regression (as per model_route.md, if approved)
Data: 03_data/student_scores.csv (assumed, adjust to actual data path)
Random seed: 42 (deterministic)
Run ID: run-20240604-001
Author: Codex codegen stage (simulated training)
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import logging
import sys
import time
import os

# Configuration
RANDOM_SEED = 42
DATA_PATH = '03_data/student_scores.csv'
LOG_PATH = '06_code/Q1_run.log'
MODEL_OUTPUT = '06_code/Q1_model.pkl'
RESULTS_OUTPUT = '07_results/Q1_candidate_results.csv'

# Setup logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def main():
    run_id = "run-20240604-001"
    logging.info(f"Run ID: {run_id}")
    logging.info("Q1 solution script started.")
    
    # Check data existence
    if not os.path.exists(DATA_PATH):
        logging.error(f"Data file not found: {DATA_PATH}")
        sys.exit(1)
    
    try:
        # Load data
        df = pd.read_csv(DATA_PATH)
        logging.info(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        logging.info(f"Columns: {list(df.columns)}")
        
        # Basic cleaning: drop rows with missing target
        df = df.dropna(subset=['final_score'])
        # Features (assumed based on model_route)
        features = ['study_hours', 'previous_score', 'absences']
        target = 'final_score'
        # Verify features exist
        for f in features:
            if f not in df.columns:
                logging.error(f"Feature missing: {f}")
                sys.exit(1)
        
        # Fill missing features with median
        for f in features:
            if df[f].isnull().any():
                median_val = df[f].median()
                df[f].fillna(median_val, inplace=True)
                logging.info(f"Filled missing values in {f} with median {median_val}")
        
        X = df[features]
        y = df[target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=RANDOM_SEED
        )
        logging.info(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
        
        # Model training
        model = LinearRegression()
        model.fit(X_train, y_train)
        logging.info("Model training completed.")
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        logging.info(f"MSE: {mse:.4f}")
        logging.info(f"RMSE: {rmse:.4f}")
        logging.info(f"R2: {r2:.4f}")
        
        # Save model
        joblib.dump(model, MODEL_OUTPUT)
        logging.info(f"Model saved to {MODEL_OUTPUT}")
        
        # Save results
        results_df = pd.DataFrame({
            'y_test': y_test.values,
            'y_pred': y_pred
        })
        results_df.to_csv(RESULTS_OUTPUT, index=False)
        logging.info(f"Results saved to {RESULTS_OUTPUT}")
        
        # Store run metadata (for contract)
        metadata = {
            'run_id': run_id,
            'code_file': os.path.basename(__file__),
            'data_file': DATA_PATH,
            'model': 'LinearRegression',
            'random_seed': RANDOM_SEED,
            'features': features,
            'target': target,
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        }
        # Write metadata to a log file or stdout
        with open('07_results/Q1_run_metadata.txt', 'w') as f:
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")
        
        logging.info("Q1 script finished successfully.")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
