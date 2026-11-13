#!/usr/bin/env python3
"""Reproducible structural audit of the user-supplied syneresis curve CSV.

Run from repository root:
    python LITERATURE/audit_kurvendigitalisierung.py

No kinetic fitting, smoothing, interpolation, filtering, or monotonic correction.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "DATA" / "raw" / "kurvendigitalisierung.csv"
OUT = ROOT / "DATA" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(SOURCE, sep=";", encoding="utf-8-sig", dtype=str)
required = ["panel", "series", "condition", "time_h",
            "relative_volume_decrease_or_shrinkage", "trace_type"]
if list(df.columns) != required:
    raise ValueError(f"Unexpected columns: {list(df.columns)}")
for col in ("time_h", "relative_volume_decrease_or_shrinkage"):
    df[col] = pd.to_numeric(df[col].str.replace(",", ".", regex=False), errors="raise")
if df[required].isna().any().any():
    raise ValueError("Missing values detected")

df.to_csv(OUT / "kurvendigitalisierung_numeric.csv", index=False, float_format="%.8g")
rows = []
for (panel, series), group in df.groupby(["panel", "series"], sort=True):
    g = group.sort_values("time_h")
    dt = g["time_h"].diff()
    dy = g["relative_volume_decrease_or_shrinkage"].diff()
    rows.append({
        "panel": panel, "series": series, "condition": g["condition"].iloc[0],
        "n_points": len(g), "time_min_h": g["time_h"].min(),
        "time_max_h": g["time_h"].max(), "time_unique": g["time_h"].nunique(),
        "nonpositive_time_steps": int((dt.dropna() <= 0).sum()),
        "negative_shrinkage_steps": int((dy.dropna() < -1e-10).sum()),
        "largest_negative_shrinkage_step": float(dy.min()),
        "shrinkage_min": g["relative_volume_decrease_or_shrinkage"].min(),
        "shrinkage_max": g["relative_volume_decrease_or_shrinkage"].max(),
        "trace_type": g["trace_type"].iloc[0],
    })
audit = pd.DataFrame(rows)
audit.to_csv(OUT / "kurvendigitalisierung_series_audit.csv", index=False, float_format="%.8g")
print(f"Rows: {len(df)}; curves: {len(audit)}")
print(f"Negative y steps: {int(audit.negative_shrinkage_steps.sum())}")
print(f"Curves with negative y steps: {(audit.negative_shrinkage_steps > 0).sum()}/{len(audit)}")
