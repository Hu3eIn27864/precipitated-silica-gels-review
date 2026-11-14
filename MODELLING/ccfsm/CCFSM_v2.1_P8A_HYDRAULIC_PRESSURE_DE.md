# CCFSM v2.1 – P8a: geschlossener Druck-Speicher-Darcy-Block

**Datum:** 14.11.2026  
**Ziel:** P8 erhält einen hydraulischen Drucklöser. Druck, Darcy-Fluss und Fluidkapazität werden nicht länger unabhängig vorgegeben.  
**Status:** linearer, semidiskreter 1D-Speicher-Darcy-Block mit positiver Zellpermeabilität und geschlossenem Rand, gekoppelt an P8-M/O/N/B-Transport. Softwareverifikation; kein vollständiger Biot-Mechaniklöser, keine offene freie Oberfläche, kein empirischer Nachweis.

## 1. Konstitutive Schließung ist erforderlich

Die Kontinuitätsgleichung allein
[
partial_t	heta+operatorname{Div}Q=0,qquad Q=-K
abla p
]
bestimmt (p,	heta,Q) nicht eindeutig. Es fehlt eine Speicher-/Kompressibilitätsbeziehung. P8a schließt den reduzierten hydraulischen Block ausdrücklich durch
[
	heta=	heta_{m ref}+S_p(p-p_{m ref}),qquad S_p>0.
	ag{P8a.1}
]
(S_p) hat die Einheit Pa(^{-1}), wenn (	heta) dimensionslos als Fluidvolumen pro Referenzvolumen geführt wird. Diese lineare Beziehung ist eine lokale Modellannahme in einem zulässigen Druckintervall, keine universelle Silica-Gel-Gleichung. Für Biot-Poroelastizität wäre sie später durch die gekoppelte Beziehung mit (operatorname{tr}arepsilon) und Biot-Koeffizient zu ersetzen.

Mit konstantem (S_p) folgt
[
S_ppartial_t p+operatorname{Div}Q=0,qquad
Q=-K
abla p,
]
also
[
S_ppartial_t p-operatorname{Div}(K
abla p)=0.
	ag{P8a.2}
]
Das Vorzeichen ist dissipativ: Multiplikation mit (p-p_{m ref}), Integration und No-Flow-Rand ergeben
[
rac{S_p}{2}rac{d}{dt}|p-p_{m ref}|_{L^2}^2
+int_{Omega_0}K|
abla p|^2,dX=0.
	ag{P8a.3}
]
Dies ist eine Druck-Abklingidentität des reduzierten hydraulischen Blocks, nicht die Gesamtenergieungleichung des chemo-poroelastischen Systems.

## 2. 1D-Finite-Volumen-Diskretisierung

Zellzentrierte Drücke (p_j), Zellpermeabilitäten (K_j>0), Zellkapazitäten
[
	heta_j=	heta_{{m ref},j}+S_{p,j}(p_j-p_{m ref})
]
und innere Flüsse
[
Q_{j+1/2}=-K_{j+1/2}rac{p_{j+1}-p_j}{Delta x},
quad
K_{j+1/2}=rac{2K_jK_{j+1}}{K_j+K_{j+1}}
	ag{P8a.4}
]
werden verwendet. Der harmonische Mittelwert respektiert serielle Widerstände. An beiden äußeren Flächen gilt (Q=0). Dann
[
dot	heta_j=-rac{Q_{j+1/2}-Q_{j-1/2}}{Delta x},
qquad
dot p_j=dot	heta_j/S_{p,j}.
	ag{P8a.5}
]
Der diskrete Druckoperator ist symmetrisch dissipativ; der Volumenmittelwert von (	heta) und – bei konstantem Speicherkoeffizienten – der Druckmittelwert bleiben erhalten. Die Kapazität bleibt nur solange physikalisch zulässig, wie (	heta_j>0); ein Zeitschrittverfahren muss diese Schranke erhalten.

## 3. Kopplung mit P8-Chemie und Transport

Der aus dem Druck berechnete Darcy-Fluss wird unverändert an den P8-Transportoperator übergeben. Damit gilt dieselbe Flussbilanz für Fluidkapazität und mobile Silica-Inventare:
[
dot m_i=-operatorname{Div}_{h}left(Qc_i-	heta D_i
abla_hc_iight)+R_i,
quad c_i=m_i/	heta.
	ag{P8a.6}
]
Die Zustandsableitungen werden gemeinsam zurückgegeben: ((dot m,dot p,dot	heta,Q)). N/B bleiben immobilisiert und werden nur durch Reaktionen verändert. Chemie wirkt hier über (c_i=m_i/	heta) auf die Reaktionsraten zurück; chemischer osmotischer Druck wirkt noch nicht auf die Druckgleichung zurück. Diese letzte Rückkopplung erfordert P8c und eine konsistente Variation der Gesamtenergie.

## 4. Randbedingungen und natürliche Synärese

P8a ist ein geschlossener No-Flow-Testblock. Er beschreibt Druckausgleich innerhalb eines geschlossenen Porenraums, nicht den Flüssigkeitsaustritt einer frei drainierenden natürlichen Synäreseprobe. Ein offener Rand benötigt einen physikalisch begründeten Kapillar-/Umgebungsdruck, eine Randflussbedingung und den dazu konsistenten Austrag mobiler Si-Spezies. Dies folgt in P8b; es wird hier nicht vorweggenommen.

## 5. Mathematischer Status

Für (S_p) beschränkt und strikt positiv sowie (K) beschränkt und strikt positiv ist der diskrete Druckoperator eine dissipative gewichtete Graph-Laplacian. Die Druck-Abklingidentität (P8a.3) und Erhaltung der mittleren Fluidkapazität folgen direkt aus Summation über Zellen und dem No-Flow-Rand. Das ist ein exakter semidiskreter Beweis für diesen linearen hydraulischen Teilblock.

Nicht bewiesen sind:
- Existenz/Regularität des vollständigen nichtlinearen Systems mit variabler, zustandsabhängiger Permeabilität;
- gemeinsame Biot-Mechanik (operatorname{Div}sigma=0);
- Rückwirkung osmotischer chemischer Potentiale auf hydraulischen Druck;
- Positivität unter beliebigen Zeitschrittverfahren;
- offene Drainage / natürliche freie Oberfläche;
- empirische Gültigkeit oder Kalibrierung von (S_p,K).

## 6. Tests und Freigabe

`ccfsm_p8a_hydraulic_pressure.py` berechnet Druck, Darcy-Flüsse, Fluidkapazität und koppelt die berechneten Flüsse an den P8-Chemieoperator. Die Tests prüfen Flussvorzeichen, harmonische Permeabilität, No-Flow-Ränder, Fluidkapazitätserhaltung, Druckmittelwert, Dissipationsidentität, Druck-zu-θ-Schließung und Si-Erhaltung.

Die Parameter (S_p,K,	heta_{m ref}) sind Eingaben ohne Literaturkalibrierung. P8a ist eine mathematisch geschlossene hydraulische Referenzkomponente, kein empirisch bestätigtes Gesetz für gefällte Kieselsäure.

## 7. Nächste Stufen

- **P8b:** offene freie-Oberflächen-Drainage mit Kapillar-/Umgebungsdruck und Si-Austragsbilanz.
- **P8c:** osmotischen Druck und variable-θ-Energie in einer gemeinsamen thermodynamischen Herleitung koppeln.
- **P9:** Biot-Mechanik, Brückeneigenverformung und Permeabilitätsrückkopplung zuschalten; nur mit expliziter Identifizierbarkeits- und Kalibrierungsstrategie.
