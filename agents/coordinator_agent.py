from llm import get_hf_llm
from prompts import COORDINATOR_PROMPT

def run_coordinator_agent(
    ticker: str,
    scenario: str,
    forecast_note: str,
    anom_note: str,
    sentiment: dict,
    regulatory: str,
    benchmark_table: str,
    hf_token: str
) -> str:
    sentiment_score = f"{sentiment.get('score',0.0):.2f}"
    sentiment_examples = "\n".join(f"- {h}" for h in sentiment.get("headlines",[])[:6])

    prompt = COORDINATOR_PROMPT.format(
        ticker=ticker,
        scenario=scenario,
        forecast_note=forecast_note,
        anomaly_note=anom_note,
        sentiment_score=sentiment_score,
        sentiment_examples=sentiment_examples,
        regulatory_report=regulatory,
        benchmark_table=benchmark_table or "N/A"
    )
    # Attempt with multiple models
    models = ["microsoft/DialoGPT-medium", "gpt2", "google/flan-t5-base"]
    for model in models:
        try:
            llm = get_hf_llm(hf_token)
            llm.repo_id = model
            return llm.invoke(prompt)
        except Exception:
            continue

    # Fallback summary
    return f"""
## Executive Summary for {ticker}

• **Scenario**: {scenario}  
• **Forecast**: {forecast_note}  
• **Anomalies**: {anom_note}  
• **Sentiment**: {sentiment_score}  
• **Benchmark**: See tab  

**Recommendation:** Monitor earnings, regulatory updates, and sentiment shifts.  

**What to Watch (30–90 days):**  
1. Quarterly reports  
2. Regulatory announcements  
3. Competitor moves  
*Template summary due to model errors.*
"""

