# CCFSM v4.2.45 — P27.25: Rekonstruktion der Schrittintegrale aus P21/P24-Snapshots

## Ziel

P27.25 ergänzt P27.24 um eine solvernahe Rekonstruktion der Transport-Dissipation und hydraulischen Randarbeit aus dem initialen P21-Snapshot und dem akzeptierten P24-Endsnapshot. Die Zeitintegration erfolgt mit der Trapezregel.

Für (dt=t^{n+1}-t^n), Referenzquerschnitt (A) und FV-Zellbreite (\Delta x):

\[
D_{\mathrm{rxn}}\approx A\Delta x\,dt\sum_j
\frac{d_j^n+d_j^{n+1}}{2},
\qquad
D_{\mathrm{Darcy}}\approx A dt\frac{d_D^n+d_D^{n+1}}2,
\]

analog für Onsager-Diffusion. Die hydraulische Reservoirleistung aus P21 wird ebenfalls trapezförmig integriert.

## Randstofftransport und chemische Leistung

Die tatsächlichen advectiven und gesamten M/O-Randflüsse werden getrennt ausgewertet. Diffusive Flüsse ergeben sich als Gesamtfluss minus Upwind-Advektion. Mit den in P13 ausgegebenen Zell- und Reservoir-Chemiepotentialen wird eine potentialgewichtete Randflussleistung geschätzt. Zusätzlich werden die zeitintegrierten Netto-Mengenflüsse für beide mobilen Spezies ausgewiesen.

## Strikte Grenzen

- Trapezregel ist eine Quadratur zwischen zwei Snapshots, keine exakte Zeitintegration entlang des P24-Newton-Pfads.
- Potentialgewichtete Upwind-Randflüsse ersetzen keinen vollständigen diskreten Kettenregel-/Entropienachweis.
- Mechanische Dirichlet-Reaktionsarbeit, Feststoff-/Brückenreservoirarbeit und weitere äußere Beiträge werden nicht automatisch inferiert.
- Die Funktion verlangt einen konvergierten P24-Schritt und einen zum akzeptierten Zustand passenden finalen Snapshot.
- Keine solver-interne Energie-Monotonie, kein vollständiger P21/P24-Energiesatz und keine physikalische Validierung werden behauptet.

## Regressionen

Fünf Tests prüfen die Schrittintegration, Ablehnung nicht konvergierter bzw. inkonsistenter P24-Ergebnisse, positive Geometrie/Zeitschritt und die Ausgabe der Randstoffmengen.
