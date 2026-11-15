# CCFSM P27.16 — Newton-Invariantenlimiter und FV-Flussbilanz-Audit

**Stand:** 15.11.2026  
**Status:** implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel und P24-Integration

P24 ruft für jede Newton-Richtung den gemeinsamen P27.15 fraction-to-boundary-Limiter auf, bevor das Residuum-Backtracking beginnt. Der eine Faktor wirkt gleichzeitig auf Fluidkapazität und M/O/N/B. Die Line-Search darf den Schritt anschließend weiter verkleinern, aber nicht vergrößern. Aktive Schranken und Faktor werden in der Iterationshistorie abgelegt. Bei Limi­terfehler, Singularität, Line-Search-Fehler oder Iterationslimit wird kein Zustand akzeptiert.

Das erhält die diskreten Bedingungen (0<\theta\leq1) und (n_M,n_O,n_N,n_B>0) für den begrenzten Newton-Kandidaten, garantiert aber keine Newton-Konvergenz.

## FV-Flussbilanz

Für jedes Feld prüft P27.16 lokal
\[
\dot u_j=-\frac{F_{j+1/2}-F_{j-1/2}}{\Delta x_j}+S_j
\]
und global die Teleskopidentität
\[
\sum_j\Delta x_j(\dot u_j-S_j)=F_{1/2}-F_{N+1/2}.
\]
Der P21-Adapter verwendet Darcy-Fluss für Fluidkapazität und Gesamtfluss für M/O. Quellen für alle fünf Felder werden explizit vom Aufrufer geliefert. N/B werden mit Null-Fluss als quellengetriebene Felder behandelt. Es werden keine Reaktionsquellen stillschweigend geraten.

## Tests und Grenzen

Acht Regressionstests prüfen gemeinsame Schrittbegrenzung, lokale/globale Bilanz, Fehlererkennung, nichtuniforme Zellen, P21-Adapter und Aussagegrenzen. Der Audit beweist nur die algebraische Konsistenz der gelieferten RHS, Flüsse und Quellen. Er beweist weder Vollständigkeit der Quellen noch physikalische Korrektheit, Energieabnahme, Zeitstabilität, 3-D-Erhaltung oder physikalische Validierung.
