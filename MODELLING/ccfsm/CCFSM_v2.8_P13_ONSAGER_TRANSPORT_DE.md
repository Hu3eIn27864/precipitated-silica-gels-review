# CCFSM P13 — Onsager-konformer Stofftransport und mechanisches Lastpotential

**Status:** numerisch implementierter Diskretisierungsschritt; kein vollständiger offener Energiebeweis und keine empirische Kalibrierung.  
**Geltungsbereich:** 1D-Finite-Volumen-Modell der natürlichen Synärese; mobile Pools M/O, immobilisierte Netzwerkpools N/B.

## 1. Motivation

P12 zeigte, dass die chemische Reservoirleistung des P10-Upwind/Fick-Operators nur näherungsweise bilanziert werden kann. P13 formuliert den diffusionsgetriebenen Stofffluss direkt über das chemische Potential. Damit wird die lokale thermodynamische Triebkraft auch auf Zellflächen verwendet.

## 2. Onsager-Fluss

Für mobile Spezies (i\in\{M,O\}) und eine Zellfläche (f) wird

\[
J^{\mathrm{diff}}_{i,f}=-L_{i,f}\,\nabla_h\mu_{i,f},\qquad
L_{i,f}=\frac{\theta_fD_i}{RT}\,\Lambda(c_{i,L},c_{i,R}),
\]

mit logarithmischem Mittel

\[
\Lambda(a,b)=\frac{a-b}{\ln a-\ln b}>0.
\]

Für ideale Aktivitäten (\mu_i=\mu_i^0+RT\ln(\gamma_i c_i/c_*)) gilt auf jeder inneren Fläche exakt

\[
J^{\mathrm{diff}}_{i,f}
=-\theta_fD_i\frac{c_{i,R}-c_{i,L}}{\Delta x},
\]

weil (\Lambda(a,b)(\ln b-\ln a)=b-a). Die neue Form ist somit keine neue empirische Fick-Konstante, sondern eine thermodynamisch explizite Darstellung derselben idealen Fick-Diffusion.

Die innere diskrete Dissipation ist

\[
\mathcal D_{i,f}=L_{i,f}(\nabla_h\mu_{i,f})^2\Delta x\geq0.
\]

Reservoir-Halbzellen werden analog mit Abstand \(\Delta x/2\) behandelt. Die Randkonzentrationen müssen für diese logarithmische Form strikt positiv sein; Nullaktivitäten werden nicht stillschweigend regularisiert.

## 3. Was P13 tatsächlich schließt

- Der diffusive Fluss ist ein Onsager-Fluss des diskreten chemischen Potentials.
- Die innere Diffusionsdissipation ist algebraisch nichtnegativ.
- Der advective Anteil bleibt exakt der P10-Upwind-Fluss mit demselben Darcy-Fluss wie in der Fluidbilanz.
- Die mechanische Last wird als Dead-load-Potential \(\Psi_{\mathrm{load}}=\Psi-t_{\mathrm{ext}}\varepsilon_{xx}\) explizit ausgewiesen. P9-Potentialableitungen bleiben die zugehörigen Envelope-Ableitungen.

## 4. Noch nicht bewiesen

P13 ist **kein** vollständiger offener Energiebilanzsatz. Insbesondere ist der diskrete Entropiefluss des Upwind-Advektionsterms bei variabler \(\theta\), die gemeinsame Randkopplung mit dem Druckreservoir sowie die globale mechanische Randarbeit noch nicht in einer einzigen exakten Summationsidentität geschlossen. Die ausgegebene nichtnegative Diffusionsdissipation beweist nicht automatisch eine nichtzunehmende Gesamtenergie.

Die Lastpotentialfunktion ist eine thermodynamisch konsistente Kandidatenfunktion für konstante Dead-load-Traktion. Ihre vollständige Kopplung an räumliche Mechanik und Randarbeit bleibt offen; P9 ist weiterhin eine lokale 1D-Bar-Konstitutivschließung.

## 5. Verifikation

Regressionstests prüfen:
- Nichtnegativität der Onsager-Diffusionsdissipation,
- verschwindenden inneren Diffusionsfluss bei konstanten Konzentrationen,
- Null-Dissipation für \(D_i=0\),
- explizite Trennung von Advektion und Diffusion,
- Abhängigkeit des Lastpotentials von der äußeren Traktion,
- Zurückweisung nichtpositiver Reservoiraktivitäten.

Die Tests sind Software-/Algebraieverifikation, keine physikalische Validierung. Permeabilitäts-, Eigenstrain-, Aktivitäts- und Reaktionsparameter bleiben teilweise Hypothesen bzw. nicht identifiziert. Für natürliche Synärese werden keine Koeffizienten aus Oedometer- oder erzwungener Druckzellensynerese übernommen.

## 6. Nächster Schritt P14

Eine diskrete Summations-by-parts-/Entropiefluss-Analyse für Upwind-Advektion und variable Fluidkapazität; danach ein gemeinsamer Randpotentialterm für Druck- und Stoffreservoir sowie ein globaler mechanischer Lastarbeitsnachweis. Erst wenn diese Terme exakt zusammenpassen, ist ein vollständiger diskreter Energie-/Entropiesatz gerechtfertigt.
