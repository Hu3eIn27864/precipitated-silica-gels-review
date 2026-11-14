# CCFSM v1.8 – P6: Konvexitätsaudit, schwache Teilformulierung und Existenzgrenzen

**Datum:** 14.11.2026  
**Geltungsbereich:** natürliche, unbelastete Synärese gefällter Silica-Gele; isothermer P5-Referenzzustand in Kleinverformung.  
**Status:** analytisches Teilresultat zur freien Energie und schwache Form des linearen Biot-Referenzblocks. Kein Existenzsatz für das vollständige nichtlineare chemo-poroelastische 3D-System und keine empirische Validierung.

## 1. Ergebnis des P5-Audits: Fluidkonjugierte Größe

P5 setzt θ = θ₀ + ζ und p = M_B(ζ − α_B tr ε). Die mobile Mischungsenergie hängt jedoch ebenfalls von θ ab, weil a_i = γ_i m_i/(θ c*) gilt. Bei festgehaltenen Inventaren folgt deshalb

    ∂Ψ/∂ζ = p − Π_osm,       Π_osm = RT(m_M + m_O)/θ = RT(c_M + c_O).

Der mechanische Biot-Porendruck p und das vollständige Energie-Konjugierte p − Π_osm sind unterschiedliche Größen. Das ändert die Darcy-Schließung Q = −K_p ∇p nicht.

Für ideale mobile Mischungen gilt Σ_i c_i ∇μ_i = ∇Π_osm. Der Fluidterm aus ∂tθ = −Div Q liefert in der Energiebilanz ∫∇(p−Π_osm)·Q; die mobile Advektion liefert ∫Q·∇Π_osm. Zusammen ergibt sich ∫∇p·Q = −∫∇p·K_p∇p. Die P5-Dissipation bleibt damit unter den dort genannten Annahmen konsistent; der osmotische Zwischenschritt muss aber explizit ausgewiesen werden. Der P5-Kernel gibt nun osmotischen Druck und vollständiges Fluidenergie-Konjugiertes aus und prüft die Ableitung per Finite Differenzen.

## 2. Konvexität des chemischen Zustandsblocks

Bis auf lineare Standardpotentiale lautet die mobile Mischungsenergie

    f(m_M,m_O,θ) = RT Σ_i m_i [ln(γ_i m_i/(θ c*)) − 1].

Für eine Variation (h_M,h_O,h_θ) ist die zweite Variation exakt

    D²f[h,h] = RT Σ_i m_i (h_i/m_i − h_θ/θ)² ≥ 0.

Die Hesse-Matrix ist also positiv semidefinit. Die Nullrichtung entspricht gemeinsamer Skalierung: h_i/m_i = h_θ/θ. Die Netzwerk-Entropien haben die zweite Variation RT(h_N²/s_N + h_B²/s_B) ≥ 0.

**Satz P6.1 (konvexer Referenz-Energieblock).** Wenn die Brückeneigenverformung ausgeschaltet (β_B = 0) oder die Brückenfraktion fest vorgegeben ist, und G > 0, λ ≥ 0, M_B > 0 gelten, ist die P5-Energiedichte als Funktion von (ε, ζ, m_M, m_O, s_N, s_B) auf θ > 0, m_i > 0, s_i > 0 konvex. Elastische Quadratik, Biot-Speicherenergie und chemische Entropien sind konvex; Standardpotentiale sind linear.

Das ist ein Konvexitätsresultat für die lokale Energie, kein Existenzsatz für die zeitabhängige PDE.

## 3. Variable Brückeneigenverformung: Nichtkonvexität und untere Schranke

Für β_B > 0 hängt ε_ch = β_B(b−b₀)I mit b = s_B/(s_N+s_B+δ_B) nichtlinear von den Netzwerkzuständen ab. Der Term ½(ε−ε_ch):C:(ε−ε_ch) ist im Allgemeinen nicht gemeinsam konvex in (ε,s_N,s_B). Eine globale Konvexitätsbehauptung für P5 wäre unzulässig.

Da 0 ≤ b ≤ 1 gilt, ist die Eigenverformung beschränkt:

    ||ε_ch||_F ≤ √3 β_B max(b₀, 1−b₀).

Bei festem β_B bleibt die elastische Energie nach unten durch eine koerzive quadratische Form in ε minus einer endlichen Konstanten abschätzbar. Zusammen mit M_B > 0 kontrolliert der Biot-Speicherterm ζ − α_B tr ε. Diese untere Schranke ersetzt keine Konvexität und beweist für sich allein keine Existenz des gekoppelten Systems.

## 4. Schwache Form des linearen Biot-Referenzblocks

Wir übernehmen die P0-Annahmen: beschränktes Lipschitz-Gebiet Ω in R³, homogene Dirichlet-Bedingung für u, No-Flow-Rand für das Fluid, zeitunabhängige symmetrisch positiv definite Elastizität C, M_B > 0 und gleichmäßig elliptische Darcy-Mobilität K_p. Setze V = H¹₀(Ω;R³), H = L²(Ω), Q = H¹(Ω).

Für jedes p ∈ H sei T p ∈ V die eindeutige Lösung

    ∫Ω C ε(Tp):ε(v) dx = ∫Ω α_B p Div(v) dx   für alle v ∈ V.

Definiere

    m(p,r) = ∫Ω [M_B⁻¹ p r + α_B Div(Tp) r] dx,
    ℓ(p,r) = ∫Ω K_p ∇p·∇r dx.

Die reduzierte schwache Druckgleichung lautet

    <∂t p,r>_(Q',Q) + ℓ(p,r) = <s_f,r>,   p(0)=p₀,   für alle r ∈ Q.

Unter den P0-Annahmen ist m stetig und koerziv auf H, ℓ stetig und nichtnegativ auf Q. Die abstrakte lineare parabolische Evolutionsformulierung liefert für p₀ ∈ H und s_f ∈ L²(0,T;Q') eine eindeutige schwache Lösung p ∈ L²(0,T;Q) ∩ C([0,T];H), mit ∂t p ∈ L²(0,T;Q'). Die Verschiebung ist u = Tp. Dies ist der lineare Biot-Referenzsatz aus P0, hier als Grenzfall der P6-Architektur wiederverwendet; P6 behauptet keinen neuen Existenzsatz für P1–P5.

## 5. Warum der volle P5-Beweis offen bleibt

Für das vollständige P5-System müssen zusätzlich gemeinsam behandelt werden: (i) nichtlineare, zustandsabhängige Eigenverformung; (ii) positive Fluidkapazität und c_i=m_i/θ; (iii) Advektion c_i Q; (iv) logarithmische Potentiale bei Konzentrationen gegen null; (v) Reaktionsquellen und Quasi-Positivität; (vi) natürliche Drainage- und Oberflächenrandbedingungen. Eine tragfähige Route benötigt regularisierte Entropien, uniforme Energie- und Zeitderivierten-Schranken, kompakte Konvergenz der nichtlinearen Produkte und einen Grenzübergang, der Stoffbilanz und Dissipation erhält. Diese Schritte folgen nicht automatisch aus der formalen P5-Energieidentität.

## 6. Code und Freigabestatus

- ccfsm_p6_convexity.py wertet die analytische quadratische Form und eine explizite Schranke für die Eigenverformung aus.
- test_ccfsm_p6_convexity.py prüft Nichtnegativität, die exakte Nullrichtung, Skalierung und Randfälle.
- P5-Tests prüfen zusätzlich die Ableitung der Energie nach ζ einschließlich des osmotischen Terms.

**P6-Freigabe:** Konvexität des chemischen Referenzblocks und schwache Existenz des linearen Biot-Blocks: grün unter den aufgelisteten Annahmen. Globale Existenz des nichtlinearen chemo-poroelastischen P5-Systems: offen. Empirische Gültigkeit und Identifizierbarkeit der Eigenverformung: offen.
