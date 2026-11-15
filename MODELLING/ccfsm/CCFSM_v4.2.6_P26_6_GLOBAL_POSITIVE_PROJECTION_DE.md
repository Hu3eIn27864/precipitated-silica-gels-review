# P26.6 — Global gekoppelte Positivitäts- und Momentenprojektion

## Ziel

P26.4 begrenzt Zielzellpolynome radial; P26.5 projiziert jede Zelle lokal auf den nichtnegativen quadratischen Kegel. P26.6 koppelt diese Korrekturen global und hält Masse sowie erstes und zweites räumliches Moment fest.

## Zielfunktion und Nebenbedingungen

Für feste Zellmittelwerte (m_j\geq0) und Moden (a_j,b_j):

\[
\min_{\{a_j,b_j\}}\sum_j\left[w_1(a_j-a_j^0)^2+w_2(b_j-b_j^0)^2\right]
\]

unter

\[
m_j+a_j\xi+b_j(\xi^2-1/12)\geq0
\quad (\forall\xi\in[-1/2,1/2]),
\]

sowie

\[
M_1=M_1^0,\qquad M_2=M_2^0.
\]

Die Masse (M_0=\sum_jm_jh_j) bleibt automatisch erhalten, da die Zellmittelwerte unverändert bleiben. Für die Moden gelten die linearen Momentenbeiträge
\[
\Delta M_1=\sum_j a_jh_j^2/12,
\quad
\Delta M_2=\sum_j(a_jc_jh_j^2/6+b_jh_j^3/180).
\]

## Numerisches Verfahren

Dykstras Projektionsalgorithmus wird auf die Schnittmenge zweier abgeschlossener konvexer Mengen angewendet: (A) affine globale Momentenbedingungen und (B) Produkt der zellweisen Positivitätsmengen. Die Projektion auf A wird über ein 2x2 gewichtetes Gram-System berechnet; die Projektion auf B verwendet P26.5 zellweise. Bei Konvergenz liefert Dykstra die gewichtete nächste zulässige Koeffizientenfolge im gewählten Normmaß.

## Abbruch und Grenzen

- Die globale Massenbilanz ist durch unveränderte Mittelwerte exakt bis auf Gleitkomma-Arithmetik.
- Erstes und zweites Moment werden bis zur angegebenen numerischen Toleranz erhalten.
- Jede Zellpositivität wird mit dem analytischen quadratischen Minimum kontrolliert.
- Nichtkonvergenz ist **kein** Unzulässigkeitsbeweis; sie lässt Machbarkeit offen.
- Rangdefiziente Momentenbedingungen werden abgewiesen.
- Nur 1-D-Intervalle und quadratische Rekonstruktionen; keine 2-D/3-D-Geometrie, keine physikalische Validierung.


## P26.6.1 — Machbarkeitsklassifikation

P26.6.1 ergänzt eine dreistufige Machbarkeitsdiagnose. Für genau eine Zelle bestimmen die beiden globalen Momentengleichungen die beiden Moden eindeutig; ein negatives analytisches Polynomminimum ist damit ein expliziter Unzulässigkeitsnachweis. Für mehrere Zellen gilt: eine konvergierte Dykstra-Lösung liefert einen numerischen zulässigen Zeugen; Nichtkonvergenz bleibt ausdrücklich „unresolved“ und ist kein Unzulässigkeitsbeweis. Die Diagnose ist keine allgemeine Farkas-/Dualzertifizierung für Mehrzellen-Netze.
