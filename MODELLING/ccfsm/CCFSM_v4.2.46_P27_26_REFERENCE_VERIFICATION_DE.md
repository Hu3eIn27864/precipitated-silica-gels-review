# CCFSM v4.2.46 — P27.26: unabhängige Referenzprüfung der Schrittintegrale

**Datum:** 15.11.2026  
**Status:** Implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel

P27.25 rekonstruiert Dissipation und Reservoirarbeit aus zwei P21-Snapshots mit einer zeitlichen Trapezregel. P27.26 ergänzt eine davon unabhängige mathematische Referenzebene: synthetische Zeitverläufe mit exakt auswertbaren Integralen werden gegen zusammengesetzte Trapezquadratur geprüft.

## Implementierung

- \`ccfsm_p27_26_reference_verification.py\` stellt eine exakte Polynom-Integration und eine unabhängige zusammengesetzte Trapezregel bereit.
- \`manufactured_quadrature_report\` vergleicht beide Werte und gibt absoluten Quadraturfehler, Intervallzahl und den exakten Referenzwert aus.
- Die Routinen rufen P27.25 nicht auf und übernehmen keine seiner Zwischenwerte. Damit ist die Referenzprüfung nicht zirkulär.
- Fünf Regressionen prüfen konstante/lineare exakte Integration, Quadratur auf ungleichmäßigen Zeitabständen, Fehlerreduktion bei Halbierung der Schrittweite, eine kubische Referenz und ungültige Zeitgitter.

## Mathematische Referenz

Für ein Polynom \(p(t)=\sum_{k=0}^m c_k t^k\) wird
\[
I_{\mathrm{exact}}=\sum_{k=0}^m c_k\frac{t_1^{k+1}-t_0^{k+1}}{k+1}
\]
direkt ausgewertet. Für glatte quadratische Zeitverläufe zeigt die zusammengesetzte Trapezregel bei Halbierung der Schrittweite den erwarteten Fehlerfaktor vier. Lineare Verläufe werden bis auf Rundungsfehler exakt integriert.

## Aussagegrenzen und nächste Prüfschritte

Diese Referenz prüft die Quadraturmathematik, nicht die Vollständigkeit der P21-Leistungsfelder und nicht die physikalische Korrektheit der Randpotentiale. Sie beweist insbesondere weder die Upwind-Entropieschließung noch einen solverinternen Energieabschluss. Die P27.25-Endpunktrekonstruktion bleibt eine Trapezapproximation entlang des akzeptierten P24-Schritts.

Als nächste Erweiterung sind getrennte, analytisch vorgegebene geschlossene und offene Randflussfälle direkt gegen den P27.25-Adapter zu testen; dabei müssen Stofftransfer, chemische Randarbeit und hydraulische Arbeit mit unabhängigen Vorzeichenreferenzen geprüft werden.
