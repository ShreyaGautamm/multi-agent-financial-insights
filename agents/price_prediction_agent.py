import pandas as pd
import numpy as np

def run_price_prediction_agent(hist: pd.DataFrame, scenario="Baseline"):
    if hist is None or hist.empty:
        return None, "No price data."

    df = hist.copy()
    df["logC"] = np.log(df["Close"])
    x = np.arange(len(df))
    coeffs = np.polyfit(x, df["logC"].values, 1)

    # Forecast future prices
    future_x = np.arange(len(df), len(df) + 30)
    future_trend = coeffs[0] * future_x + coeffs[1]
    forecast_prices = np.exp(future_trend)

    # Create forecast DataFrame
    forecast_dates = pd.date_range(df.index[-1] + pd.Timedelta(1), periods=30)
    forecast_df = pd.DataFrame({
        "Close": [np.nan]*30,
        "Forecast": forecast_prices
    }, index=forecast_dates)

    # Combine historical + forecast
    hist_df = df[["Close"]].copy()
    hist_df["Forecast"] = np.nan
    combined_df = pd.concat([hist_df, forecast_df])

    # Apply scenario adjustment
    scenario_adj = {"Baseline": 0, "Interest rates +50bps": -0.03, "Earnings miss": -0.05}
    adj = scenario_adj.get(scenario, 0.0)
    combined_df["Forecast"] = combined_df["Forecast"].fillna(method="ffill") * (1 + adj)

    note = f"Price forecast with scenario '{scenario}' applied ({adj:+.0%} adjustment)."
    return combined_df, note
