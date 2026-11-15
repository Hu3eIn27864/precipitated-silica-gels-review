# P27.7 — tatsächliche konforme rote Tetraederverfeinerung

**Status:** implementiert; automatisierte CI-Prüfung ausstehend.

## Ablauf

1. P27.6 schließt die angeforderten Tiefen komponentenweise über gemeinsame grobe Flächen.
2. Jedes grobe Tetraeder wird mit dem exakten Acht-Kind-Schema aus P27.3 rekursiv verfeinert.
3. Alle Kindknoten werden in exakten rationalen physikalischen Koordinaten erzeugt und global dedupliziert.
4. Die vollständigen Blattpartitionen werden an den unabhängigen P27.5-Prüfer übergeben. Nur bei dessen Ergebnis `conforming` wird ein Mesh mit Status `generated_conforming_mesh` ausgegeben.
5. Exakte Kinddeterminanten werden auf Degeneration geprüft.

## Ergebnis und Grenzen

- Das Ergebnis enthält globale Knoten, Kind-Tetraeder, Parent-zu-Kind-Indizes, geschlossene Tiefen und den P27.5-Auditbericht.
- Ressourcenlimit, fehlerhafte Konnektivität, nicht-manifold Flächen oder fehlgeschlagener Konformitätsaudit liefern keinen erfolgreichen Meshstatus.
- Die P27.6-Regel bleibt konservativ: eine ganze face-zusammenhängende Komponente kann auf die maximale lokale Tiefe angehoben werden.
- Die Orientierung wird nicht stillschweigend umgeordnet; es wird nur Degeneration ausgeschlossen. Eine positive Orientierungsnormalisierung, globale Kanten-/Knotenmannigfaltigkeit, Meshqualität und Randgeometrie sind noch nicht zertifiziert.
- Der Meshgenerator zertifiziert keine P2-Feldpositivität und keine CCFSM-Transport-/Reaktionspositivität. Dafür bleiben P27.3/P27.4 sowie weitere gekoppelte Invariantenprüfungen nötig.

## Tests

Acht Tests prüfen unverfeinerte, einseitig angeforderte und zweistufige Verfeinerung, getrennte Komponenten, Ressourcenabbruch, nicht-manifold Eingaben, exakte rationale Koordinaten sowie fehlerhafte Eingaben.
