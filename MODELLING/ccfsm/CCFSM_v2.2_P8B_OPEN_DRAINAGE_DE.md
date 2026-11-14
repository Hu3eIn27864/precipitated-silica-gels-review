# CCFSM v2.2 – P8b: offene freie-Oberflächen-Drainage und Siliciumaustrag

**Datum:** 14.11.2026  
**Geltungsbereich:** natürliche Synärese, 1D-Referenzkörper mit offenen hydraulischen Randflächen; mobile Spezies M/O und immobilisierte Netzwerkpools N/B.  
**Status:** semidiskreter Finite-Volumen-Referenzoperator mit äußerem Referenzdruck und vorgegebenen Außenkonzentrationen. Keine freie-Grenzflächenbewegung, kein Kapillargesetz, keine empirische Kalibrierung und kein vollständiger Existenzsatz.

## 1. Physikalische Frage

P8a hatte an beiden Enden (Q=0). Das ist für eine frei drainierende Probe nicht ausreichend. P8b ersetzt diese Bedingung durch einen äußeren hydraulischen Referenzdruck (p_{m ext}). Flüssigkeit kann abhängig vom Druckgefälle hinein- oder herausströmen. Gleichzeitig wird der mobile Siliciumbestand über dieselben Randflächen bilanziert.

Die Randbedingung ist zunächst ein **Druckreservoir-Modell**. (p_{m ext}) kann später aus Umgebungsdruck plus Kapillardruck abgeleitet werden. P8b behauptet ausdrücklich noch kein bestimmtes Kapillargesetz und keine dynamische freie Oberfläche.

## 2. Hydraulischer Randfluss

Für Zellzentrum-Abstand (h=Delta x/2), positive Zellpermeabilität (K_j) und Zellranddruck (p_{m ext}) definieren wir die orientierten Flüsse in positiver x-Richtung:
[
Q_{1/2}=-K_1rac{p_1-p_{m ext}}{h},qquad
Q_{N+1/2}=-K_Nrac{p_{m ext}-p_N}{h}.
	ag{P8b.1}
]
An inneren Flächen wird wie in P8a die harmonische Permeabilität verwendet. Damit gilt in jeder Zelle
[
dot	heta_j=-rac{Q_{j+1/2}-Q_{j-1/2}}{Delta x},
qquad
dot p_j=dot	heta_j/S_{p,j}.
	ag{P8b.2}
]
Die integrierte Fluidbilanz ist nun offen:
[
rac{d}{dt}sum_j	heta_jDelta x=Q_{m left}-Q_{m right}.
	ag{P8b.3}
]
Hier sind (Q_{m left}) und (Q_{m right}) die orientierten Flüsse in +x-Richtung. Der nach außen gerichtete Gesamtfluss ist daher (Q_{m right}-Q_{m left}).

## 3. Mobile Silicium-Spezies am offenen Rand

Für (iin{M,O}) gilt im Inneren weiterhin
[
F_i=Q c_i-	heta D_i
abla c_i,qquad c_i=m_i/	heta.
]
An den offenen Randflächen wird der advektive Upwind-Wert verwendet: Bei Einströmung stammt er aus dem Außenreservoir (c_{i,m ext}), bei Ausströmung aus der ersten/letzten Gelzelle. Der diffusive Randfluss verwendet denselben Außenwert als Dirichlet-Referenz und den halben Zellabstand:
[
F_{i,L}=Q_L c_{i,m up}
-	heta_1D_irac{c_{i,1}-c_{i,m ext,L}}{h},
]
[
F_{i,R}=Q_R c_{i,m up}
-	heta_ND_irac{c_{i,m ext,R}-c_{i,N}}{h}.
	ag{P8b.4}
]
Die äußeren Konzentrationen sind explizite Eingaben. Für ein reines Ausströmproblem können sie auf null gesetzt werden; sobald Rückströmung möglich ist, müssen sie die reale Außenflüssigkeit repräsentieren. Nullkonzentration ist keine universelle Randbedingung.

Die Inventarbilanz lautet
[
dot m_{i,j}=-rac{F_{i,j+1/2}-F_{i,j-1/2}}{Delta x}+R_{i,j},
quad dot s_N=R_N,quaddot s_B=R_B.
	ag{P8b.5}
]
Daraus folgt die exakte semidiskrete Si-Bilanz
[
rac{d}{dt}sum_j(m_M+m_O+s_N+s_B)_jDelta x
=sum_{i=M,O}(F_{i,L}-F_{i,R}).
	ag{P8b.6}
]
Die Reaktionen erhalten lokales Gesamt-Si; nur die mobilen Randflüsse ändern das Gesamtinventar im Gel. Die immobilisierten Pools N/B werden nicht advektiv ausgetragen. Ein späteres Modell für Erosion, Fragmentablösung oder gelöste Netzwerkfreisetzung wäre ein eigener physikalischer Mechanismus.

## 4. Diskrete Druckdissipation und Grenzen

Bei gleichem konstantem Außendruck an beiden Enden und positivem (K) dissipiert die lineare hydraulische Energie relativ zu (p_{m ext}):
[
rac{d}{dt}rac12sum_j S_{p,j}(p_j-p_{m ext})^2Delta x
=-sum_{m innen}K_f(
abla_hp)^2Delta x
-sum_{m Rand}rac{K_j}{h}(p_j-p_{m ext})^2
le0,
	ag{P8b.7}
]
für den hier verwendeten konstanten Speicherkoeffizienten. Bei unterschiedlichen linken/rechten Reservoirdrücken ist die Randarbeit gesondert auszuweisen; die obige reine Dissipationsform gilt dann nicht unverändert.

## 5. Was P8b nicht behauptet

- (p_{m ext}) ist ein vorgegebener Reservoirdruck, kein hergeleitetes Kapillardruckgesetz.
- Die Geloberfläche bleibt geometrisch fest; Schrumpfung/Bewegung der freien Grenze ist nicht implementiert.
- Es gibt keine Verdunstung, keine Gasphase, keine Meniskusdynamik und keinen separaten Oberflächenwiderstand.
- Der Druckspeicher (S_p) bleibt eine lineare, unkalibrierte Schließung.
- Keine globale Existenz-/Eindeutigkeitstheorie für das nichtlineare chemo-poroelastische System.
- Keine empirische Validierung. Erzwungene Druckzellen-/Oedometerdaten bleiben aus natürlicher Synäresekalibrierungen ausgeschlossen.

## 6. Verifikation

`ccfsm_p8b_open_drainage.py` berechnet hydraulische Randflüsse, Druck-/Fluidkapazitätsentwicklung und den gekoppelten M/O/N/B-Transport. Die Tests prüfen Ausström-/Einströmvorzeichen, hydraulische Gesamtbilanz, Si-Randbilanz, Reaktions-Si-Erhaltung, Nullflussgrenze, Außenkonzentration bei Rückströmung und Druckdissipation.

Parameter (K,S_p,p_{m ext},c_{i,m ext}) sind Eingaben. Es werden keine Zahlen als experimentell bestimmt ausgegeben.

## 7. Nächste Stufen

- **P8c:** gemeinsame freie Energie bei variabler Fluidkapazität; osmotischer Druck und hydraulische Druckvariable thermodynamisch konsistent koppeln.
- **P8d/P9:** Kapillarrandbedingung und bewegliche freie Oberfläche, danach Biot-Mechanik und Brückeneigenverformung. Die Reihenfolge verhindert, dass eine willkürliche Randbedingung als Naturgesetz ausgegeben wird.
