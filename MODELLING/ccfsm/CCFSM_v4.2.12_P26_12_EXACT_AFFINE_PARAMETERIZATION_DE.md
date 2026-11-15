# CCFSM v4.2.12 — P26.12: exakte affine Parametrisierung des Momentenraums

## Ziel

P26.11 untersuchte verschiedene Zweier-Pivotpaare. P26.12 macht den vollständigen affinen Lösungsraum der globalen Momentengleichungen explizit. Bei N Zellen existieren 2N lineare/quadratische Modenkoordinaten. Nach Fixierung der Zellmittelwerte ist die Masse bereits bestimmt; erstes und zweites globales Moment liefern zwei affine Gleichungen. Bei Rang zwei bleibt ein affiner Raum der Dimension 2N−2.

## Exakte Parametrisierung

Für jede Modenkoordinate z_k=(a_0,b_0,a_1,b_1,...) ist die Spalte g_k in Q²:
\[
g_{a_j}=\left(h_j^2/12,\ c_jh_j^2/6\right),\qquad
g_{b_j}=\left(0,\ h_j^3/180\right).
\]
Mit den durch Zellmittelwerte erzeugten Basismomenten B_1,B_2 und Zielmomenten T_1,T_2 gilt
\[
\sum_{k=1}^{2N}g_kz_k=(T_1-B_1,T_2-B_2).
\]
Ein beliebiges linear unabhängiges Spaltenpaar p,q wird als Pivot gewählt. Alle übrigen Koordinaten bilden z_F. Exakt rational:
\[
(z_p,z_q)^T=G_{pq}^{-1}\left(r-\sum_{k\in F}g_kz_k\right).
\]
Damit ist die Abbildung zwischen freien Koordinaten und dem vollständigen affinen Momentenraum bijektiv. Jeder rationale freie Vektor erzeugt rationale Modenkoeffizienten und erfüllt beide Momentengleichungen exakt.

## Positivitätssuche

Die Zellpositivität ist keine weitere lineare Bedingung, sondern die konvexe Schnittbedingung
\[
m_j+a_j\xi+b_j(\xi^2-1/12)\geq0
\quad\forall\xi\in[-1/2,1/2].
\]
P26.12 enumeriert rationale Gitterpunkte um die rationalisierte Ausgangsrekonstruktion im gesamten freien Koordinatenraum. Jeder Treffer wird mittels exakter rationaler Intervallminima geprüft. Bei mehreren Treffern wird die größte minimale Zellreserve bevorzugt.

## Statussemantik

- `feasible_exact_primal_witness`: exakter rationaler Zeuge mit Masse, erstem/zweitem Moment und kontinuierlicher Zellpositivität.
- `unresolved`: im endlichen Gitter kein Zeuge gefunden oder Kandidatenbudget erreicht. Das ist kein Unzulässigkeitsbeweis.
- Ein P26.8-Dualzertifikat bleibt ein eigenständiger rigoroser Unzulässigkeitsnachweis.

## Grenzen

Die affine Parametrisierung ist vollständig und exakt, sofern die beiden Momentbedingungen Rang zwei haben. Die rationale Gittersuche ist dagegen endlich und nicht vollständig: Ein nichtleerer reeller zulässiger Schnitt muss keinen rationalen Punkt enthalten; außerdem kann das Kandidatenbudget die Suche begrenzen. P26.12 ist somit ein vollständiger Koordinatenchart, aber noch kein vollständiger Machbarkeitsalgorithmus. Geltungsbereich: 1-D-Intervalle, feste Zellmittelwerte, stückweise quadratische Rekonstruktion. Keine 2-D/3-D-Erweiterung, keine physikalische Validierung.
