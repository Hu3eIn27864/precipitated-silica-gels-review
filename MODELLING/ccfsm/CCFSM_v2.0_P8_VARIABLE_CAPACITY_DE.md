# CCFSM v2.0 – P8: variable Fluidkapazität und chemo-hydraulische Rückkopplung

**Datum:** 14.11.2026  
**Geltungsbereich:** natürliche, mechanisch unbelastete Synärese; isothermer Referenzkörper; mobile M/O-Spezies und immobilisierte Netzwerkpools N/B.  
**Status:** konservative gekoppelte Bilanz und semidiskreter 1D-Referenzoperator. Darcy-Fluss wird vorgegeben; keine vollständige Biot-Darcy-Lösung, kein nichtlinearer Existenzsatz und keine empirische Kalibrierung.

## 1. Ziel und Abgrenzung

P8 führt die variable Fluidkapazität aus P4 mit der Phasentrennung und Reaktionskette aus P5/P7 zusammen. Anders als P7 ist θ nicht konstant. Der mobile Zustand wird als Referenzinventar (m_i) gespeichert; die Porenfluidkonzentration ist (c_i=m_i/θ). Die Änderung von θ wird aus derselben diskreten Darcy-Bilanz bestimmt, die auch den advektiven Speziesfluss antreibt.

Diese Kopplung ist ein echter Fortschritt gegenüber P7: Kompression/Drainage verändert die Konzentration, und der Konzentrationszustand verändert dadurch wiederum die Reaktionsraten. Sie ist aber noch keine vollständige bidirektionale Mechanik-Chemie-Kopplung. Der Darcy-Fluss (Q) ist Eingabe des Operators und muss außerhalb durch einen mit θ konsistenten hydraulischen/mechanischen Löser geliefert werden. Insbesondere löst P8 weder (operatorname{Div}σ=0) noch (Q=-mathbb K_p
abla p).

## 2. Zustände und Einheiten

In der festen Referenzkonfiguration Ω0:
- (θ>0): Fluidkapazität pro Referenzvolumen (m³ Fluid/m³ Referenzkörper);
- (m_M,m_O): mobile Si-Äquivalentinventare pro Referenzvolumen (mol/m³ Referenzkörper);
- (s_N,s_B): immobilisierte Netzwerk-Si-Inventare pro Referenzvolumen;
- (c_M=m_M/θ, c_O=m_O/θ): mobile Konzentrationen pro Porenfluidvolumen;
- (Q): Darcy-Volumenfluss pro Referenzfläche (m/s);
- (D_M,D_O): effektive Referenz-Diffusionskoeffizienten (m²/s).

N/B werden nicht mit dem Porenwasser advectiert. Diese Trennung folgt der P5-Modellentscheidung; der ältere P4-Vier-Spezies-Transport bleibt ein separater vereinfachter Zweig.

## 3. Kontinuierliche Bilanzstruktur

Die quellfreie Fluidbilanz lautet
[
partial_tθ+operatorname{Div}Q=0.
	ag{P8.1}
]
Für die mobilen Inventare gilt konservativ
[
partial_t m_i+operatorname{Div}left(c_iQ-θ D_i
abla c_iight)=R_i,
quad c_i=m_i/θ,quad i=M,O.
	ag{P8.2}
]
Die immobilisierten Pools erfüllen
[
partial_t s_N=R_N,qquad partial_t s_B=R_B.
	ag{P8.3}
]
Die lokalen Reaktionsraten sind im P8-Referenzoperator die detailliert balancierte, mechanisch entkoppelte P5-Grenzkinetik
[
a=(gamma_Mm_M/(θ c_*),gamma_Om_O/(θ c_*),
gamma_Ns_N/c_*,gamma_Bs_B/c_*),
]
[
r_j=k_jc_*(a_j-a_{j+1}/K_j),quad
R=(-r_1,r_1-r_2,r_2-r_3,r_3).
	ag{P8.4}
]
Damit ist (sum_iR_i=0). Die mechanischen Potentialbeiträge aus P5 sind hier ausgeschaltet; würde man sie zuschalten, müsste man die Gesamtenergie und die Reaktionsmobilität gemeinsam erneut herleiten.

Aus (P8.1) und (P8.2) folgt für hinreichend glatte Felder
[
θ,partial_t c_i+Qcdot
abla c_i
-operatorname{Div}(θ D_i
abla c_i)=R_i.
	ag{P8.5}
]
Die konservative Inventarform (P8.2) ist maßgeblich für schwache Form und Diskretisierung. Die Konzentrationsform zeigt explizit, dass die Fluidkapazitätsänderung nicht als zusätzlicher, frei wählbarer Verdünnungsterm eingeführt werden darf: Sie folgt bereits aus der Fluidbilanz.

## 4. Diskrete Kopplung und Erhaltung

Auf einem uniformen 1D-Referenzgitter mit Zellweite Δx werden orientierte innere Flüsse (Q_{j+1/2}) verwendet; an beiden äußeren Rändern gilt für den hier geprüften geschlossenen Referenzfall (Q=0) und kein diffusive Speziesfluss. Für jede Zelle:
[
dotθ_j=-rac{Q_{j+1/2}-Q_{j-1/2}}{Δx}.
	ag{P8.6}
]
Der mobile Gesamtfluss an einer inneren Fläche ist
[
F_{i,j+1/2}=Q_{j+1/2}c_{i,up}
-θ_{j+1/2}D_irac{c_{i,j+1}-c_{i,j}}{Δx},
	ag{P8.7}
]
mit Upwind-Konzentration und arithmetischem θ-Flächenmittel. Die Inventarableitung ist
[
dot m_{i,j}=-rac{F_{i,j+1/2}-F_{i,j-1/2}}{Δx}+R_{i,j}.
	ag{P8.8}
]
Die N/B-Ableitungen sind (R_{N,j},R_{B,j}). Damit teleskopieren die inneren Flüsse exakt. Bei geschlossenen Rändern folgt
[
rac{d}{dt}int_{Ω0}(m_M+m_O+s_N+s_B),dX=0,
qquad
rac{d}{dt}int_{Ω0}θ,dX=0.
	ag{P8.9}
]
Dies sind semidiskrete Identitäten, keine Aussage über beliebige explizite Zeitschritte.

## 5. Positivität, zulässiger Zustandsraum und mathematischer Status

Der Operator akzeptiert nur endliche, nichtnegative Inventare, strikt positive Fluidkapazität, nichtnegative Diffusivitäten und einen endlichen Darcy-Fluss mit geschlossenen äußeren Randwerten. Die kontinuierliche lineare Reaktionsgrenzkinetik ist kooperativ und Si-erhaltend. Die Upwind-Flüsse sind konservativ. Diese Eigenschaften stützen die Positivitätsstruktur des reduzierten Systems; eine konkrete Zeitintegration muss zusätzlich eine geeignete positivity-preserving Schrittweiten-/CFL-Bedingung erfüllen.

**Nicht behauptet wird:** ein globaler Existenz- oder Eindeutigkeitssatz für das gekoppelte nichtlineare System mit unbekanntem (u,p,Q,θ,m,s). Auch die Existenz des P7-Satzes lässt sich nicht einfach übertragen: variable θ, die Abhängigkeit (c=m/θ) und die Fluidbilanz ändern den Operator. Für einen Satz wären mindestens gleichmäßige Schranken (0<θ_*leθleθ^*), geeignete Regularität/Kontrolle von (Q), positive Diffusion und eine präzise Evolutionsgleichung für das hydraulische Feld nachzuweisen.

## 6. Energiefrage – bewusst offen

P5 zeigt, dass bei idealer mobiler Mischung der Fluid-Energiekonjugierte einen osmotischen Beitrag enthält. P8 ändert θ zeitlich und darf deshalb die P7/P5-Energieidentität nicht unverändert übernehmen. Der vorliegende Code beansprucht keinen diskreten oder kontinuierlichen Gesamtenergiebeweis. Vor einer solchen Aussage müssen die freie Energie (m_i[ln(m_i/(θ c_*))-1]), der Fluidkonjugierte, der Druckfluss und die Randarbeit auf derselben Referenzbasis variiert und gekoppelt werden. Insbesondere ist zu prüfen, welche hydraulische Druckvariable die Darcy-Gesamtdissipation erzeugt.

## 7. Natürliche Synärese und Randbedingungen

Die Implementierung prüft zunächst einen geschlossenen No-Flux-Referenzkörper, um die inneren Bilanzidentitäten isoliert zu verifizieren. Natürliche Synärese kann jedoch über eine freie Oberfläche Flüssigkeit abgeben. Dafür ist ein offener Rand mit physikalisch begründetem Druck-/Kapillarrandwert und ausströmender Spezieskonzentration nötig. Ein solcher Rand darf nicht durch die hier verwendete Nullflussbedingung ersetzt werden. Die erzwungene Druckzellen- und Oedometerdaten bleiben aus der natürlichen Synäresekalibrierung ausgeschlossen.

## 8. Implementierung und Prüfungen

- `ccfsm_p8_variable_capacity.py`: semidiskreter 1D-Finite-Volumen-Operator; θ-Bilanz, mobile M/O-Advektion/Diffusion in Inventarform, immobilisierte N/B und lokale Reaktion.
- `test_ccfsm_p8_variable_capacity.py`: Fluidkapazitätserhaltung, Gesamt-Si-Erhaltung, Spezieserhaltung ohne Reaktion, gleichförmige Konzentration unter Fluidbewegung, Nullflussgrenze, Eingabevalidierung.
- Kein Zeitintegrator, kein Druck-/Mechaniklöser, kein 2D/3D-Solver, keine Kalibrierung.

## 9. Nächste Freigabestufen

1. P8a: hydraulischen Drucklöser und θ-Evolution so koppeln, dass (Q=-mathbb K_p
abla p) und (dotθ+operatorname{Div}Q=0) gemeinsam erfüllt sind.
2. P8b: offene natürliche Drainagerandbedingungen mit expliziter Flüssigkeits- und Siliciumabgabe formulieren.
3. P8c: gemeinsame freie Energie für variable θ, osmotischen Druck und Biot-Speicherung variieren; erst dann eine Energieungleichung beweisen.
4. P9: Brückeneigenverformung und Brücken-Permeabilitäts-Rückkopplung mit identifizierbaren bzw. klar als Hypothesen markierten Parametern zuschalten.

Alle Transport-, Reaktions- und hydraulischen Parameter bleiben unkalibriert. P8 ist ein Bilanz- und Softwareverifikationsschritt für natürliche Synärese, keine empirische Bestätigung des CCFSM.
