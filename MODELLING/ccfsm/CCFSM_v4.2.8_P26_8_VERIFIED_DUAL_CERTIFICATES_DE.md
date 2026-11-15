# P26.8 — Verifizierte duale Unzulässigkeitszertifikate

## Ziel
P26.8 ersetzt die numerische Supportfunktionssuche aus P26.7 durch eine analytische Zell-Supportfunktion und eine rational nach oben eingeschlossene Supportschranke. Ein positiver rationaler Trennungsabstand ist damit ein überprüfbares Unzulässigkeitszertifikat für die eingegebenen Dezimalwerte.

## Zellgeometrie
Für m >= 0 sei
K(m)={(a,b): m+a*xi+b*(xi^2-1/12) >= 0 für alle xi in [-1/2,1/2]}.
Für m=0 folgt aus Nichtnegativität und Mittelwert null K(0)={(0,0)}.
Für m>0 besteht der Rand aus zwei geraden Segmenten mit Eckpunkten (0,-6m), (-3m,3m), (3m,3m) sowie dem oberen Ellipsenbogen
a=sqrt(12)m sin(phi), b=6m(1+cos(phi)), |phi|<=2pi/3.

Für eine lineare Richtung (p,q) ist die Supportfunktion das Maximum aus dem unteren Eckpunkt und dem Ellipsenbogen. Mit P=sqrt(12)m p und Q=6m q liegt der unbeschränkte Kreisbogenmaximierer im zulässigen Bogen genau dann, wenn |p| >= 3|q|. Daraus folgt:
- wenn q >= 0 oder |p| >= 3|q|: h = max(-6mq, 6m[q + sqrt(q^2+p^2/3)]);
- andernfalls: h = max(-6mq, 3m[|p|+q]).
Die Formel ist geschlossen und vermeidet Winkelsuche.

## Globale Trennung
Für y=(y1,y2) werden die zellweisen Richtungen
p_j = y1*h_j^2/12 + y2*c_j*h_j^2/6,
q_j = y2*h_j^3/180
gebildet. Ein strikter Nachweis
y dot t > Sum_j h_Kj(p_j,q_j)
beweist, dass die vorgegebenen globalen ersten und zweiten Momente unter zellweiser Positivität nicht gleichzeitig erreichbar sind.

## Exakte rationale Schranken
Eingaben werden anhand ihrer Dezimalstring-Darstellung als rationale Zahlen interpretiert. Quadratwurzeln werden durch ganzzahlige Quadratwurzel mit Skalierung nach oben eingeschlossen. Der Supportwert wird daher nach oben, der Trennungsabstand nach unten durch eine rationale Zahl beschränkt. Nur wenn diese untere Schranke strikt positiv ist, meldet der Verifier `verified=true`.

Das Zertifikat enthält Richtung, Ziel-Skalarprodukt, Support-Oberschranke sowie Zähler und Nenner der positiven rationalen Abstandsschranke. Es kann unabhängig mit `verify_dual_certificate` erneut geprüft werden.

## Bedeutung und Grenzen
- Ein Zertifikat beweist Unzulässigkeit für die exakt aus den Dezimalstrings gebildeten rationalen Eingabedaten.
- Kein gefundenes Zertifikat bedeutet nicht Machbarkeit: die Richtungssuche verwendet nur ein endliches ganzzahliges Richtungsraster.
- Der Beweis gilt für 1-D-Intervalle, feste Zellmittelwerte und quadratische Rekonstruktionen; keine 2-D/3-D-Verallgemeinerung.
- Softwaretests und Zertifikate validieren weder das physikalische CCFSM noch natürliche Synäreseexperimente.
