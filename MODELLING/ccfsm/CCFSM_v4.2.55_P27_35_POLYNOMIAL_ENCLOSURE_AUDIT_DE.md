# CCFSM v4.2.55 — P27.35: unabhängige Polynom-Intervallprüfung

**Datum:** 15.11.2026  
**Status:** implementiert; gezielte Hosted-CI-Prüfung ausstehend.

## Ziel

P27.35 prüft P27.34 mit einer reproduzierbaren Intervallfortsetzung für Polynome. Die Auswertung erfolgt in Horner-Form unter Verwendung der nach außen gerundeten Intervalloperationen aus P27.34. Damit werden bekannte positive, lineare und tangentiale Referenzfälle durch eine unabhängige Testschicht geführt.

## Ergebnisinterpretation

- Wenn die Horner-Einschließung Null ausschließt, klassifiziert P27.34 das gesamte Intervall als nullstellenfrei — vorausgesetzt, die verwendete Intervallarithmetik erfüllt ihren Einschließungsvertrag.
- Wenn die Einschließung Null enthält, bleibt der Fall ungelöst. Das gilt auch für bekannte lineare oder tangentiale Nullstellen.
- Intervallabhängigkeit kann Einschließungen verbreitern. Unterteilung kann diese Überabschätzung reduzieren, ist aber hier kein automatischer globaler Isolationsalgorithmus.
- Dichte Punktabtastungen dienen nur als Regressionstest auf implementierte Einschließungsfehler; sie sind für sich genommen kein mathematischer Einschließungsbeweis.

## Dateien

- `ccfsm_p27_35_polynomial_enclosure_audit.py`: Horner-Auswertung eines Polynoms über einem Intervall und Anbindung an P27.34.
- `test_ccfsm_p27_35_polynomial_enclosure_audit.py`: sieben Regressionen.
- Diese Spezifikation.

## Aussagegrenzen

Keine automatische Intervallfortsetzung beliebiger realer Flussfunktionen, kein Existenz-/Eindeutigkeitsbeweis tangentialer Nullstellen, keine Vollständigkeitsgarantie der Ereigniserkennung, keine vollständige Upwind-Entropie-Kettenregel, keine P24-Trajektorienintegration und keine physikalische Validierung.
