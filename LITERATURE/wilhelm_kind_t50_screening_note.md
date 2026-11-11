# Explorative Halbzeit-Auswertung der Wilhelm-&-Kind-Digitalisierung

## Fragestellung
Als einfacher, fitfreier Screening-Schritt wird die Zeit (t_{50}) bestimmt, zu der die digitalisierte Reihe erstmals die Hälfte des publizierten empirischen Fit-Amplitudenparameters (A) erreicht. Zwischen den zwei benachbarten Punkten, die (A/2) einschließen, wird linear interpoliert.

Für ein einfaches empirisches Gesetz (S(t)=A[1-exp(-t/\tau)]) wäre (t_{50}=\tau\ln 2). Der Vergleich prüft nur die interne zeitliche Plausibilität der Näherungspunkte gegenüber dem publizierten Zeitparameter. Es wird **kein neuer Fit** berechnet.

## Resultatdatei
`wilhelm_kind_t50_screening.csv` enthält alle 12 Reihen, (A), publiziertes \(\tau\), digitales (t_{50}), erwartetes (\tau\ln2) und deren Verhältnis.

## Interpretation und Einschränkungen
- Figure 8 / Zylinder: Die beiden basischen Reihen bei 40 und 60 °C ergeben ein digitales (t_{50}), das nahe bei \(\tau\ln2\) liegt. Bei sauer/40 und 60 °C liegen die interpolierten digitalen Halbzeiten deutlich später als erwartet. Für sauer/20 liegt sie früher. Das ist ein Hinweis, die Zeitablesung und Zuordnung der frühen Punkte in Figure 8a zu kontrollieren.
- Figure 10 / Tröpfchen: Die (t_{50})-Werte liegen für alle sechs Reihen größenordnungsmäßig nahe bei \(\tau\ln2\) (Verhältnisse ca. 0.65–1.51). Das ist ein nützlicher, aber grober Konsistenzcheck und keine unabhängige Validierung.
- Figure 10b bleibt trotz relativ ähnlicher Halbzeiten kritisch: Die späten digitalen Maxima liegen bei 0.51/0.67/0.86, während die Fit-Amplituden 0.30/0.39/0.51 betragen. Ein plausibler früher Verlauf kann eine falsche späte Symbolzuordnung nicht ausschließen.
- Die publizierte Tröpfchenmethode hält die Temperatur in den ersten 20 min bei 20 °C, bevor die Probe in die temperaturgeregelte Zelle überführt wird. Die hier ermittelten (t_{50}) sind ab der Diagrammzeitachse gelesen; eine mögliche thermische Anlaufphase ist bei der Interpretation zu berücksichtigen.
- Digitale Punktablesungen sind ungefähre JPEG-Werte. Keine Pixelunsicherheit, keine Fehlerbalken und keine Rohdaten vorliegend. Lineare Interpolation zwischen grob abgelesenen Punkten ist nur Screening.
- Der publizierte Parameter \(\tau\) wird hier als Zeitkonstante eines einfachen Einzelexponentialansatzes interpretiert. Vor einer stärkeren Aussage muss die genaue im Artikel verwendete Gleichung nochmals gegen den Volltext geprüft werden.

## Nächster Schritt
Originalgrafik erneut prüfen: Figure 8a frühe Zeitachse und alle drei Reihen; Figure 10b späte Symbole/Maxima; dann die sechs empirischen Modellkurven getrennt digitalisieren und deren Zeit-/Amplitudenparameter direkt visuell gegen Tabelle 1/2 prüfen.
