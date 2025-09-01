from typing import List, Optional, Dict
import datetime as dt
import pandas as pd
import yfinance as yf

def safe_ticker(t: str) -> bool:
    return len(t) <= 8 and t.isalnum()

def get_price_history(ticker: str, period: str = "6mo", interval: str = "1d") -> Optional[pd.DataFrame]:
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
        if isinstance(df, pd.DataFrame) and not df.empty:
            return df
        return None
    except Exception:
        return None

def get_company_profile(ticker: str) -> Optional[Dict]:
    try:
        tk = yf.Ticker(ticker)
        info = tk.get_info() if hasattr(tk, "get_info") else tk.info  # yfinance version differences
        return info if isinstance(info, dict) else None
    except Exception:
        return None

# --- News utility via DuckDuckGo (no API key) ---
def get_recent_news(query: str, limit: int = 10) -> List[str]:
    """
    Lightweight headline fetcher using duckduckgo-search package (no key).
    Returns just the titles / snippets to keep it simple.
    """
    try:
        from duckduckgo_search import DDGS
        items = []
        with DDGS() as ddgs:
            for r in ddgs.news(keywords=query, max_results=limit):
                title = r.get("title") or ""
                source = r.get("source") or ""
                date = r.get("date") or ""
                if title:
                    items.append(f"{title} ({source}, {date})")
        return items[:limit]
    except Exception:
        return []
