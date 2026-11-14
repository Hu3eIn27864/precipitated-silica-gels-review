# CCFSM P21 — räumliche Druckrückkopplung in den FV-Transport

**Stand: 14.11.2026 · Implementierungsstufe: gestaffelte Snapshot-Kopplung**

## Ziel

P20 führte P9/P13-Felder in die räumliche P19-Mechanik hinein, ließ aber den P13-Transport unverändert auf dem lokalen P9-Porendruck beruhen. P21 schließt diesen bislang offenen Rückweg für einen einzelnen Zustand: P19-Porendrücke werden auf FV-Zellen projiziert und treiben anschließend den Darcy-Fluss sowie die mobile M/O-Advektion.

## Projektion des FE-Drucks

Für alle FE-Quadraturpunkte (q\) einer FV-Zelle (j\) wird der Druck mit positiven Quadraturgewichten gemittelt:

\[
p_j^{FE}=\frac{\sum_{q\in Q_j}w_q p_q^{P19}}{\sum_{q\in Q_j}w_q}.
\]

Jede FV-Zelle muss mindestens einen FE-Druckwert besitzen; Gewichte müssen endlich und strikt positiv sein. Dies ist eine zellweise gewichtete Mittelwertprojektion, kein allgemeiner konservativer FE-zu-FV-Projektor für beliebige nicht deckungsgleiche Netze.

## Ein gemeinsamer Darcy-Fluss

Mit der aus P9 übernommenen Zellpermeabilität (K_j\), harmonischen inneren Flächenwerten und dem äußeren Reservoirdruck (p_{ext}\):

\[
q_{1/2}=-K_1\frac{p_1^{FE}-p_{ext}}{\Delta x/2},\quad
q_{j+1/2}=-K_{j+1/2}\frac{p_{j+1}^{FE}-p_j^{FE}}{\Delta x},\quad
q_{N+1/2}=-K_N\frac{p_{ext}-p_N^{FE}}{\Delta x/2}.
\]

Dieser identische Fluss aktualisiert Fluidkapazität und mobile Advektion:

\[
\dot\theta_j=-\frac{q_{j+1/2}-q_{j-1/2}}{\Delta x},\qquad
J_{i,f}^{adv}=q_f c_{i,upwind}.
\]

Die P13-Onsager-Diffusionsflüsse bleiben unverändert. Für M/O wird nur der alte advektive Anteil durch den neuen ersetzt; die P10-Reaktionsraten und N/B-Reaktionsbilanz bleiben erhalten. Dadurch bleibt die FV-Divergenzform konservativ und die hydraulische/mobile Advektion verwendet exakt dasselbe (q_f\).

## Software und Prüfungen

- `ccfsm_p21_two_way_pressure_feedback.py`: P20-Aufruf, FE→FV-Projektion, neuer Darcy-Fluss und konservative Ersetzung der M/O-Advektion.
- `test_ccfsm_p21_two_way_pressure_feedback.py`: Projektion, Druckrückkopplungsflags, geschlossene Fluidbilanz, fehlende Zellabdeckung und ungültige Gewichte.
- P13-Diffusion und P10-Reaktionen werden bewusst nicht neu parametrisiert.

## Statusgrenzen

P21 ist eine **gestaffelte Ein-Zustands-Rückkopplung**. Es iteriert P19 und P13 nicht bis zur Konvergenz und integriert das gekoppelte System nicht gemeinsam in der Zeit. Die FE-zu-FV-Mittelwertprojektion ist nur für die explizit zugeordneten Zellquadraturpunkte definiert. Die P9-Permeabilität bleibt eine unkalibrierte Hypothese; die mechanischen FE-Daten, Randbedingungen und Geometrie sind vom Anwender bereitzustellen. Kein globaler Energie-/Entropiesatz, kein PDE-Existenzbeweis, keine Netzkonvergenz und keine physikalische Validierung werden behauptet. Natürliche Synärese bleibt vom erzwungenen Druckzell-/Oedometerzweig getrennt.

## Nächste mathematische Schritte

1. Projektion auf nicht deckungsgleichen FE/FV-Netzen mit nachgewiesener Erhaltung und Fehlerabschätzung.
2. Iterierte Druck-/Fluss-/Mechanik-Kopplung mit Abbruchkriterium und Positivitätskontrolle.
3. Gemeinsame diskrete Energieidentität einschließlich mechanischer Randarbeit, Darcy-Dissipation, Onsager-Diffusion, Reaktionsdissipation und Reservoirleistung.
4. Erst danach ein gekoppelter Zeitintegrator; anschließend Parameteridentifikation ausschließlich aus zulässigen natürlichen Syneresedaten bzw. unabhängigen passenden Struktur-/Transportdaten.
