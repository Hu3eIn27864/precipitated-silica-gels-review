# CCFSM v1.1 – P0-Energieabschätzung und schwache Formulierung

## 1. Referenzproblem

Sei \(\Omega\subset\mathbb R^3\) beschränkt und Lipschitz. Wir betrachten das lineare, isotherme, gesättigte Biot-Darcy-System:
\[
-\nabla\cdot(\mathbb C:\varepsilon(\mathbf u)-\alpha_Bp\mathbf I)=\mathbf f,
\]
\[
\partial_t\zeta+\nabla\cdot\mathbf q=s_f,\quad
\zeta=\alpha_B\nabla\cdot\mathbf u+p/M,\quad
\mathbf q=-\mathbb L_p\nabla p.
\]
\(\mathbb C\) symmetrisch koerziv, \(M>0\), \(\mathbb L_p\) symmetrisch und gleichmäßig positiv definit. Mechanische Randbedingungen müssen starre Bewegungen ausschließen; Fluidrandbedingungen werden homogen und geschlossen gewählt, um die einfachste Dissipationsaussage zu erhalten.

## 2. Schwache Form

Für \(V\subset H^1(\Omega)^3\), \(Q=H^1(\Omega)\), finde \(\mathbf u(t)\in V\), \(p(t)\in Q\), sodass
\[
\int_\Omega\mathbb C:\varepsilon(\mathbf u):\varepsilon(\mathbf w)\,dx
-\alpha_B\int_\Omega p\,\nabla\cdot\mathbf w\,dx
=\langle\mathbf f,\mathbf w\rangle
\quad\forall\mathbf w\in V,
\]
\[
\int_\Omega\left(\alpha_B\partial_t\nabla\cdot\mathbf u+
M^{-1}\partial_t p\right)r\,dx
+\int_\Omega\mathbb L_p\nabla p\cdot\nabla r\,dx
=\langle s_f,r\rangle
\quad\forall r\in Q.
\]
Bei geschlossenen Rändern ist der natürliche Fluidfluss null. Druck ist bei rein neumannartigen Bedingungen nur bis auf eine Konstante bestimmt; die Mittelwert-/Kompatibilitätsbedingung muss festgelegt werden. In einem mechanisch vollständig traction-freien Körper sind starre Bewegungsmodi ebenfalls zu quotentieren oder durch eine Referenzfixierung zu entfernen.

## 3. Formale Energieabschätzung

Setze in der Mechanik \(\mathbf w=\partial_t\mathbf u\), in der Fluidgleichung \(r=p\). Addiere:
\[
\frac{d}{dt}\left[
\frac12\int_\Omega\varepsilon(\mathbf u):\mathbb C:\varepsilon(\mathbf u)\,dx
+\frac1{2M}\int_\Omega p^2\,dx
\right]
+\int_\Omega\nabla p\cdot\mathbb L_p\nabla p\,dx
=
\langle\mathbf f,\partial_t\mathbf u\rangle+\langle s_f,p\rangle.
\]
Die Kopplungsterme \(-\alpha_Bp\,\nabla\cdot\partial_t\mathbf u\) aus der Mechanik und \(+\alpha_Bp\,\partial_t\nabla\cdot\mathbf u\) aus der Fluidgleichung heben sich exakt auf. Die Energie ist dieselbe \(\psi_0\) aus der thermodynamischen Herleitung:
\[
\mathcal F_0=\frac12\int_\Omega\varepsilon:\mathbb C:\varepsilon\,dx
+\frac1{2M}\int_\Omega p^2\,dx.
\]
Für \(\mathbf f=0,s_f=0\) folgt:
\[
\mathcal F_0(t)+\int_0^t\!\int_\Omega
\nabla p\cdot\mathbb L_p\nabla p\,dx\,ds
=\mathcal F_0(0).
\]
Dies ist zunächst eine a-priori-Energieidentität für hinreichend reguläre Lösungen. Sie ist zugleich die zentrale Abschätzung für einen Galerkin-/Approximationsbeweis.

## 4. Konsequenzen und Grenzen

- Koerzivität von \(\mathbb C\) und \(M>0\) kontrollieren \(\varepsilon(\mathbf u)\) und \(p\) in \(L^\infty_tL^2_x\).
- Positive Definitheit von \(\mathbb L_p\) kontrolliert \(\nabla p\) in \(L^2_{t,x}\).
- Korn-Ungleichung kontrolliert \(\mathbf u\) in \(L^\infty_tH^1_x\), sofern starre Modi ausgeschlossen sind.
- Für die vollständige Existenztheorie sind Datenräume, Drucknormalisierung, Galerkin-Approximation, Zeitregularität und Kompaktheit sauber auszuführen.
- Eindeutigkeit folgt im linearen System aus der Energieidentität auf die Differenz zweier Lösungen mit gleichen Daten.
- Diese Argumente beweisen nicht Existenz oder Regularität des nichtlinearen CCFSM P1–P5 und insbesondere keine globale klassische Regularität für die volle 3D-Theorie.

## 5. Geplante nächste formale Arbeit

1. Exakte Datenräume und Randzerlegung für Dirichlet-/Neumann-/Robin-Mischbedingungen.
2. Galerkin-Konstruktion mit gleichmäßigen Abschätzungen.
3. Grenzübergang und Nachweis der schwachen Gleichungen.
4. Differenzargument für Eindeutigkeit.
5. Danach beschränkte interne Variable \(B\) mit dissipativer Mobilität und gekoppelter Energie.
