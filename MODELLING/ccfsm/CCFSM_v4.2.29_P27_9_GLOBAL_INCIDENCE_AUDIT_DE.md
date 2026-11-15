# CCFSM v4.2.29 — P27.9 globaler Tetraedernetz-Inzidenz-Audit

**Ziel.** P27.9 ergänzt P27.7/P27.8 um einen globalen Audit der aus dem vollständigen Tetraedernetz abgeleiteten Flächen-, Kanten- und Knoteninzidenzen.

## Definition und Verfahren

1. P27.8 wird zuerst aufgerufen: degenerierte Tetraeder werden abgewiesen und alle Elemente exakt rational auf positive Orientierung gebracht.
2. Jede Tetraederfläche wird als sortiertes Knotentripel kanonisiert. Inzidenz 1 kennzeichnet eine Randfläche, Inzidenz 2 eine innere Fläche, Inzidenz größer 2 einen nichtmanifoldalen Flächenkandidaten.
3. Die von positiv orientierten Tetraedern induzierten Orientierungen gemeinsamer Flächen werden verglichen. Eine innere Fläche muss von ihren beiden Nachbarelementen entgegengesetzt induziert werden.
4. Kanten werden nach eindeutigen inzidenten Tetraedern und nach inzidenten Flächen gezählt. Knotenverwendung, isolierte Knoten und face-zusammenhängende Elementkomponenten werden ausgegeben.
5. Doppelte Tetraeder (auch bei anderer lokaler Knotenanordnung) werden vor dem Audit zurückgewiesen.

## Statussemantik

- `incidence_audited`: keine erkannte Überinzidenz oder innere Flächenorientierungskollision.
- `incidence_inconsistent`: mindestens eine Fläche hat mehr als zwei inzidente Elemente, eine innere Fläche besitzt inkonsistente induzierte Orientierung oder eine Kante ist mit mehr als zwei Flächen verbunden.
- `invalid`: ungültige Konnektivität, doppelte/degenerierte Elemente oder fehlerhafte Eingabe.

## Aussagegrenzen

Der Prüfer liefert exakte geometrische Orientierung und diskrete Inzidenzzahlen, aber **keinen vollständigen topologischen Mannigfaltigkeitsbeweis**. Insbesondere werden Link-Komplexe der Knoten und Kanten nicht geprüft; lokale Singularitäten können trotz plausibler einfacher Inzidenzzahlen verbleiben. Randflächen werden identifiziert, aber nicht als geometrisch geschlossene oder physikalisch zulässige Randbedingung interpretiert. Ebenso wenig folgen daraus FE-Konditionierung, CCFSM-Zustandspositivität, Energieabschluss oder physikalische Validität.

P27.9 ist ein globaler Mesh-Struktur-Audit, kein Solver und kein Validierungsnachweis für das physikalische Silica-Modell.
