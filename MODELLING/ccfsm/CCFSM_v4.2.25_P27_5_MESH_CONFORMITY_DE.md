# P27.5 — exakte Konformitätsprüfung benachbarter Tetraeder

**Status:** implementiert als Audit-Prüfer für P27.3-Blattpartitionen.

## Ziel und Verfahren

P27.3 zertifiziert ein einzelnes Tetraeder. P27.5 prüft, ob benachbarte grobe Tetraeder auf ihrer gemeinsamen Fläche dieselbe exakte Dreieckszerlegung induzieren. Alle Koordinaten werden rational verarbeitet. Blattflächen auf einer groben Elementfläche werden aus den baryzentrischen Wurzelkoordinaten rekonstruiert, kanonisiert und exakt verglichen. Hanging-Face-Konstellationen und nicht-manifold grobe Flächen werden erkannt.

## Tests

- Unverfeinerte gemeinsame Fläche auf beiden Seiten: konform.
- Nur eine Seite verfeinert: nichtkonform.
- Gleiche Achtfachverfeinerung beider Seiten: konform.
- Früher Negativpunktabbruch, nicht-manifold face und fehlerhafte Konnektivität: abgewiesen.

## Grenzen

Dies ist ein nachgelagerter Konformitäts-Audit, kein konformer Verfeinerungsalgorithmus. Er prüft gemeinsame Dreiecksflächen, aber noch keine globale Knoten-/Kantenkonnektivität aller Blattelemente, Elementorientierung oder Mesh-Qualität. Ein P27.3-Negativpunktresultat liefert keine vollständige Blattpartition und wird daher nicht als Mesh-Partition akzeptiert. Keine globale Positivitätsinvarianz des gekoppelten CCFSM und keine physikalische Validierung.
