# Explorative Einzelexponential-Fits der KI-gestützten Diagrammablesungen

## Datenstatus und Fragestellung

Die 164 Kurvenpunkte sind KI-gestützte, ungeprüfte Näherungsablesungen aus Wilhelm & Kind (2015), Figures 8 und 10. Sie wurden nicht pixelkalibriert und nicht unabhängig am Originalbild geprüft. Diese Auswertung behandelt sie ausdrücklich als explorative Näherungswerte, nicht als experimentelle Rohdaten.

Ziel ist zu prüfen, ob sich die übermittelten Punktreihen mit der in der Publikation verwendeten empirischen Funktion beschreiben lassen und wie stark die daraus geschätzten Parameter von den publizierten Tabellenwerten abweichen.

## Modell und numerisches Verfahren

Für jede der 12 Reihen wurde unabhängig das Modell

\[
S(t)=A\left[1-\exp\left(-t/\tau\right)\right]
\]

an alle übermittelten Punkte angepasst. Für jeden getesteten positiven \(\tau\)-Wert wurde der least-squares-optimale Amplitudenparameter \(A\) analytisch bestimmt; anschließend wurde der quadratische Fehler eindimensional über \(\log\tau\) minimiert. Es wurden keine Gewichte verwendet, da keine Punktunsicherheiten verfügbar sind. Es wurden keine Punkte entfernt, geglättet oder an Tabellenwerte angepasst.

Reproduzierbarer Code: `MODELLING/transport_model/fit_wilhelm_kind_approximate_curves.py`. Ergebnisdatei: `LITERATURE/wilhelm_kind_approximate_curve_fits.csv`.

## Ergebnisse

| Reihe | \(A_\mathrm{fit}\) | \(A_\mathrm{publ.}\) | \(\tau_\mathrm{fit}\) (h) | \(\tau_\mathrm{publ.}\) (h) | R² |
|---|---:|---:|---:|---:|---:|
| 8a sauer 20 °C | 0.187 | 0.20 | 11.11 | 21.3 | 0.962 |
| 8a sauer 40 °C | 0.200 | 0.20 | 8.93 | 11.7 | 0.999 |
| 8a sauer 60 °C | 0.203 | 0.20 | 8.24 | 5.0 | 0.996 |
| 8b basisch 20 °C | 0.285 | 0.30 | 41.27 | 50.1 | 0.935 |
| 8b basisch 40 °C | 0.359 | 0.39 | 24.82 | 32.0 | 0.991 |
| 8b basisch 60 °C | 0.492 | 0.51 | 24.90 | 27.5 | 0.961 |
| 10a sauer 20 °C | 0.369 | 0.37 | 0.524 | 0.40 | 0.987 |
| 10a sauer 40 °C | 0.426 | 0.41 | 0.697 | 0.64 | 0.938 |
| 10a sauer 60 °C | 0.471 | 0.48 | 0.620 | 0.77 | 0.965 |
| 10b basisch 20 °C | 0.419 | 0.30 | 0.726 | 0.67 | 0.944 |
| 10b basisch 40 °C | 0.643 | 0.39 | 0.683 | 0.57 | 0.986 |
| 10b basisch 60 °C | 0.825 | 0.51 | 1.118 | 0.95 | 0.967 |

Alle Werte in dieser Tabelle sind Fitresultate aus den KI-gestützten Näherungspunkten oder publizierte Vergleichswerte. Die hohen R²-Werte sind kein Nachweis korrekter Ablesung: Ein glatter, monotoner Trend mit Plateau kann auch bei systematisch falsch zugeordneten Punkten ein hohes R² ergeben.

## Interpretation

### 1. Amplituden

- Figure 8a und 8b: Die angepassten Amplituden liegen relativ nahe an den publizierten Werten (ungefähr 0.92–1.01 des Tabellenwertes). Das ist ein grober interner Konsistenzhinweis, keine Validierung.
- Figure 10a: Ebenfalls gute Übereinstimmung der Amplituden (ungefähr 0.98–1.04 des Tabellenwertes).
- Figure 10b: Die angepassten Amplituden sind systematisch deutlich höher: etwa 1.40-, 1.65- und 1.62-fach der publizierten Tabellenwerte. Diese Abweichung ist groß und konsistent über alle drei Temperaturen. Die Zuordnung der Symbole/Kurven oder die Werteübertragung in Figure 10b ist deshalb vorrangig zu überprüfen.

### 2. Zeitkonstanten

- Figure 8a, 40/60 °C: Die Fit-Zeitkonstanten sind 8.93 bzw. 8.24 h. Besonders der 60-°C-Fit liegt deutlich über dem publizierten Wert von 5.0 h. Beide Reihen enthalten als ersten von null verschiedenen Punkt erst 22 h. Der frühe Kurvenverlauf ist damit nicht aufgelöst; \(A\) und \(\tau\) können stark korreliert und die Zeitkonstante schlecht identifizierbar sein. Die scheinbar sehr hohen R²-Werte ändern daran nichts.
- Figure 8a, 20 °C: Der Fit liefert 11.11 h statt 21.3 h; der erste nicht-null Punkt liegt bei 6 h. Auch hier beeinflusst die grobe zeitliche Abtastung die Schätzung.
- Figure 8b: Die gefitteten Zeitkonstanten sind durchweg etwas kleiner als die publizierten, aber in derselben Größenordnung.
- Figure 10a: Die Zeitkonstanten liegen relativ nahe an den publizierten Werten, mit sichtbaren Abweichungen bei 20 und 60 °C.
- Figure 10b: Die Zeitkonstanten liegen in derselben Größenordnung, aber das Modell kompensiert die überhöhten Kurvenwerte nicht durch eine passende Amplitude. Ein hoher R²-Wert darf hier nicht als Übereinstimmung mit der Publikation missverstanden werden.

### 3. Warum wir noch keine physikalischen Parameter ableiten

\(A\) und \(\tau\) sind Parameter einer empirischen Schrumpfungskurve. Insbesondere \(\tau\) ist keine direkt gemessene Permeabilität, Diffusivität oder Reaktionszeit eines isolierten Prozesses. Die vorliegenden Fits können Transport und Netzwerkreorganisation nicht voneinander trennen.

Die Abbildungen enthalten Mittelwerte/Mehrfachserien und Fehlerbalken; unsere Näherungsdaten enthalten weder Pixelkoordinaten noch Fehlerbalken, Replikatstreuung oder Ableseunsicherheiten. Deshalb werden keine Konfidenzintervalle oder Signifikanztests berichtet.

## Schlussfolgerung für die nächste Modellierungsstufe

Die Näherungsablesungen reichen aus, um gezielte Prüffragen zu erzeugen und Sensitivitätsrechnungen zu starten. Sie reichen nicht aus, um eine belastbare Kalibrierung zu behaupten.

Priorität für eine spätere Originalbildprüfung:
1. Figure 10b bei allen Temperaturen, besonders die hohen späten Werte.
2. Figure 8a bei 40 und 60 °C wegen fehlender früher Punkte und auffälliger Zeitkonstanten.
3. Figure 8a bei 20 °C wegen der Abweichung der Zeitkonstante.
4. Figure 8b und Figure 10a als vorläufig weniger auffällige Vergleichsreihen.

Die Daten bleiben als `ai_assisted_approximation` gekennzeichnet. Keine physikalische Modellvalidierung wird beansprucht.


## Nachprüfung Figure 10b: möglicher Widerspruch zwischen Abbildung und Table 2

Die Original-PNGs der Figures 8 und 10 wurden am 11.11.2026 direkt auf der Verlagsseite geöffnet. Die visuelle Prüfung zeigt, dass die späten Messmarker und Modellkurven in Figure 10b deutlich oberhalb der in Table 2 gedruckten basischen Maximalamplituden 0.30/0.39/0.51 liegen. Die zuvor übermittelten Näherungsmaxima 0.51/0.67/0.86 sind qualitativ mit den sichtbaren Markerlagen vereinbar. Außerdem sind die basischen Table-2-Amplituden zahlenidentisch mit den basischen Table-1-Amplituden für Figure 8. Das legt einen möglichen Übertragungs-/Tabellenfehler nahe, beweist ihn aber nicht.

Daher wird die bisherige Interpretation „Figure 10b muss vorrangig wegen möglicher Symbol-/Kurvenfehlzuordnung korrigiert werden“ eingeschränkt: Die Diskrepanz kann bereits in der Publikation selbst liegen. Die Fitparameter aus der KI-gestützten Kurvenablesung (A≈0.419/0.643/0.825; τ≈0.726/0.683/1.118 h) sind keine unabhängig verifizierten Werte, stimmen aber in der Größenordnung der sichtbaren Figure-10b-Kurven besser überein als die gedruckten Table-2-Amplituden. Die Zahlen werden nicht ersetzt oder angepasst.

**Wissenschaftliche Behandlung:** Table 2 bleibt als wörtlich publizierte Tabelle gespeichert; Figure 10b bleibt als separate graphische Evidenz. Beide Evidenzstränge müssen in einer künftigen Auswertung getrennt ausgewiesen werden. Keine stillschweigende Korrektur der Tabelle oder der Messpunkte.
