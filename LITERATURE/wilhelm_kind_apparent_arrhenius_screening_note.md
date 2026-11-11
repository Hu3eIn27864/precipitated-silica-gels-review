# Deskriptive Arrhenius-Auswertung der publizierten Synerese-Zeitkonstanten

## Zweck und Datengrundlage

Diese Auswertung verwendet ausschließlich die in Wilhelm & Kind (2015), Tabellen 1 und 2, publizierten Zeitkonstanten \(\tau\) für natürliche Synerese: Zylinder (12 mm, ca. 3 mL) und Tröpfchen (ca. 3 mm), jeweils sauer und basisch bei 20, 40 und 60 °C. Die KI-gestützten Kurvenablesungen gehen **nicht** in diese Rechnung ein.

Als rein deskriptive Transformation wird \(k_\mathrm{app}=1/\tau\) gesetzt und \(\ln k_\mathrm{app}\) linear gegen \(1/T\) regressiert. Mit Arrhenius-Notation \(k=A\exp[-E_\mathrm{app}/(RT)]\) ist \(E_\mathrm{app}=-R\,d\ln(1/\tau)/d(1/T)\). Der Fit hat je Reihe nur drei Temperaturpunkte; R² ist daher keine belastbare Modellprüfung.

## Ergebnisse

| Geometrie | Katalyse | \(E_\mathrm{app}\) (kJ mol⁻¹) | R² | Einordnung |
|---|---|---:|---:|---|
| Zylinder | sauer | +29.27 | 0.981 | positiver scheinbarer Temperaturtrend |
| Zylinder | basisch | +12.29 | 0.943 | positiver scheinbarer Temperaturtrend |
| Tröpfchen | sauer | −13.40 | 0.957 | negatives Vorzeichen; nicht als chemische Aktivierungsenergie deuten |
| Tröpfchen | basisch | −6.79 | 0.411 | schwacher linearer Zusammenhang; keine sinnvolle Arrhenius-Interpretation |

## Wissenschaftliche Interpretation und Grenzen

1. Die Zylinder-Zeitkonstanten sinken mit Temperatur; daraus folgen positive scheinbare Arrhenius-Steigungen. Die Zahlen sind keine identifizierten Aktivierungsenergien eines einzelnen elementaren oder transportbestimmenden Schritts.
2. Bei den Tröpfchen steigen die publizierten \(\tau\)-Werte für die saure Reihe von 0.40 auf 0.77 h und zeigen bei der basischen Reihe keinen monotonen Verlauf (0.67, 0.57, 0.95 h). Die resultierenden negativen scheinbaren Werte sind ein Warnsignal gegen eine einfache Arrhenius-Deutung.
3. Die Autoren halten die Tröpfchen in den ersten 20 min bei 20 °C und überführen sie danach in die temperierte Zelle. Sie diskutieren ähnliche Kurvenverläufe in den ersten 30 min und eine mögliche Aufheizverzögerung, insbesondere bei 40/60 °C. Das kann die aus nomineller Badtemperatur und globaler \(\tau\)-Anpassung abgeleitete Temperaturabhängigkeit verfälschen.
4. Geometrie, Probenvolumen, Oberfläche-zu-Volumen-Verhältnis, Randbedingungen und thermische Vorgeschichte unterscheiden sich. Die Zylinder- und Tröpfchenwerte dürfen daher nicht als einheitliche kinetische Serie gepoolt werden.
5. \(1/\tau\) ist hier lediglich eine inverse empirische Zeitkonstante. Sie ist weder eine gemessene Permeabilität noch ein isolierter Reaktionsgeschwindigkeitskoeffizient. Die Auswertung kann keine Transport- und Netzwerkreaktionsbeiträge trennen.

## Konsequenz für das Modellierungsprojekt

- Die Zylinderreihen sind eine mögliche spätere Temperatur-Sensitivitätsreferenz, aber erst nach unabhängiger Prüfung der Kurven-/Fitparameter und der thermischen Randbedingungen.
- Die Tröpfchenreihen sollten nicht zur Kalibrierung eines Arrhenius-Gesetzes verwendet werden, solange die Probentemperatur-Zeit-Verläufe unbekannt sind.
- Für eine belastbare Trennung von Transport und Netzwerkreorganisation werden zusätzlich zeitaufgelöste Probentemperatur, Schrumpfung und vorzugsweise Porenflüssigkeits-/Permeabilitätsdaten benötigt.

Quelle: Wilhelm, S.; Kind, M. (2015), *Polymers* 7, 2504–2521, Tabellen 1–2, Gleichung (3), Abschnitt 4.1; DOI: 10.3390/polym7121528. Open article: https://www.mdpi.com/2073-4360/7/12/1528.
