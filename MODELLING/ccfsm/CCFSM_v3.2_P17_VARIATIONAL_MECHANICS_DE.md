# CCFSM P17 — variational konsistente axiale Eigenstrain-/Biot-Reduktion

**Status:** algebraische Korrektur der lokalen P9-Schließung; Energieableitung und Gleichgewichtsgleichung werden nun aus derselben 3D-isotropen Energie abgeleitet. Regressionstests prüfen die Ableitung per zentraler Differenz und das Traktionsgleichgewicht. Kein globaler räumlicher Mechanik- oder PDE-Energiesatz.

## 1. Geometrie und gespeicherte Energie

Wir betrachten eine 1D-Bar-Reduktion mit axialer Gesamtdehnung e und verschwindenden lateralen Gesamtdehnungen. Die chemische Eigenstrain ist isotrop:
\[
E=\operatorname{diag}(e-e_{ch},-e_{ch},-e_{ch}),\qquad
\operatorname{tr}E=e-3e_{ch}.
\]
Die lokale elastische plus Biot-Speicherenergie pro Referenzvolumen ist
\[
\psi(e,\theta,n)=
\frac{\lambda}{2}(e-3e_{ch})^2
+G\left[(e-e_{ch})^2+2e_{ch}^2\right]
+\frac{M}{2}(\zeta-\alpha e)^2,
\quad \zeta=\theta-\theta_{ref}.
\]

## 2. Spannung aus Energievariation

Bei festgehaltenen Fluid- und chemischen Zuständen folgt
\[
\frac{\partial\psi}{\partial e}
=\lambda(e-3e_{ch})+2G(e-e_{ch})-\alpha p,
\quad p=M(\zeta-\alpha e).
\]
Damit ist die axiale Gesamtspannung
\[
\boxed{t=\lambda(e-3e_{ch})+2G(e-e_{ch})-\alpha p.}
\]
Die frühere P9-Formel \((\lambda+2G)(e-e_{ch})-\alpha p\) vernachlässigte den lateralen Eigenstrain-Beitrag in \(\operatorname{tr}E\). P17 ersetzt sie durch die Variationsableitung.

## 3. Analytische geschlossene Lösung

Mit \(H=\lambda+2G\) und \(C_e=3\lambda+2G\) gilt
\[
t=He-C_e e_{ch}-\alpha p,\qquad
e=\frac{t+C_e e_{ch}+\alpha p}{H}.
\]
Einsetzen in die Biot-Beziehung ergibt
\[
\boxed{
p=\frac{M\left[\zeta-\alpha C_e e_{ch}/H-\alpha t/H\right]}
{1+M\alpha^2/H},
\qquad
e=\frac{t+C_e e_{ch}+\alpha p}{H}.
}
\]
Somit bleiben Fluidinhaltsidentität \(\zeta=p/M+\alpha e\) und Traktionsgleichgewicht exakt erfüllt.

## 4. Chemische Rückwirkung

Die Energieableitung nach der isotropen Eigenstrain ist
\[
\frac{\partial\psi}{\partial e_{ch}}
=-(3\lambda+2G)(e-3e_{ch}).
\]
Da \(e_{ch}=\beta_B(b-b_0)\), folgt mit dem Hüllkurvenargument im quasistatischen axialen Gleichgewicht
\[
\frac{d\psi^*}{db}
=-\beta_B(3\lambda+2G)(e-3e_{ch}).
\]
Die P9-Ableitung für die mechanischen Beiträge zu den N/B-Chemiepotentialen bleibt damit konsistent; es wird keine separate Brückenenergie addiert.

## 5. Verifikation und Grenzen

- P9-Regressionstest: zentrale finite Differenz der gespeicherten Energie gegen die ausgewiesene axiale Spannung.
- P9-Traktionstest und Biot-Fluidinhaltsidentität bleiben bestehen.
- P16-Regressionstest: mechanische Stationaritätsresiduen müssen nach der Korrektur innerhalb der Toleranz liegen.
- Keine räumliche 3D-Mechanik, keine laterale Verschiebungs-/Spannungsrandbedingungen, keine mechanische Randarbeitsbilanz und kein globaler nichtlinearer PDE-Energiesatz.
- Permeabilitätsabhängigkeit von Brückenfraktion und axialer Dehnung bleibt eine unkalibrierte, falsifizierbare Hypothese.
- Natürliche Synärese bleibt vom erzwungenen Druckzell-/Oedometerzweig getrennt; keine neue empirische Kalibrierung wird behauptet.

## 6. Wissenschaftliche Bedeutung

P17 behebt eine interne Inkonsistenz zwischen P9-Energie und P9-Spannung für die explizit gewählte plane-strain-Bar-Reduktion. Es ist ein formaler Modellfortschritt, aber noch kein Nachweis, dass diese Reduktion die reale räumliche Mechanik eines alternden Silicagels vollständig beschreibt.
