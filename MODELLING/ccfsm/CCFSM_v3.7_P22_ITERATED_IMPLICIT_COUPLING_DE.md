# CCFSM P22 — iterierte Druck-Mechanik-Transport-Kopplung

**Stand: 14.11.2026 · Implementierungsstufe: gedämpfte Picard-Iteration für einen impliziten Schritt**

## Ziel und Gleichung

P21 berechnet die P19-Druckrückkopplung einmal pro Zustand. P22 iteriert diesen Rückweg innerhalb eines Zeitschritts. Für den Zustandsvektor (x=(\theta,n_M,n_O,n_N,n_B)) wird ein impliziter-Euler-Schritt durch die Fixpunktgleichung

\[
x^{k+1}=x^n+\Delta t\,F_{P21}(x^k)
\]

approximiert. In jedem Iterationsschritt werden P9/P13-Zustände aktualisiert, P19 erneut gelöst, dessen Quadraturdruck auf FV-Zellen projiziert und der P21-Darcy-/Advektionsoperator neu ausgewertet. Die Iteration verwendet Unterrelaxation.

## Konvergenzkontrolle (P22.1)

Das Zustandskriterium verwendet den **unrelaxierten Fixpunktdefekt**:

\[
r_{FP}^k =
\frac{\|x^n+\Delta t F_{P21}(x^k)-x^k\|_\infty}
{\max(10^{-30},\|x^n+\Delta t F_{P21}(x^k)\|_\infty,\|x^k\|_\infty)}.
\]

Damit kann eine kleine Unterrelaxation \(\omega\) den gemeldeten Defekt nicht künstlich verkleinern. Der Druckdefekt bleibt ein separates relatives Änderungsmaß zwischen aufeinanderfolgenden P21-Druck-Snapshots. Ein akzeptierter Zustand ist der aktuelle Iterand \(x^k\), an dem auch der zuletzt gespeicherte Druck-Snapshot ausgewertet wurde. Die Akzeptanz erfordert, dass beide Kriterien erfüllt sind.

Der Admissibilitäts-Limiter berücksichtigt nun sowohl die strikte Positivität der Inventare und Fluidkapazität als auch die obere Schranke \(\theta\leq1\). Bei einer Bewegung zur unteren oder oberen Grenze wird eine Sicherheitsmarge von 5 % eingehalten. Kann die erforderliche Relaxation nicht oberhalb der Mindestrelaxation ausgeführt werden, wird kein Zustand akzeptiert.


## Implementierung und Tests

- `ccfsm_p22_iterated_implicit_coupling.py`: gedämpfter Picard-Fixpunktlöser.
- `test_ccfsm_p22_iterated_implicit_coupling.py`: Konvergenz, Positivität, Zeitfortschritt, unrelaxierter Fixpunktdefekt, Schutz gegen Scheinkonvergenz bei kleiner Relaxation, obere Fluidkapazitätsgrenze und explizite Nichtannahme bei Nichtkonvergenz.
- P22.1 ersetzt das relaxierte Update-Residuum durch den unrelaxierten Fixpunktdefekt und stellt sicher, dass der ausgegebene Druck-Snapshot zum akzeptierten Iteranden gehört.

## Geltungsbereich und Grenzen

P22 ist ein iterierter, gestaffelter Fixpunktlöser für einen impliziten-Euler-Schritt. Es ist weder ein monolithischer Newton-Löser noch ein Existenz-/Eindeutigkeitsbeweis. Die Konvergenz ist zustands- und zeitschrittabhängig; Unterrelaxation garantiert sie nicht. Die Positivitätsbegrenzung schützt die Zustandsvariablen, ist aber kein Energieargument. Es wird keine monotone Gesamtenergie behauptet: mechanische Randarbeit, offene Reservoirleistungen und die vollständige diskrete Energiebilanz sind nicht gemeinsam geschlossen. Die FE→FV-Projektion und P9-Permeabilität behalten die P21-Einschränkungen. Keine Kalibrierung oder physikalische Validierung wird behauptet. Natürliche Synärese bleibt getrennt von erzwungener Druckzell-/Oedometerkonsolidierung.

## Nächste Schritte

1. P23: diskrete Energie- und Siliziumbilanz des akzeptierten P22-Schritts einschließlich Randflüssen.
2. P24: Vergleich mit einem unabhängigen monolithischen/Newton-Referenzlöser auf kleinen Testnetzen.
3. P25: Netz- und Zeitschrittverfeinerung.
4. Danach konservative FE/FV-Projektion und Parameteridentifikation.
