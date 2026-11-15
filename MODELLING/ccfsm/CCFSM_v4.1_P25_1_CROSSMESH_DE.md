# CCFSM P25.1 — konservative Netzübertragung und Gradient-Stresstest

**Status:** Implementierung angelegt; quantitative Freigabe erst nach CI-Lauf und Artefaktprüfung.  
**Ziel:** die offene P25-Lücke schließen, dass bisherige Raumvergleiche nur P22 gegen P24 auf demselben Netz verglichen und die Anfangsprofile netzabhängig parametrisiert waren.

## Methodik

1. Ein gemeinsames, mesh-unabhängiges lineares Anfangsprofil wird an Zellmittelpunkten abgetastet. Damit ist der FV-Zellmittelwert auf allen gleichmäßigen Netzen konsistent.
2. Zeitverfeinerung bei festem Netz (N=4), identischer Endzeit (T=10^{-2},s), 1/2/4/8/16 implizite Schritte.
3. Raumfolge (N=1,2,4,8), ein P19-Element pro FV-Zelle, jeweils ein Schritt bis zur identischen Endzeit.
4. Grobe FV-Zellmittelwerte werden aus dem feinsten (N=8)-Zustand durch blockweise Volumenmittelung zurückprojiziert. Für gleichmäßige verschachtelte Netze erhält diese Restriktion das Integral jeder Zustandskomponente bis auf Gleitkomma-Rundung exakt.
5. Der P19-Druck wird separat durch dieselbe Volumenmittelung verglichen; Druck ist keine konservierte Stoffinventargröße.
6. Ein erhöhter konstanter Reservoirdruck (10^5,Pa) und räumlich veränderliche Anfangszustände erzeugen einen anspruchsvolleren gekoppelten Druck-/Darcy-Fall. Druckspanne und maximale Darcy-Flussstärke werden dokumentiert.
7. P23 prüft die globale Siliciumbilanz auf jedem erfolgreichen Netz; separate P22/P24-Vergleiche prüfen Solverübereinstimmung auf identischen Netzen.

## Fehlernormen

Für Zustandsvektor (u) und seine auf das grobe Netz restringierte Feinlösung:

- (L^infty): maximaler Zellfehler.
- volumen-gewichtete (L^1): (sum_j Delta x |e_j|).
- volumen-gewichtete (L^2): ((sum_j Delta x e_j^2)^{1/2}).

Relative Normen werden gegen die restringierte Feinlösung normiert. Paarweise beobachtete Raten werden nur als Diagnose aus den Fehlern relativ zur (N=8)-Referenz ausgewiesen; da die feinste Lösung selbst nicht exakt ist, sind dies keine mathematischen Konvergenzbeweise. Die (N=8)-Referenz hat definitionsgemäß Fehler null und wird nicht zur Rate herangezogen.

## Freigabegrenzen

- Restriktion muss Mittelwerte/Integrale jeder FV-Komponente erhalten.
- Anfangsprofil muss beim Wechsel der Netzauflösung dieselbe kontinuierliche Referenz darstellen.
- Zeit-/Raumfolgen müssen Konvergenzstatus, Solverresiduen, Admissibilität und Stoffbilanz sichtbar ausweisen.
- Druckgradient und Darcy-Fluss müssen tatsächlich ungleich null sein; andernfalls gilt der Stresstest als nicht aktiviert.
- P22/P24-Abweichungen auf identischen Netzen separat von Netzfehlern berichten.
- Keine Energie-Monotonie, Materialkalibrierung oder physikalische Validierung aus diesem synthetischen Test ableiten.

## Reproduktion

```bash
python ccfsm_p25_1_refinement_study.py --output-dir ccfsm-p25-1-results
python -m unittest MODELLING/ccfsm/test_ccfsm_p25_1_refinement_study.py -v
```

CI veröffentlicht Zeit-, Cross-Mesh- und Solververgleichs-CSV sowie `summary.json`.
