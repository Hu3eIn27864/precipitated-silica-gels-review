# CCFSM P26.1 — höhergradige 1-D-Projektion mit Momentenerhaltung

**Status:** implementierter und CI-geprüfter 1-D-Methodenschritt; keine allgemeine 3-D-Freigabe.

## Motivation

P26 übertrug stückweise konstante Quellzellmittelwerte. Das erhält das nullte Moment (Integral), verliert aber im Allgemeinen die innerhalb einer Zielzelle vorhandene lineare Information. P26.1 ergänzt eine stückweise lineare Quellrekonstruktion und überträgt pro Zielzelle sowohl Masse als auch erstes zentriertes Moment.

## Quellrekonstruktion

In Quellzelle (I_i=[x_i,x_{i+1}]) mit Mittelpunkt (c_i) wird

[
u_i(x)=\bar u_i+s_i(x-c_i)
]

verwendet. Die Zellmittelwerte bleiben unverändert, weil der lineare Anteil über die symmetrische Zelle zu null integriert. Die Steigungen werden mit Minmod aus benachbarten Zellmittelwertgradienten bestimmt; am Rand wird ein einseitiger Gradient verwendet. Ein optionaler Positivitätsbegrenzer reduziert (s_i) so, dass beide Zellrandwerte nichtnegativ bleiben, sofern alle Quellmittelwerte nichtnegativ sind.

## Zielprojektion: zwei Momente

Für Zielzelle (J_j=[a,b]), Mittelpunkt (c), Breite (h), berechnet die Implementierung

[
\bar u_j=\frac1h\int_a^b u_h(x)\,dx,
\qquad
s_j^T=\frac{12}{h^3}\int_a^b(x-c)u_h(x)\,dx.
]

Damit reproduziert die Zielrekonstruktion (u_j^T(x)=\bar u_j+s_j^T(x-c)) exakt das nullte und erste zentrierte Moment des integrierten Quellfeldes in jeder Zielzelle. Folglich bleiben globale Masse und globales erstes räumliches Moment erhalten (bis auf Rundungsfehler), sofern beide Netze dasselbe Gebiet abdecken.

## Warum das wichtig ist

- Die Zielmittelwerte bewahren weiterhin die konservierten Zellinventare.
- Die Zielsteigungen bewahren zusätzliche räumliche Information, die P26 bei der stückweise konstanten Übertragung verworfen hat.
- Für ein lineares Feld (u(x)=a+bx) ist die Minmod-Rekonstruktion auf einem nichtuniformen Netz exakt, solange die Daten monoton sind und der Positivitätsbegrenzer nicht aktiv werden muss.
- Druck kann ebenfalls als Feld rekonstruiert werden, bleibt aber eine nicht-konservierte Größe. Mechanisch konsistenter Zielnetzdruck erfordert weiterhin eine P19-Neuberechnung.

## Tests und reproduzierbarer Lauf

- `ccfsm_p26_1_moment_projection.py`: Minmod-Steigungen, Positivitätsbegrenzung, analytische Überlappungsintegrale für Masse und erstes Moment, CSV/JSON-Referenzlauf.
- `test_ccfsm_p26_1_moment_projection.py`: lineare Exaktheit auf nichtuniformen, nicht übereinstimmenden Netzen; Erhaltung beider Momente; Konstanten- und Identitätstest; Positivitäts- und Eingabevalidierung.
- CI veröffentlicht `ccfsm-p26-1-moment-projection-results`.

## Grenzen

Minmod ist robust und nicht oszillatorisch, aber nahe Extrema bzw. bei nichtmonotonen Feldern kann es die Ordnung lokal reduzieren. Der Positivitätsbegrenzer kann lineare Exaktheit verändern, wenn die Zellmittelwerte eine Rekonstruktion mit negativen Randwerten erzwingen. Der Operator ist 1-D, intervallbasiert und verwendet stückweise lineare Rekonstruktionen; er löst weder allgemeine FE-Polynomprojektion noch 2-D/3-D-Schnittgeometrie oder gekrümmte Zylindergeometrie. Sämtliche Referenzwerte sind synthetische Softwareverifikation, keine Materialvalidierung.
