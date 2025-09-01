from agents.price_prediction_agent import run_price_prediction_agent
from agents.anomaly_agent import run_anomaly_agent
from agents.sentiment_agent import run_sentiment_agent
from agents.regulatory_agent import run_regulatory_agent
from agents.competitor_agent import run_competitor_agent
from agents.coordinator_agent import run_coordinator_agent

def run_all_agents(hist, ticker, scenario, headlines, profile_text, peers, hf_token):
    forecast_df, forecast_note = run_price_prediction_agent(hist, scenario)
    anom_df, anom_note = run_anomaly_agent(hist)
    sentiment = run_sentiment_agent(headlines)
    regulatory = run_regulatory_agent(ticker, profile_text, scenario, hf_token)
    benchmark, bench_note = run_competitor_agent([ticker]+peers)

    coordinator_summary = run_coordinator_agent(
        ticker=ticker,
        scenario=scenario,
        forecast_note=forecast_note,
        anom_note=anom_note,
        sentiment=sentiment,
        regulatory=regulatory,
        benchmark_table=benchmark.to_markdown(index=False) if benchmark is not None else "",
        hf_token=hf_token
    )

    return {
        "forecast_df": forecast_df,
        "forecast_note": forecast_note,
        "anom_df": anom_df,
        "anom_note": anom_note,
        "sentiment": sentiment,
        "regulatory": regulatory,
        "benchmark": benchmark,
        "bench_note": bench_note,
        "coordinator_summary": coordinator_summary
    }
