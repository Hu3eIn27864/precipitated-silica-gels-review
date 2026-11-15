# CCFSM P26 — konservative FE/FV-Projektion auf nicht übereinstimmenden 1-D-Netzen

**Status:** implementierter 1-D-Methodenbaustein; keine allgemeine 3-D-Freigabe.

## Ziel und Definition

P25.1 konnte nur verschachtelte uniforme FV-Netze durch Blockmittelung vergleichen. P26 verwendet geometrische Überlappungen beliebiger eindimensionaler Intervallnetze mit identischem Gesamtgebiet.

Quellzelle (I_i=[x_i,x_{i+1}]), Quellmittelwert \\(\\bar u_i\\), Zielzelle (J_j=[y_j,y_{j+1}]). Die Überlappungslänge ist

\\[
\\ell_{ij}=\\max(0,\\min(x_{i+1},y_{j+1})-\\max(x_i,y_j)).
\\]

Der Zielmittelwert lautet

\\[
\\bar u_j^T=\\frac{1}{|J_j|}\\sum_i\\ell_{ij}\\bar u_i.
\\]

Bei identischem Gebiet gilt \\(\\sum_i\\ell_{ij}=|J_j|\\). Daher bleiben Konstanten erhalten. Da \\(\\ell_{ij}\\geq0\\), ist die Abbildung positivitätserhaltend. Global folgt

\\[
\\sum_j|J_j|\\bar u_j^T=\\sum_i|I_i|\\bar u_i.
\\]

Dies ist Integralerhaltung für die stückweise konstante Quellrekonstruktion.

## FE-Quadratur-Eingang

Die Funktion \`quadrature_to_cell_averages\` bildet pro Quellzelle ein quadraturgewichtetes Mittel \\(\\bar u_i^Q=\\sum_qw_qu_q/\\sum_qw_q\\), mit positiven Gewichten. Anschließend erfolgt die Überlappungsprojektion. Die Genauigkeit hängt von der bereitgestellten Quadratur und Zellmittelwertrepräsentation ab. Für konservierte Inventare müssen die Gewichte das korrekte physikalische Maß einschließlich Geometrie-/Jacobi-Faktor enthalten.

## Erhaltungsgrößen und Druck

- Für FV-Inventare (n_M,n_O,n_N,n_B) und Fluidkapazität kann die Projektion bei konsistentem Maß die Gebietsintegale erhalten.
- Druck ist keine Erhaltungsgröße. Eine Mittelung kann als numerische Darstellungstransformation dienen; Druckintegralerhaltung ist aber keine physikalische Bilanz. Druckfehler und mechanische Residuen sind separat zu auditieren.
- Die Projektion erzeugt keine neue mechanische Gleichgewichtslösung. Für einen konsistenten Zielnetz-Druck muss P19 dort erneut gelöst werden.

## Implementierung und Grenzen

- `ccfsm_p26_conservative_projection.py`: Kantenvalidierung, identisches Gebiet, positive Überlappungsgewichte, quadraturgewichtete Quellmittelwerte, Integraldiagnostik.
- `test_ccfsm_p26_conservative_projection.py`: nichtverschachtelte Netze, Integralerhaltung, Konstantenerhaltung, Identität, Positivität und Eingabevalidierung.
- CI führt die P26-Tests mit der gesamten Suite aus und veröffentlicht CSV/JSON-Ergebnisse.

Dies ist keine beliebige FE-Funktionsprojektion: FE-Felder werden pro Quellintervall auf ein quadraturgewichtetes Zellmittel reduziert; zwischen Quellzellen gilt eine stückweise konstante Rekonstruktion. Keine 2-D/3-D-Flächen-/Volumenintersection, Polyeder-Momentintegration, gekrümmten Geometrien oder automatische FE-DoF-Zuordnung. Nächste Ausbaustufen: 1-D höhere Momente/Polynomrekonstruktion, danach geometrische 2-D/3-D Common-Refinement- oder Intersection-Operatoren mit Maß- und Randabdeckungsaudit.

Alle Zahlen sind synthetische Softwaretests, keine physikalische Validierung.
