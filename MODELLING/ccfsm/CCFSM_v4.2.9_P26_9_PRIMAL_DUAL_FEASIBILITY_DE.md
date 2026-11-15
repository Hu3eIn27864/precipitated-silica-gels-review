# CCFSM v4.2.9 — P26.9: primal-duale Machbarkeitsentscheidung

## Ziel

P26.9 verbindet den globalen primalen Positivitätsprojektor aus P26.6 mit den rational verifizierten dualen Unzulässigkeitszertifikaten aus P26.8. Für feste Zielzellmittelwerte und vorgegebene globale erste und zweite räumliche Momente entsteht eine dreistufige Entscheidung:

1. **certified_infeasible**: P26.8 findet einen strikt trennenden dualen Zeugen. Der rationale positive Abstand beweist, dass keine zulässige nichtnegative quadratische Rekonstruktion mit diesen Zellmittelwerten die verlangten Momente erreichen kann.
2. **feasible_verified_primal_witness**: P26.6 liefert einen Kandidaten. P26.9 prüft dessen ausgegebene Dezimalkoeffizienten anschließend mit exakter rationaler Arithmetik auf kontinuierliche Nichtnegativität in jeder Zelle. Die drei globalen Momente (einschließlich Masse) müssen innerhalb einer expliziten rationalen absoluten/relativen Toleranz liegen.
3. **unresolved**: Weder ein dualer Beweis noch ein unabhängig verifizierter primaler Zeuge liegt vor. Weder ein fehlender Separator im endlichen Suchraster noch eine fehlgeschlagene Iteration wird als Beweis fehlender Machbarkeit ausgegeben.

## Mathematische Prüfung des primalen Zeugen

Für jede Zelle wird das Minimum von
u(xi)=m+a*xi+b*(xi²-1/12), -1/2 <= xi <= 1/2
exakt aus den beiden Endpunkten und – falls b>0 und der Scheitel im Intervall liegt – dem inneren Scheitel bestimmt. Alle Eingaben und ausgegebenen Koeffizienten werden als rationale Zahlen aus ihren Dezimaldarstellungen interpretiert. Damit ist die Zellpositivität des zurückgegebenen Zeugen kein Floating-Point-Test.

Die Momentenresiduen werden ebenfalls rational berechnet und gegen
|M_k(witness)-M_k(target)| <= epsilon*max(1,|M_k(target)|)
geprüft. Der Status ist deshalb ein **verifizierter näherungsweiser primaler Zeuge**, nicht automatisch ein exakter Gleichheitsbeweis. Bei Residuum null sind die jeweiligen Momentengleichheiten exakt.

## Ablauf

- Zuerst wird P26.8 mit einem endlichen Raster ganzzahliger Richtungen aufgerufen.
- Bei positivem rationalem Trennungsabstand wird sofort certified_infeasible zurückgegeben.
- Sonst berechnet P26.6 eine gewichtete Dykstra-Projektion auf die affine Momentenmenge und das Produkt der zellweisen Positivitätsmengen.
- Der Projektionskandidat wird unabhängig rational geprüft. Nur bei exakter Zellpositivität und bestandenen rationalen Momentenschranken wird feasible_verified_primal_witness gemeldet.
- Fehler oder Nichtkonvergenz ergeben unresolved.

## Tests und Reproduzierbarkeit

ccfsm_p26_9_primal_dual_feasibility.py enthält den Orchestrator und verify_primal_witness; test_ccfsm_p26_9_primal_dual_feasibility.py deckt rationale Minima, positive und negative Zeugen, duale Priorität und Eingabevalidierung ab. Der CI-Studienlauf erzeugt CSV- und JSON-Statusberichte.

## Geltungsgrenzen

- eindimensionale Intervalle;
- feste, nichtnegative Zellmittelwerte;
- stückweise quadratische Zellrekonstruktionen;
- Erhaltung der globalen Masse durch feste Zellmittelwerte und Prüfung der globalen ersten/zweiten Momente;
- endliche duale Richtungssuche kann vorhandene Separatoren übersehen;
- die primale Projektion bleibt numerisch, auch wenn ihr ausgegebener Zeuge anschließend exakt rational geprüft wird;
- Momentengleichheiten werden mit expliziter rationaler Toleranz verifiziert;
- keine allgemeine 2-D/3-D-FE/FV-Geometrie, keine Materialkalibrierung und keine physikalische Validierung.

Softwaretests prüfen Implementierung und Reproduzierbarkeit. Sie sind kein experimenteller Nachweis für natürliche Synärese gefällter Silica-Gele.
