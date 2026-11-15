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
