# CCFSM v4.2.57 — P27.37: adaptive Polynom-Nullstellenisolation

**Datum:** 15.11.2026  
**Status:** implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel und Verfahren

P27.37 ergänzt P27.36 um eine begrenzte rekursive Intervallunterteilung. Jedes Teilintervall wird mit dem P27.36-Ableitungsvorzeichen-/Endpunktkriterium geprüft:

- `certified_unique_root`: genau eine innere Nullstelle im Teilintervall.
- `certified_no_root`: keine Nullstelle im Teilintervall.
- ungelöste Teilintervalle werden bis zur maximalen Rekursionstiefe oder minimalen Intervallbreite unterteilt; danach bleiben sie explizit ungelöst.

Die Ausgabe enthält die Blätter der Intervallpartition, die Zahl zertifizierter einfacher Nullstellen, die Zahl nullstellenfreier Blätter, ungelöste Blätter und eine konservative Schranke für die Gesamtzahl. Eine endliche obere Schranke wird nur ausgegeben, wenn kein ungelöstes Blatt verbleibt.

## Tests

Acht Regressionen prüfen eine einfache Nullstelle, zwei getrennte einfache Nullstellen, Nullstellenfreiheit, tangentiale Nullstelle, eine Nullstelle exakt an einer Teilungsgrenze, Tiefenlimit, lückenlose Partition und Eingabevalidierung.

## Aussagegrenzen

Die Zertifizierung gilt ausschließlich für Polynome und unter dem Intervall-Einschließungsvertrag von P27.34–P27.36. Eine Nullstelle exakt auf einer rekursiven Teilungsgrenze kann bewusst ungelöst bleiben; sie wird nicht doppelt gezählt. Tangentiale/mehrfache Nullstellen bleiben ungelöst, wenn die Ableitungseinschließung Null enthält. Die Routine garantiert keine vollständige Isolation für beliebige Flussfunktionen und keine Vollständigkeit der vorgelagerten P27.31/P27.33-Ereignisabtastung. Keine physikalische Validierung.
