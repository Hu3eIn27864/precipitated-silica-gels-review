# Kuratierte Primärfits und Residuen — 14.11.2026

## Zweck und Abgrenzung

Diese Auswertung wendet erstmals die am 14.11.2026 festgelegten Verwendungsregeln tatsächlich auf die 164 KI-gestützten Diagramm-Näherungsablesungen an. Der Primärzweig enthält ausschließlich `primary_exploratory` und `primary_with_local_reversals`: 98 Punkte in sieben Reihen. Die 22 Punkte `sensitivity_only` aus Figure 8a (sauer, 40/60 °C) und die 44 Punkte `figure_table_conflict_branch` aus Figure 10b (basisch) sind nicht in diese Fits eingegangen.

Die Punkte sind keine Autoren-Rohdaten, nicht pixelkalibriert und nicht unabhängig visuell nachgeprüft. Es gibt keine Punktfehler, Pixelunsicherheiten oder Replikatstreuungen. Deshalb: keine Gewichte, keine Konfidenzintervalle, keine Signifikanztests und keine physikalische Parameteridentifikation.

## Modell und Verfahren

Für jede Reihe separat:

\[
S(t)=A\left(1-e^{-t/\tau}\right).
\]

Für festes \(\tau\) wird die quadratisch optimale Amplitude analytisch bestimmt; anschließend wird die Summe der quadrierten Residuen eindimensional über \(\log\tau\) minimiert (Golden-Section-Verfahren). Die Punktreihen werden weder geglättet noch um lokale Umkehrungen bereinigt.

Reproduzierbarer Code:
- `MODELLING/transport_model/fit_curated_wilhelm_kind_curves.py`

Ergebnisse:
- `LITERATURE/wilhelm_kind_curated_primary_fits_2026-11-14.csv`
- `LITERATURE/wilhelm_kind_curated_primary_residuals_2026-11-14.csv`

Der Code kann die getrennten Zweige optional einschließen (`--include-sensitivity`, `--include-figure-table-conflict`). Standardmäßig bleiben sie ausgeschlossen.

## Primärergebnis

| Reihe | n | A Fit | A publ. | τ Fit (h) | τ publ. (h) | RMSE |
|---|---:|---:|---:|---:|---:|---:|
| Figure 8a sauer 20 °C | 13 | 0.1870 | 0.20 | 11.12 | 21.3 | 0.0104 |
| Figure 8b basisch 20 °C | 11 | 0.2847 | 0.30 | 41.28 | 50.1 | 0.0213 |
| Figure 8b basisch 40 °C | 9 | 0.3587 | 0.39 | 24.83 | 32.0 | 0.0108 |
| Figure 8b basisch 60 °C | 10 | 0.4915 | 0.51 | 24.90 | 27.5 | 0.0298 |
| Figure 10a sauer 20 °C | 15 | 0.3691 | 0.37 | 0.524 | 0.40 | 0.0134 |
| Figure 10a sauer 40 °C | 19 | 0.4263 | 0.41 | 0.696 | 0.64 | 0.0320 |
| Figure 10a sauer 60 °C | 21 | 0.4710 | 0.48 | 0.620 | 0.77 | 0.0259 |

## Residuenbefund

Die RMSE-Werte liegen zwischen rund 0.010 und 0.032 relativen Schrumpfungseinheiten. Die Residuen sind jedoch nicht durchweg zufällig verteilt. Die deskriptive Lag-1-Korrelation der zeitlich sortierten Residuen beträgt für Figure 10a ungefähr 0.60 (20 °C), 0.78 (40 °C) und 0.45 (60 °C). Das ist ein Warnsignal für zeitlich strukturierte Abweichungen vom Einzelexponentialmodell oder für Ablese-/Zuordnungsartefakte; mit diesen ungeprüften Punkten ist es kein formaler Test.

Für Figure 8b liegen die Lag-1-Werte ungefähr bei 0.10 (20 °C), -0.50 (40 °C) und -0.37 (60 °C). Bei den kleinen Stichproben und lokalen Kurvenumkehrungen sind diese Kennzahlen nur deskriptiv zu lesen.

## Interpretation

1. **Amplituden:** Im Primärzweig liegen die Fits nahe bei den publizierten Amplituden (ungefähr 0.92–1.04 des Tabellenwerts). Das ist ein interner Plausibilitätscheck, keine unabhängige Validierung.
2. **Zeitkonstanten:** Die Fits weichen merklich ab. Figure 8a, 20 °C ergibt etwa die Hälfte der publizierten Zeitkonstante; Figure 10a, 20 und 60 °C weichen ebenfalls um rund 31 % bzw. 20 % ab. Der Fit allein entscheidet nicht, ob dies aus Ablesefehlern, Parameterkorrelation, unzureichender Zeitauflösung oder Modellabweichung stammt.
3. **Residualstruktur:** Insbesondere Figure 10a zeigt positive aufeinanderfolgende Residuenkorrelation. Ein hoher R²-Wert wäre daher keine ausreichende Modellgütebegründung. Ein zusätzlicher flexiblerer kinetischer Fit wäre erst nach visueller/pixelbasierter Prüfung sinnvoll, sonst würde er möglicherweise Ableseartefakte modellieren.
4. **Ausgeschlossene Zweige:** Figure 8a sauer 40/60 °C bleibt eine Sensitivitätsanalyse; Figure 10b basisch bleibt wegen der Figure/Table-2-Diskrepanz getrennte graphische Evidenz. Die publizierten Tabellenparameter wurden nicht überschrieben.

## Nächster methodischer Schritt

Vor einem Mehrparameter- oder physikalischen Modellfit sollten die Originalfiguren pixelkalibriert und die Marker/Kurvenzuordnung unabhängig überprüft werden. Danach: (i) Sensitivitätsfits der beiden Figure-8a-Reihen, (ii) separate Fits von Figure 10b ohne erzwungene Table-2-Amplituden, (iii) Vergleich Einzelexponentialmodell gegen ein minimal erweitertes Modell nur bei belastbarer Residuenstruktur. Keine dieser Erweiterungen darf die Datenprovenienz verwischen.
