# P27.3 — Adaptive Tetraeder-Unterteilung für P2-Bernstein-Positivität

**Stand: 15. November 2026**

## Verfahren

P27.2 liefert einen exakten hinreichenden Test auf einem Tetraeder. Ist ein Bernstein-Koeffizient negativ, ist die Aussage zunächst unentschieden. P27.3 zerlegt das Referenztetraeder exakt in acht Kindtetraeder:

- vier Ecktetraeder,
- vier Tetraeder, die das zentrale Oktaeder entlang der Diagonale \(m_{01}\)--\(m_{23}\) teilen.

Alle Kindknoten werden als rationale baryzentrische Koordinaten des Elternelements dargestellt. Das P2-Polynom wird an den vier Kindknoten und sechs Kantenmittelpunkten exakt ausgewertet; daraus werden die zehn Kind-Bernstein-Koeffizienten rekonstruiert. Die Rekursion akzeptiert nur, wenn **jedes** Blatt zehn nichtnegative Koeffizienten besitzt.

## Drei strikt getrennte Ergebnisse

1. \`certified_nonnegative\`: Alle Blätter sind durch nichtnegative Bernstein-Koeffizienten zertifiziert.
2. \`certified_negative_point\`: Ein exakt ausgewerteter Unterteilungsknoten hat einen negativen Feldwert; dies ist ein echter Gegenbeweis zur Nichtnegativität.
3. \`unresolved\`: Die maximale Tiefe wurde erreicht oder Eingabedaten/Geometrie sind ungültig. Ein fehlendes Zertifikat wird niemals als Negativitätsbeweis ausgegeben.

## Regressionstest mit positivem Polynom

\[
u(\lambda)=(\lambda_0-\lambda_1)^2+\frac1{16}>0.
\]

Der ursprüngliche Bernstein-Koeffizient \(b_{01}=-15/16\) ist negativ. P27.3 zeigt, dass die exakte Unterteilung die Zertifizierung dennoch auf einer endlichen Tiefe ermöglichen kann. Das schützt vor der falschen Gleichsetzung „negativer Bernstein-Koeffizient = negatives Polynom“.

## Grenzen

- Das Verfahren ist ein hinreichender Zertifikatsalgorithmus, kein vollständiger Entscheider für alle nichtnegativen P2-Polynome.
- Endliche maximale Tiefe kann zu \`unresolved\` führen, obwohl das Polynom nichtnegativ ist.
- Die Unterteilung ist geometrisch eine exakte Partition des Referenztetraeders; sie prüft noch keine globale Netzkonformität benachbarter Elemente.
- Noch keine Anbindung an P19-Quadratur-/FE-Assemblierung, P20/P21/P22 oder einen 3-D-Transport-/Reaktions-Zeitschritt.
- Keine universelle 3-D-Invariantenbereichsgarantie und keine physikalische Validierung.

## Reproduktion

python -m unittest discover -s MODELLING/ccfsm -p 'test_ccfsm_p27_3_tetra_p2_subdivision.py' -v
