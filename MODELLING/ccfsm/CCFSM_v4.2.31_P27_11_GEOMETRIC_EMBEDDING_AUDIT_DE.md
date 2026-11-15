# CCFSM v4.2.31 — P27.11 geometrischer Einbettungs-Audit

## Zweck
P27.11 ergänzt P27.10 um einen geometrischen Test der Tetraederinterieurs. Nach erfolgreichem P27.10-Link-Audit werden alle Tetraederpaare mit einem exakten Separating-Axis-Test (SAT) untersucht.

## Exakte Prüfung
Die Achsenmenge enthält die Normalen aller vier Dreiecksflächen beider Tetraeder sowie Kreuzprodukte aller Kantenrichtungs-Paare. Alle Koordinaten werden von P27.8 als rationale Zahlen repräsentiert. Für jede nichtverschwindende Achse werden die Projektionsintervalle exakt berechnet. Ist die Überlappung auf mindestens einer Achse nicht positiv, sind die Tetraederinterieurs getrennt oder berühren sich nur. Ist sie auf sämtlichen SAT-Achsen strikt positiv, wird eine positive Volumenüberlappung gemeldet.

Gemeinsame Flächen-, Kanten- und Knotenberührungen sind daher erlaubt und werden nicht als positive Volumenüberlappung klassifiziert. Zusätzlich werden verschiedene Knoten-IDs mit identischen exakten Koordinaten gemeldet.

## Status
- `geometric_embedding_audited`: keine positive Volumenüberlappung und keine doppelten Koordinaten unter verwendeten Knoten-IDs gefunden.
- `geometric_embedding_inconsistent`: mindestens eine Volumenüberlappung oder ein Koordinatenalias gefunden.
- `base_audit_failed`: P27.10 hat die topologischen Voraussetzungen nicht erfüllt.

## Grenzen
P27.11 prüft positive Volumenüberlappungen zwischen Tetraederpaaren, nicht sämtliche niederdimensionalen Schnittmengen nicht inzidenter Simplizes. Insbesondere werden isolierte Berührungen von nicht benachbarten Flächen/Kanten, Selbstüberschneidungen einer Randtriangulierung und globale Orientierung/Einbettung des Randes nicht vollständig klassifiziert. Die Paarprüfung ist quadratisch in der Elementzahl und besitzt noch keine räumliche Beschleunigungsstruktur.

Der Audit zertifiziert weder FE-Konditionierung noch CCFSM-Zustandspositivität, Energieabschluss oder physikalische Validität.
