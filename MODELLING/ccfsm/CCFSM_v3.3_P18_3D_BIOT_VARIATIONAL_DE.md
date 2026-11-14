# CCFSM P18 — 3D-Biot-Eigenstrain-Kern und Randbedingungsreduktionen

**Status:** dreidimensionaler isotroper Kleinverzerrungs-Kern aus einer gemeinsamen Energie; numerisch durch Energieableitungen und Reduktionsidentitäten geprüft. Noch kein räumlicher PDE-Löser und keine physikalische Kalibrierung.

## 1. 3D-Zustand und freie Energie

Für symmetrische infinitesimale Gesamtdehnung \(\varepsilon\), isotrope chemische Eigenstrain \(\varepsilon_{ch}\mathbf I\), Fluidinhaltsänderung \(\zeta\), Lamé-Parameter \(\lambda,G\), Biot-Modul \(M\) und Biot-Koeffizient \(\alpha\) definieren wir
\[
E=\varepsilon-\varepsilon_{ch}\mathbf I,\quad
p=M(\zeta-\alpha\operatorname{tr}\varepsilon).
\]
Die gespeicherte Energie pro Referenzvolumen:
\[
\boxed{\psi(\varepsilon,\zeta,\varepsilon_{ch})=
\frac{\lambda}{2}(\operatorname{tr}E)^2+
G E:E+\frac{M}{2}(\zeta-\alpha\operatorname{tr}\varepsilon)^2.}
\]

## 2. 3D-Spannung und Konjugierte

Direkte Variation liefert
\[
\boxed{\sigma=\lambda\operatorname{tr}(E)\mathbf I
+2GE-\alpha p\mathbf I.}
\]
Die Fluidkonjugierte ist \(\partial_\zeta\psi=p\). Die isotrope Eigenstrain-Konjugierte ist
\[
\frac{\partial\psi}{\partial\varepsilon_{ch}}
=-(3\lambda+2G)\operatorname{tr}E.
\]
Damit ist die mechanische Rückwirkung auf den Brückenanteil bei \(\varepsilon_{ch}=\beta_B(b-b_0)\) aus derselben Energie bestimmt. Schubspannungen folgen als \(\sigma_{ij}=2G\varepsilon_{ij}\) für \(i\ne j\).

## 3. Zwei verschiedene axiale Randwertreduktionen

Die Randbedingungen dürfen nicht vermischt werden.

**A. Plane strain / seitlich festgehalten:** \(\varepsilon_{yy}=\varepsilon_{zz}=0\). Für \(\varepsilon_{xx}=e\):
\[
t=\lambda(e-3\varepsilon_{ch})+2G(e-\varepsilon_{ch})-\alpha p.
\]
Das ist exakt die P17-Reduktion. Die seitlichen Reaktionsspannungen sind im Allgemeinen nicht null.

**B. Uniaxial stress / seitlich spannungsfrei:** \(\sigma_{yy}=\sigma_{zz}=0\), bei Symmetrie \(\varepsilon_{yy}=\varepsilon_{zz}=l\). Dann werden \(e,l,p\) gemeinsam aus
\[
\begin{aligned}
(\lambda+2G)e+2\lambda l-\alpha p
 &=t+(3\lambda+2G)\varepsilon_{ch},\\
\lambda e+2(\lambda+G)l-\alpha p
 &=(3\lambda+2G)\varepsilon_{ch},\\
\alpha M(e+2l)+p&=M\zeta
\end{aligned}
\]
bestimmt. Die laterale Dehnung ist eine Lösung, keine vorab verschwindende Größe. P18 implementiert beide Fälle getrennt.

## 4. Verifikation

- Zentrale Finite-Differenzen prüfen \(\partial\psi/\partial\varepsilon_{ii}=\sigma_{ii}\).
- Schubspannungs-/Schubdehnungs-Konjugation wird geprüft.
- Plane-strain-Auswertung reproduziert die P17-Gleichungen.
- Uniaxial-stress-Lösung prüft axiale Traktion, beide lateralen Nullspannungen und Biot-Druck.
- Eingaben werden auf endliche Werte und symmetrische Dehnung geprüft.

## 5. Geltungsgrenzen und Konsequenzen für CCFSM

- Kleinverzerrung, isotrope lineare Elastizität, isotrope Eigenstrain, skalares Biot-Modell und konstante Materialparameter.
- Keine räumliche Gleichgewichts-PDE \(\nabla\cdot\sigma=0\), keine Verschiebungsrandbedingungen auf einer realen Zylinder-/Tropfengeometrie und keine freien Oberflächenbewegungen.
- Keine mechanische Randarbeitsbilanz in P16 und kein vollständiger offener System-Energiesatz.
- P17 entspricht dem seitlich festgehaltenen Spezialfall; eine reale Probe mit freien Seitenflächen könnte eher eine uniaxiale Spannungsreduktion oder eine räumliche Randwertlösung verlangen. Die passende Geometrie muss anhand des Versuchsaufbaus entschieden werden.
- Keine neuen Parameter werden aus den natürlichen Schrumpfkurven identifiziert; keine Druckzell-/Oedometerwerte werden in natürliche Synäresekalibrierung übernommen.

P18 ist somit der 3D-konstitutive Kern und die saubere Trennung zweier axialer Randbedingungsmodelle, nicht bereits der vollständige 3D-Solver.
