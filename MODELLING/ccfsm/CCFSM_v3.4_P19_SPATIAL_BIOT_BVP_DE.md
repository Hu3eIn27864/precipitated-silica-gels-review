# CCFSM P19 — räumliches 3D-Biot-Eigenstrain-Randwertproblem

**Status:** linearer quasistatischer FE-Assembler auf nutzerseitig bereitgestellten Quadraturdaten. Kein Netzgenerator, keine Fluid-/Chemie-Zeitschrittintegration und keine empirische Kalibrierung.

## 1. Kontinuierliche starke und schwache Form

Mit Verschiebung u, Kleindehnung epsilon(u)=sym(grad u), isotroper chemischer Eigenstrain c, Fluidinhaltsänderung zeta gilt:
\[
E=\varepsilon(u)-cI,\quad p=M(\zeta-\alpha\nabla\cdot u),
\quad \sigma=\lambda\operatorname{tr}(E)I+2GE-\alpha pI.
\]
Ohne Körperkräfte:
\[
\boxed{\nabla\cdot\sigma=0\text{ in }\Omega.}
\]
Auf disjunkten Randteilen:
\[
u=\bar u\text{ auf }\Gamma_D,\qquad \sigma n=\bar t\text{ auf }\Gamma_N.
\]
Für Testverschiebungen v=0 auf Gamma_D:
\[
\boxed{\int_\Omega\varepsilon(v):\sigma\,dV
=\int_{\Gamma_N}v\cdot\bar t\,dA.}
\]

## 2. Variationale Tangente

Einsetzen des Biot-Gesetzes ergibt
\[
\sigma=\mathbb C:(\varepsilon-cI)-\alpha M\zeta I
+\alpha^2M(\operatorname{tr}\varepsilon)I.
\]
Die Tangente ist
\[
\mathbb C_{tan}:\eta=\lambda\operatorname{tr}(\eta)I+
2G\eta+\alpha^2M\operatorname{tr}(\eta)I.
\]
Für lambda >= 0, G > 0 und M > 0 ist sie positiv definit auf symmetrischen Dehnungen. Nach Entfernung starrer Körpermoden durch ausreichende Dirichlet-Bedingungen ist die reduzierte Systemmatrix positiv definit.

## 3. Diskrete Implementierung

Das Modul ccfsm_p19_spatial_biot_bvp.py nimmt je Volumenquadraturpunkt eine Dehnungs-Verschiebungs-Matrix B (6 x ndof), Volumengewicht, Eigenstrain und Fluidinhalt entgegen. Randquadraturpunkte enthalten N (3 x ndof), äußere Gesamttraktion und Flächengewicht. Der Code assembliert die Energie-Hesse-Matrix, Eigen-/Fluidlast und Neumann-Lasten, eliminiert vorgeschriebene Verschiebungs-DOFs und löst die freien DOFs. Ausgegeben werden Verschiebung, Dehnung, Spannung, Porendruck, gespeicherte Energie, Traktionsarbeit und Reaktionsresiduen.

Voigt-Konvention: technische Dehnungen (exx, eyy, ezz, 2exy, 2eyz, 2exz); Spannungen (sxx, syy, szz, sxy, syz, sxz).

## 4. Energie und Randarbeit

\[
E_h=\sum_qw_q[\tfrac{\lambda}{2}(\operatorname{tr}E_q)^2+
GE_q:E_q+\tfrac M2(\zeta_q-\alpha\operatorname{tr}\varepsilon_q)^2].
\]
Die äußere Traktionsarbeit:
\[
W_{N,h}=\sum_{q\in\Gamma_N}w_q\,\bar t_q\cdot(N_qu).
\]
Dirichlet-Reaktionen werden separat ausgewiesen. Bei zeitabhängigen vorgeschriebenen Verschiebungen muss deren Arbeit als zusätzliche Randarbeitsleistung berücksichtigt werden.

## 5. Verifikation und Grenzen

- Regressionstests prüfen einen axialen Patch-/Bar-Fall, Eigenstrain-/Fluidantrieb, freie DOF-Gleichgewichtsresiduen, Dirichlet-Reaktionen und Singularitätsbehandlung.
- Quadratur und Interpolationsmatrizen kommen vom Aufrufer; keine konkrete Zylinder-/Tropfengeometrie oder Netzkonvergenz wird behauptet.
- zeta(x) und c(x) sind vorgeschriebene Felder. Die zeitabhängige Rückkopplung an Fluid-/Si-Reaktions-PDEs ist noch nicht implementiert.
- Keine Trägheit, Viskoelastizität, endliche Dehnung, freie Oberflächenbewegung, Kontaktmechanik oder kapillare Randspannung.
- Keine neue empirische Parameterschätzung; Druckzell-/Oedometerdaten bleiben von der natürlichen Synäresekalibrierung getrennt.

P19 ist der erste räumliche mechanische Randwertlöser im Projekt, nicht bereits der vollständig gekoppelte 3D-CCFSM-Zeitintegrator.
