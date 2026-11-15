# CCFSM v4.2.52 — P27.32: abgesicherte Bisektionsverfeinerung von Ereigniszeitpunkten

## Ziel

P27.31 erzeugt durch adaptive Mittelpunktabtastung zusätzliche Flux-Stützstellen und kann dadurch versteckte Vorzeichenwechsel sichtbar machen. P27.32 verfeinert jeden so gefundenen Vorzeichenwechsel mit einer abgesicherten Bisektion.

## Verfahren

Für einen kontinuierlichen skalaren Fluss (f(t)) und einen strikt vorzeichenwechselnden Startklammer ([a_0,b_0]) gilt: Die Bisektion wählt (m_k=(a_k+b_k)/2) und behält die Teilklammer, deren Endwerte unterschiedliche Vorzeichen besitzen. Damit bleibt eine Nullstelle innerhalb der Klammer, sofern (f) stetig ist. Abbruch erfolgt über Flusstoleranz, Klammerbreite oder Iterationslimit.

Ausgegeben werden Nullstellenschätzer, finale Zeitklammer, Klammerbreite, Flussresiduum, Iterationszahl und Abbruchgrund. Ein nicht konvergierter Iterationslimit-Fall wird ausdrücklich als solcher markiert.

## Synthetischer Referenzfall

- Verstecktes Nullstellenpaar: (f(t)=(t-0.35)(t-0.75)), beide groben Endpunkte haben dasselbe Vorzeichen.
- Zusätzliche lineare Flüsse: (t-1.0) und (t-1.5).
- P27.31 stellt adaptive Brackets bereit; P27.32 verfeinert sie auf eine Zeitklammerbreite von höchstens (10^{-10},mathrm{s}) im Standardfall.

## Verifikation

Sechs Regressionstests decken das versteckte Nullstellenpaar, lineare Nullstellen, eine Nullstelle am Intervallrand, ungültige Klammern, nichtendliche Flüsse und den expliziten Iterationslimit-Fall ab.

## Mathematische Reichweite und Grenzen

Die Bisektion liefert eine robuste Einschließung **für jede bereits gefundene strikt vorzeichenwechselnde Klammer**, unter der Annahme der Stetigkeit. Sie beweist nicht, dass P27.31 alle Nullstellen gefunden hat. Berührende Nullstellen ohne Vorzeichenwechsel, hochfrequente Oszillationen zwischen Abtastpunkten und Nullstellen außerhalb der adaptiv erkannten Klammern können unentdeckt bleiben. Es wird keine Intervallarithmetik eingesetzt; Rundungsfehler sind daher nicht formal zertifiziert.

P27.32 beweist weder die vollständige diskrete Upwind-Entropiekette noch die Positivität des gekoppelten 3D-Systems, integriert noch keine reale P24-Newton-Trajektorie und ist keine experimentelle/physikalische Validierung.

## Nächster wissenschaftlicher Gate

Als nächstes sind (i) die P27.31/P27.32-Verifikation im vollständigen CI, (ii) adversariale Fluxfamilien mit tangentialen und mehrfachen Nullstellen und (iii) Intervall- oder Ableitungsgrenzen für eine echte Vollständigkeitsgarantie erforderlich.
