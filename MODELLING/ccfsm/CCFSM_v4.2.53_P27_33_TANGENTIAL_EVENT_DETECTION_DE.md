# CCFSM v4.2.53 — P27.33: Suche nach tangentialen Randflussereignissen

## Motivation

P27.31/P27.32 erkennen und verfeinern primär Nullstellen, die als Vorzeichenwechsel sichtbar werden. Eine Nullstelle gerader Vielfachheit, beispielsweise (f(t)=(t-t_*)^2), berührt die Nulllinie ohne das Vorzeichen zu wechseln und kann daher von einer reinen Vorzeichenwechselroutine übersehen werden.

## Methode

P27.33 ergänzt die adaptive P27.31-Stützstellenfolge um eine lokale quadratische Kandidatensuche:
1. Drei aufeinanderfolgende, nicht notwendigerweise äquidistante Samples definieren ein quadratisches Interpolationspolynom.
2. Liegt dessen Scheitel innerhalb des Dreierintervalls, wird der ursprüngliche Flux-Funktionswert an dieser Zeit direkt ausgewertet.
3. Nur wenn dieser Originalwert innerhalb der vorgegebenen Flusstoleranz liegt, wird ein tangentialer Ereigniskandidat gemeldet.
4. Vorzeichenwechselereignisse bleiben separat über die P27.32-Bisektion auswertbar.

Die Methode unterscheidet ausdrücklich zwischen einem tangentialen Kandidaten und einem zertifizierten Nullstellenbeweis.

## Manufactured Referenzfälle

- Tangentiale Nullstelle ohne Vorzeichenwechsel: (f(t)=(t-0.37)^2).
- Zwei gewöhnliche Vorzeichenwechsel: (g(t)=(t-0.23)(t-0.81)).
- Zusätzlich wird ein Test mit nichtäquidistanten Samples sowie ein absichtlich inkonsistenter Original-Flux verwendet, um zu prüfen, dass nicht allein das interpolierte Polynom den Kandidaten bestimmt.

## Verifikation

Sechs Regressionstests prüfen die tangentiale Nullstelle, die direkte Auswertung des Originalflusses, nichtäquidistante Zeitpunkte, die weiterhin funktionierende Bisektion von Vorzeichenwechseln sowie Eingabe-/Nichtendlichkeitsschutz.

## Grenzen / mathematische Aussage

Die lokale quadratische Interpolation ist eine diagnostische Heuristik. Ein kleiner Original-Fluxwert an einem geschätzten Scheitel ist Evidenz für einen Kandidaten, aber ohne Ableitungs- oder Intervallgrenzen keine formale Garantie einer exakten Nullstelle. Bei nichtquadratischen, stark oszillierenden oder schlecht aufgelösten Flüssen können Scheitelpunkte verfehlt oder falsche Kandidaten erzeugt werden. Auch die P27.31-Abtastung ist nicht vollständig zertifiziert.

Keine vollständige diskrete Upwind-Entropie-Kettenregel, keine tatsächliche P24-Newton-Trajektorienintegration, keine 3-D-Positivitätsgarantie und keine physikalische Validierung.

## Nächster mathematischer Gate

P27.34 sollte die Kandidatensuche mit Ableitungsintervallen oder Intervallarithmetik verbinden: stationäre Punkte isolieren, (f(t_*)) einschließen und Nullstellen-/Nichtnullstellen-Aussagen mit expliziten Restschranken unterscheiden.
