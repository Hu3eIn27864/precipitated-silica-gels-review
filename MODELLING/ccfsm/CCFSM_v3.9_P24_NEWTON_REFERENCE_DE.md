# CCFSM P24 — unabhängiger Newton-Referenzlöser für den P22-Zeitschritt

**Stand:** 15.11.2026  
**Ziel:** P22 (gedämpfter Picard) gegen einen unabhängig implementierten Löser derselben impliziten P21-Zustandsgleichung vergleichen.

## 1. Nichtlineares Referenzproblem

Gesucht ist der FV-Zustand (x=(\theta,n_M,n_O,n_N,n_B)) mit

[
R(x)=x-x^n-\Delta t F_{P21}(x)=0.
]

Jede Residuumsauswertung ruft P21 mit dem aktuellen vollständigen Zustand auf. P21 projiziert den P19-FE-Druck auf FV-Zellen und verwendet ihn in Darcy-Fluss und mobiler M/O-Advektion. Die P19-Gleichgewichtsmechanik wird bei jeder Residuumsauswertung neu gelöst. Die FE-Verschiebungsfreiheitsgrade werden somit durch den P19-Unterlöser statisch kondensiert; sie werden nicht als zusätzliche Newton-Unbekannte geführt.

Der Referenzlöser verwendet einen vorwärts-differenzierten Jacobi-Operator und einen gedämpften Newton-Schritt mit Backtracking. Dies ist bewusst ein transparenter kleiner Referenzlöser, kein effizienter Produktionssolver und kein analytischer Jacobian.

## 2. Algorithmus

1. Anfangszustand (x^n) als Startwert setzen.
2. Für jeden Versuchszustand (x): P21/P20/P19 neu auswerten und (R(x)) bilden.
3. Skalierte Jacobi-Matrix mit vorwärts gerichteten endlichen Differenzen aufbauen.
4. Lineares Newton-System mit Pivotisierung lösen.
5. Backtracking akzeptiert nur strikt positive Inventare, (0<\theta\leq1) und eine echte Verringerung der skalierten Residualnorm.
6. Bei Erreichen der Toleranz den finalen P21/P19-Snapshot am exakt zurückgegebenen Zustand erneut berechnen.
7. Bei Singularität, fehlgeschlagener Liniensuche oder Iterationslimit keinen akzeptierten Zustand zurückgeben.

Die Normierung verwendet die Größenordnung des jeweiligen Anfangszustands. Die finite-difference Schrittweite, Toleranz und Iterationsgrenze sind explizite Parameter.

## 3. Vergleich zu P22

`p24_compare_with_p22` vergleicht nach erfolgreicher Konvergenz:
- absolute und relative Unendlichnorm-Differenz des gesamten FV-Zustands,
- absolute und relative Differenz des auf FV-Zellen projizierten P19-Drucks,
- Übereinstimmung der akzeptierten Endzeit.

Beide Löser müssen dieselbe Anfangsbedingung, Zeitschrittweite, Geometrie-/FE-Quadratur, Randbedingungen, Parameter und P21-Operator verwenden. Unterschiedliche Solverkonvergenz bedeutet nicht automatisch unterschiedliche Physik; zuerst sind Residualtoleranz, FD-Schrittweite und Newton-Abbruch zu prüfen.

## 4. Tests und Aussagegrenzen

- `ccfsm_p24_newton_reference.py`: unabhängiger gedämpfter Newton-Referenzlöser.
- `test_ccfsm_p24_newton_reference.py`: Konvergenz/Admissibilität, Vergleich mit P22, Nichtannahme bei Iterationslimit und Validierung des Vergleichseingangs.
- P19 wird in jeder Residuumsauswertung neu gelöst; die Jacobian-Spalten enthalten dadurch numerisch auch die mechanische Druckrückkopplung.
- Die FD-Jacobi-Matrix ist schrittweitenabhängig und kann bei stark nichtlinearen oder schlecht konditionierten Fällen unzuverlässig sein. P24 meldet Singularität bzw. Liniensuchversagen statt einen Zustand zu akzeptieren.
- Ein erfolgreicher Solververgleich ist numerische Verifikation für den konkreten diskreten Testfall, kein Beweis allgemeiner Newton-Konvergenz, keine Netz-/Zeitkonvergenz und keine physikalische Validierung.

## 5. Bewusste Reichweite

P24 ist ein Referenzlöser für kleine FV/FE-Probleme. Er löst nicht gleichzeitig die FE-Verschiebungen in einem voll monolithischen Blocksystem, sondern eliminiert sie durch den direkten P19-Gleichgewichtslöser innerhalb jeder Residuumsauswertung. Das ist eine mathematisch definierte reduzierte/Schur-komplementartige Formulierung derselben gekoppelten Gleichung, sofern P19 für jeden Zustand eindeutig lösbar ist.

**Status:** Implementierung und Regressionstests eingecheckt. Hosted workflow [#283](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43669754294) ist grün; der vollständige Testlauf meldet 270 Tests bestanden. Das ist Softwareverifikation, keine physikalische Validierung. Nächster Schritt nach erfolgreichem Vergleich: P25 Zeit-/Raumverfeinerung und Konditions-/Robustheitsanalyse.
