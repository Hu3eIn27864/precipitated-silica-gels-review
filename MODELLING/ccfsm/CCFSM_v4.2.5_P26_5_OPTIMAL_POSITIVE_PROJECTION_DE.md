# CCFSM v4.2.5 — P26.5 momentenschonende Positivitätsprojektion

## Ziel

P26.4 skaliert die lineare und quadratische Zielzellenmode gemeinsam. P26.5 ersetzt diese radiale Begrenzung durch eine lokale gewichtete Nächstpunktprojektion auf den konvexen Kegel nichtnegativer quadratischer Rekonstruktionen.

## 1. Optimierungsproblem

Für festes Zellmittel \(m\geq0\) und ursprüngliche Moden \(z_0=(a_0,b_0)\) wird gelöst:

\[
\min_{a,b}\;w_1(a-a_0)^2+w_2(b-b_0)^2
\]
unter
\[
m+a\xi+b(\xi^2-1/12)\geq0
\quad\forall\xi\in[-1/2,1/2],
\qquad w_1,w_2>0.
\]

Die zulässige Menge ist der Schnitt einer Familie von Halbräumen und damit konvex. Für \(m=0\) ist nur \(a=b=0\) zulässig. Die Masse bleibt fest, weil die beiden Moden zellweise Mittelwert null besitzen.

## 2. Numerische Lösung

Der Solver verwendet ein Cutting-Plane-/Active-Set-Verfahren in zwei Koeffizientenvariablen:

1. Starte mit den ursprünglichen Moden.
2. Bestimme das exakte Minimum des aktuellen quadratischen Polynoms aus den beiden Randpunkten und ggf. dem inneren Scheitelpunkt.
3. Ist die Positivitätsbedingung verletzt, füge die zugehörige lineare Halbraumbedingung hinzu.
4. Projiziere den Ausgangspunkt im gewichteten euklidischen Abstand auf den Schnitt der bisher aktiven Halbräume. In zwei Dimensionen genügt die Prüfung des Ausgangspunkts, der Einzelrandprojektionen und paarweiser aktiver Schnittpunkte.
5. Wiederhole bis zur Toleranz; bei Nichterreichen wird explizit abgebrochen.

Die Implementierung benötigt keine externe Optimierungsbibliothek. Die Gewichte sind positive dimensionslose Koeffizientengewichte; Standard ist (1,1). Ein kleiner numerischer Sicherheitsabstand und endliche Iterationsgrenzen sind dokumentiert.

## 3. Erhaltung und Zielkonflikte

- Zellmittelwert und Zellmasse bleiben exakt fest; damit bleibt die globale Masse fest.
- Nichtnegativität wird über das gesamte Zellintervall geprüft, nicht nur an Stützstellen.
- Erste und zweite räumliche Momente werden nach der Projektion bilanziert, sind aber keine expliziten Nebenbedingungen dieses lokalen Optimierungsproblems.
- Das Minimum der Koeffizientendistanz ist nicht dasselbe wie das Minimum eines globalen Momentenfehlers. Eine globale Nebenbedingung für erstes/zweites Moment wäre ein anderes, gekoppeltes Optimierungsproblem über mehrere Zellen.

## 4. Vergleich mit P26.4

Die Studie vergleicht P26.5 gegen P26.4 für fünf synthetische Fälle: Randunterschwinger, inneres Scheitelpunktunterschwingen, gemischte Moden, Nullmittelwert und bereits positives Polynom. Berichtet werden Positivitätsminimum, Massenänderung, Änderungen der ersten/zweiten Momente und Koeffizienten-Zielfunktion. Eine Verbesserung der globalen Momente wird nur dann behauptet, wenn sie in den Ergebnissen tatsächlich beobachtet wird.

## 5. Grenzen

1-D-Intervalle und quadratische Felder; lokale zellweise Optimierung, keine globale Momentenrestriktion, keine 2-D/3-D-Geometrie, keine Druck-/Energieerhaltung und keine physikalische Validierung. Die Koeffizientenmetrik ist eine Modellierungswahl und muss bei dimensions-/skalenverschiedenen Zustandsgrößen gegebenenfalls angepasst werden.
