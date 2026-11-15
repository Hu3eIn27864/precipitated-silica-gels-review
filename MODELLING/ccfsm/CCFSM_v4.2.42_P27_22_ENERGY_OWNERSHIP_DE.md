# CCFSM P27.22 — P9/P19-Energieäquivalenz und Exklusivitäts-Audit

**Datum:** 15.11.2026  
**Status:** implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel und Ergebnis

P9 gibt eine lokale gespeicherte Energiedichte aus elastischem, Biot-Speicher- und chemischem Anteil aus. P19 integriert elastische und Biot-Speicherenergie über FE-Quadratur. P27.22 vergleicht die mechanischen Terme punktweise und integriert, statt beide Darstellungen zu addieren.

Das Modul rekonstruiert P19s Quadraturenergie unabhängig aus B-Matrix, Verschiebungs-DOFs, Eigenstrain, Fluidgehaltszuwachs und Volumengewicht:
\[
\psi_{el}=\tfrac12\lambda[\operatorname{tr}(\varepsilon-\varepsilon^*)]^2
+G(\varepsilon-\varepsilon^*):(\varepsilon-\varepsilon^*),\qquad
\psi_B=\tfrac12M(\zeta-\alpha\operatorname{tr}\varepsilon)^2.
\]

P9 und P19 müssen dieselben Lamé-/Biot-Parameter und an jedem Quadraturpunkt denselben Zustand besitzen. Für die Vergleichbarkeit wird P9s Spezialkinematik ausdrücklich verlangt: nur axiale Gesamtdehnung, verschwindende laterale und Scherdehnungen, isotroper Eigenstrain. Zusätzlich muss die Summe der rekonstruierten P19-Terme P19s gespeicherter Gesamtenergie entsprechen.

## Exklusivitätsregel

mechanical_energy_owner wählt genau eine mechanische Buchung: p9 oder p19. Die jeweils andere Darstellung dient nur als Auditvergleich. P9-Chemie ist separat und wird nur bei chemical_energy_owner="p9" aufgenommen. P19 enthält derzeit keinen chemischen Energieterm.

## Grenzen

Die Äquivalenz gilt nur für den abgeglichenen Spezialfall, nicht für beliebige 3D-Dehnungszustände. Äußeres Traktionspotential, Dirichlet-Reaktionsarbeit, Gradientenergien sowie P10/P13-Reaktions- und Transportbeiträge sind nicht enthalten. Eine gemeinsame freie Energie für P10/P13/P19/P21, vollständige Variationsstruktur, geschlossener diskreter Energiebilanzsatz und physikalische Validierung bleiben offen.

## Regressionen

Fünf Tests prüfen Übereinstimmung, alternative exklusive P9-Buchung sowie Zurückweisung von Parameter-, Zustands- und Ownership-Fehlern. Ausführung: python -m unittest test_ccfsm_p27_22_energy_ownership.py -v.
