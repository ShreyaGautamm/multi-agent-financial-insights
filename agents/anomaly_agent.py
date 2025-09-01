import pandas as pd
import numpy as np

def zscore(series):
    m = np.nanmean(series)
    s = np.nanstd(series)
    return (series - m)/s if s != 0 else series*0

def run_anomaly_agent(hist: pd.DataFrame):
    if hist is None or hist.empty:
        return None, "No data for anomalies."
    df = hist.copy()
    df["Return"] = df["Close"].pct_change()
    df["VolZ"] = zscore(df["Volume"])
    df["RetZ"] = zscore(df["Return"].fillna(0))
    df["Anomaly"] = (df["VolZ"].abs()>2.5)|(df["RetZ"].abs()>2.5)
    return df, "Anomalies flagged where |Z|>2.5 on volume or returns."

