# CCFSM v4.2.48 — P27.28: zeitabhängige Randfluss-Quadraturreferenz

**Datum:** 15.11.2026  
**Status:** Implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel und Methode

P27.28 erweitert die konstanten Referenzfälle aus P27.27 um zeitabhängige analytische Randdaten. Der P27.25-Adapter erhält Anfangs- und End-Snapshots eines synthetischen Zeitschritts. Seine Zweipunkt-Trapezrekonstruktion wird mit unabhängig analytisch integrierten Polynomen verglichen.

Verwendet werden quadratische diffusive M-Randflüsse, lineare Reservoir-Chemiepotentiale und eine quadratische hydraulische Reservoirleistung. Das Produkt aus Potential und Fluss ist kubisch. Advektion, Reaktion, Darcy- und Onsager-Innendissipation sind im isolierten Referenzfall null.

## Referenzgleichungen

Für ein Polynom q(t) = Summe(q_k t^k) wird das exakte Integral als Summe(q_k T^(k+1)/(k+1)) berechnet. Für das chemische Randarbeitsintegral werden Potential und Fluss zunächst polynomial multipliziert und anschließend exakt integriert:

- Chemische Arbeit: A Integral[mu_L(t) j_L(t) - mu_R(t) j_R(t)] dt
- Netto-M-Transfer: A Integral[j_L(t) - j_R(t)] dt
- Hydraulische Arbeit: A Integral[p_hyd(t)] dt

Der Adapter verwendet dagegen die Endpunkt-Trapezregel. Sie ist für lineare Leistungs-/Flussraten exakt, nicht jedoch allgemein für quadratische Materialflussraten oder kubische chemische Leistungsprodukte.

## Implementierung und Prüfumfang

- `ccfsm_p27_28_time_dependent_boundary.py`: synthetische Anfangs-/End-Snapshots, Aufruf von P27.25 und unabhängige exakte Polynomreferenz.
- `test_ccfsm_p27_28_time_dependent_boundary.py`: vier Regressionen für Referenzwerte, getrennte Fehlerbudgets, Linearitätsidentität und ungültige Eingaben.
- Stoff- und Energiefehler werden getrennt und sowohl vorzeichenbehaftet als auch absolut ausgegeben.

Für den Standardfall T=2 s und A=1.5 m² ergeben die analytischen Integrale:
- Netto-M-Transfer: 2.9 mol
- chemische Randarbeit: 18.21 J
- hydraulische Randarbeit: 8.3 J

Die Zweipunkt-Trapezrekonstruktion liefert in diesem Fall 3.6 mol, 19.26 J und 8.7 J. Die absoluten Abweichungen betragen somit 0.7 mol, 1.05 J und 0.4 J. Diese Fehler werden getrennt ausgewiesen und von den Regressionen ausdrücklich erwartet; sie werden nicht als Testfehler kaschiert.

## Aussagegrenzen

Dies ist eine Quadratur-/Adapterprüfung mit synthetischen Zeitfunktionen. Sie rekonstruiert nicht den tatsächlichen inneren Newton-Pfad eines P24-Schritts und beweist keine P24-Energieidentität. Die vollständige Upwind-Entropie-/Kettenregel, Feststoff-/Brückenreservoirarbeit, mechanische Randarbeit und physikalische Reservoirgesetze bleiben offen. Keine physikalische Validierung oder vollständige Energieabschlussgarantie.
