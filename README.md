# 📊 Multi-Agent Financial Insights Platform

A **Streamlit application** that orchestrates multiple specialized AI agents to deliver **comprehensive financial insights** for any stock ticker.  
Get real-time forecasts, sentiment analysis, anomaly detection, regulatory risk assessment, competitor benchmarking, and an executive summary—all in one place.

---

## 🚀 Features

| Agent | Description |
|-------|-------------|
| 📈 **Price Prediction Agent** | Uses historical closing prices to fit a log-linear trend and forecast the next 30 days under various scenarios. |
| 🚨 **Anomaly Detection Agent** | Flags volume or return outliers where the Z-score exceeds ±2.5. |
| 🗣️ **Sentiment Analysis Agent** | Applies **FinBERT** on recent news headlines to compute a sentiment score between –1 and +1. |
| ⚖️ **Regulatory Risk Agent** | Summarizes potential regulatory, compliance, or legal risks using a Hugging Face LLM based on company profile and news. |
| 🏢 **Competitor Benchmark Agent** | Fetches peer tickers’ price history and computes cumulative returns for performance comparison. |
| 🧾 **Coordinator Agent** | Synthesizes all outputs into an executive-ready market brief with key takeaways, recommendations, and “what to watch” items. |

---

## 🛠 Tools & Technologies

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) 
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/) 
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFDE2A?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/) 
[![Transformers](https://img.shields.io/badge/Transformers-00FF00?style=for-the-badge&logo=transformers&logoColor=black)](https://huggingface.co/docs/transformers/index) 
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/) 
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/) 
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/) 
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://matplotlib.org/) 
[![FinBERT](https://img.shields.io/badge/FinBERT-00FF00?style=for-the-badge)](https://huggingface.co/ProsusAI/finbert) 

---
## 🌟 Highlights
- **Multi-agent orchestration**: Each agent specializes in a market theme.  
- **Real-world datasets**: Integrates Yahoo Finance, FinBERT sentiment, regulatory filings.  
- **Executive-ready dashboard**: Synthesizes outputs into actionable insights.  
- **Scenario analysis**: Test different market conditions and risk projections in real time.  

**Empower your financial analysis workflow with AI-driven insights, all in one interactive dashboard!**

---
## 🎮 Checkout the deployed app on Streamlit 👉🏻 [here](https://multi-agent-financial-insights.streamlit.app/?embed_options=show_toolbar,show_padding,show_footer,light_theme,show_colored_line)
