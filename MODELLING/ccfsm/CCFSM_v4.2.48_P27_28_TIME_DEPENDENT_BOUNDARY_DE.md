# CCFSM v4.2.48 — P27.28: zeitabhängige Randfluss-Quadraturreferenz

**Datum:** 15.11.2026  
**Status:** Implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel und Methode

P27.28 erweitert die konstanten Referenzfälle aus P27.27 um zeitabhängige analytische Randdaten. Der P27.25-Adapter erhält Anfangs- und End-Snapshots eines synthetischen Zeitschritts. Seine Zweipunkt-Trapezrekonstruktion wird mit unabhängig analytisch integrierten Polynomen verglichen.

Verwendet werden quadratische diffusive M-Randflüsse, lineare Reservoir-Chemiepotentiale und eine quadratische hydraulische Reservoirleistung. Das Produkt aus Potential und Fluss ist kubisch. Advektion, Reaktion, Darcy- und Onsager-Innendissipation sind im isolierten Referenzfall null.

## Referenzgleichungen

Für ein Polynom (q(t)=sum_k q_k t^k) wird das exakte Integral als
[
int_0^T q(t),dt=sum_k rac{q_k T^{k+1}}{k+1}
]
berechnet. Für das chemische Randarbeitsintegral werden Potential und Fluss zunächst polynomial multipliziert und anschließend exakt integriert:
[
W_{m chem}=Aint_0^T[mu_L(t)j_L(t)-mu_R(t)j_R(t)],dt.
]
Der Netto-M-Transfer lautet
[
N_M=Aint_0^T[j_L(t)-j_R(t)],dt.
]
Die hydraulische Arbeit ist (W_{m hyd}=Aint_0^T p_{m hyd}(t),dt).

Der Adapter verwendet dagegen die Endpunkt-Trapezregel. Sie ist für lineare Leistungs-/Flussraten exakt, nicht jedoch allgemein für quadratische Materialflussraten oder kubische chemische Leistungsprodukte.

## Implementierung und Prüfumfang

- `ccfsm_p27_28_time_dependent_boundary.py`: synthetische Anfangs-/End-Snapshots, Aufruf von P27.25 und unabhängige exakte Polynomreferenz.
- `test_ccfsm_p27_28_time_dependent_boundary.py`: vier Regressionen für Referenzwerte, getrennte Fehlerbudgets, Linearitätsidentität und ungültige Eingaben.
- Stoff- und Energiefehler werden getrennt und sowohl vorzeichenbehaftet als auch absolut ausgegeben.

Für den Standardfall (T=2,mathrm{s}), (A=1.5,mathrm{m^2}) ergeben die analytischen Integrale:
- Netto-M-Transfer: (2.25,mathrm{mol})
- chemische Randarbeit: (17.67,mathrm{J})
- hydraulische Randarbeit: (8.1,mathrm{J})

Die nichtverschwindenden Abweichungen der Zweipunkt-Trapezregel werden vom Test explizit erwartet und nicht als Testfehler kaschiert.

## Aussagegrenzen

Dies ist eine Quadratur-/Adapterprüfung mit synthetischen Zeitfunktionen. Sie rekonstruiert nicht den tatsächlichen inneren Newton-Pfad eines P24-Schritts und beweist keine P24-Energieidentität. Die vollständige Upwind-Entropie-/Kettenregel, Feststoff-/Brückenreservoirarbeit, mechanische Randarbeit und physikalische Reservoirgesetze bleiben offen. Keine physikalische Validierung oder vollständige Energieabschlussgarantie.
