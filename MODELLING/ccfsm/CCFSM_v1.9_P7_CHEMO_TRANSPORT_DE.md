# CCFSM v1.9 – P7: räumlicher chemo-hydraulischer Reaktionstransport

**Datum:** 14.11.2026  
**Geltungsbereich:** natürliche, unbelastete Synärese; isothermer Referenzzustand, konstante positive Fluidkapazität, linearer Biot-Druckfluss aus P6.  
**Status:** schwache Existenztheorie für einen triangularen Teilblock und konservativer Finite-Volumen-Referenzoperator. Keine globale Existenz des voll rückgekoppelten P5-Systems; keine empirische Kalibrierung.

## 1. Ziel und Modellreduktion

P7 erweitert den P6-Druckblock um räumlichen Transport und die P5-Reaktionskette. Die Biot-Lösung wird zuerst bestimmt; ihr Darcy-Fluss Q(x,t) wird anschließend als vorgegebener Transportfluss verwendet. Chemie beeinflusst Q in P7 noch nicht zurück. Diese Dreiecksstruktur ist bewusst gewählt, damit ein belastbarer Existenzsatz möglich ist.

Die Fluidkapazität θ>0 wird konstant gehalten, die Brückeneigenverformung β_B wird für diesen Existenzblock ausgeschaltet. Die vier Si-äquivalenten Inventare pro Referenzvolumen heißen m_M,m_O,s_N,s_B. M/O sind mobil; N/B sind im Netzwerk immobilisiert.

## 2. PDE-System

In einem beschränkten Gebiet Ω⊂Rᵈ sei v=Q/θ ein vorgegebener Transportgeschwindigkeitsvektor. Für i=M,O gilt

    ∂t m_i + div(v m_i − D_i grad m_i) = R_i(U),

und für die immobilisierten Pools

    ∂t s_N = R_N(U),       ∂t s_B = R_B(U).

Die Reaktionsraten sind die detailliert balancierten linearen P5-Grenzraten

    r_j = k_j c* (a_j − a_(j+1)/K_j),
    R = (−r_1, r_1−r_2, r_2−r_3, r_3),

mit a_M=γ_M m_M/(θ c*), a_O=γ_O m_O/(θ c*), a_N=γ_N s_N/c*, a_B=γ_B s_B/c*. Die Reduktion der logarithmischen Mittelkinetik auf diese Form gilt bei abgeschalteter mechanischer Rückkopplung, denn Λ(x,y)(ln x−ln y)=x−y. Randbedingung: (v m_i−D_i∇m_i)·n=0.

## 3. Schwache Existenz: präziser Satz

**Annahmen.** Ω ist beschränkt und Lipschitz; θ>0 und D_M,D_O>0 konstant; v∈L∞(0,T;W¹,∞(Ω;Rᵈ)), div v=0 und v·n=0 auf ∂Ω; k_j≥0, K_j>0, γ_i>0; U₀=(m_M,m_O,s_N,s_B)∈L²(Ω)⁴∩L∞(Ω)⁴ ist nichtnegativ.

Unter diesen Annahmen ist R(U)=A U eine lineare Abbildung mit konstanten Koeffizienten. Ihre Matrix ist Metzler (alle außerdiagonalen Einträge nichtnegativ) und 1ᵀA=0. Der Transport-Diffusionsoperator ist linear und parabolisch auf den mobilen Komponenten; die Netzwerkkomponenten erfüllen gekoppelte lineare Evolutionsgleichungen am Ort.

**Satz P7.1.** Es existiert genau eine nichtnegative Lösung mit m_M,m_O∈L²(0,T;H¹(Ω))∩C([0,T];L²(Ω)), s_N,s_B∈C([0,T];L²(Ω)) und ∂t m_i∈L²(0,T;H¹(Ω)′). Die Lösung hängt stetig von den Anfangsdaten in L² ab. Für fast alle t gilt

    ∫Ω (m_M+m_O+s_N+s_B)(t) dx = ∫Ω (m_M+m_O+s_N+s_B)(0) dx.

**Begründung.** Die mobilen Operatoren mit gleichmäßig elliptischem D_i und beschränktem v erzeugen eine Evolutionshalbgruppe. Die Netzwerkkomponenten werden durch Variation der Konstanten an die mobilen Komponenten gekoppelt. Da A beschränkt ist, liefert die Duhamel-Formel eine eindeutige Lösung im Produkt-L²-Raum. Positivität folgt aus der kooperativen Struktur (Metzler-Matrix) und der Positivität des Advektions-Diffusionsflusses. Summiert man die vier Gleichungen, heben sich die Reaktionsraten exakt auf; die Randflüsse verschwinden, also ist die Gesamt-Si-Menge konstant. Das ist ein Existenzsatz für den reduzierten, vorgegebenen-Fluss-Block, nicht für das vollständig rückgekoppelte CCFSM.

## 4. Energie- und Dissipationshinweis

Für strikt positive Zustände ist die ideale chemische freie Energie konvex. Reaktionen dissipieren sie aufgrund detaillierter Balance. Diffusion dissipiert die mobile Mischungsenergie. Bei divergenzfreiem v und undurchlässigem Rand trägt die Advektion keine Änderung der integrierten chemischen Energie bei. Der P7-Code prüft Stoffbilanz und Flusskonservativität; er implementiert keinen Zeitintegrator und beansprucht keinen diskreten Entropiebeweis für beliebige Zeitschritte.

## 5. Finite-Volumen-Referenzoperator

ccfsm_p7_chemo_transport.py implementiert in 1D: mobile M/O mit Upwind-Darcy-Advektion und zentraler Diffusion; immobilisierte N/B ohne Transport; lokale detailliert balancierte Reaktionsquellen; geschlossene Nullflussränder und konservative interne Flüsse. Der Operator ist semidiskret. Ein expliziter Integrator, CFL-Steuerung, variable Porosität, nichtlineare Mechanik und 2D/3D-Löser sind nicht enthalten.

## 6. Grenzen und nächste mathematische Schritte

1. Variable θ und die vollständige Biot-Speicherung mit Chemiequelle koppeln.
2. Rückwirkung der Brückenfraktion auf Eigenverformung, Spannung und Darcy-Mobilität zuschalten.
3. Konzentrationsgrenzen bei Null und degenerierende Mobilitäten behandeln.
4. Natürliche Drainage-/Oberflächenrandbedingungen aus den realen Versuchsgeometrien formulieren.
5. Erst dann den Existenzbeweis von der Dreiecksstruktur auf ein nichtlineares geschlossenes System erweitern.

Alle D_i, k_j, K_j, γ_i und hydraulischen Koeffizienten bleiben unkalibriert oder sind reine Testwerte. Natürliche Synärese bleibt der einzige Anwendungszweck; erzwungene Druckzell- und Oedometerdaten werden nicht verwendet.