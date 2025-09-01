from llm import get_hf_llm
from prompts import REGULATORY_RISK_PROMPT
from tools import get_recent_news

def run_regulatory_agent(ticker, profile_text, scenario, hf_token):
    headlines = get_recent_news(ticker, limit=8)
    news_blob = "\n".join(headlines) if headlines else "No recent headlines."
    prompt = REGULATORY_RISK_PROMPT.format(
        ticker=ticker,
        profile=profile_text,
        scenario=scenario,
        news=news_blob
    )
    # Try multiple LLMs until one works
    models = ["microsoft/DialoGPT-medium", "gpt2", "google/flan-t5-base"]
    last_exception = None
    for model in models:
        try:
            llm = get_hf_llm(hf_token)
            llm.repo_id = model      
            return llm.invoke(prompt)
        except Exception as e:
            last_exception = e
    # Final fallback: template report
    return f"""
## Regulatory Risk Analysis for {ticker}

**Scenario:** {scenario}

• Market volatility exposure  
• Compliance and legal review needs  
• Sector‐specific regulatory changes  

**Severity:** Medium (6/10)  

**Recommendations:**  
– Monitor official filings  
– Track regulators’ announcements  
– Review quarterly compliance disclosures  
*Note: Fallback template used due to upstream errors.*
"""

