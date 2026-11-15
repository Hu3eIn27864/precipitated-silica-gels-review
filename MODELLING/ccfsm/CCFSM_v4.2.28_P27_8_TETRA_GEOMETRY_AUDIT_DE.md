# P27.8 — exakte Orientierung und Elementqualitätsprüfung für Tetraedernetze

**Status:** implementiert; CI-Prüfung ausstehend.

## Exakte Geometrie

Für jedes Tetraeder wird die orientierte sechsfache Volumengröße D=det(x1−x0,x2−x0,x3−x0) mit rationaler Arithmetik berechnet. D=0 wird als degeneriert zurückgewiesen. Bei D<0 werden zwei lokale Knoten vertauscht; danach gilt D>0. Alle akzeptierten Elemente besitzen damit positive lokale Orientierung.

## Dimensionsloser Formqualitätsindikator

Mit S als Summe der Quadrate aller sechs Kantenlängen wird Q=432 D²/S³ verwendet. Q ist exakt rational, dimensionslos und skaleninvariant; ein reguläres Tetraeder hat Q=1, ein degeneriertes Q=0. Kleine Werte kennzeichnen flache/gestreckte Elemente. Ein optionaler exakter Grenzwert min_quality_ratio kann als harte Freigabeschwelle gesetzt werden. Bei Unterschreitung wird kein Mesh ausgegeben.

## Schnittstelle und Tests

- tetrahedron_geometry(vertices, tet) liefert signiertes sechsmaliges Volumen und Q.
- normalize_and_audit_tetra_mesh(...) normalisiert die Orientierung und prüft alle Elemente.
- Neun Tests decken reguläres Tetraeder, positive/negative Orientierung, Skalierungsinvarianz, Qualitätsgrenze, Degeneration, fehlerhafte Eingaben und gemischte Orientierungen ab.

## Aussagegrenzen

Dies ist eine geometrische Aussage über die gelieferten linearen Tetraederelemente. Sie ist kein Nachweis globaler Knoten-/Kantenmannigfaltigkeit, keine Randapproximation, keine Fehlerabschätzung und keine CCFSM-Zustandspositivitätsgarantie. Die Qualitätsmetrik ist ein Formindikator, kein vollständiges Qualitäts- oder Konditionierungszertifikat für alle FE-Operatoren. Schwellenwerte müssen problembezogen begründet werden; standardmäßig wird nur Degeneration ausgeschlossen.