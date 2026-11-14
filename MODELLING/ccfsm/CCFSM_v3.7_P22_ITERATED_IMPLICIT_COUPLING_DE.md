# CCFSM P22 — iterierte Druck-Mechanik-Transport-Kopplung

**Stand: 14.11.2026 · Implementierungsstufe: gedämpfte Picard-Iteration für einen impliziten Schritt**

## Ziel und Gleichung

P21 berechnet die P19-Druckrückkopplung einmal pro Zustand. P22 iteriert diesen Rückweg innerhalb eines Zeitschritts. Für den Zustandsvektor (x=(\theta,n_M,n_O,n_N,n_B)) wird ein impliziter-Euler-Schritt durch die Fixpunktgleichung

\[
x^{k+1}=x^n+\Delta t\,F_{P21}(x^k)
\]

approximiert. In jedem Iterationsschritt werden P9/P13-Zustände aktualisiert, P19 erneut gelöst, dessen Quadraturdruck auf FV-Zellen projiziert und der P21-Darcy-/Advektionsoperator neu ausgewertet. Die Iteration verwendet Unterrelaxation.

## Konvergenzkontrolle

Zwei dimensionslose Residuen werden getrennt überwacht:

\[
r_x^k=\frac{\|x^{k+1}-x^k\|_\infty}
{\max(10^{-30},\|x^{k+1}\|_\infty,\|x^k\|_\infty)},\quad
r_p^k=\frac{\|p^{k}-p^{k-1}\|_\infty}
{\max(10^{-30},\|p^{k}\|_\infty,\|p^{k-1}\|_\infty)}.
\]

Ein Schritt wird nur als konvergiert gemeldet, wenn beide Toleranzen erfüllt sind. Eine Positivitätsbegrenzung reduziert die Relaxation, damit (0<\theta\le1) und alle vier Inventare strikt positiv bleiben. Erreicht die nötige Relaxation eine vorgegebene Untergrenze oder wird das Iterationslimit erreicht, liefert P22 ausdrücklich **keinen akzeptierten Zustand**.

## Implementierung und Tests

- `ccfsm_p22_iterated_implicit_coupling.py`: gedämpfter Picard-Fixpunktlöser.
- `test_ccfsm_p22_iterated_implicit_coupling.py`: Konvergenz, Positivität, Zeitfortschritt, Residuen und explizite Nichtannahme bei Nichtkonvergenz.

## Geltungsbereich und Grenzen

P22 ist ein iterierter, gestaffelter Fixpunktlöser für einen impliziten-Euler-Schritt. Es ist weder ein monolithischer Newton-Löser noch ein Existenz-/Eindeutigkeitsbeweis. Die Konvergenz ist zustands- und zeitschrittabhängig; Unterrelaxation garantiert sie nicht. Die Positivitätsbegrenzung schützt die Zustandsvariablen, ist aber kein Energieargument. Es wird keine monotone Gesamtenergie behauptet: mechanische Randarbeit, offene Reservoirleistungen und die vollständige diskrete Energiebilanz sind nicht gemeinsam geschlossen. Die FE→FV-Projektion und P9-Permeabilität behalten die P21-Einschränkungen. Keine Kalibrierung oder physikalische Validierung wird behauptet. Natürliche Synärese bleibt getrennt von erzwungener Druckzell-/Oedometerkonsolidierung.

## Nächste Schritte

1. Kontraktions-/Stabilitätsbedingungen für den Fixpunktoperator und adaptive Zeitschrittsteuerung.
2. Energie- und Siliziumbilanz-Audits des tatsächlich iterierten Schritts einschließlich Randflüssen.
3. Vergleich mit einem unabhängigen monolithischen/ Newton-Referenzlöser auf kleinen Testnetzen.
4. Netz- und Zeitschrittverfeinerung sowie Parameteridentifikation erst nach diesen numerischen Prüfungen.
