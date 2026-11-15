# CCFSM v4.2.11 — P26.11: allgemeine exakte Zwei-Koordinaten-Momentkorrektur

## Ziel

P26.10 korrigiert zwei Modenkoeffizienten innerhalb einer Pivotzelle. P26.11 verallgemeinert dies: Aus den 2N linearen und quadratischen Zellmoden werden beliebige zwei Pivotkoordinaten gewählt. Alle übrigen Koordinaten werden rationalisiert; die beiden Pivotkoeffizienten werden aus den globalen Momentengleichungen exakt bestimmt.

## Mathematische Form

Für Zelle j mit Mittelpunkt c_j, Breite h_j und festem Mittel m_j:
\[
u_j(\xi)=m_j+a_j\xi+b_j(\xi^2-1/12),\quad -1/2\leq\xi\leq1/2.
\]
Die beiden Modenmomente lauten
\[
T_1=\sum_j a_j h_j^2/12,\qquad
T_2=\sum_j(c_j a_j h_j^2/6+b_j h_j^3/180).
\]
Die Masse ist wegen der festen Zellmittelwerte bereits exakt festgelegt.

Jede Modenkoordinate besitzt eine rationale Spalte g_k in diesem linearen Gleichungssystem. Für ein beliebiges Paar p,q mit nichtverschwindender Determinante wird
\[
[g_p\;g_q]\begin{bmatrix}z_p\\z_q\end{bmatrix}
=\begin{bmatrix}T_1\\T_2\end{bmatrix}-\sum_{k\ne p,q}g_k z_k
\]
mit exakter rationaler 2x2-Elimination gelöst. Anschließend wird das quadratische Minimum jeder Zelle exakt über beide Endpunkte und gegebenenfalls den inneren Scheitelpunkt bestimmt.

## Suchstrategie und Status

- Für jede vorgegebene signifikante Dezimalpräzision werden alle \({2N\choose2}\) Koordinatenpaare untersucht.
- Singuläre Paare werden übersprungen; nur exakt gelöste und exakt positive Kandidaten werden akzeptiert.
- Unter erfolgreichen Kandidaten wird zuerst die größte minimale Zellreserve, bei Gleichstand die geringste quadratische Abweichung von den Eingabemoden gewählt.
- `feasible_exact_primal_witness`: exakte rationale Masse, erstes und zweites Moment sowie kontinuierliche Nichtnegativität.
- `no_exact_positive_witness_found`: endliche Suche ohne Zeugen; ausdrücklich kein Unzulässigkeitsbeweis.
- Ein rationales duales Trennungszertifikat aus P26.8 bleibt unabhängig und kann Unzulässigkeit beweisen.

## Abgrenzung

P26.11 ist eine systematische Erweiterung der Pivotwahl, aber noch kein vollständiger exakter konvexer Optimierer oder vollständiger Machbarkeitsalgorithmus: Die Präzisionsliste ist endlich, die rationalisierten Nicht-Pivot-Kandidaten stammen aus einer vorgegebenen Ausgangsrekonstruktion, und eine vorhandene reelle/rationale Lösung kann außerhalb dieser endlichen Kandidatenfamilie liegen. Die Dykstra-Projektion bleibt ein numerischer Kandidatengenerator. Geltungsbereich: 1-D-Intervalle, feste Zellmittelwerte, stückweise quadratische Rekonstruktionen. Keine 2-D/3-D-Erweiterung und keine physikalische Validierung.

## Reproduktion

`python -m unittest MODELLING/ccfsm/test_ccfsm_p26_11_all_pair_exact_witness.py`

Der CI-Workflow führt zusätzlich den reproduzierbaren CSV/JSON-Referenzlauf aus.
