# CCFSM v2.3 – P8c: thermodynamische Schließung bei variabler Fluidkapazität

**Datum:** 14.11.2026  
**Geltungsbereich:** natürliche Synärese gefällter Silica-Gele; isothermer, gesättigter Referenzkörper; mobile Pools M/O und immobilisierte Netzwerkpools N/B.  
**Status:** analytische lokale Energieableitungen plus semidiskreter 1D-Referenzoperator. Formale Dissipationsstruktur im geschlossenen, glatten Fall. Keine empirische Kalibrierung und kein globaler Existenzsatz des vollständigen nichtlinearen PDE-Systems.

## 1. Kernfrage: zwei verschiedene Drücke

P5/P6 zeigen, dass die mobile ideale Mischungsenergie von der Fluidkapazität \(\theta\) abhängt. Deshalb ist der Energie-Konjugierte zur Fluidkapazität nicht einfach der mechanische Biot-/Speicherdruck.

Wir verwenden die lokale Energie pro Referenzvolumen
\[
\Psi(\theta,m_M,m_O,s_N,s_B)
=\Psi_h(\theta)+RT\sum_{i=M,O}m_i\left[\ln\frac{\gamma_i m_i}{\theta c_*}-1\right]
+RT\sum_{i=N,B}s_i\left[\ln\frac{\gamma_i s_i}{c_*}-1\right]
+\sum_i\mu_i^0 n_i .
\tag{P8c.1}
\]
Die Standardpotentiale sind konsistent mit \(\mu_{i+1}^0=\mu_i^0-RT\ln K_i\). Die hydraulische Speicherenergie wird als explizite Referenzschließung gewählt:
\[
\Psi_h(\theta)=p_{ref}(\theta-\theta_{ref})
+\frac{(\theta-\theta_{ref})^2}{2S_p},
\qquad
p=p_{ref}+\frac{\theta-\theta_{ref}}{S_p}.
\tag{P8c.2}
\]
Damit folgt exakt
\[
\boxed{\frac{\partial\Psi}{\partial\theta}
=p-\Pi_{osm}},\qquad
\Pi_{osm}=RT(c_M+c_O)=RT\frac{m_M+m_O}{\theta}.
\tag{P8c.3}
\]
Die chemischen Potentiale sind \(\mu_i=\partial\Psi/\partial n_i\). Für M/O gilt \(\mu_i=\mu_i^0+RT\ln(\gamma_i m_i/(\theta c_*))\); für N/B entfällt der Faktor \(\theta\).

**Entscheidend:** \(p\) treibt weiterhin den Darcy-Fluss \(Q=-K\nabla p\). Der vollständige Fluidenergie-Konjugierte \(p-\Pi_{osm}\) ist nicht an dessen Stelle einzusetzen. Das folgt aus der gemeinsamen Variation der Fluidenergie und der mobilen Advektion.

## 2. Gibbs-Duhem-Kompensation

Für ideale mobile Pools mit konstantem \(T,\gamma_i\) gilt
\[
\sum_{i=M,O}c_i\nabla\mu_i
=RT\sum_i c_i\nabla\ln c_i
=\nabla\left[RT(c_M+c_O)\right]
=\nabla\Pi_{osm}.
\tag{P8c.4}
\]
Die Fluidbilanz \(\partial_t\theta+\operatorname{Div}Q=0\), multipliziert mit \(p-\Pi_{osm}\), liefert nach partieller Integration den Beitrag \(\nabla(p-\Pi_{osm})\cdot Q\). Die mobile Advektion \(c_iQ\), multipliziert mit \(\nabla\mu_i\), liefert \(Q\cdot\nabla\Pi_{osm}\). Zusammen bleibt
\[
\nabla p\cdot Q=-\nabla p\cdot K\nabla p\le0.
\tag{P8c.5}
\]
Damit wird die hydraulische Dissipation durch den mechanischen Druck gesteuert, obwohl die Energieableitung nach \(\theta\) den osmotischen Term enthält.

## 3. Diffusion und Reaktion

Die thermodynamisch konsistente mobile Diffusionsflussdichte ist
\[
\mathcal J_i=-\frac{D_i m_i}{RT}\nabla\mu_i
=-\theta D_i\nabla c_i
\tag{P8c.6}
\]
für konstante Aktivitätskoeffizienten und ideale Aktivitäten. Dies ist die P8-Fick-Form.

Für die Kette M ⇌ O ⇌ N ⇌ B setzen wir \(a_i=\gamma_i n_i/(\theta c_*)\) für M/O und \(a_i=\gamma_i n_i/c_*\) für N/B. Mit \(x_i=a_i\), \(y_i=a_{i+1}/K_i\), Affinität \(\mathcal A_i=\mu_i-\mu_{i+1}=RT\ln(x_i/y_i)\) und logarithmischem Mittelwert
\[
\Lambda(x,y)=\frac{x-y}{\ln x-\ln y}>0
\]
lautet die Rate
\[
r_i=\frac{k_i c_*}{RT}\Lambda(x_i,y_i)\mathcal A_i.
\tag{P8c.7}
\]
Folglich \(r_i\mathcal A_i\ge0\), und die Reaktionsquellen \((-r_1,r_1-r_2,r_2-r_3,r_3)\) erhalten lokales Gesamt-Si exakt. N/B bleiben immobilisiert.

## 4. Formale Gesamtenergiebilanz

Für glatte positive Lösungen, konstante Temperatur und Aktivitätskoeffizienten, positive \(S_p,K\), nichtnegative \(D_i,k_i\), quasistatische/arbeitsfreie Mechanik (hier im P8c-Referenzblock ausgeschaltet) und geschlossene No-Flux-Ränder ergibt sich formal
\[
\frac{d}{dt}\int_{\Omega_0}\Psi\,dX
=-\int_{\Omega_0}\nabla p\cdot K\nabla p\,dX
-\int_{\Omega_0}\sum_{i=M,O}\frac{D_i m_i}{RT}|\nabla\mu_i|^2\,dX
-\int_{\Omega_0}\sum_{j=1}^3r_j\mathcal A_j\,dX
\le0.
\tag{P8c.8}
\]
Dies ist eine formale Identität unter Glattheits- und Positivitätsannahmen, kein schwacher Existenzsatz. Bei offenen P8b-Rändern kommen hydraulische Arbeit sowie chemische Energie- und Diffusionsrandflüsse hinzu. Sie müssen als Reservoir-Leistung bilanziert werden; die geschlossene Ungleichung darf nicht unverändert auf offene Ränder übertragen werden.

## 5. Semidiskrete Implementierung

- ccfsm_p8c_thermodynamic_closure.py berechnet freie Energie, chemische Potentiale, osmotischen Druck und das vollständige Fluidenergie-Konjugierte.
- Der gekoppelte Operator übernimmt den hydraulischen Druck-/Darcy-Block aus P8b, verwendet logarithmische Mittelwert-Reaktionen und dieselben konservativen mobilen Randflüsse.
- Die Tests prüfen die Ableitung \(\partial_\theta\Psi=p-\Pi_{osm}\), chemische Potentialableitungen, nichtnegative Reaktionsdissipation, lokale Si-Erhaltung, mechanischen Darcy-Druck und offene Randbilanz.

Die lineare hydraulische Energie \(\Psi_h\) ist die zur P8a-Speicherbeziehung passende konstitutive Wahl. Sie ist nicht aus direkten Silica-Messungen bestimmt. Aktivitätskoeffizienten sind hier konstant; nichtideale Mischungen benötigen eine konsistente Aktivitäts-/Exzessenergie.

## 6. Mathematische und empirische Grenzen

**Exakt hergeleitet:** lokale Energieableitungen (P8c.3), Gibbs-Duhem-Kompensation für ideale mobile Pools (P8c.4), algebraische Nichtnegativität der logarithmischen Reaktionsdissipation und lokale Si-Erhaltung der Reaktionskette.

**Formal unter glatten positiven Lösungen:** geschlossene Gesamtenergiedissipation (P8c.8).

**Konstitutive Hypothesen:** lineare Speicherenergie/\(S_p\), ideale mobile und Netzwerk-Mischungsenergie, konstante Aktivitätskoeffizienten, Fick-Diffusion, lokale Reaktionskette.

**Nicht bewiesen/nicht validiert:** globaler schwacher Existenzsatz des vollständigen nichtlinearen chemo-poroelastischen Systems; freie Grenzflächenbewegung; Kapillargesetz; nichtideale Elektrolyt-/Silica-Aktivitäten; Empirie/Kalibrierung von \(S_p,K,D_i,k_i\). Keine erzwungenen Druckzell- oder Oedometerdaten werden zur natürlichen Synäresekalibrierung verwendet.

## 7. Grenzfälle und Anschluss

- Ohne mobile Konzentrationen ist \(\Pi_{osm}=0\); P8c reduziert hydraulisch auf den P8a-Speicher-Darcy-Block.
- Bei konstantem \(\theta\) und ohne Druckentwicklung bleibt die lokale Chemie-/Reaktionsstruktur aus P5 erhalten.
- Mit offenen Druck- und Speziesreservoirs folgt die P8b-Randbilanz; die Energie erhält zusätzliche Reservoirterme.
- P9 kann die P5-Brückeneigenverformung und Biot-Mechanik wieder zuschalten, sobald die Energievariation einschließlich mechanischer Arbeit vollständig konsistent implementiert ist.
