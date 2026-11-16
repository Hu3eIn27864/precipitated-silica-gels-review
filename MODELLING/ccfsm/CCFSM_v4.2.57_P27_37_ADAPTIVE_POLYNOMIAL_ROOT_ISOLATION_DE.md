# CCFSM v4.2.57 — P27.37: adaptive Polynom-Nullstellenisolation

**Datum:** 15.11.2026  
**Status:** implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel und Verfahren

P27.37 ergänzt P27.36 um eine begrenzte rekursive Intervallunterteilung. Jedes Teilintervall wird zuerst mit dem P27.35-Null-Ausschluss geprüft. Falls dessen Horner-Einschließung Null ausschließt, ist das Teilintervall nullstellenfrei. Andernfalls folgt das P27.36-Ableitungsvorzeichen-/Endpunktkriterium:

- `certified_unique_root`: genau eine innere Nullstelle im Teilintervall.
- `certified_no_root`: keine Nullstelle im Teilintervall.
- ungelöste Teilintervalle werden bis zur maximalen Rekursionstiefe oder minimalen Intervallbreite unterteilt; danach bleiben sie explizit ungelöst.

Die Kombination aus P27.35-Null-Ausschluss und P27.36-Monotoniekriterium vermeidet, dass Teilintervalle um kritische Punkte allein wegen einer nicht strikt vorzeichenbestimmten Ableitung unnötig ungelöst bleiben. Die Ausgabe enthält die Blätter der Intervallpartition, die Zahl zertifizierter einfacher Nullstellen, die Zahl nullstellenfreier Blätter, ungelöste Blätter und eine konservative Schranke für die Gesamtzahl. Eine endliche obere Schranke wird nur ausgegeben, wenn kein ungelöstes Blatt verbleibt.

## Tests

Neun Regressionen prüfen eine einfache Nullstelle, zwei getrennte einfache Nullstellen, Nullstellenfreiheit, tangentiale Nullstelle, eine Nullstelle exakt an einer tatsächlich erzwungenen Teilungsgrenze, Tiefen- und Mindestbreitenlimit, lückenlose Partition und Eingabevalidierung.

**Regressionstest-Korrektur (16.11.2026):** Der ursprüngliche Testfall `p(x)=x-0,5` auf `[0,1]` erzwingt keine Unterteilung, weil P27.36 bereits auf dem Gesamtintervall eine eindeutige innere Nullstelle zertifiziert. Er wurde durch `p(x)=(x-0,5)(x²+1)` ersetzt: Die natürliche Horner-Einschließung der Ableitung enthält auf `[0,1]` die Null und löst dadurch die Unterteilung bei `x=0,5` aus. Die Nullstelle liegt anschließend auf der gemeinsamen Grenze beider Kinder und bleibt dort ausdrücklich ungelöst. Auch der Tiefenlimit-Test wurde korrigiert: Eine lineare Nullstelle, die bereits auf dem Elternintervall zertifiziert wird, prüft kein Rekursionslimit. Der neue Tiefentest verwendet eine tangentiale Nullstelle, deren Ableitungseinschließung ungelöst bleibt. Die Implementierung von P27.37 wurde für beide Korrekturen nicht verändert.

## Aussagegrenzen

Die Zertifizierung gilt ausschließlich für Polynome und unter dem Intervall-Einschließungsvertrag von P27.34–P27.36. Eine Nullstelle exakt auf einer rekursiven Teilungsgrenze kann bewusst ungelöst bleiben; sie wird nicht doppelt gezählt. Tangentiale/mehrfache Nullstellen bleiben ungelöst, wenn die Ableitungseinschließung Null enthält. Die Routine garantiert keine vollständige Isolation für beliebige Flussfunktionen und keine Vollständigkeit der vorgelagerten P27.31/P27.33-Ereignisabtastung. Keine physikalische Validierung.
