import os, sys, logging, traceback
from datetime import datetime
import numpy as np
import pandas as pd
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(WORK_DIR, '03_data')
RESULT_DIR = os.path.join(WORK_DIR, '07_results')
LOG_DIR = os.path.join(WORK_DIR, '10_ai_logs')
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOG_DIR, 'Q1_run.log'), filemode='w', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def main():
    logging.info('Q1 codegen started')
    try:
        data_path = os.path.join(DATA_DIR, 'Q1_time_series.csv')
        if os.path.exists(data_path):
            logging.info('Loading data from %s', data_path)
            df = pd.read_csv(data_path, parse_dates=['date'], index_col='date')
            ts = df['value'].astype(float)
        else:
            logging.warning('Data not found, generating synthetic data')
            dates = pd.date_range('2020-01-01', periods=200, freq='D')
            trend = np.linspace(10, 20, 200)
            season = 3 * np.sin(2 * np.pi * np.arange(200) / 30)
            noise = np.random.normal(0, 1.5, 200)
            ts = pd.Series(trend + season + noise, index=dates)
        split_idx = int(len(ts) * 0.9)
        train, test = ts.iloc[:split_idx], ts.iloc[split_idx:]
        from statsmodels.tsa.arima.model import ARIMA
        order = (1, 1, 1)
        model = ARIMA(train, order=order)
        fit = model.fit()
        logging.info('Model fitted, AIC=%.3f', fit.aic)
        forecast = fit.forecast(steps=len(test))
        forecast = pd.Series(forecast, index=test.index)
        out_df = pd.DataFrame({'date': forecast.index.strftime('%Y-%m-%d'), 'actual': test.values, 'forecast': forecast.values, 'residual': test.values - forecast.values})
        out_path = os.path.join(RESULT_DIR, 'Q1_candidate_forecasts.csv')
        out_df.to_csv(out_path, index=False)
        logging.info('Forecasts saved to %s', out_path)
        mae = np.mean(np.abs(out_df['residual']))
        rmse = np.sqrt(np.mean(out_df['residual']**2))
        metrics = {'model': 'ARIMA(1,1,1)', 'random_seed': RANDOM_SEED, 'mae': mae, 'rmse': rmse, 'aic': fit.aic, 'execution_time': datetime.now().isoformat()}
        mdf = pd.DataFrame([metrics])
        m_path = os.path.join(RESULT_DIR, 'Q1_candidate_metrics.csv')
        mdf.to_csv(m_path, index=False)
        logging.info('Metrics saved: MAE=%.4f, RMSE=%.4f', mae, rmse)
        logging.info('Q1 codegen finished')
        return 0
    except Exception as e:
        logging.error('Execution failed: %s', e)
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
