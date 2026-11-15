# CCFSM v4.2.33 — P27.13: integrierter 3D-Netz-Gesamtaudit

## Zweck

P27.13 bündelt die Prüfschritte P27.8 bis P27.12 zu einem reproduzierbaren Freigabebericht für ein tetraedrisches 3D-Netz. Die einzelnen Prüfungen bleiben separat sichtbar; ein später Gate-Fehler darf nicht durch einen früheren Erfolg verdeckt werden.

## Prüfkette

| Gate | Prüfung | Bestehenskriterium |
|---|---|---|
| P27.8 | Exakte Orientierung, Nichtdegeneration, Formqualität | Alle Elemente positiv orientiert und nicht degeneriert; optionale rationale Mindestqualität eingehalten |
| P27.9 | Globale Inzidenz | Keine überinzidenten Flächen, keine widersprüchliche Orientierung gemeinsamer Innenflächen, keine Duplikate |
| P27.10 | Lokale Links | Kanten-Links Weg/Kreis und Knoten-Links Scheibe/Sphäre gemäß Rand-/Innenlage |
| P27.11 | Geometrische Einbettung | Keine positiven Volumenüberlappungen von Tetraederinterieurs; keine verschiedenen verwendeten Knoten-IDs mit identischen Koordinaten |
| P27.12 | Orientierter Rand | Geschlossene, orientierungskonsistente Randkanteninzidenzen, Euler-/Genus-Prüfung und exakte Volumenbilanz |

## API und Ausgabe

`audit_tetra_mesh_3d(vertices, tetrahedra, min_quality_ratio=0)` liefert einen strukturierten Bericht mit:
- `status` und `overall_pass`,
- einzelnem `gate_results` für P27.8–P27.12,
- kompakter `mesh_summary`,
- vollständigen Unterberichten für Geometrie, Inzidenz, Links, Einbettung und Rand.

Bei einem Fehler wird die Kette kontrolliert angehalten und der erste fehlgeschlagene Gate-Status samt Diagnose ausgegeben. Die Qualitätsuntergrenze ist optional und wird exakt rational geprüft.

## Regressionsabdeckung

Die Tests umfassen ein einzelnes Tetraeder, zwei Tetraeder mit gemeinsamer Fläche, getrennte gültige Komponenten, einen absichtlich nicht erfüllten Qualitätsgrenzwert und einen ungültigen Duplikatfall.

## Strenge Freigabegrenze

`integrated_mesh_audited` bedeutet ausschließlich, dass die implementierten P27.8–P27.12-Checks bestanden wurden. Der paarweise SAT-Schritt ist quadratisch in der Elementzahl. P27.11/P27.12 liefern keinen vollständigen Beweis für alle niederdimensionalen nichtinzidenten Schnitte oder Rand-Selbstüberschneidungen. Der Audit zertifiziert weder FE-Konditionierung noch CCFSM-Zustandspositivität, diskreten Energieabschluss oder physikalische Validität. Dafür sind separate mathematische, numerische und experimentelle Nachweise erforderlich.

**Freigabestatus:** Implementierung und Regressionstests angelegt; Hosted CI muss nach Abschluss geprüft werden.
