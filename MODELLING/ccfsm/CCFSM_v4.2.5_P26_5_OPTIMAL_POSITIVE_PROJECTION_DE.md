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

Die zulässige Randkurve wird in zwei Typen zerlegt: zwei lineare Randbedingungen an den Zellenden und ein elliptischer Bogen für ein inneres Minimum. Der Solver prüft die gewichteten Projektionen auf den beiden Randgeraden, deren Schnittpunkt sowie alle lokalen Minima der Zielfunktion auf dem elliptischen Bogen. Die eindimensionale Bogenminimierung erfolgt mit geklammertem Golden-Section-Verfahren:

1. Wenn das Ausgangspolynom zulässig ist, bleibt es unverändert.
2. Berechne die gewichtete orthogonale Projektion auf jede verletzte Endpunkt-Halbraumgrenze.
3. Berücksichtige den Schnittpunkt der beiden Endpunktgrenzen.
4. Parametrisiere den Rand für ein inneres Minimum als elliptischen Bogen und suche alle lokalen Minima der gewichteten Zielfunktion auf diesem Bogen mit geklammerter Golden-Section-Suche.
5. Verwerfe Kandidaten, die die vollständige Nichtnegativitätsbedingung verletzen, und wähle den zulässigen Kandidaten mit kleinstem Zielfunktionswert.
6. Prüfe das exakte quadratische Minimum erneut auf dem vollständigen Zellintervall.

Die Implementierung benötigt keine externe Optimierungsbibliothek. Die elliptische Bogenauflösung ist einstellbar (Standard 1024 Unterintervalle). Die Gewichte sind positive dimensionslose Koeffizientengewichte; Standard ist (1,1). Ein kleiner numerischer Sicherheitsabstand und die abschließende Kontinuumsprüfung sind dokumentiert.

## 3. Erhaltung und Zielkonflikte

- Zellmittelwert und Zellmasse bleiben exakt fest; damit bleibt die globale Masse fest.
- Nichtnegativität wird über das gesamte Zellintervall geprüft, nicht nur an Stützstellen.
- Erste und zweite räumliche Momente werden nach der Projektion bilanziert, sind aber keine expliziten Nebenbedingungen dieses lokalen Optimierungsproblems.
- Das Minimum der Koeffizientendistanz ist nicht dasselbe wie das Minimum eines globalen Momentenfehlers. Eine globale Nebenbedingung für erstes/zweites Moment wäre ein anderes, gekoppeltes Optimierungsproblem über mehrere Zellen.

## 4. Vergleich mit P26.4

Die Studie vergleicht P26.5 gegen P26.4 für fünf synthetische Fälle: Randunterschwinger, inneres Scheitelpunktunterschwingen, gemischte Moden, Nullmittelwert und bereits positives Polynom. Berichtet werden Positivitätsminimum, Massenänderung, Änderungen der ersten/zweiten Momente und Koeffizienten-Zielfunktion. Eine Verbesserung der globalen Momente wird nur dann behauptet, wenn sie in den Ergebnissen tatsächlich beobachtet wird.

## 5. Grenzen

1-D-Intervalle und quadratische Felder; lokale zellweise Optimierung, keine globale Momentenrestriktion, keine 2-D/3-D-Geometrie, keine Druck-/Energieerhaltung und keine physikalische Validierung. Die Koeffizientenmetrik ist eine Modellierungswahl und muss bei dimensions-/skalenverschiedenen Zustandsgrößen gegebenenfalls angepasst werden.


## 6. CI-Referenz und Ergebnisse

GitHub Actions Lauf **#373** erfolgreich; **324/324 Unit-Tests** bestanden. Der P26.5-Studienlauf und der Upload des separaten Ergebnisartefakts waren erfolgreich.

Fünf synthetische Fälle wurden gegen P26.4 verglichen. Das Minimum nach P26.5 betrug 0; die maximale absolute Massenänderung betrug 0. Die Summe der absoluten Änderungen des ersten Moments über die fünf Fälle sank von 0.2328275 (P26.4) auf 0.2157950 (P26.5); für das zweite Moment von 0.2439617 auf 0.2215272. In jeweils zwei von fünf Fällen war die betreffende Momentenänderung kleiner. Das ist eine Verbesserung der aggregierten Testmetrik, keine Garantie für jeden Fall oder für beliebige Daten.

- CI-Lauf: https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43673679478
- Ergebnisartefakt: https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43673679478/artifacts/14145283276

**Hinweis:** Diese CI-Zahlen stammen aus dem P26.5-Lauf vor der reinen Korrektur der Studien-Metadaten. Der Algorithmus und die Tests waren bereits erfolgreich; ein erneuter Lauf nach der Metadatenkorrektur wird separat geprüft.
