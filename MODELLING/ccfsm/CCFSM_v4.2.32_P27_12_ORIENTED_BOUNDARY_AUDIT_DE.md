# CCFSM v4.2.32 — P27.12: Exakter Audit der orientierten Randfläche

**Ziel.** P27.12 ergänzt P27.11 um eine exakte Prüfung des aus positiv orientierten Tetraedern induzierten Randketten-Komplexes. Es wird keine physikalische CCFSM-Validierung behauptet.

## Implementierung

- P27.11 wird zuerst ausgeführt; ein fehlgeschlagener Link-/Einbettungs-Audit wird unverändert als `base_audit_failed` weitergereicht.
- Für jedes positiv orientierte Tetraeder werden die vier induzierten orientierten Dreiecksflächen verwendet: `(b,c,d), (a,d,c), (a,b,d), (a,c,b)`.
- Randkanten werden nach ihrer unorientierten ID und gerichteten Inzidenz geprüft. Eine geschlossene orientierte Randfläche benötigt genau zwei Vorkommen jeder Randkante in entgegengesetzten Richtungen.
- Randdreiecke werden über gemeinsame Kanten zu Randkomponenten gruppiert. Für jede Komponente werden V/E/F und die Euler-Charakteristik berechnet. Bei geschlossenen orientierbaren Komponenten wird der aus `chi = 2 - 2g` abgeleitete ganzzahlige Genus ausgegeben.
- Das orientierte Randvolumen wird exakt als Summe der Dreiecksdeterminanten geteilt durch sechs berechnet und mit der Summe der orientierten Tetraedervolumina verglichen.

## Exakte Aussage und Grenzen

Bei bestandenem Audit sind die geprüften Randkanteninzidenzen orientierungskonsistent, die Randkomponenten erfüllen den Euler-Paritätstest geschlossener orientierbarer Flächen, und die orientierte Randvolumensumme stimmt exakt mit der Tetraedervolumensumme überein.

Die Volumenidentität ist eine algebraische Ketten-/Divergenzidentität; sie ist für sich allein kein Beweis einer global injektiven Einbettung. P27.11 prüft positive Volumenüberlappung von Tetraederpaaren, aber keine vollständige Klassifikation aller niedrigerdimensionalen nichtinzidenten Schnittfälle. P27.12 prüft außerdem keine Selbstüberschneidungen der Randfläche, keine FE-Konditionierung, keine CCFSM-Positivität, keinen Energieabschluss und keine physikalische Validität. Bei mehreren Randkomponenten werden deren vorzeichenbehaftete Volumenbeiträge getrennt berichtet; negative Beiträge können beispielsweise bei inneren Hohlraumrändern geometrisch sinnvoll sein.

## Regressionen

`test_ccfsm_p27_12_oriented_boundary_audit.py` prüft ein einzelnes Tetraeder, zwei Tetraeder mit gemeinsamer Fläche, getrennte Randkomponenten, exakte Volumenbilanz und die Fehlerweitergabe des Basis-Audits.

**Freigabestatus:** Implementierung und Regressionstests angelegt; die Freigabe hängt vom lokalen Testlauf und dem abgeschlossenen Hosted-CI-Lauf ab.
