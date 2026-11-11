#!/usr/bin/env python3
"""Transform manually selected figure-marker pixels into calibrated data.

No image processing or automatic marker recognition is attempted. The operator
must supply axis tick calibration points and marker-centre pixels separately.
Supports linear and log10 axes; all calibration is panel-specific.
"""
from __future__ import annotations
import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

CAL_FIELDS = {"figure_panel", "axis", "pixel", "value", "scale"}
POINT_FIELDS = {
    "figure_panel", "point_id", "curve_type", "gel_type", "temperature_C",
    "x_pixel", "y_pixel", "x_pixel_uncertainty", "y_pixel_uncertainty",
    "extraction_confidence", "notes",
}

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader), set(reader.fieldnames or [])

def fit_axis(rows, panel, axis):
    selected = [r for r in rows if r["figure_panel"] == panel and r["axis"] == axis]
    if len(selected) < 2:
        raise ValueError(f"{panel}/{axis}: at least two calibration ticks are required")
    scales = {r["scale"].strip().lower() for r in selected}
    if len(scales) != 1 or not scales <= {"linear", "log10"}:
        raise ValueError(f"{panel}/{axis}: scale must be consistently linear or log10")
    scale = scales.pop()
    px = [float(r["pixel"]) for r in selected]
    vals = [float(r["value"]) for r in selected]
    if scale == "log10":
        if any(v <= 0 for v in vals):
            raise ValueError("log10 axis calibration values must be positive")
        vals = [math.log10(v) for v in vals]
    mean_x, mean_y = sum(px)/len(px), sum(vals)/len(vals)
    denom = sum((x-mean_x)**2 for x in px)
    if denom == 0:
        raise ValueError(f"{panel}/{axis}: calibration pixels must differ")
    slope = sum((x-mean_x)*(y-mean_y) for x,y in zip(px,vals))/denom
    intercept = mean_y - slope*mean_x
    return slope, intercept, scale

def convert(pixel, pixel_unc, model):
    slope, intercept, scale = model
    transformed = intercept + slope*pixel
    value = 10**transformed if scale == "log10" else transformed
    deriv = abs(slope) * (math.log(10)*value if scale == "log10" else 1.0)
    return value, deriv*pixel_unc

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--calibration", required=True, type=Path)
    p.add_argument("--pixels", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    cal, cal_fields = read_csv(args.calibration)
    points, point_fields = read_csv(args.pixels)
    if not CAL_FIELDS <= cal_fields:
        raise SystemExit(f"Calibration CSV missing columns: {sorted(CAL_FIELDS-cal_fields)}")
    if not POINT_FIELDS <= point_fields:
        raise SystemExit(f"Pixel CSV missing columns: {sorted(POINT_FIELDS-point_fields)}")
    panels = sorted({r["figure_panel"] for r in points})
    models = {}
    for panel in panels:
        models[(panel,"x")] = fit_axis(cal,panel,"x")
        models[(panel,"y")] = fit_axis(cal,panel,"y")
    out_fields = [
        "figure_panel","point_id","curve_type","gel_type","temperature_C",
        "x_pixel","y_pixel","time_h","relative_volume_decrease",
        "x_pixel_uncertainty","y_pixel_uncertainty","time_h_uncertainty",
        "relative_volume_decrease_uncertainty","extraction_confidence","notes",
    ]
    seen=set()
    with args.output.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=out_fields)
        writer.writeheader()
        for r in points:
            key=(r["figure_panel"],r["point_id"])
            if key in seen: raise SystemExit(f"Duplicate point id: {key}")
            seen.add(key)
            xp, yp=float(r["x_pixel"]),float(r["y_pixel"])
            xu, yu=float(r["x_pixel_uncertainty"]),float(r["y_pixel_uncertainty"])
            t, tu=convert(xp,xu,models[(r["figure_panel"],"x")])
            y, yuval=convert(yp,yu,models[(r["figure_panel"],"y")])
            writer.writerow({
                "figure_panel":r["figure_panel"],"point_id":r["point_id"],
                "curve_type":r["curve_type"],"gel_type":r["gel_type"],
                "temperature_C":r["temperature_C"],"x_pixel":xp,"y_pixel":yp,
                "time_h":f"{t:.8g}","relative_volume_decrease":f"{y:.8g}",
                "x_pixel_uncertainty":xu,"y_pixel_uncertainty":yu,
                "time_h_uncertainty":f"{tu:.8g}",
                "relative_volume_decrease_uncertainty":f"{yuval:.8g}",
                "extraction_confidence":r["extraction_confidence"],"notes":r["notes"],
            })
    print(f"Wrote {len(points)} calibrated points to {args.output}")

if __name__ == "__main__":
    main()
