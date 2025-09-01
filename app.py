import streamlit as st
import pandas as pd
import time
from dotenv import load_dotenv
import os

from tools import get_price_history, get_company_profile, get_recent_news, safe_ticker
from utils import to_markdown_bullets
from orchestrator_agent import run_all_agents

# Load .env for HF_TOKEN
load_dotenv()
HF_TOKEN = os.getenv("HF_API_KEY")

st.set_page_config(page_title="📊 Multi-Agent Financial Insights", layout="wide", page_icon="💹")
st.title("📊 Multi-Agent Financial Insights Platform")
st.caption("Powered by LangChain + Hugging Face (Mistral) | Streamlit")

# --- Sidebar Inputs --- #
with st.sidebar:
    st.header("🔧 Controls")
    ticker = st.text_input("Ticker (e.g., AAPL, TSLA, NVDA):", value="AAPL").upper().strip()
    period = st.selectbox("Price History Period", ["1mo","3mo","6mo","1y","2y"], index=2)
    interval = st.selectbox("Interval", ["1d","1wk"], index=0)
    peers_str = st.text_input("Competitor tickers (comma-separated)", value="MSFT, GOOGL, AMZN")
    scenario = st.selectbox("What-if scenario", [
        "Baseline",
        "Interest rates +50bps",
        "Earnings miss next quarter",
        "Supply chain disruption",
        "New regulation on the sector"
    ])
    run_btn = st.button("🚀 Run Analysis")

# Guard for invalid ticker
if not ticker or not safe_ticker(ticker):
    st.stop()

# --- Load Historical Prices & Company Profile --- #
@st.cache_data
def load_data(ticker, period, interval):
    return get_price_history(ticker, period, interval), get_company_profile(ticker), get_recent_news(ticker, limit=12)

hist, profile, headlines = load_data(ticker, period, interval)

# Layout columns
price_col, profile_col = st.columns([2,1])

with price_col:
    st.subheader(f"Price History — {ticker}")
    if hist is not None and not hist.empty:
        st.line_chart(hist["Close"])
    else:
        st.error("No historical price data found.")

with profile_col:
    st.subheader("Company Snapshot")
    if profile:
        st.write({
            "Name": profile.get("shortName"),
            "Sector": profile.get("sector"),
            "Industry": profile.get("industry"),
            "Market Cap": profile.get("marketCap"),
            "Website": profile.get("website")
        })
    else:
        st.info("No profile metadata available.")

st.markdown("---")

# --- Run Multi-Agent Orchestrator --- #
if run_btn:
    start = time.time()
    peers = [p.strip().upper() for p in peers_str.split(",") if p.strip()]

    with st.spinner("Running all agents…"):
        results = run_all_agents(hist, ticker, scenario, headlines, str(profile), peers, HF_TOKEN)

    # Create all tabs in a single call
    tab_forecast, tab_anom, tab_sent, tab_reg, tab_bench, tab_coordinator = st.tabs([
        "📈 Forecast", "🚨 Anomalies", "🗣️ Sentiment", "⚖️ Regulatory Risk", "🏢 Competitor Benchmark", "🧾 Executive Summary"
    ])

    # Forecast Tab
    with tab_forecast:
        forecast_df = results["forecast_df"]
        st.write(results["forecast_note"])
        if forecast_df is not None and not forecast_df.empty:
            st.line_chart(forecast_df)

    # Anomalies Tab
    with tab_anom:
        st.write(results["anom_note"])
        anom_df = results["anom_df"]
        if anom_df is not None:
            st.dataframe(anom_df.tail(20))

    # Sentiment Tab
    with tab_sent:
        sent = results["sentiment"]
        st.metric("Sentiment Score (-1 to 1)", f"{sent['score']:.2f}")
        st.write("Recent Headlines:")
        st.markdown(to_markdown_bullets(sent["headlines"]))
        st.caption("FinBERT via Hugging Face")

    # Regulatory Tab
    with tab_reg:
        st.markdown(results["regulatory"])

    # Benchmark Tab
    with tab_bench:
        bench_df = results["benchmark"]
        st.write(results["bench_note"])
        if bench_df is not None:
            st.dataframe(bench_df)

    # Coordinator Tab
    with tab_coordinator:
        summary = results.get("coordinator_summary", "")
        if summary:
            st.markdown(summary)
        else:
            st.info("Coordinator summary not available.")

    st.success(f"Analysis completed in {time.time()-start:.1f}s")
else:
    st.info("Set your inputs in the sidebar and click **Run Analysis** to generate insights.")
