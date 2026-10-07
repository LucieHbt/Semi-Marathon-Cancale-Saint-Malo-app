"""Transforme results_all.xlsx (une feuille = une édition) en data/resultats.csv."""
import datetime as dt
import sys

import pandas as pd

src = sys.argv[1] if len(sys.argv) > 1 else "data/results_all.xlsx"


def to_seconds(v):
    if isinstance(v, (dt.time, dt.datetime)):
        return v.hour * 3600 + v.minute * 60 + v.second
    if isinstance(v, dt.timedelta):
        return v.total_seconds()
    if isinstance(v, str):
        p = v.strip().split(":")
        if len(p) == 3 and all(q.isdigit() for q in p):
            return int(p[0]) * 3600 + int(p[1]) * 60 + int(p[2])
    return float("nan")  # DNF, vide...


frames = []
x = pd.ExcelFile(src)
for sheet in x.sheet_names:
    d = x.parse(sheet)
    out = pd.DataFrame({
        "Annee": int(sheet),
        "Nom": d["Nom"].astype(str).str.replace("\xa0", " ").str.strip(),
        "Club": d["Club"].astype(str).replace("nan", "").str.strip(),
        "Sx": d["Sx"].astype(str).str.strip(),
        "Cat": d["Cat"].astype(str).replace("nan", "").str.strip(),
        "Temps_s": d["Temps pistolet"].map(to_seconds),
    })
    frames.append(out)
df = pd.concat(frames, ignore_index=True)
df.to_csv("data/resultats.csv", index=False)
print(df.groupby("Annee").agg(coureurs=("Nom", "size"), arrivants=("Temps_s", "count")))
