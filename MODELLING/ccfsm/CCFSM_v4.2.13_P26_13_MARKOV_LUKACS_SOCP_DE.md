# CCFSM v4.2.13 — P26.13: exakte Markov-Lukács-Zertifikate und SOCP-Formulierung

## Ziel

P26.12 parametrisiert den vollständigen affinen Raum der Koeffizienten, welche die globalen Masse-, Erst- und Zweitmomentbedingungen erfüllen. P26.13 formuliert die zusätzliche kontinuierliche Zellpositivität als endlichdimensionale konvexe Kegelbedingung.

Für eine Zelle mit normierter lokaler Koordinate \(x\in[-1/2,1/2]\) gilt

\[
u(x)=m+a x+b(x^2-1/12)
=(m-b/12)+a x+b x^2.
\]

Nach dem Markov-Lukács-Satz ist ein quadratisches Polynom auf diesem Intervall genau dann nichtnegativ, wenn es eine Darstellung

\[
u(x)=
\begin{bmatrix}1&x\end{bmatrix}
Q
\begin{bmatrix}1\\x\end{bmatrix}
+\lambda(1/4-x^2),
\qquad Q\succeq0,\quad \lambda\ge0
\]

besitzt. Für \(Q=\begin{bmatrix}q_{00}&q_{01}\\q_{01}&q_{11}\end{bmatrix}\) folgt durch Koeffizientenvergleich

\[
q_{00}=m-b/12-\lambda/4,\quad
q_{01}=a/2,\quad
q_{11}=b+\lambda.
\]

Die PSD-Bedingung einer symmetrischen 2x2-Matrix ist exakt äquivalent zu
\[
q_{00}\ge0,\quad q_{11}\ge0,\quad
q_{00}q_{11}-q_{01}^2\ge0.
\]

## Exakte rationale Zertifikatskonstruktion

Setze \(A_0=m-b/12\). Die zulässigen Multiplikatoren liegen im Intervall
\[
\lambda\in[\max(0,-b),\,4A_0].
\]
Auf diesem Intervall ist
\[
f(\lambda)=(A_0-\lambda/4)(b+\lambda)
\]
eine konkave quadratische Funktion. Ihr Maximum liegt bei
\[
\lambda_* = 2A_0-b/2,
\]
auf das zulässige Intervall projiziert. Da alle Eingaben rational sind, ist auch der so gewählte \(\lambda\) rational. Der Test \(f(\lambda)\ge a^2/4\) ist ein exakter rationaler Vergleich. Damit wird für jedes akzeptierte Zellpolynom ein rationales PSD-Zertifikat konstruiert.

## Globale Kopplung

Die P26.12-Abbildung setzt die zwei globalen höheren Momentengleichungen exakt durch zwei Pivotkoeffizienten um. Werden die freien Koordinaten \(z_F\) und die lokalen Hilfsvariablen \(\lambda_j,Q_j\) gemeinsam betrachtet, ergeben sich affine Gleichungen plus je Zelle ein 2x2-PSD-Kegel und \(\lambda_j\ge0\). Das ist eine endlichdimensionale SOCP-/SDP-artige konvexe Machbarkeitsformulierung (2x2-PSD ist äquivalent zu einer Rotated-SOC-Bedingung).

Die Implementierung konstruiert und prüft exakte Zellzertifikate für vorgegebene Koeffizienten bzw. freie P26.12-Koordinaten. Sie enthält ausdrücklich **noch keinen** globalen SOCP-Optimierer und löst daher nicht automatisch die gekoppelten freien Koordinaten.

## Software und Status

- `ccfsm_p26_13_markov_lukacs_socp.py`: exakte rationale Zellzertifikate und globaler P26.12-Kandidatenaudit.
- `test_ccfsm_p26_13_markov_lukacs_socp.py`: Randberührung, Nullpolynom, negative Fälle, unabhängiger exakter Minimumvergleich auf rationalem Testgitter und globaler Momenten-Audit.
- P26.12-Regression korrigiert: rationale Zielmomente werden im Test als `Fraction` statt als binäre Python-Floats notiert. Der CI-Fehler war ein Testdaten-Typfehler, kein Fehler der affinen Parametrisierung.

## Grenzen

1. 1-D-Intervalle, feste nichtnegative Zellmittelwerte und quadratische Rekonstruktionen.
2. Exakte Zellzertifikate sind kein globaler Suchalgorithmus für die freien Koordinaten.
3. Keine 2-D/3-D-Geometrie, keine physikalische Validierung und keine Aussage zur experimentellen Güte des CCFSM.
4. Ein nicht gefundener globaler Kandidat bleibt unresolved; nur ein gültiges duales Zertifikat belegt Unzulässigkeit.
