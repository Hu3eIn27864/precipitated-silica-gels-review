# P27.2 — Exakte hinreichende P2-Bernstein-Zertifikate auf Tetraedern

**Stand: 15. November 2026**

## Satz

Auf dem Referenztetraeder mit baryzentrischen Koordinaten \(\lambda_i\ge0\), \(\sum_i\lambda_i=1\), bilden die zehn Bernstein-Basisfunktionen vom Grad 2

\[
\lambda_i^2,\qquad 2\lambda_i\lambda_j\quad (0\le i<j\le3)
\]

eine nichtnegative Partition der Eins. Für

\[
u(\lambda)=\sum_{i=0}^3 b_{ii}\lambda_i^2+
2\sum_{0\le i<j\le3}b_{ij}\lambda_i\lambda_j
\]

folgt daher unmittelbar:

\[
b_{ii}\ge0,\ b_{ij}\ge0\ \forall i,j
\quad\Longrightarrow\quad
u(\lambda)\ge0\ \forall\lambda.
\]

Die Implikation ist hinreichend, nicht notwendig.

## Exakte Konvertierung aus P2-Lagrange-Knotenwerten

Die vier Eckwerte sind \(b_{ii}=u(e_i)\). Für den Mittelpunkt der Kante \(ij\) gilt

\[
u\!\left(\frac{e_i+e_j}{2}\right)
=\frac14b_{ii}+\frac14b_{jj}+\frac12b_{ij}.
\]

Damit wird der zugehörige Bernstein-Koeffizient exakt rekonstruiert:

\[
b_{ij}=2u\!\left(\frac{e_i+e_j}{2}\right)
-\frac{b_{ii}+b_{jj}}{2}.
\]

P27.2 rechnet alle zehn Koeffizienten mit rationalen Brüchen aus und zertifiziert nur, wenn jeder Koeffizient nichtnegativ ist. Ein negatives Bernstein-Koeffizientenergebnis bedeutet **nicht**, dass das Polynom negativ ist; es bedeutet ausschließlich, dass dieser einfache hinreichende Test keinen Beweis liefert.

## Gegenbeispiel zur Notwendigkeit

\[
u(\lambda)=(\lambda_0-\lambda_1)^2\ge0
\]

hat einen negativen Bernstein-Koeffizienten \(b_{01}=-1\). Der Prüfer muss deshalb „nicht zertifiziert“ und nicht „negativ“ melden. Dieser Regressionstest schützt ausdrücklich vor einer falschen Infeasibilitätsaussage.

## Reproduktion

- ccfsm_p27_2_tetra_p2_bernstein.py — exakte Konvertierung und hinreichender P2-Zertifikatsprüfer.
- test_ccfsm_p27_2_tetra_p2_bernstein.py — positive Konstante, rationale Koeffizienten, nicht notwendiges Zertifikat, negative Polynome und degenerierte Geometrie.

python -m unittest discover -s MODELLING/ccfsm -p 'test_ccfsm_p27_2_tetra_p2_bernstein.py' -v

## Grenzen

- Ein fehlendes Bernstein-Zertifikat ist kein Beweis für Negativität.
- Höhere Ordnungen, Subdivision/Verfeinerung und SOS/Semidefinitheitszertifikate sind nicht implementiert.
- Noch keine direkte Kopplung an die von P19 aufruferseitig gelieferten FE-Quadraturdaten oder an P20/P21/P22.
- Keine Positivitätsgarantie für den vollständigen 3-D-Zeitschritt und keine physikalische Validierung.
