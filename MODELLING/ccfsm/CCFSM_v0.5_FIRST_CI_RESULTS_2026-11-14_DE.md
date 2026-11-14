# CCFSM v0.5 — Provenienzkorrektur zum ersten CI-Lauf

**Wichtige Korrektur:** Die erste v0.5-CI-Fassung vom 14.11.2026 (Run 43595413689) hat 14 Reihen aus DATA/Raw/kurvendigitalisierung.csv fälschlich als natürliche Synärese eingestuft. Die Bedingungsfelder weisen diese Reihen jedoch als Druckdifferenzbedingungen Δp aus. Der Abgleich mit Wilhelm & Kind (2015), Figure 12/Table 3, bestätigt, dass es sich um erzwungene Synärese in einer Druckzelle handelt. Die frühere Zusammenfassung mit 14 natürlichen Kurven, 42 Fits, 4/10/0 AICc-Siegen und den dazugehörigen Holdout-Fehlern ist als natürliche Kalibrierung **zurückgezogen** und darf nicht für natürliche CCFSM-Schlussfolgerungen verwendet werden.

Die Softwaretests des alten Laufs waren technisch erfolgreich, aber ein technischer Test kann eine falsche wissenschaftliche Datenklassifikation nicht erkennen. Dieser Eintrag bleibt zur vollständigen Nachvollziehbarkeit erhalten.

## Korrigierte Datenbasis

Die korrigierte Pipeline verwendet nur sieben primäre natürliche Näherungskurven aus LITERATURE/wilhelm_kind_approximate_measurement_points_curated.csv (Figures 8 und 10). Diese Punkte sind KI-gestützte ungeprüfte Näherungsablesungen, keine pixelkalibrierten Originalmarker und keine Autor-Rohdaten. Die 22 sensitivity_only-Punkte und 44 figure_table_conflict_branch-Punkte bleiben getrennt und ausgeschlossen.

DATA/Raw/kurvendigitalisierung.csv wird nur noch auf Provenienz geprüft. Seine 21 Reihen mit Δp-Bedingungen werden als Druckzell-/erzwungene Synärese geführt und nicht in natürliche Fits eingespeist.

## Maßgebliche Quellen

- Wilhelm & Kind (2015), Abschnitt 4.1: natürliche Zylinder- und Tröpfchenreihen in Figures 8 und 10, Tables 1 und 2.
- Wilhelm & Kind (2015), Abschnitt 4.2: erzwungene Druckzell-Synärese in Figure 12 und Table 3.
- Wilhelm, Dissertation (2017), Abschnitt 5.2: erzwungene Synärese; Table 5.4 mit Δp-Werten.

Die korrigierte CI-Auswertung wird in einem separaten neuen Lauf dokumentiert. Bis dahin gibt es aus v0.5 keine gültigen neuen natürlichen Modellvergleichsergebnisse.
