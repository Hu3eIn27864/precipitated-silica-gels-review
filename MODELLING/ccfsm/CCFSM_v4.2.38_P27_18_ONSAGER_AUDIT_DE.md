# CCFSM P27.18 — unabhängige Onsager-Flussrekonstruktion

**Stand:** 15.11.2026  
**Status:** implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel

P27.17 leitete den Diffusionsfluss als gespeicherten Gesamtfluss minus Advektionsfluss ab. P27.18 ergänzt eine zweite Berechnungsroute: Aus Konzentrationen, chemischen Potentialen, Fluidkapazität, Diffusivität und Temperaturfaktor wird der Onsager-Fluss eigenständig neu aufgebaut und mit P13/P21 verglichen.

## Rekonstruktion

Für jede Spezies gilt auf inneren Flächen
\[
J_{diff,f}^{*}=-\frac{\theta_f D\,\Lambda(c_L,c_R)}{RT}
\frac{\mu_R-\mu_L}{\Delta x},
\]
mit logarithmischem Mittel \(\Lambda\). An den Reservoirgrenzen werden die halben Zellabstände verwendet. Die Dissipation wird unabhängig aus
\[
\mathcal D=\sum_f L_f(\nabla_f\mu)^2\,\ell_f\geq0
\]
einschließlich der beiden Rand-Halbzellen rekonstruiert.

## Prüfgates

- Vergleich jedes inneren und äußeren Diffusionsflusses mit P13/P21: \(J_{total}-J_{adv}\).
- Vergleich der unabhängig rekonstruierten Diffusionsdissipation mit dem gespeicherten P13-Wert.
- Nichtnegativität der rekonstruierten Dissipation.
- Null-Diffusivität, Ein-Zell-Grenzfall, identische Konzentrationen und ungültige positive Zustände.

## Aussagegrenzen

Die Rekonstruktion ist unabhängig vom gespeicherten Gesamtfluss, verwendet aber die vom Aufrufer gelieferten Konzentrationen und chemischen Potentiale. Sie validiert weder deren chemische Herleitung noch die Parameterwahl, die Vollständigkeit der P13-Kopplung, die Entropiebilanz der Advektion, 3-D-Erhaltung oder experimentelle Physik. Die numerische Toleranz ist eine algebraische Vergleichstoleranz, kein Fehlerabschätzungssatz.
