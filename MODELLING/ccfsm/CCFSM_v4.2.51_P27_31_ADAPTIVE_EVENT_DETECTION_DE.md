# CCFSM v4.2.51 — P27.31: adaptive Ereignisabtastung für Randfluss-Nullstellen

**Datum:** 15.11.2026  
**Status:** Implementiert; Hosted-CI-Prüfung ausstehend.

## Motivation

P27.30 lokalisiert Nullstellen zwischen bereitgestellten Abtastpunkten. Es kann jedoch zwei Nullstellen übersehen, wenn der Fluss an beiden Intervallenden dasselbe Vorzeichen besitzt. P27.31 ergänzt deshalb eine begrenzte rekursive Mittelpunktabtastung.

## Algorithmus

- Flussfunktionen werden auf einem groben Basisgitter ausgewertet.
- Jedes Intervall erhält eine Mittelpunktprobe.
- Eine Halbierung wird ausgelöst, wenn ein Vorzeichenwechsel in einer der beiden Halbintervalle sichtbar wird oder die Mittelpunktabweichung von der linearen Endpunktinterpolation eine absolute/relative Krümmungstoleranz überschreitet.
- Die Rekursion ist durch `max_depth` begrenzt.
- Die resultierenden sortierten Stichproben werden an den P27.30-Nullstelleninterpolator übergeben.

## Manufactured test

Eine glatte Testfunktion (f(t)=(t-0.35)(t-0.75)) besitzt zwei Nullstellen bei 0.35 s und 0.75 s, obwohl ihre Werte bei 0 s und 2 s dasselbe Vorzeichen haben. Die adaptive Mittelpunkt-/Krümmungsregel soll diese beiden Ereignisse aufdecken. Zusätzlich werden die linearen Randflüsse aus P27.29 mit Nullstellen bei 1.0 s und 1.5 s mitgeführt.

Sechs Tests decken das verborgene Nullstellenpaar, lineare Ereignisse, Gitterverfeinerung, flache gleichsignige Flüsse, ungültige/nichtendliche Eingaben und die Rekursionstiefengrenze ab.

## Aussagegrenzen

P27.31 ist eine adaptive numerische Heuristik, kein zertifizierter Root-Isolation-Algorithmus. Hochfrequente/oscillatorische Flüsse können Ereignisse auch bei begrenzter Mittelpunktabtastung verbergen; `max_depth` begrenzt Aufwand, nicht den Fehler rigoros. Eine Garantie würde zusätzliche Regularitätsannahmen und z.B. Intervallarithmetik oder belastbare Ableitungs-/Krümmungsschranken erfordern. Keine vollständige diskrete Upwind-Entropie-Kettenregel, keine Integration der tatsächlichen P24-Newton-Trajektorie und keine physikalische Validierung.
