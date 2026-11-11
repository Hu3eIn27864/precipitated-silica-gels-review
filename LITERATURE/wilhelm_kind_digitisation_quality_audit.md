# Wilhelm & Kind (2015): Qualitätsprüfung der vorläufigen JPEG-Digitalisierung

## Herkunft und Status
Die 164 Näherungswerte wurden durch einen anderen ChatGPT-Account aus den Diagrammen abgelesen und anschließend als Text übermittelt. Es liegen keine Pixelkoordinaten, Achsenkalibrierungen oder unabhängigen Sichtprüfungen vor. Es handelt sich um KI-gestützte, ungeprüfte Diagrammablesungen, nicht um Originalmesswerte. Die internen Namen Fig1/Fig2 wurden auf Figure 8/Figure 10 abgebildet. Werte selbst wurden nicht an Fitparameter angepasst.

## Strukturprüfung
- 164 Punkte in 12 Reihen (Figure 8: 65; Figure 10: 99).
- Zeitpunkte sind innerhalb jeder Reihe streng aufsteigend.
- Alle Punkte sind in der Datendatei als `source_type=ai_assisted_approximation` markiert.
- Pixelkoordinaten, Digitalisierungsunsicherheiten und Fehlerbalken fehlen.
- Keine Modellkurven sind in dieser Datei enthalten.

## Reihenweise Maxima
| Abbildung/Panel | Bedingung | T | n | digitales Maximum | Zeit |
|---|---|---:|---:|---:|---:|
| 8a | sauer | 20 °C | 13 | 0.200 | 245 h |
| 8a | sauer | 40 °C | 11 | 0.200 | 50 h |
| 8a | sauer | 60 °C | 11 | 0.210 | 125 h |
| 8b | basisch | 20 °C | 11 | 0.310 | 195 h |
| 8b | basisch | 40 °C | 9 | 0.380 | 145 h |
| 8b | basisch | 60 °C | 10 | 0.540 | 220 h |
| 10a | sauer | 20 °C | 15 | 0.370 | 4.0 h |
| 10a | sauer | 40 °C | 19 | 0.490 | 6.8 h |
| 10a | sauer | 60 °C | 21 | 0.510 | 6.6 h |
| 10b | basisch | 20 °C | 15 | 0.510 | 5.3 h |
| 10b | basisch | 40 °C | 16 | 0.670 | 5.4 h |
| 10b | basisch | 60 °C | 13 | 0.860 | 4.4 h |

## Auffälligkeiten
1. **Figure 10b, 60 °C:** 0.86 (4.4 h) und 0.85 (5.2 h) weichen stark vom publizierten Tabellenparameter der maximalen Schrumpfung von 0.51 ab. Unbedingt Symbol-/Kurvenzuordnung und y-Achse im Original prüfen. Nicht automatisch korrigieren.
2. **Figure 10b, 40 °C:** digitales Maximum 0.67 bei 5.4 h gegenüber Tabellenparameter 0.39. Ebenfalls erhebliche Diskrepanz; Reihe prüfen.
3. **Figure 10b, 20 °C:** Maximum 0.51 gegenüber Tabellenparameter 0.30. Ebenfalls prüfen.
4. **Figure 10a, 60 °C:** Rückgang von 0.47 (3.2 h) auf 0.41 (4.0 h), danach erneuter Anstieg.
5. **Figure 8b, 40 °C:** 0.38 (145 h) auf 0.34 (170 h).
6. **Figure 8b, 60 °C:** Rückgänge 0.52→0.44 (145–170 h) und 0.54→0.46 (220–245 h).
7. Kleinere Rückgänge in den Messreihen werden als abgelesen beibehalten, nicht geglättet.

## Fitparameter aus der Publikation – Vergleich, keine Gleichsetzung
Publizierte maximale Schrumpfungsparameter:
- Figure 8/Zylinder, sauer: 0.20 bei 20/40/60 °C; basisch: 0.30/0.39/0.51.
- Figure 10/Tröpfchen, sauer: 0.37/0.41/0.48; basisch: 0.30/0.39/0.51.
Die publizierten Werte stammen aus den empirischen Fits und sind nicht identisch mit unabhängig digitalisierten Einzelmesspunkten. Die systematischen Überschreitungen in Figure 10b sind dennoch zu groß, um sie ohne Bildprüfung als gewöhnliche Ableseabweichung abzutun.

## Zulässige Verwendung
Derzeit explorative Visualisierung, grobe Plausibilitätskontrolle und Priorisierung einer späteren manuellen Prüfung. Nicht als hochpräzise Rohdatenbasis oder Grundlage belastbarer Parameteridentifikation verwenden. Vor Modellanpassung müssen die auffälligen Reihen anhand des Originals neu geprüft und Digitalisierungsunsicherheiten abgeschätzt werden.

## Nächste Arbeitsschritte
1. Figure 10b alle drei Temperaturen visuell gegen Original prüfen (besonders 20/40/60 °C).
2. Figure 10a/60 °C sowie Figure 8b/40 und 60 °C kontrollieren.
3. Danach Modellkurven separat digitalisieren (`source_type=model_curve`).
4. Fehlerbalken getrennt erfassen.
5. Erst dann Fit-/Kinetikvergleich und Unsicherheitsanalyse.
