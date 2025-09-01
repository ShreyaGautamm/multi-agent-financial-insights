import numpy as np

def zscore(series):
    s = series.astype(float)
    m = float(np.nanmean(s))
    sd = float(np.nanstd(s))
    if sd == 0.0:
        return (s * 0.0)
    return (s - m) / sd

def to_markdown_bullets(items):
    if not items:
        return "• None"
    return "\n".join([f"- {x}" for x in items])
