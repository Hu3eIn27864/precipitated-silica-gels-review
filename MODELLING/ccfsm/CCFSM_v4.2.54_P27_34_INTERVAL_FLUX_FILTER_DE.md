# CCFSM v4.2.54 — P27.34: Intervall-Enclosure-Filter für Flussnullstellen

**Datum:** 15.11.2026  
**Status:** implementiert; gezielte CI-Prüfung ausstehend.

## Ziel

P27.33 erzeugt lokale quadratische Kandidaten für tangentiale Flussnullstellen. P27.34 ergänzt einen konservativen Filter: Eine vom Aufrufer bereitgestellte Intervallfortsetzung des Originalflusses wird auf einem Kandidatenintervall ausgewertet. Schließt die resultierende Einschließung die Null aus, wird der Kandidat als ausgeschlossen klassifiziert. Enthält sie Null, bleibt der Fall ausdrücklich ungelöst.

## Mathematischer Vertrag

Sei I=[a,b] und F_I(I) eine gültige Intervallfortsetzung mit
f(t) ∈ F_I(I) für alle t∈I. Gilt 0∉F_I(I), folgt daraus rigoros
f(t)≠0 für alle t∈I. Dies ist eine zertifizierte Nullstellenausschließung
unter der Voraussetzung, dass die vom Aufrufer gelieferte Intervallfortsetzung
tatsächlich einschließt.

Aus 0∈F_I(I) folgt dagegen **nicht**, dass eine Nullstelle existiert.
Insbesondere wird eine tangentiale Nullstelle nicht allein durch
Intervallinklusion bewiesen. Der Status lautet dann
`unresolved_zero_inclusion`.

Die implementierten Grundoperationen runden jede elementare Fließkommaoperation
mit `math.nextafter` nach außen. Dies liefert einen konservativen Schutz für
diese elementaren Operationen im üblichen IEEE-754-Betrieb, ist aber kein
allgemeines Zertifikat für beliebige benutzerdefinierte Intervallfunktionen,
transzendente Bibliotheksfunktionen oder nicht eingeschlossene Modellfehler.

## Dateien

- `ccfsm_p27_34_interval_flux_filter.py`: geschlossene Intervalle, nach außen gerundete Grundoperationen, Intervallquadrat, Division mit Nullprüfung und Kandidatenklassifikation.
- `test_ccfsm_p27_34_interval_flux_filter.py`: sieben Regressionen.
- Diese Spezifikation.

## Aussagegrenzen

- Die Korrektheit hängt von einer mathematisch gültigen Intervallfortsetzung des Originalflusses ab.
- Null-Ausschluss ist zertifiziert, Null-Inklusion bleibt ungelöst; kein Existenz- oder Eindeutigkeitsbeweis für tangentiale Nullstellen.
- Keine automatische Ableitungsschranke, keine vollständige Root-Isolation und keine Vollständigkeitsgarantie für P27.31/P27.33.
- Keine vollständige diskrete Upwind-Entropie-Kettenregel, keine P24-Trajektorienintegration und keine physikalische Validierung.
