import pandas as pd
from tools import get_price_history

def run_competitor_agent(tickers, period="6mo", interval="1d"):
    frames = []
    for tk in tickers:
        df = get_price_history(tk, period, interval)
        if df is None or df.empty:
            continue
        
        # Fix: Use .name attribute to rename the Series
        ret = (df["Close"]/df["Close"].iloc[0]-1)
        ret.name = tk  # This is the correct way to rename a Series
        frames.append(ret)
    
    if not frames:
        return None, "No sufficient data."
    
    bench = pd.concat(frames, axis=1).ffill().iloc[-1:].T.reset_index()
    bench.columns = ["Ticker", "Cumulative Return"]
    bench["Cumulative Return"] = (bench["Cumulative Return"]*100).round(2)
    return bench, "Cumulative returns over selected period."


