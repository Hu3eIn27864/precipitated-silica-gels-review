# Verwendung der 164 KI-gestützten Näherungspunkte

**Stand:** 14. November 2026  
**Status:** kuratierter explorativer Datensatz; keine unabhängige Pixel-Digitalisierung.

Die 164 übermittelten Punkte werden ab jetzt nicht pauschal verworfen. Sie werden aber nach einer vorab festgelegten Evidenzregel in drei getrennte Verwendungszweige aufgeteilt. Die Originaldatei bleibt unverändert.

## Verwendungsregeln

1. **Primärer explorativer Zweig:** Reihen, deren Verlauf und Größenordnung nicht durch die bisherigen Plausibilitätsprüfungen auffällig geworden sind. Sie dürfen für vorläufige Kurvenvergleiche und explorative Fits verwendet werden, aber nicht als präzise Rohdaten oder zur belastbaren physikalischen Parameteridentifikation.
2. **Sensitivitätszweig:** Figure 8a bei 40 und 60 °C. Die aus den Punkten interpolierte Halbzeit weicht deutlich von der durch den publizierten Exponential-Fit erwarteten Halbzeit (t_{50}=\tau\ln 2) ab. Diese Punkte bleiben erhalten und werden nur in Sensitivitätsanalysen verwendet, bis die Originalmarker erneut geprüft sind.
3. **Separater Figure/Table-Zweig:** Figure 10b bei 20, 40 und 60 °C. Die sichtbaren Kurven/Marker und die ungefähren Punktablesungen liegen über den publizierten Table-2-Amplituden. Die Abweichung wird als mögliche publikationsinterne Figure/Table-Inkonsistenz behandelt. Diese Punkte dürfen die publizierten Tabellenwerte nicht stillschweigend überschreiben und werden nicht in einen Fit aufgenommen, dessen Ziel die Reproduktion von Table 2 ist. Sie bleiben aber als eigenständige Figure-Evidenz für einen separaten Fit-/Diskussionszweig verfügbar.

## Lokale Nichtmonotonien

Kleinere lokale Rückgänge in Figure 8b bei 40/60 °C und Figure 10a bei 60 °C werden **nicht gelöscht und nicht geglättet**. Sie können reale Streuung, Ablesefehler, Symbolüberlagerung oder zeitliche Schwankung repräsentieren. Im Fit sind robuste Residuen bzw. ein explizites Messfehlermodell zu verwenden; monotone Regression darf höchstens als Sensitivitätsvergleich dienen, nicht als Ersatz für die beobachteten Punkte.

## Inhalt des kuratierten CSV

`wilhelm_kind_approximate_measurement_points_curated.csv` enthält alle 164 Originalzeilen unverändert plus zwei Klassifikationsspalten:
- `reanalysis_use`
- `reanalysis_reason`

Es werden keine numerischen Gewichte vergeben, weil aus den vorliegenden Informationen keine belastbaren punktweisen Unsicherheiten ableitbar sind. Die Kategorien sind Verwendungsregeln, keine Qualitätswahrscheinlichkeiten.

## Grenzen

- Keine Pixelkoordinaten, Achsenkalibrierungsresiduen oder Punktunsicherheiten.
- Die Punkte sind KI-gestützte Näherungsablesungen und keine Autoren-Rohdaten.
- Published fit amplitudes/time constants are separate evidence and must remain in the original literature table.
- Jede spätere Neudigitalisierung muss Rohpunkte und diese Näherungsablesungen getrennt halten.

## Empfohlene Fit-Strategie

Zunächst Kurvenformen des primären Zweigs deskriptiv vergleichen und Residuen gegen die publizierte Exponentialfunktion darstellen. Danach Sensitivitätsvergleich (a) mit/ohne Figure 8a 40/60 °C und (b) separat für Figure 10b gegenüber Table 2. Keine gemeinsame Anpassung aller Reihen mit einem einzigen Transportparameter, bevor Geometrie, Randbedingungen und thermische Vorgeschichte explizit modelliert sind.
