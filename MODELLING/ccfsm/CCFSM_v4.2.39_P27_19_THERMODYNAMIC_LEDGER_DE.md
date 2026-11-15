# CCFSM v4.2.39 — P27.19 integrierter thermodynamischer Konsistenz-Ledger

**Stand:** 15.11.2026  
**Status:** implementierter algebraischer Auditbaustein; kein vollständiger Energieabschluss.

## Ziel

P27.19 ergänzt nach P27.18 einen komponentenübergreifenden Ledger für die Energierate. Geprüft wird die Bilanz

\[
\dot E_h = P_{\mathrm{ext}} - \mathcal D_h,
\qquad
R_E=\dot E_h-P_{\mathrm{ext}}+\mathcal D_h.
\]

Alle Eingaben müssen dieselbe Bezugsfläche, Zeitskalierung und Einheit W/m² besitzen. Energie-Raten, Dissipationen und äußere Leistungen werden getrennt summiert; das Residuum wird unabhängig berechnet und nicht auf null gesetzt.

## Implementierte Prüfungen

- getrennte Komponenten für chemische, mechanische und hydraulische Energieraten;
- nichtnegative, getrennt ausgewiesene Dissipationen (z. B. Onsager, Reaktion, Darcy);
- explizite externe Leistungen (Reservoir-/Randarbeit);
- optionales P27.18-Onsager-Audit-Gate;
- Vorzeichenprüfung der Reaktionsprodukte \(r_i A_i\geq0\);
- optionale Darcy-Konstitutivitätsprüfung \(q_f+K_f\nabla_f p=0\) auf inneren Flächen.

Die Funktion ist bewusst ein Ledger und kein automatischer Adapter, der unvollständige P10/P13/P19/P21-Snapshots zu einer scheinbar vollständigen Energie kombiniert. P19s FE-Energie (J), P10-Reaktionsdissipation (W/m³) und P13/Darcy-Größen (W/m²) sind erst nach einer dokumentierten Geometrie-/Querschnittsabbildung addierbar.

## Physikalische und mathematische Grenzen

- P10-Reaktionsdissipation wird zellweise pro Referenzvolumen ausgegeben; vor dem Ledger ist sie mit korrekten Zellvolumina/-flächen in W/m² umzurechnen.
- P10/P21-Darcy-Dissipation umfasst innere Flächen; Reservoir-Hydraulikleistung muss explizit und mit konsistentem Vorzeichen als äußerer Leistungsterm übergeben werden.
- P13/P27.18 prüft den Onsager-Diffusionsanteil, nicht die vollständige Entropiebilanz offener Advektion.
- P19 liefert quasistatische FE-Energie und Traktionsarbeit; eine zeitliche Energierate benötigt zwei konsistente mechanische Zustände und Rand-/Dirichlet-Arbeit.
- Die komponentenübergreifende Ableitung aus einer gemeinsamen freien Energie ist nicht bewiesen. Ein bestandener Ledger belegt nur die algebraische Konsistenz der gelieferten Zahlen.
- Keine Aussage über PDE-Existenz, globale Regularität, 3D-Positivität oder experimentelle Validierung.

## Tests und Freigabe

Die Regressionen prüfen geschlossene/offene Bilanzen, Defekterkennung, Dissipationsvorzeichen, Reaktionsaffinitäten, Onsager-Gate und Darcy-Vorzeichen.

**Nächster Schritt:** P27.20 sollte einen dimensionskonsistenten Snapshot-Adapter entwickeln, zunächst mit klar getrennten 1D-FV-Energiegrößen und mechanischen Differenzen aus zwei P19-Zuständen; inkompatible Einheiten dürfen nicht summiert werden.
