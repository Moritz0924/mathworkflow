'''
Q1: Drought Adaptation Model - Linear Regression Baseline
Implements model route: OLS regression on plant traits.
Random seed: 42 (deterministic after seed).
Dependencies: pandas, numpy, scikit-learn
'''
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import logging
from pathlib import Path
log_dir = Path('10_ai_logs')
log_dir.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=log_dir/'run_q1.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
def main():
    logger.info('Q1 codegen started.')
    np.random.seed(42)
    logger.info('Random seed set to 42.')
    data_path = Path('03_data/drought_data.csv')
    if not data_path.exists():
        logger.warning('Data file not found. Generating synthetic data.')
        n_samples = 500
        np.random.seed(42)
        trait1 = np.random.normal(0, 1, n_samples)
        trait2 = np.random.normal(0, 1, n_samples)
        drought_res = 0.3*trait1 - 0.1*trait2 + np.random.normal(0, 0.1, n_samples)
        df = pd.DataFrame({'trait1': trait1, 'trait2': trait2, 'drought_resistance': drought_res})
        logger.info(f'Generated synthetic data: {df.shape}')
    else:
        df = pd.read_csv(data_path)
        logger.info(f'Loaded data: {df.shape}')
    X = df[['trait1', 'trait2']].values
    y = df['drought_resistance'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    logger.info(f'Model coefficients: {model.coef_}')
    preds = model.predict(X_test)
    results_df = pd.DataFrame({'actual': y_test, 'predicted': preds})
    results_dir = Path('07_results')
    results_dir.mkdir(parents=True, exist_ok=True)
    out_path = results_dir / 'q1_candidate_predictions.csv'
    results_df.to_csv(out_path, index=False)
    logger.info(f'Results saved to {out_path}')
    logger.info('Q1 codegen completed successfully.')
if __name__ == '__main__':
    main()
