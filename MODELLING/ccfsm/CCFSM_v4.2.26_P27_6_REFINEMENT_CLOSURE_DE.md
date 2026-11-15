# P27.6 — konservativer Abschluss der Tetraeder-Verfeinerungstiefen

**Status:** implementiert als konservativer Tiefenabschluss; keine eigentliche Mesh-Erzeugung.

## Regel

Aus der groben Tetraederkonnektivität wird die Nachbarschaft über gemeinsame Dreiecksflächen aufgebaut. Jede face-zusammenhängende Komponente erhält die größte angeforderte lokale Verfeinerungstiefe:

d_i_closed = max_{j in C(i)} d_j_requested.

Damit besitzen beide Seiten jeder gemeinsamen groben Fläche dieselbe rote P27.3-Verfeinerungstiefe. Die Regel ist bewusst konservativ: Ein einzelnes markiertes Element kann die gesamte face-zusammenhängende Komponente auf dieselbe Tiefe anheben. Getrennte Komponenten bleiben unabhängig.

## Implementierung und Sicherheitsgrenzen

- ccfsm_p27_6_refinement_closure.py berechnet Komponenten, geschlossene Tiefen, angehobene Elemente und die prognostizierte Blattzahl sum_i 8^d_i.
- Nicht-manifold Flächen, fehlerhafte Konnektivität und ungültige Tiefen werden zurückgewiesen.
- Tiefen- und Gesamt-Elementlimits führen zu unresolved; es wird kein partiell verändertes Netz ausgegeben.
- mesh_modified=False: P27.6 liefert einen Verfeinerungsplan, erzeugt aber keine neuen Knoten oder Tetraeder.
- Nach tatsächlicher P27.3-Subdivision muss P27.5 weiterhin auf den resultierenden Blattpartitionen laufen. Erst dessen conforming-Ergebnis bestätigt die gemeinsame Flächenzerlegung.

## Bewusste Nichtbehauptungen

P27.6 ist keine adaptive grüne Übergangsverfeinerung und keine minimale Closure. Die Komponentenglättung kann erheblich mehr Elemente erzeugen als lokal nötig. Der Baustein garantiert weder positive Jacobideterminanten noch Elementqualität, globale Knoten-/Kantenkonformität oder CCFSM-Zustandspositivität. Er ist ein geometrischer Vorbereitungsbaustein für die spätere 3-D-Zertifizierung.

## Tests

test_ccfsm_p27_6_refinement_closure.py deckt einseitige Markierung, Nachbarschaftsketten, getrennte Komponenten, bereits ausgeglichene Tiefen, nicht-manifold Flächen, Ressourcenabbruch und ungültige Eingaben ab.
