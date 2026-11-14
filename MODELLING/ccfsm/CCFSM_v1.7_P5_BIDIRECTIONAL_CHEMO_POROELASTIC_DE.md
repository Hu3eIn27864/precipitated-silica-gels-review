# CCFSM v1.7 – P5: bidirektionale chemo-poroelastische Kopplung

**Datum:** 14.11.2026  
**Geltungsbereich:** natürliche, unbelastete Synärese gefällter Silica-Gele; isothermer, gesättigter, kleinverformter Referenzkörper.  
**Status:** thermodynamisch konsistente Modellschließung unter expliziten Annahmen plus lokaler konstitutiver Referenzkernel. Kein vollständiger PDE-Solver, kein globaler Existenzsatz für das nichtlineare 3D-System und keine empirische Kalibrierung.

## 1. Ziel und bewusste Modellentscheidung

P5 verbindet Mechanik, Porenfluid und Chemie bidirektional. Die wesentliche Änderung gegenüber P3/P4 betrifft die Phasenrolle der vier Si-Pools:

- \(M,O\): mobile gelöste Pools im Porenfluid;
- \(N,B\): immobilisierte, netzwerkgebundene Si-Pools im Feststoffgerüst.

Diese Zuordnung ist eine explizite Modellhypothese und physikalisch plausibler als alle vier Pools ohne Unterscheidung mit dem Porenwasser zu advectieren. P5 verwendet daher nicht unverändert den P4-Transportoperator für \(N,B\). P4 bleibt der konservative Transportprototyp; P5 führt mobile und immobilisierte Inventare getrennt.

Wir arbeiten in einer festen Referenzkonfiguration \(\Omega_0\) und im Kleinverformungsbereich. \(u\) ist die Verschiebung, \(\varepsilon(u)=\tfrac12(\nabla u+\nabla u^T)\), \(e_v=\operatorname{tr}\varepsilon\). Das Modell ist eine Biot-Näherung und keine finite-strain-Fortsetzung von P4.

## 2. Zustände und Einheiten

Die Fluidkapazität pro Referenzvolumen ist
\[
\theta=\theta_0+\zeta>0,
\]
wobei \(\theta_0\) die Referenz-Fluidkapazität und \(\zeta\) die Biot-Fluidgehaltsänderung ist. Es gilt
\[
\zeta=\alpha_B\operatorname{div}u+\frac{p}{M_B},
\qquad
p=M_B(\zeta-\alpha_B\operatorname{div}u).
\tag{P5.1}
\]
\(p\) ist der Biot-Porendruck, \(M_B>0\) der Biot-Modul und \(\alpha_B\in[0,1]\) der Biot-Koeffizient.

Die mobilen Inventare \(m_M,m_O\) und die immobilisierten Inventare \(s_N,s_B\) werden in mol Si-Äquivalent pro m³ Referenzvolumen gemessen. Die mobilen Porenfluidkonzentrationen sind
\[
c_M=m_M/\theta,\qquad c_O=m_O/\theta.
\]
Die Netzwerkaktivitäten werden aus \(s_N,s_B\) gebildet. Alle vier Inventare sind nichtnegativ. Die aktuelle Referenzformulierung setzt \(m_M,m_O,s_N,s_B>0\) voraus, damit die idealen chemischen Potentiale endlich sind; Nullzustände sind über Grenzwerte bzw. regularisierte Numerik zu behandeln.

## 3. Gemeinsame freie Energie

Die Brückenfraktion wird regularisiert als
\[
b=\frac{s_B}{s_N+s_B+\delta_B},\qquad \delta_B>0.
\]
Die chemisch induzierte isotrope Eigenverformung ist die prüfbare Schließung
\[
\varepsilon^{ch}(b)=\beta_B(b-b_0)I.
\tag{P5.2}
\]
\(\beta_B\) und \(b_0\) sind unkalibrierte Materialparameter; (P5.2) ist keine bereits nachgewiesene Silica-Konstitutivbeziehung.

Mit isotroper linearer Elastizität \(C:e=2G e+\lambda\operatorname{tr}(e)I\) definieren wir
\[
\begin{aligned}
\Psi(\varepsilon,\zeta,m_M,m_O,s_N,s_B)
={}&\frac12(\varepsilon-\varepsilon^{ch}):C:(\varepsilon-\varepsilon^{ch})\\
&+\frac{M_B}{2}(\zeta-\alpha_B\operatorname{tr}\varepsilon)^2\\
&+\sum_{i=M,O}m_i[\mu_i^0+RT(\ln a_i-1)]\\
&+\sum_{i=N,B}s_i[\mu_i^0+RT(\ln a_i-1)].
\end{aligned}
\tag{P5.3}
\]
Für mobile Pools \(a_i=\gamma_i m_i/(\theta c_*)\); für Netzwerkpools \(a_i=\gamma_i s_i/c_*\). Die Standardpotentiale werden konsistent mit den P2-Gleichgewichtskonstanten gesetzt:
\[
\mu^0_{i+1}=\mu^0_i-RT\ln K_i.
\]
Die Energie ist pro Referenzvolumen (J/m³ Referenzvolumen).

## 4. Konjugierte Größen und Rückkopplung

Ableitung derselben Energie liefert
\[
\sigma=C:(\varepsilon-\varepsilon^{ch})-\alpha_BpI,
\qquad
p=M_B(\zeta-\alpha_B\operatorname{tr}\varepsilon).
\tag{P5.4}
\]
Damit beeinflusst die Brückenbildung über \(\varepsilon^{ch}(b)\) die Spannung. Umgekehrt beeinflusst die mechanische Spannung die chemischen Potentiale der immobilisierten Netzwerkpools.

Für \(d=s_N+s_B+\delta_B\) gilt
\[
\frac{\partial b}{\partial s_N}=-\frac{s_B}{d^2},
\qquad
\frac{\partial b}{\partial s_B}=\frac{s_N+\delta_B}{d^2}.
\]
Der mechanische Beitrag zu den Netzwerkpotentialen lautet
\[
\mu_N^{mech}=\frac{\partial\Psi_{el}}{\partial b}\frac{\partial b}{\partial s_N},
\quad
\mu_B^{mech}=\frac{\partial\Psi_{el}}{\partial b}\frac{\partial b}{\partial s_B},
\quad
\frac{\partial\Psi_{el}}{\partial b}
=-\beta_B\operatorname{tr}[C:(\varepsilon-\varepsilon^{ch})].
\tag{P5.5}
\]
Die totalen chemischen Potentiale sind \(\mu_i^{tot}=\mu_i^{chem}+\mu_i^{mech}\), wobei der mechanische Zusatz für \(M,O\) in dieser Schließung null ist. Die Reaktionsaffinitäten werden aus den totalen Potentialen berechnet:
\[
\mathcal A_j^{tot}=\mu_j^{tot}-\mu_{j+1}^{tot}.
\]

## 5. Reaktionskinetik mit garantierter Dissipation

Die P2-Kinetik \(r_j=k_jc_*(x_j-y_j)\), \(x_j=a_j\), \(y_j=a_{j+1}/K_j\), dissipiert die chemische Energie allein. Sobald die Eigenverformung von \(s_N,s_B\) abhängt, wäre es falsch, diese unveränderte Rate ohne Prüfung als Dissipation der **Gesamtenergie** auszugeben.

P5 verwendet deshalb die logarithmische Mittelwert-Mobilität
\[
\Lambda(x,y)=\frac{x-y}{\ln x-\ln y}>0
\]
mit stetigem Grenzwert \(\Lambda(x,x)=x\), und setzt
\[
r_j=\frac{k_jc_*}{RT}\Lambda(x_j,y_j)\mathcal A_j^{tot}.
\tag{P5.6}
\]
Wenn der mechanische Potentialbeitrag null ist, reduziert sich (P5.6) exakt auf die P2-Rate. Allgemein gilt
\[
r_j\mathcal A_j^{tot}
=\frac{k_jc_*}{RT}\Lambda(x_j,y_j)(\mathcal A_j^{tot})^2\ge0.
\tag{P5.7}
\]
Damit wird die mechanische Rückkopplung in die Reaktionsrichtung aufgenommen, ohne die Nichtnegativität der Reaktionsdissipation zu verlieren. Die Gleichgewichtskonstanten und die kinetischen Konstanten bleiben unkalibriert.

Die Inventarquellen sind
\[
(\dot m_M,\dot m_O,\dot s_N,\dot s_B)_{rxn}
=(-r_1,r_1-r_2,r_2-r_3,r_3),
\tag{P5.8}
\]
also exakt Si-erhaltend.

## 6. Gekoppeltes P5-Feldsystem

Der isotherme, quasistatische Referenzblock lautet:

**Mechanisches Gleichgewicht**
\[
\operatorname{Div}\sigma+f=0.
\tag{P5.9}
\]

**Biot-Speicher und Fluidbilanz**
\[
\zeta=\alpha_B\operatorname{div}u+p/M_B,\quad
\theta=\theta_0+\zeta,\quad
\partial_t\theta+\operatorname{Div}Q=0,
\quad Q=-\mathbb K_p\nabla p.
\tag{P5.10}
\]

**Mobile Spezies**
\[
\partial_t m_i+\operatorname{Div}(c_iQ+\mathcal J_i)=R_i,
\quad i=M,O,
\tag{P5.11}
\]
mit
\[
\mathcal J_i=-\frac{D_i m_i}{RT}\nabla\mu_i^{tot}.
\tag{P5.12}
\]
In der aktuellen Schließung \(\mu_M^{mech}=\mu_O^{mech}=0\). Für konstante Aktivitätskoeffizienten reduziert sich (P5.12) auf die übliche Fick-Form für \(c_i=m_i/\theta\).

**Immobilisierte Netzwerkpools**
\[
\partial_t s_N=R_N,\qquad \partial_t s_B=R_B.
\tag{P5.13}
\]
Es gibt für \(N,B\) keinen advektiven oder diffusen Porenwasserfluss. Das ist die bewusste Phasentrennung gegenüber P3/P4.

## 7. Energieabschätzung – formaler Satz unter glatten Voraussetzungen

Nehmen wir glatte positive Lösungen, konstante Temperatur und Koeffizienten, symmetrisch positiv definite \(C\), \(M_B>0\), \(\mathbb K_p\ge k_0I>0\), \(D_i\ge0\), mechanisch arbeitsfreie Randbedingungen und geschlossene No-Flux-Ränder an. Zusätzlich gelte die ideale mobile Mischung in (P5.3), so dass die Gibbs-Duhem-Identität für die mobilen Pools gilt. Dann ergibt Multiplikation der Bilanzgleichungen mit den konjugierten Potentialen und partielle Integration formal:
\[
\begin{aligned}
\frac{d}{dt}\int_{\Omega_0}\Psi\,dX
={}&-\int_{\Omega_0}\nabla p\cdot\mathbb K_p\nabla p\,dX\\
&-\int_{\Omega_0}\sum_{i=M,O}
\frac{D_i m_i}{RT}|\nabla\mu_i^{tot}|^2\,dX\\
&-\int_{\Omega_0}\sum_{j=1}^3r_j\mathcal A_j^{tot}\,dX
\le0.
\end{aligned}
\tag{P5.14}
\]
Die Darcy-/Advektionsterme ergeben zusammen \(\nabla p\cdot Q\); die chemischen Diffusions- und Reaktionsterme sind separat dissipativ. Die mechanische Arbeit verschwindet bei quasistatischem Gleichgewicht und arbeitsfreien mechanischen Rändern.

**Status des Resultats:** (P5.14) ist eine formale Energieidentität für hinreichend glatte Lösungen unter den ausdrücklich genannten Annahmen. Sie ist noch kein Existenzbeweis für schwache Lösungen. Bei offenen Drainagerändern, vorgegebenen Traktionen, zeitabhängigen Randdaten, nichtidealen Aktivitäten oder variabler Temperatur treten zusätzliche Rand-/Kopplungsterme auf, die gesondert bilanziert werden müssen.

## 8. Erhaltung und Invarianten

Aus (P5.8), (P5.11) und (P5.13) folgt lokal
\[
\partial_t(m_M+m_O+s_N+s_B)
+\operatorname{Div}(c_MQ+c_OQ+\mathcal J_M+\mathcal J_O)=0.
\tag{P5.15}
\]
Die Gesamtmenge an Si-Äquivalenten ist bei geschlossenen Randbedingungen erhalten. Die nichtnegativen Inventare bilden den physikalischen Zustandsraum, sofern die Reaktionskinetik und der numerische Integrator die Quasi-Positivität erhalten. Ein explizites Zeitschrittverfahren benötigt dafür Schrittweitenbeschränkungen oder eine positivity-preserving Integrationsmethode.

## 9. Mathematischer Status und offene Beweisfragen

P5 liefert eine gemeinsame freie Energie, konjugierte Spannung und Potentiale, eine thermodynamisch dissipative Reaktionsschließung sowie eine konsistente Feldarchitektur. **Nicht bewiesen** sind:
- globale Existenz und Eindeutigkeit schwacher Lösungen des nichtlinearen 3D-Systems;
- Regularität oder globale Glattheit;
- Eindeutigkeit bei nichtkonvexer Eigenverformungsenergie;
- Existenz bei degenerierenden Konzentrationen \(m_i,s_i\to0\);
- empirische Gültigkeit der linearen Eigenverformung \(\beta_B(b-b_0)I\);
- Identifizierbarkeit von \(\beta_B,\mathbb K_p,D_i,k_j,K_j\) aus den vorhandenen Synäresekurven allein.

Der P5-Code ist ein lokaler konstitutiver Kernel zur Auswertung von Energie, Spannung, Potentialen und dissipativen Reaktionsraten. Er ist kein räumlicher PDE-Löser und ersetzt weder Konvergenzstudien noch Materialkalibrierung.

## 10. Nächste Schritte P6

1. Schwache Formulierung und Existenzroute für den gekoppelten Kleinverformungsblock unter koerziven/konvexen Annahmen.
2. Positivität und degenerierende Konzentrationsgrenzen mathematisch behandeln.
3. Konservativer räumlicher Solver mit mechanischem Gleichgewicht, Druck und mobilem Stofftransport.
4. Randmodell für natürliche Drainage (freie Oberfläche/Kapillarkräfte) ohne erzwungene Druckzellbedingungen.
5. Quellenkritische Identifikation zulässiger Parameter aus vorhandener Literatur; TEOS- und Druckzellzweige bleiben getrennt.
6. Erst danach Erweiterung um Temperatur, Elektrolyte, Wasseraktivität und nichtideale Aktivitäten.
