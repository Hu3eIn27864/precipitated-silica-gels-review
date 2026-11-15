# CCFSM v4.0 — P25: Zeit-/Raumverfeinerung und Solverrobustheit

**Status:** Implementierung der reproduzierbaren Verfeinerungsstudie angelegt; numerische Freigabe erst nach erfolgreichem CI-Lauf und Auswertung der Artefakte.  
**Geltungsbereich:** synthetische, kleine FV/FE-Referenzfälle der P19–P24-Kette. Keine neue Materialkalibrierung und keine physikalische Validierung.

## Fragestellung

P25 prüft, ob die gekoppelte diskrete Lösung unter getrennten Verfeinerungen stabil und reproduzierbar bleibt. Die Studie trennt:

1. Zeitverfeinerung bei festem FV/FE-Netz: Endzeit konstant, 1/2/4 implizite Euler-Schritte.
2. Raumverfeinerung bei festem Endzeit-/Zeitschritt: 1/2/4 FV-Zellen mit zugeordneten axialen P19-FE-Elementen.
3. Newton-Robustheit: Vorwärts-FD-Schrittweiten (10^{-4},10^{-6},10^{-8}).
4. Picard-Robustheit: Relaxationen (0.2,0.5,1.0).

Die Referenzmechanik bettet einen axialen 1D-FE-Ansatz in den 3D-Voigt-Assembler ein. Transversale Freiheitsgrade und die linke axiale Verschiebung sind fixiert; je FV-Zelle wird ein positiver FE-Quadraturpunkt mit dem Zellindex verknüpft. Das ist ein kontrollierter Verfeinerungstest des vorhandenen Adapters, kein allgemeiner nichtpassender FE/FV-Projektionsbeweis.

## Kennzahlen

- Zeitfolge: relative (L^infty)-Abweichung jeder Endlösung gegen die feinste Zeitfolge bei gleicher Endzeit; kumulierte Iterationszahl und maximales nichtlineares Residuum.
- Raumfolge: P22/P24-Zustands- und projizierter Druckvergleich auf jedem identischen Netz; Iterationen und Solverresiduen.
- P23: unabhängiges Siliciumbilanzresiduum gegen den offenen M/O-Randfluss.
- Admissibilität: (min	heta>0), (max	hetaleq1), positive Inventare.
- Solverrobustheit: Konvergenzstatus, Iterationen, Endresiduum, FD-Schrittweite bzw. Picard-Relaxation.

Eine beobachtete Ordnung wird nur dann ausgewiesen, wenn mindestens drei asymptotische, monotone Fehlerstufen vorliegen. Ein Fehler gegen die feinste berechnete Lösung ist zunächst ein Verfeinerungsindikator, kein Fehler gegen eine exakte Lösung. Die Zeitstudie mit implizitem Euler kann bei zu groben Schritten außerhalb des asymptotischen Bereichs liegen.

## Ausführung

Im Paketverzeichnis:

```bash
python ccfsm_p25_refinement_study.py --output-dir ccfsm-p25-results
python -m unittest -v
```

Die drei CSV-Dateien und `summary.json` werden als CI-Artefakt veröffentlicht. Die Tests der Studienkonfiguration allein belegen noch keine Konvergenz.

## Vorläufige Grenzen und Freigabekriterien

- Die P24-Jacobi-Matrix bleibt vorwärts-finiten-differenziert; die drei Schrittweiten messen Empfindlichkeit, ersetzen aber keine analytische Jacobimatrix oder Konditionsanalyse.
- P22-Relaxationswerte testen Solverrobustheit, beweisen keine globale Kontraktion.
- P19 bleibt quasistatisch; P21 ist eine gestaffelte Momentankopplung.
- P23 liefert eine FV-Siliciumbilanz, aber keinen globalen diskreten Energieabschluss.
- Ein grüner Softwaretest ist numerische Implementierungsverifikation, keine physikalische Validierung.

**Freigabe P25:** Zeit- und Raumfolgen müssen mit vollständigen Status-/Residuenangaben vorliegen; Admissibilität und Siliciumbilanz müssen auf jedem erfolgreichen Raumfall geprüft sein. Abbrüche und nichtmonotone Fehlerfolgen bleiben sichtbar und dürfen nicht aus der Auswertung entfernt werden.
