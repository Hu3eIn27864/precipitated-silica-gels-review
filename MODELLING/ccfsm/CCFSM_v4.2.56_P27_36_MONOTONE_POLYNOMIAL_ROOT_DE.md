# CCFSM v4.2.56 — P27.36: Ableitungsvorzeichen und eindeutige Polynom-Nullstellen

**Datum:** 15.11.2026  
**Status:** implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel

P27.36 erweitert die P27.34/P27.35-Intervallprüfung um einen Ableitungstest für Polynome. Eine Nullstelle wird nur dann als eindeutig im offenen Intervall klassifiziert, wenn

1. die Intervallfortsetzung der Ableitung auf dem gesamten Intervall strikt positiv oder strikt negativ ist und
2. die nach außen eingeschlossenen Funktionswerte an den beiden Intervallenden strikt entgegengesetzte Vorzeichen haben.

Unter diesen Voraussetzungen ist das Polynom streng monoton. Die entgegengesetzten Endpunktvorzeichen liefern per Zwischenwertsatz die Existenz einer Nullstelle; strenge Monotonie liefert deren Eindeutigkeit. Bei gleichen strikten Endpunktvorzeichen folgt unter derselben Monotoniebedingung Nullstellenfreiheit.

## Statuswerte

- `certified_unique_root`: genau eine Nullstelle im offenen Intervall, bedingt auf gültige Intervall-Einschließungen.
- `certified_no_root`: keine Nullstelle im Intervall, bedingt auf gültige Intervall-Einschließungen.
- `unresolved_derivative_contains_zero`: die Ableitungseinschließung enthält Null; keine Monotonieaussage.
- `unresolved_endpoint_sign`: mindestens ein Endpunktwert hat kein strikt zertifiziertes Vorzeichen; Randnullstellen werden nicht als innere Nullstellen ausgegeben.

## Dateien und Tests

- `ccfsm_p27_36_monotone_polynomial_root.py`: Ableitungskoeffizienten und monotone Nullstellenklassifikation.
- `test_ccfsm_p27_36_monotone_polynomial_root.py`: acht Regressionstests zu steigenden/fallenden linearen Polynomen, Nullstellenfreiheit, tangentialem Fall, Randnullstelle und Eingabevalidierung.

## Aussagegrenzen

Die Aussage ist auf Polynome und die implementierte Intervallarithmetik beschränkt. Sie hängt davon ab, dass die nach außen gerundeten Intervalloperationen tatsächlich alle exakten Zwischenwerte einschließen. Es gibt keinen automatischen Beweis für beliebige caller-supplied Flussfunktionen, keine Vollständigkeitsgarantie der vorgelagerten Ereignisabtastung und keine physikalische Validierung. Tangentiale oder mehrfache Nullstellen bleiben typischerweise ungelöst, weil die Ableitungseinschließung Null enthält.


## Hosted-CI-Nachtrag

Im Hosted-Lauf [#763](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43748370567) bestanden alle acht P27.36-Regressionen. Der vollständige Lauf führte 655 Tests aus und blieb wegen sechs Fehlern und einer Exception in älteren Modulen P27.10, P27.13, P27.17 (zwei Tests), P27.18, P27.23 und P27.28 rot. P27.36 wird daher als gezielt getestet, aber nicht als Freigabe der Gesamtintegration gewertet.
