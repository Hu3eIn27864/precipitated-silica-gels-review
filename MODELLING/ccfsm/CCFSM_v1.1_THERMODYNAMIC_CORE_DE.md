# CCFSM v1.1 – thermodynamischer Kern und konstitutive Schließungsstrategie

**Datum:** 14.11.2026  
**Bezug:** CCFSM v1.0  
**Status:** explizit hergeleiteter thermodynamischer Referenzkern P0 plus dissipative Erweiterungsarchitektur. Kein vollständiger thermodynamischer Abschluss des gesamten P5-Modells.

## 1. Warum eine neue Zustandsvariable nötig ist

Porendruck ist im gesättigten Biot-Modell zweckmäßig eine thermodynamische Kraft bzw. ein Lagrange-/Potentialfeld, nicht ohne Weiteres eine unabhängige gespeicherte Energiedichte. Wir führen deshalb den Fluidgehaltszuwachs \(\zeta\) pro Referenz-Gesamtvolumen ein. Im linearen Biot-Grenzfall gilt:
\[
\zeta=\alpha_B\,\operatorname{tr}\varepsilon(\mathbf u)+\frac{p}{M},
\qquad p=M(\zeta-\alpha_B\operatorname{tr}\varepsilon).
\]
\(M>0\) ist der Biot-Kompressionsmodul. \(\zeta\) ist nicht identisch mit der Porosität \(\phi\); es ist eine inkrementelle Speichergröße, die Volumenänderung und Fluidkompressibilität zusammenfasst.

## 2. Freie Energie des linearen isothermen P0-Systems

Für kleine Dehnungen und konstante Referenzparameter definieren wir pro Referenzvolumen:
\[
\psi_0(\varepsilon,\zeta)=
\frac12\varepsilon:\mathbb C:\varepsilon+
\frac M2(\zeta-\alpha_B\operatorname{tr}\varepsilon)^2.
\]
Annahmen:
- \(\mathbb C\) ist symmetrisch und koerziv auf symmetrischen Tensoren;
- \(M>0\);
- \(\alpha_B\) ist konstant;
- isotherm, gesättigt, keine chemischen Reaktionen, keine Netzwerkvariablen;
- Referenzgebiet fest, lineare Kinematik.

Die konjugierten Größen sind:
\[
\boldsymbol\sigma=\partial_\varepsilon\psi_0
=\mathbb C:\varepsilon-\alpha_Bp\mathbf I,
\qquad
p=\partial_\zeta\psi_0.
\]
Damit folgen Spannung und Porendruck aus derselben Energie. Die Vorzeichen der Biot-Kopplung sind konsistent mit \(\zeta=\alpha_B\operatorname{tr}\varepsilon+p/M\).

## 3. Bilanz- und Flussgesetz

Quasistatische Mechanik:
\[
-\nabla\cdot\boldsymbol\sigma=\mathbf f.
\]
Fluidgehalt:
\[
\partial_t\zeta+\nabla\cdot\mathbf q=s_f.
\]
Darcy/Onsager:
\[
\mathbf q=-\mathbb L_p\nabla p,\qquad
\mathbb L_p=\frac{\mathbf K}{\mu}.
\]
\(\mathbb L_p\) symmetrisch positiv definit. Bei Schwerkraft wird \(p\) durch das hydraulische Potential \(p-\rho_f\mathbf g\cdot\mathbf x\) ersetzt; Rand- und Energiebeiträge sind entsprechend anzupassen.

## 4. Energieidentität (P0)

Mit \(\dot{\varepsilon}=\varepsilon(\partial_t\mathbf u)\) gilt punktweise:
\[
\dot\psi_0=\boldsymbol\sigma:\dot{\boldsymbol\varepsilon}+p\dot\zeta.
\]
Multipliziert man die Fluidbilanz mit \(p\), integriert partiell und addiert die mechanische Gleichung getestet mit \(\partial_t\mathbf u\), erhält man bei hinreichend glatten Lösungen:
\[
\frac{d}{dt}\int_\Omega\psi_0\,dx+
\int_\Omega\nabla p\cdot\mathbb L_p\nabla p\,dx
=
\mathcal P_{\rm mech}+\mathcal P_{\rm fluid}+
\int_\Omega p\,s_f\,dx.
\]
Dabei enthalten \(\mathcal P_{\rm mech}\) die mechanische Randtraktion und Volumenkraftleistung sowie \(\mathcal P_{\rm fluid}\) die Druck-/Fluidrandarbeit. Bei verschwindender äußerer mechanischer Leistung, geschlossenen Fluidrändern \(\mathbf q\cdot\mathbf n=0\), \(s_f=0\) und ohne Volumenkraft:
\[
\frac{d}{dt}\mathcal F_0(t)
=-\int_\Omega\nabla p\cdot\mathbb L_p\nabla p\,dx\le0.
\]
Dies ist die thermodynamische Dissipation des linearen P0-Referenzsystems. Für drainierende Ränder ist der Randterm explizit zu behalten; ein offenes System muss nicht monoton dieselbe interne Energie verlieren, wenn Reservoirarbeit nicht mit bilanziert wird.

## 5. Dissipative Erweiterung auf interne Variablen

Sei \(a=(B,D_f,z,\xi_u,\xi_r,\ldots)\) der Vektor interner Variablen und \(\psi(\varepsilon,\zeta,a,\nabla a,\mathbf c)\) eine noch zu identifizierende freie Energie. Thermodynamische Kräfte:
\[
A_a=-\frac{\delta\mathcal F}{\delta a}.
\]
Eine zulässige lokale Onsager-Kinetik lautet:
\[
D_t a=\mathbb L_a A_a,\qquad
\mathbb L_a=\mathbb L_a^\mathsf T\succeq0.
\]
Dann ist der lokale Beitrag zur Energierate \( - A_a^\mathsf T\mathbb L_a A_a\le0\), sofern Transport-/Randterme korrekt bilanziert sind. Bei beschränkten Zuständen muss die Mobilität bzw. Projektion den zulässigen Zustandsraum invariant halten. Beispielsweise kann für \(0\le B\le B_\infty\) eine degenerierte Mobilität proportional zu \(B(B_\infty-B)\) gewählt werden. Das ist eine thermodynamisch zulässige Modellklasse, noch kein empirisch belegtes Silica-Kinetikgesetz.

Für Gradientenergien \(\tfrac12\nabla a:\mathsf A_a\nabla a\) enthält die Variationsableitung den Term \(-\nabla\cdot(\mathsf A_a\nabla a)\). Die natürliche Randbedingung ist der zugehörige Null-Normalfluss, sofern keine Oberflächenenergie vorgegeben ist.

## 6. Chemische Spezies: chemische Potentiale statt bloßer Konzentrationsgradienten

Für ideal verdünnte Spezies kann als Startpunkt
\[
\psi_{\rm mix}=RT\sum_i c_i(\ln(c_i/c^\circ)-1)
\]
verwendet werden, sodass \(\mu_i=RT\ln(c_i/c^\circ)\) (zuzüglich Standardpotentiale und elektrostatischer Beiträge). Ein Onsager-Fluss:
\[
\mathbf J_i=-\sum_j\mathbb L_{ij}\nabla\mu_j,
\qquad \mathbb L=\mathbb L^\mathsf T\succeq0.
\]
Die Dissipation \(\sum_{ij}\nabla\mu_i\cdot\mathbb L_{ij}\nabla\mu_j\) ist nichtnegativ. Im idealen verdünnten Grenzfall und diagonalem \(\mathbb L\) ergibt sich Fick-Diffusion. Für konzentrierte Natriumsilikat-/Sulfat-Liquoren ist das ideale Modell nicht automatisch quantitativ gültig; Aktivitäten und Ionenpaarbildung bleiben erforderlich.

Reaktionen mit stöchiometrischer Matrix \(\nu\), Reaktionsfortschritten \(r\) und Affinitäten \(\mathcal A=-\nu^\mathsf T\boldsymbol\mu\) müssen so gewählt werden, dass \(\mathcal A^\mathsf T r\ge0\) und damit die freie Energie durch Reaktion nicht zunimmt. Element- und Ladungserhaltung verlangen \(A_{\rm elem}\nu=0\) und gesonderte Elektroneutralitäts-/Elektrotransportbedingungen.

## 7. Mechanische Dissipation

Eine viskoelastische Erweiterung kann über
\[
\boldsymbol\sigma=\partial_\varepsilon\psi+
\mathbb V:\dot{\boldsymbol\varepsilon}_{\rm e},
\qquad
\mathbb V=\mathbb V^\mathsf T\succeq0
\]
formuliert werden. Die dissipative Leistung ist
\(\dot{\boldsymbol\varepsilon}_{\rm e}:\mathbb V:\dot{\boldsymbol\varepsilon}_{\rm e}\ge0\).
\(\varepsilon_{\rm e}=\varepsilon-\varepsilon_{\rm sh}(a)\). Die interne Variable muss in der Energiebilanz mitgeführt werden, damit die Eigenstrain-Kopplung keine Energiequelle aus dem Nichts erzeugt.

## 8. Was damit tatsächlich erreicht wurde

**Hergeleitet:** gemeinsame Energie für Spannung und Porendruck im linearen P0-Biot-System; Darcy-Dissipation; geschlossene-System-Energieidentität unter den genannten Annahmen.

**Als zulässige Struktur formuliert:** Onsager-Kinetik interner Variablen, chemische Potentialflüsse, dissipative Reaktionskinetik und viskoelastische Dissipation.

**Noch offen:** konkrete silica-spezifische Energieanteile für Netzwerkbildung, Morphologie, Siloxanbrücken, Kontraktion und Oberflächenchemie; Parameterwerte; Identifizierbarkeit; nichtlineare Koerzivität; bewegte Grenzflächen und vollständiger P5-Energienachweis.

Diese Trennung verhindert, dass eine plausible Energieansatzfunktion fälschlich als experimentell bewiesenes Materialgesetz ausgegeben wird.
