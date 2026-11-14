# Getrennte Sensitivitäts- und Figure/Table-Zweige — 14.11.2026

Diese Fits ergänzen die Primäranalyse, ersetzen sie aber nicht. Die Reihen wurden bewusst getrennt gehalten.

## A. Figure 8a, sauer: Sensitivitätszweig

| Temperatur | n | A Fit | A Table 1 | τ Fit (h) | τ Table 1 (h) | RMSE |
|---:|---:|---:|---:|---:|---:|---:|
| 40 °C | 11 | 0.2001 | 0.20 | 8.93 | 11.7 | 0.00142 |
| 60 °C | 11 | 0.2025 | 0.20 | 8.24 | 5.0 | 0.00372 |

Die Amplituden stimmen nahezu exakt mit Table 1 überein. Die Zeitkonstanten stimmen nicht: bei 40 °C liegt der Diagramm-Fit etwa 24 % unter Table 1, bei 60 °C etwa 65 % darüber. Das ist bemerkenswert, weil die Kurvenpunkte in diesem Zweig gerade wegen einer Diskrepanz zwischen aus Diagramm ablesbarem Verlauf und publiziertem Fitparameter als Sensitivitätsdaten klassifiziert wurden. Die sehr kleinen RMSE-Werte dürfen nicht als Beweis hoher Genauigkeit interpretiert werden: Die Daten sind grobe, teilweise gerundete Diagrammablesungen und die Fitfunktion hat nur zwei Parameter.

## B. Figure 10b, basisch: Figure/Table-Konfliktzweig

| Temperatur | n | A Fit | A Table 2 | A-Fit/Table | τ Fit (h) | τ Table 2 (h) | RMSE |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 20 °C | 15 | 0.4195 | 0.30 | 1.40 | 0.726 | 0.67 | 0.0333 |
| 40 °C | 16 | 0.6432 | 0.39 | 1.65 | 0.683 | 0.57 | 0.0248 |
| 60 °C | 13 | 0.8253 | 0.51 | 1.62 | 1.118 | 0.95 | 0.0480 |

Die Kurven-Fits der Diagramm-Näherung liegen rund 40–65 % über den Tabellenamplituden. Die Zeitkonstanten sind ebenfalls höher, aber die größere und konsistente Abweichung betrifft die Amplitude. Diese Berechnung quantifiziert die bereits dokumentierte Diskrepanz, löst sie aber nicht auf. Mögliche Erklärungen (Ablese-/Markerzuordnung, Bild-/Tabellenübertragungsfehler, abweichende Darstellung oder andere Kurvenbedeutung) bleiben Hypothesen.

**Wichtig:** Der Fit wurde frei auf die Diagrammpunkte angesetzt. Die Table-2-Amplituden wurden nicht als Nebenbedingung erzwungen. Die Fitparameter sind daher keine neuen publizierten Parameter und dürfen Table 2 nicht ersetzen.

## Dateien und Reproduzierbarkeit

- `wilhelm_kind_separate_branch_fits_2026-11-14.csv`
- `wilhelm_kind_separate_branch_residuals_2026-11-14.csv`
- Fitcode: `MODELLING/transport_model/fit_curated_wilhelm_kind_curves.py`

Der Fit ist ungewichtet. Die Punktablesungen besitzen keine unabhängigen Unsicherheitsangaben. RMSE und R² beschreiben ausschließlich die Anpassung an diese Näherungspunkte, nicht die Genauigkeit der zugrundeliegenden Messungen.

## Korrektur zur Kurzbeschreibung der Primäranalyse

Die Primäranalyse umfasst **sieben Kurvenreihen**, nicht acht: eine Reihe Figure 8a (sauer, 20 °C), drei Figure 8b (basisch, 20/40/60 °C) und drei Figure 10a (sauer, 20/40/60 °C). Zusammen sind dies 98 Punkte. Eine frühere Zwischenmeldung nannte irrtümlich acht Reihen; die Tabellen und Fitdateien enthalten sieben.
