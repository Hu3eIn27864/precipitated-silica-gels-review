# CCFSM v4.2.10 — P26.10: exakte rationale Momentenkorrektur

## Ziel

P26.10 schließt die in P26.9 verbliebene Lücke: Ein primaler Zeuge soll nicht nur Momentenresiduen innerhalb einer Toleranz besitzen, sondern globale Masse, erstes und zweites räumliches Moment exakt erfüllen. Zugleich muss die stückweise quadratische Dichte auf jeder Zelle kontinuierlich nichtnegativ sein.

## Konstruktion

Auf Zelle j mit Breite h_j und Mittelpunkt c_j gilt
u_j(xi)=m_j+a_j*xi+b_j*(xi²-1/12), -1/2<=xi<=1/2.
Bei festen Zellmittelwerten ist die Masse bereits fest. Für die beiden höheren Modal-Momente gelten

T1 = sum_j a_j*h_j²/12
T2 = sum_j (a_j*c_j*h_j²/6 + b_j*h_j³/180).

Alle Koeffizienten außerhalb einer ausgewählten Pivotzelle werden aus dem numerischen Kandidaten als rationale Zahlen ihrer Dezimaldarstellung fixiert. In der Pivotzelle werden anschließend zwei Unbekannte exakt gelöst:

a_p = (T1 - sum_(j!=p) a_j*h_j²/12)/(h_p²/12)

b_p = (T2 - sum_(j!=p)(a_j*c_j*h_j²/6+b_j*h_j³/180) - a_p*c_p*h_p²/6)/(h_p³/180).

Damit sind beide globalen höheren Momente und folglich auch die Masse exakt erfüllt – in rationaler Arithmetik, nicht nur bis zur Maschinenpräzision.

## Positivitätszertifikat

Für jede Zelle wird das exakte Minimum aus den Endpunkten und gegebenenfalls dem inneren Scheitel bestimmt. Ein Zeuge wird nur akzeptiert, wenn alle Minima rational nichtnegativ sind. Der Algorithmus durchsucht mehrere Pivotzellen und Dezimalgenauigkeiten und wählt unter erfolgreichen Kandidaten den mit der größten minimalen Zellreserve.

## Statussemantik

- feasible_exact_primal_witness: exakte rationale Masse, erstes und zweites Moment sowie exakte kontinuierliche Zellpositivität.
- certified_infeasible: positiver rationaler dualer Trennungsabstand aus P26.8.
- unresolved: kein Zeuge in der endlichen Korrektursuche gefunden oder numerischer Projektor nicht konvergiert. Das ist kein Unzulässigkeitsbeweis.

## Grenzen

Die Korrektur verändert zwei Koeffizienten einer Pivotzelle. Die endliche Suche über Pivotzellen und Rundungsgenauigkeiten kann einen existierenden exakten positiven Zeugen übersehen. P26.6 bleibt ein Gleitkomma-Kandidatengenerator; P26.10 ist kein allgemeiner exakter Konvexitätslöser. Geltungsbereich: eindimensionale Intervalle, feste nichtnegative Zellmittelwerte und stückweise quadratische Rekonstruktionen. Keine 2-D/3-D-Verallgemeinerung und keine physikalische Validierung.

Softwaretests prüfen die mathematische Implementierung und die Reproduzierbarkeit, nicht die experimentelle Gültigkeit des natürlichen Synäresemodells.
