# P27.1 — 3-D-Tetraedergeometrie und exakte P1-Positivität

**Stand: 15. November 2026**

## Ziel und bewusst enger Geltungsbereich

P27.1 ist der erste echte 3-D-Positivitätsschritt nach den eindimensionalen P26-Zertifikaten. Er behandelt skalare, affine P1-Felder auf nichtentarteten Tetraederelementen. Das ist ein sinnvoller Start für Größen wie nichtnegative lokale Inventare, aber noch kein Zertifikat für sämtliche CCFSM-Zustandsgrößen oder für ein vollständiges 3-D-Zeitschrittverfahren.

## Exakte Geometrie

Für Eckpunkte \(v_0,\ldots,v_3\in\mathbb Q^3\) wird

\[
6V=\det(v_1-v_0,v_2-v_0,v_3-v_0)
\]

mit rationaler Arithmetik berechnet. \(6V\ne0\) ist die Nichtentartungsbedingung. Ein negatives Vorzeichen bedeutet lediglich umgekehrte Orientierung und ist für die lokale Positivitätsprüfung zulässig.

## P1-Positivitätsaussage

Jeder Punkt im Tetraeder besitzt baryzentrische Koordinaten \(\lambda_i\ge0\), \(\sum_i\lambda_i=1\). Für ein affines P1-Feld gilt

\[
u(x)=\sum_{i=0}^3\lambda_i(x)u_i.
\]

Daraus folgt die Äquivalenz

\[
u(x)\ge0\;\forall x\in T
\quad\Longleftrightarrow\quad
u_i\ge0\;\text{für alle vier Eckwerte}.
\]

Die vier nodalen Werte sind zugleich die Bernstein-Koeffizienten vom Grad 1 auf dem Simplex. Der Prüfer validiert Geometrie und Werte exakt mit \(\mathbb Q\)-Arithmetik. Die Mesh-Routine akzeptiert ein Netz nur, wenn jedes gelistete Tetraeder die lokale Prüfung besteht.

## Reproduktion

- ccfsm_p27_1_tetra_p1_positivity.py: exakte Determinante, Volumen und P1-Zertifikatsprüfung.
- test_ccfsm_p27_1_tetra_p1_positivity.py: Tests für Volumen, Orientierung, Randberührung, negative Werte, entartete Elemente, Konnektivität und rationale Koordinaten.

python -m unittest discover -s MODELLING/ccfsm -p 'test_ccfsm_p27_1_tetra_p1_positivity.py' -v

## Was damit noch nicht bewiesen ist

- Keine Positivitätsgarantie für P2- oder höhere Polynome; dort sind positive Bernstein-Koeffizienten hinreichend, aber auf dem ursprünglichen Element nicht notwendig.
- Keine automatische Netzkonformität, Nichtüberlappung, Randtreue oder Qualitätssicherung des globalen Tetraedernetzes.
- Keine Erhaltung der Positivität durch einen konkreten CCFSM-Transport-/Reaktions-Zeitschritt.
- Keine Garantie für Druck, Verschiebung, Spannung oder andere vorzeichenbehaftete Größen.
- Keine 3-D-SOS-/Semidefinitheitszertifikate höherer Ordnung und keine physikalische Validierung.

**Freigabestatus:** Exakte lokale P1-Positivität auf nichtentarteten Tetraedern ist bewiesen und softwareseitig prüfbar. Eine globale 3-D-Invariantenbereichsgarantie für das gekoppelte CCFSM ist ausdrücklich noch offen.
