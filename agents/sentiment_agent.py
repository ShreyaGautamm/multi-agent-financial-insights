from transformers import pipeline
import numpy as np

def run_sentiment_agent(headlines):
    if not headlines:
        return {"score":0.0, "headlines":["No headlines."]}
    clf = pipeline("text-classification", model="ProsusAI/finbert")
    scores = []
    annotated = []
    for h in headlines:
        pred = clf(h[:512])[0]
        label = pred["label"].lower()
        score_map = {"positive":1,"neutral":0,"negative":-1}
        mapped = score_map.get(label,0)*pred["score"]
        scores.append(mapped)
        annotated.append(f"{h} — {label} ({pred['score']:.2f})")
    avg = float(np.mean(scores))
    return {"score":avg, "headlines":annotated}
