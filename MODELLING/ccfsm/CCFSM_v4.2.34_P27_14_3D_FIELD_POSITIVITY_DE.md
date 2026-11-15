# CCFSM v4.2.34 — P27.14: integrierter 3D-Feldpositivitäts- und Margen-Audit

**Status: implementiert; CI-Prüfung ausstehend.**

P27.14 ergänzt den P27.13-Netzaudit um einen zellweisen exakten Positivitätscheck für skalare FE-Felder auf Tetraedern:

- P1: nichtnegative vier Eckwerte sind notwendig und hinreichend für Nichtnegativität des affinen Feldes auf dem Tetraeder.
- P2: exakte quadratische Bernstein-Koeffizienten und adaptive Unterteilung aus P27.3; ein Erfolg wird unabhängig durch den P27.4-Verifikator nachgerechnet.
- Ein negativer Bernstein-Koeffizient allein gilt weiterhin nicht als Negativitätsbeweis. Exakte negative Punktzeugen, nicht zertifizierte/unaufgelöste Zellen und positive Zertifikate bleiben getrennte Status.
- Für zertifizierte Zellen wird eine konservative untere Schranke aus den P1-Knotenwerten beziehungsweise den P2-Blatt-Bernstein-Koeffizienten ausgewiesen. Ein optionaler Mindestabstand zur Null ist ein separates Freigabekriterium.

Die Pipeline verlangt zuerst den vollständigen P27.13-Netz-Audit. Bei einem Netzfehler wird die Feldprüfung nicht ausgeführt. Pro Tetraeder wird genau ein P1- oder P2-Skalarpolynom erwartet; P2-Kantenmittelpunkte folgen der Ordnung (01,02,03,12,13,23).

**Mathematische Aussage:** Ein erfolgreiches P1/P2-Ergebnis zertifiziert die punktweise Nichtnegativität des angegebenen diskreten Skalarpolynoms auf allen geprüften Tetraedern. Die ausgegebene positive Marge ist eine konservative Bernstein-Untergrenze, keine Schätzung des Minimums.

**Nicht behauptet:** Keine Positivitätsgarantie für sämtliche CCFSM-Komponenten, keine Invarianz des gekoppelten Reaktions-/Transport-Zeitschritts, keine Stabilitäts- oder Konvergenzgarantie des 3D-Solvers, kein FE-Konditionierungs-/Koerzivitätsbeweis, kein Energieabschluss und keine physikalische Validierung. Für gekoppelte Zustände müssen die konkreten FE/FV-Repräsentationen, Reaktionsquellen, Flüsse, Randbedingungen und der Zeitintegrator gemeinsam analysiert werden.

Regressionen: P1-Positivität und negativer Knoten, P2-Unterteilungszertifikat plus unabhängige Verifikation, unresolved bei zu geringer Tiefe, vorgeschaltetes Mesh-Gate, separate Margenschwelle sowie fehlerhafte Eingaben.
