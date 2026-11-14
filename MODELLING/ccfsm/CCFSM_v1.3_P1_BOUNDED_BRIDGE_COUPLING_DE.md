# CCFSM v1.3 – P1: beschränkte Netzwerkbrückenvariable und gekoppelte Biot-Darcy-Existenz

**Datum:** 14.11.2026  
**Bezug:** P0 aus v1.2; thermodynamischer Kern aus v1.1.  
**Geltungsbereich:** isothermes, gesättigtes 3D-Referenzgebiet mit quasistatischer linearer Biot-Mechanik, Darcy-Transport und einer dimensionslosen effektiven Netzwerkbrückenfraktion.  
**Status:** schwacher Existenz- und Eindeutigkeitssatz für die hier ausdrücklich definierte P1-Schließung. Keine empirische Validierung und kein Existenzsatz für das volle CCFSM.

## 1. Modellentscheidung und Status der Konstitutivannahmen

Wir ergänzen P0 um eine dimensionslose lokale Zustandsvariable
\[
b(\mathbf x,t)=B(\mathbf x,t)/B_\infty,\qquad 0\le b\le1,
\]
wobei \(B\) eine effektive lasttragende Siloxan-Netzwerkbrückendichte und \(B_\infty>0\) ihre bislang nicht unabhängig bestimmte Referenzskala bezeichnet.

P1 verwendet bewusst nur eine minimale Brückenkinetik:
\[
\partial_t b=k_b(\mathbf x)\,[b_{\rm eq}(\mathbf x)-b],
\qquad b(\mathbf x,0)=b_0(\mathbf x).
\tag{B}
\]
Es gelten \(0<k_-\le k_b(\mathbf x)\le k_+<\infty\) sowie
\(b_0,b_{\rm eq}\in L^\infty(\Omega)\) mit Werten in \([0,1]\).
\(b_{\rm eq}\) ist zeitlich fest. Damit ist
\[
b(\mathbf x,t)=b_{\rm eq}(\mathbf x)+
[b_0(\mathbf x)-b_{\rm eq}(\mathbf x)]e^{-k_b(\mathbf x)t}.
\tag{B-exakt}
\]
Dies ist eine mathematisch kontrollierte Relaxationsschließung, kein bereits nachgewiesenes Gesetz der Silica-Kondensation. Die Abhängigkeit von pH, Temperatur, Natrium-/Sulfataktivität, gelöstem Silicium, Alter und Mischhistorie ist in \(b_{\rm eq}\) und \(k_b\) noch nicht aufgelöst.

Die einzige Rückwirkung von \(b\) auf P0 erfolgt zunächst über die Darcy-Mobilität:
\[
\mathbb L_p(b)=(1-b)\mathbb L_0+b\mathbb L_1.
\tag{L}
\]
\(\mathbb L_0,\mathbb L_1\) sind vorgegebene symmetrische Mobilitätstensoren. Es wird angenommen, dass beide messbar und gleichmäßig beschränkt sowie gleichmäßig positiv definit sind:
\[
\lambda_*|\xi|^2\le \mathbb L_j(\mathbf x)\xi\cdot\xi
\le\Lambda_*|\xi|^2,\quad j=0,1.
\]
Dann gelten dieselben Schranken für jedes \(b\in[0,1]\). Die affine Interpolation ist eine mathematisch zulässige, Lipschitz-stetige Platzhalterschließung. Sie behauptet **nicht**, dass die reale Permeabilität linear mit der Brückendichte wächst oder fällt. Richtung und Form dieser Beziehung sind experimentell offen.

Die P1-Variante lässt die Elastizität \(\mathbb C\), den Biot-Koeffizienten \(\alpha_B\) und den Speicherkoeffizienten \(M\) zunächst unverändert. Insbesondere wird keine ungemessene Funktion \(\mathbb C(b)\) eingeführt.

## 2. Gekoppeltes schwaches System

Die Räume, Geometrie, Randbedingungen und der mechanische Lösungsoperator \(T:H\to V\) sind wie in v1.2:
\[
V=H^1_0(\Omega;\mathbb R^3),\quad Q=H^1(\Omega),\quad H=L^2(\Omega),
\]
mit geschlossenem No-Flow-Rand für das Fluid und homogenen Verschiebungs-Dirichletbedingungen. Das Speicherprodukt bleibt
\[
m(p,r)=M^{-1}(p,r)_H+a(Tp,Tr).
\]
Gesucht sind \(b,p,u\) mit \(u=Tp\), so dass (B) punktweise fast überall und
\[
m(\partial_t p,r)+
\int_\Omega\mathbb L_p(b)\nabla p\cdot\nabla r\,dx
=\langle s_f,r\rangle
\quad\forall r\in Q
\tag{P1}
\]
für fast alle Zeiten gilt. Anfangsdaten: \(p(0)=p_0\in H\), \(b(0)=b_0\).

Äquivalent in den ursprünglichen Feldern:
\[
-\nabla\cdot(\mathbb C\varepsilon(u)-\alpha_BpI)=0,
\]
\[
\partial_t\!\left(\alpha_B\nabla\cdot u+M^{-1}p\right)
-\nabla\cdot[\mathbb L_p(b)\nabla p]=s_f,
\]
\[
\partial_t b=k_b(b_{\rm eq}-b).
\]
Die mechanische Gleichung ist quasistatisch und wird wie in P0 schwach verstanden.

## 3. Invarianz der physikalischen Zustandsmenge

**Lemma (Brückenfraktion bleibt beschränkt).** Für fast alle \(\mathbf x\) und alle \(t\ge0\) gilt
\[
0\le b(\mathbf x,t)\le1.
\]

**Beweis.** Nach (B-exakt) ist \(b(\mathbf x,t)\) eine konvexe Kombination aus \(b_0(\mathbf x)\) und \(b_{\rm eq}(\mathbf x)\), denn
\[
b=e^{-k_bt}b_0+(1-e^{-k_bt})b_{\rm eq},
\]
und beide Gewichte liegen in \([0,1]\) und summieren sich zu eins. Da beide Zustände in \([0,1]\) liegen, liegt auch \(b\) in diesem Intervall. \(\square\)

Damit bleibt auch \(\mathbb L_p(b)\) zwischen den beiden gleichmäßig elliptischen Endtensoren. Es werden weder eine abgeschnittene numerische Lösung noch eine nachträgliche Projektion benötigt.

## 4. P1-Existenz- und Eindeutigkeitssatz

**Satz.** Sei \(\Omega\subset\mathbb R^3\) beschränkt und Lipschitz, \(T>0\). Es gelten die P0-Annahmen aus v1.2 an \(\mathbb C,M,\alpha_B\), die oben genannten Annahmen an \(k_b,b_0,b_{\rm eq},\mathbb L_0,\mathbb L_1\), sowie
\[
p_0\in H,\qquad s_f\in L^2(0,T;Q').
\]
Dann existiert genau ein Paar \((b,p)\) mit
\[
b\in W^{1,\infty}(0,T;L^\infty(\Omega)),\quad 0\le b\le1,
\]
\[
p\in L^2(0,T;Q)\cap C([0,T];H),\quad
\partial_t p\in L^2(0,T;Q'),
\]
das (B) und (P1) erfüllt. \(u=Tp\) ist eindeutig und liegt in
\(L^\infty(0,T;V)\cap C([0,T];V)\).

### Beweis

**Schritt 1 – Brückenfeld.** Die explizite Formel (B-exakt) definiert ein eindeutiges messbares \(b\). Aus den Schranken für \(k_b,b_0,b_{\rm eq}\) folgt \(b\in W^{1,\infty}(0,T;L^\infty(\Omega))\), und das Lemma liefert \(0\le b\le1\).

**Schritt 2 – zeitabhängige Darcy-Form.** Setze
\[
\ell_t(v,r)=\int_\Omega\mathbb L_p(b(\mathbf x,t))
\nabla v\cdot\nabla r\,dx.
\]
Die Form ist messbar in \(t\), gleichmäßig stetig auf \(Q\times Q\) und gleichmäßig koerziv auf dem Gradientenanteil:
\[
|\ell_t(v,r)|\le\Lambda_*\|v\|_Q\|r\|_Q,
\qquad
\ell_t(v,v)\ge\lambda_*\|\nabla v\|_H^2.
\]
Zusammen mit der Äquivalenznorm \(m(v,v)\simeq\|v\|_H^2\) folgt
\[
m(v,v)+\ell_t(v,v)\ge c\|v\|_Q^2
\]
mit einem von \(t\) unabhängigen \(c>0\).

**Schritt 3 – parabolische Existenz.** Die nichtautonome lineare Evolutionsgleichung
\[
m(\partial_t p,r)+\ell_t(p,r)=\langle s_f,r\rangle
\]
liegt damit im Rahmen der Theorie messbarer, gleichmäßig beschränkter und koerziver zeitabhängiger Bilinearformen auf dem Gelfand-Tripel \(Q\hookrightarrow H\hookrightarrow Q'\). Der Lions-Typ-Evolutionssatz liefert eine Lösung in
\(L^2(0,T;Q)\cap C([0,T];H)\) mit Ableitung in \(L^2(0,T;Q')\) und Anfangswert \(p_0\). Die mechanische Verschiebung folgt eindeutig aus \(u=Tp\).

**Schritt 4 – Eindeutigkeit.** Das Feld \(b\) ist durch (B-exakt) eindeutig. Für zwei Drucklösungen mit demselben \(b\) und denselben Daten erfüllt die Differenz \(w\) die homogene Gleichung. Testen mit \(w\) ergibt
\[
\frac12m(w(t),w(t))+
\int_0^t\ell_s(w,w)\,ds=0.
\]
Wegen der Positivität von \(m\) folgt \(w=0\); somit stimmen auch die Verschiebungen überein. \(\square\)

Der Existenzschritt verwendet hier bewusst den etablierten Satz für nichtautonome parabolische Formen. Eine vollständig ausgeschriebene Galerkin-Konstruktion mit stabilen zeitabhängigen Projektionen wäre eine zusätzliche Beweisvertiefung, ist aber nicht nötig, um den genannten schwachen Satz aus diesem abstrakten Resultat abzuleiten.

## 5. Thermodynamische Bilanz

Wir ergänzen die P0-Energie um eine konvexe Brückenrelaxationsenergie:
\[
\mathcal F_1(p,b)=\frac12m(p,p)+
\int_\Omega\frac{\kappa_B}{2}(b-b_{\rm eq})^2\,dx,
\qquad \kappa_B>0.
\]
Die Kinetik (B) ist ein lokaler Gradientfluss:
\[
\partial_t b=-\mathcal M_B
\frac{\partial}{\partial b}
\left[\frac{\kappa_B}{2}(b-b_{\rm eq})^2\right],
\qquad \mathcal M_B=k_b/\kappa_B>0.
\]
Für hinreichend reguläre Daten bzw. in der integrierten schwachen Energiebilanz gilt
\[
\begin{aligned}
\mathcal F_1(t)
&+\int_0^t\!\int_\Omega
\nabla p\cdot\mathbb L_p(b)\nabla p\,dx\,ds\\
&+\int_0^t\!\int_\Omega
\frac{k_b}{\kappa_B}
\left|\kappa_B(b-b_{\rm eq})\right|^2\,dx\,ds\\
&=\mathcal F_1(0)+
\int_0^t\langle s_f,p\rangle\,ds .
\end{aligned}
\tag{E-P1}
\]
Bei \(s_f=0\) ist die Gesamtenergie nicht zunehmend. Die beiden Dissipationskanäle sind Darcy-Fluss und Brückenrelaxation. Für nichtglatte Daten ist die Identität als Energieungleichung zu lesen; die Regularität des expliziten \(b\)-Feldes und die parabolische Energieklasse erlauben die übliche Approximation.

**Wichtige Interpretation:** Die Brückenenergie ist hier ein mathematisch konsistenter Minimalansatz, keine gemessene chemische freie Energie der Siloxankondensation. \(b_{\rm eq}\) ist ein festgehaltener Zielzustand. Wenn \(b_{\rm eq}\) von pH, Temperatur, Spezies oder Zeit abhängt, entsteht zusätzliche chemische Arbeit; diese muss in einer erweiterten Energiebilanz explizit erscheinen.

## 6. Was P1 leistet – und was noch fehlt

**Mathematisch erreicht:**
- die Zustandsmenge \(0\le b\le1\) ist invariant;
- die Darcy-Mobilität bleibt gleichmäßig positiv definit;
- der gekoppelte P1-Druck-/Mechanikblock besitzt eine eindeutige schwache Lösung;
- eine konsistente dissipative Energiebilanz ist formuliert.

**Noch nicht erreicht:**
- keine Rückwirkung von Druck, pH oder gelösten Spezies auf die Brückenkinetik;
- keine räumliche Diffusion/Gradientenergie der Brückenvariable;
- keine Brückenabhängigkeit des Elastizitätsmoduls oder der Eigenkontraktion;
- keine Kapillar-, freie-Oberflächen- oder drainierende Randbilanz natürlicher Synärese;
- keine empirisch identifizierte Form von \(\mathbb L_p(b)\), \(k_b\), \(b_{\rm eq}\), \(\kappa_B\) oder \(B_\infty\);
- keine klassische Regularität und kein globaler Regularitätsbeweis für das volle nichtlineare 3D-CCFSM.

Die lineare Interpolation in (L) ist eine Platzhalterfamilie, die durch Messdaten zu ersetzen oder zu falsifizieren ist. Die vorhandenen Wilhelm-&-Kind-Kurven allein identifizieren diese Brücken- und Mobilitätsparameter nicht. Erzwungene Druckzell-/Oedometerdaten und Trocknungsdaten werden nicht als natürliche-Synärese-Kalibrierung verwendet.

## 7. Nächster Schritt P2

P2 sollte die chemische Triebkraft der Brückenbildung aus Silicium-Spezies, pH und Ionenaktivitäten einführen. Dazu müssen Reaktionsstöchiometrie, Elementbilanzen, chemische Potentiale und Reaktionsaffinität gemeinsam mit der Brückenenergie definiert werden. Erst dann kann \(b_{\rm eq}\) durch eine chemisch konsistente Reaktionskinetik ersetzt werden, ohne die Dissipationsbilanz zu verletzen. Die vorhandene Rezeptur-Speziation ist ein Startpunkt, aber noch kein validiertes konzentriertes Prozessbrühenmodell.
