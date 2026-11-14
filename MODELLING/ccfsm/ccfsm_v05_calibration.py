#!/usr/bin/env python3
"""CCFSM v0.5 exploratory fits to natural-syneresis chart readings.

The natural input is the curated 164-point literature file, not DATA/Raw/
kurvendigitalisierung.csv. That latter file contains pressure-cell/enforced
syneresis series and is audited separately, never used for natural calibration.
"""
from __future__ import annotations
import argparse, csv, math
from collections import defaultdict
from pathlib import Path

EPS=1e-15
MODELS=("exponential","stretched_exponential","ccfsm_two_stage")
PRIMARY={"primary_exploratory","primary_with_local_reversals"}

def number(value):
    return float(value.strip().replace(",", "."))

def audit_pressure_file(path):
    groups=defaultdict(set)
    with open(path,newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f,delimiter=";")
        required={"panel","series","condition"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Pressure audit input has an unexpected schema")
        for r in reader:
            groups[(r["panel"].strip(),r["series"].strip())].add(r["condition"].strip())
    if len(groups)!=21:
        raise ValueError(f"Expected 21 pressure-cell/enforced series in the audit file, found {len(groups)}")
    if any(not any("Δp" in c for c in conditions) for conditions in groups.values()):
        raise ValueError("A series lacks the expected applied-pressure metadata; review provenance")
    return {"pressure_cell_curves":len(groups),"natural_calibration_curves":0}

def read_natural_curves(path):
    groups=defaultdict(list); meta={}
    with open(path,newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        required={"figure","panel","condition","series","source_type","time_h","relative_shrinkage","reanalysis_use","digitization_note"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Natural calibration requires the curated literature point schema; the pressure-cell CSV is not admissible")
        for r in reader:
            if r["source_type"].strip()!="ai_assisted_approximation" or r["reanalysis_use"].strip() not in PRIMARY:
                continue
            key=(r["figure"].strip(),r["panel"].strip(),r["condition"].strip(),r["series"].strip(),r["reanalysis_use"].strip())
            t=number(r["time_h"]); y=number(r["relative_shrinkage"])
            if t<0 or not 0<=y<1: raise ValueError(f"Out-of-domain natural chart point {key}: {t}, {y}")
            groups[key].append((t,y))
            meta[key]={"source_type":r["source_type"].strip(),"digitization_note":r["digitization_note"].strip()}
    curves={}
    for key,pts in groups.items():
        pts.sort()
        if len(pts)<7: raise ValueError(f"Too few primary chart readings for comparison: {key}")
        curves[key]={"points":pts,**meta[key]}
    if len(curves)!=7:
        raise ValueError(f"Expected 7 primary natural chart series (curated primary branches); found {len(curves)}")
    return curves

def amplitude_sse(points,shape):
    den=sum(g*g for g in shape)
    amp=0.0 if den<=EPS else sum(g*y for (_,y),g in zip(points,shape))/den
    amp=min(1.0,max(0.0,amp))
    return amp,sum((y-amp*g)**2 for (_,y),g in zip(points,shape))

def shape_exp(points,lt):
    tau=math.exp(lt)
    return [1-math.exp(-t/tau) for t,_ in points]

def shape_stretched(points,lt,ln):
    tau,n=math.exp(lt),math.exp(ln)
    return [0.0 if t==0 else 1-math.exp(-min(700.0,max(0,t/tau)**n)) for t,_ in points]

def shape_ccfsm(points,lk1,lk2):
    a,b=sorted((math.exp(lk1),math.exp(lk2))); out=[]
    for t,_ in points:
        d=b-a
        g=1-(1+a*t)*math.exp(-a*t) if abs(d)<=1e-7*max(a,b) else 1-(b*math.exp(-a*t)-a*math.exp(-b*t))/d
        out.append(min(1.0,max(0.0,g)))
    return out

def fit_1d(points,lo,hi,fn):
    ratio=(math.sqrt(5)-1)/2; x1,x2=hi-ratio*(hi-lo),lo+ratio*(hi-lo)
    ev=lambda x:amplitude_sse(points,fn(x))
    f1,f2=ev(x1)[1],ev(x2)[1]
    for _ in range(100):
        if f1<=f2:
            hi,x2,f2=x2,x1,f1; x1=hi-ratio*(hi-lo); f1=ev(x1)[1]
        else:
            lo,x1,f1=x1,x2,f2; x2=lo+ratio*(hi-lo); f2=ev(x2)[1]
    x=(lo+hi)/2; amp,sse=ev(x)
    return x,amp,sse

def fit_2d(points,bounds,fn):
    (lo1,hi1),(lo2,hi2)=bounds; best=None
    for i in range(25):
        x=lo1+(hi1-lo1)*i/24
        for j in range(25):
            y=lo2+(hi2-lo2)*j/24; amp,sse=amplitude_sse(points,fn(x,y))
            if best is None or sse<best[0]: best=(sse,x,y,amp)
    sse,x,y,amp=best; dx=(hi1-lo1)/12; dy=(hi2-lo2)/12
    for _ in range(100):
        improved=False
        for sx,sy in ((dx,0),(-dx,0),(0,dy),(0,-dy)):
            xx=min(hi1,max(lo1,x+sx)); yy=min(hi2,max(lo2,y+sy))
            aa,ss=amplitude_sse(points,fn(xx,yy))
            if ss<sse: sse,x,y,amp=ss,xx,yy,aa; improved=True
        if not improved: dx*=.5; dy*=.5
        if max(dx,dy)<1e-7: break
    return x,y,amp,sse

def fit_model(points,model):
    dts=[points[i][0]-points[i-1][0] for i in range(1,len(points)) if points[i][0]>points[i-1][0]]
    if not dts: raise ValueError("Distinct time values required")
    dt=min(dts); tmax=max(t for t,_ in points)
    lo=math.log(max(1e-8,dt/1000)); hi=math.log(max(dt,tmax)*1000)
    if model=="exponential":
        x,amp,sse=fit_1d(points,lo,hi,lambda v:shape_exp(points,v))
        params={"amplitude":amp,"tau_h":math.exp(x)}; k=2
        boundary=x-lo<1e-4 or hi-x<1e-4
    elif model=="stretched_exponential":
        x,y,amp,sse=fit_2d(points,((lo,hi),(math.log(.3),math.log(3))),lambda a,b:shape_stretched(points,a,b))
        params={"amplitude":amp,"tau_h":math.exp(x),"stretch_exponent":math.exp(y)}; k=3
        boundary=x-lo<1e-4 or hi-x<1e-4 or min(abs(math.exp(y)-.3),abs(math.exp(y)-3))<1e-4
    elif model=="ccfsm_two_stage":
        x,y,amp,sse=fit_2d(points,((lo,hi),(lo,hi)),lambda a,b:shape_ccfsm(points,a,b))
        rates=sorted((math.exp(x),math.exp(y)))
        params={"amplitude_product_eta_qinf":amp,"rate_slow_per_h":rates[0],"rate_fast_per_h":rates[1],
                "rate_ratio_fast_over_slow":rates[1]/rates[0]}; k=3
        boundary=min(x,y)-lo<1e-4 or max(x,y)-hi<1e-4
    else: raise ValueError(model)
    n=len(points); mse=max(sse/n,EPS); aic=n*math.log(mse)+2*k
    aicc=aic+2*k*(k+1)/(n-k-1) if n>k+1 else float("inf")
    return {"model":model,"params":params,"sse":sse,"rmse":math.sqrt(sse/n),"aicc":aicc,"boundary":boundary}

def predict(fit,times):
    p=fit["params"]; model=fit["model"]
    if model=="exponential": return [p["amplitude"]*(1-math.exp(-t/p["tau_h"])) for t in times]
    if model=="stretched_exponential": return [p["amplitude"]*(1-math.exp(-max(0,t/p["tau_h"])**p["stretch_exponent"])) for t in times]
    shape=shape_ccfsm([(t,0) for t in times],math.log(p["rate_slow_per_h"]),math.log(p["rate_fast_per_h"]))
    return [p["amplitude_product_eta_qinf"]*g for g in shape]

def write_csv(path,rows,fields):
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def run(input_csv,output_dir,pressure_audit=None):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    curves=read_natural_curves(input_csv)
    pressure_info=audit_pressure_file(pressure_audit) if pressure_audit else {"pressure_cell_curves":"not checked"}
    fits=[]; preds=[]
    for (figure,panel,condition,series,use),meta in sorted(curves.items()):
        pts=meta["points"]; cut=max(5,min(len(pts)-2,int(math.floor(.8*len(pts)))))
        train,hold=pts[:cut],pts[cut:]
        for model in MODELS:
            full=fit_model(pts,model); tf=fit_model(train,model)
            hp=predict(tf,[t for t,_ in hold])
            hrmse=math.sqrt(sum((y-p)**2 for (_,y),p in zip(hold,hp))/len(hold))
            row={"figure":figure,"panel":panel,"condition":condition,"series":series,"reanalysis_use":use,
                 "source_type":meta["source_type"],"model":model,"n_points":len(pts),"n_train":len(train),
                 "n_holdout":len(hold),"train_rmse":tf["rmse"],"holdout_rmse":hrmse,
                 "full_rmse":full["rmse"],"full_aicc":full["aicc"],"boundary_hit":full["boundary"],**full["params"]}
            fits.append(row)
            fullpred=predict(full,[x for x,_ in pts])
            for (t,y),pr in zip(pts,fullpred):
                preds.append({"figure":figure,"panel":panel,"condition":condition,"series":series,
                    "reanalysis_use":use,"model":model,"time_h":t,"approximate_digitized_shrinkage":y,
                    "fitted_shrinkage":pr,"residual":y-pr,"source_type":meta["source_type"]})
    winners={}
    for r in fits:
        key=(r["figure"],r["panel"],r["condition"],r["series"])
        if key not in winners or r["full_aicc"]<winners[key]["full_aicc"]: winners[key]=r
    winrows=[{k:r[k] for k in ("figure","panel","condition","series","model","full_aicc","full_rmse","holdout_rmse","boundary_hit")} for _,r in sorted(winners.items())]
    fields=sorted({k for r in fits for k in r})
    write_csv(out/"ccfsm_v05_curve_fits.csv",fits,fields)
    write_csv(out/"ccfsm_v05_model_comparison.csv",fits,fields)
    write_csv(out/"ccfsm_v05_predictions_residuals.csv",preds,["figure","panel","condition","series","reanalysis_use","model","time_h","approximate_digitized_shrinkage","fitted_shrinkage","residual","source_type"])
    write_csv(out/"ccfsm_v05_curve_winners.csv",winrows,["figure","panel","condition","series","model","full_aicc","full_rmse","holdout_rmse","boundary_hit"])
    counts={m:sum(r["model"]==m for r in winrows) for m in MODELS}
    boundary_counts={m:sum(bool(r["boundary_hit"]) for r in fits if r["model"]==m) for m in MODELS}
    medians={m:sorted(r["holdout_rmse"] for r in fits if r["model"]==m)[len(curves)//2] for m in MODELS}
    report=["# CCFSM v0.5 — explorativer Vergleich natürlicher Synäresekurven","",
      f"- Primäre natürliche Kurven: {len(curves)}; nur die kuratierten Zweige primary_exploratory und primary_with_local_reversals.",
      "- Datenstatus: KI-gestützte ungeprüfte Näherungsablesungen aus Wilhelm & Kind (2015), Figures 8 und 10; keine pixelkalibrierten Marker-Rohdaten.",
      f"- Separater Provenienz-Audit der Datei DATA/Raw/kurvendigitalisierung.csv: {pressure_info}. Diese Datei enthält Druckzell-/erzwungene Synärese und wird NICHT für natürliche Fits verwendet.",
      "- Die 22 sensitivity_only-Punkte und 44 figure_table_conflict_branch-Punkte bleiben ausgeschlossen; die lokalen Reversals im primären Zweig bleiben unverändert erhalten.",
      "- Keine i.i.d.-Konfidenzintervalle: die Punktreihen sind ungeprüfte, korrelierte Näherungsablesungen.","",
      "## Modelle","",
      "Exponentiell: S=A(1-exp(-t/tau)); gestreckt exponentiell: S=A[1-exp(-(t/tau)^n)].",
      "Zweistufiges CCFSM: S=A_eff{1-[k_f exp(-k_s t)-k_s exp(-k_f t)]/(k_f-k_s)}; bei gleichen Raten gilt S=A_eff[1-(1+kt)exp(-kt)].",
      "A_eff=eta_a*q_inf; die Faktoren sind aus S(t) allein nicht separat identifizierbar. Das Ratenpaar ist ungeordnet; langsam/schnell ist keine physikalische Zuordnung.","",
      "## Vergleich","",
      "| Modell | AICc-Sieger (von 7) | Fits mit Randtreffer (von 7) | Median Holdout-RMSE |","|---|---:|---:|---:|"]
    for m in MODELS: report.append(f"| {m} | {counts[m]} | {boundary_counts[m]} | {medians[m]:.6g} |")
    report += ["","Je Kurve: Vollfit mit AICc/RMSE und chronologischer Holdout (erste 80 % Fit, letzte 20 % Test). Wegen weniger Punkte pro Reihe und unsicherer Herkunft ist dies nur explorative Konsistenzprüfung, keine unabhängige Validierung.",
      "AICc/Holdout-Werte sind angesichts ungeprüfter Näherungsablesungen und kleiner Kurvenzahl rein deskriptiv. Parameter an Suchgrenzen sind mit boundary_hit=True markiert.",
      "Aus diesen Reihen werden keine Aktivierungsenergie, kein kausales pH-Gesetz und keine hydraulischen Materialkonstanten abgeleitet.","",
      "## Reproduktion","",
      "python MODELLING/ccfsm/ccfsm_v05_calibration.py --input LITERATURE/wilhelm_kind_approximate_measurement_points_curated.csv --pressure-audit DATA/Raw/kurvendigitalisierung.csv --output-dir MODELLING/ccfsm/results_v0.5","",
      "Die Ergebnisse sind explorative Modellvergleiche der Näherungsablesungen. Sie validieren nicht das vollständige chemisch-hydraulische CCFSM."]
    (out/"CCFSM_v0.5_CALIBRATION_REPORT_DE.md").write_text("\n".join(report)+"\n",encoding="utf-8")
    return {"natural_curves":len(curves),"fit_rows":len(fits),"pressure_audit":pressure_info,
            "winner_counts":counts,"boundary_hit_counts":boundary_counts,"median_holdout_rmse":medians}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    p.add_argument("--pressure-audit")
    p.add_argument("--output-dir",required=True)
    a=p.parse_args(); print(run(a.input,a.output_dir,a.pressure_audit))

if __name__=="__main__": main()
