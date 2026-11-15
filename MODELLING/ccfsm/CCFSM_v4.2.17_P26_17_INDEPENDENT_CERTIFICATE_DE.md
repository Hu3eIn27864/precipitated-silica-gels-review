# P26.17 — Reproduzierbarer Primal-Dual-Zertifikatsbericht und unabhängige Prüfung

**Stand: 15. November 2026**

## Ziel

P26.17 definiert ein portables JSON-Berichtsformat und einen unabhängigen Verifikator. Die Kandidatenerzeugung bleibt Aufgabe von P26.14/P26.15; die Prüfung importiert weder diese Solver noch P26.8 oder P26.13. Sie verwendet nur Python-Standardbibliothek und rationale Ganzzahlarithmetik.

## Berichtsschema

Jeder Bericht enthält:
- Schema-Version ccfsm-p26.17-certificate-report-v1;
- kanonische rationale Eingaben (Intervallgrenzen, Zellmittelwerte und Ausgangskoeffizienten);
- einen der Status feasible_exact_primal_witness, certified_infeasible oder unresolved;
- bei primaler Machbarkeit die Zellkoeffizienten sowie Markov-Lukács-\(\lambda\)- und Gram-Matrix-Daten je Zelle;
- bei dualer Unzulässigkeit die Separatorrichtung und die Quadratwurzel-Präzision;
- SHA-256-Fingerabdruck des kanonisch serialisierten Berichts.

Der Hash erkennt versehentliche oder nachträgliche Änderungen. Er ist keine digitale Signatur und kein Herkunftsnachweis.

## Unabhängige Primärprüfung

Der Verifikator berechnet die drei globalen Momente aus den rationalen Eingaben und dem vorgeschlagenen Profil neu. Er verlangt exakte Gleichheit zu den vorgegebenen Zielmomenten. Pro Zelle prüft er separat:
\[
q(x)=[1,x]Q[1,x]^T+\lambda(1/4-x^2),
\quad Q\succeq0,\quad\lambda\ge0.
\]
Dazu werden Symmetrie, Diagonaleinträge, Determinante, PSD-Bedingung und Koeffizientenidentität exakt mit Fraction geprüft. Eine positive Primärprüfung ist damit ein eigenständig nachprüfbarer Existenzbeleg.

## Unabhängige Dualprüfung

Aus der übermittelten Richtung berechnet der Verifikator die Support-Obergrenze erneut. Quadratwurzeln werden mit ganzzahliger Quadratwurzel und rationaler Obergrenze eingeschlossen. Nur eine strikt positive rationale untere Trennungslücke wird als certified_infeasible akzeptiert. Suchradius und Suchhistorie sind kein Beweisbestandteil.

## Unresolved und Fehlerfälle

Ein Bericht ohne exakten Beleg bleibt unresolved; der Verifikator stuft ihn niemals aufgrund einer fehlgeschlagenen Suche als machbar oder unmachbar ein. Falsche Hashes, inkonsistente Zertifikate, Momentenabweichungen oder nicht-PSD-Gram-Matrizen werden abgewiesen.

## Dateien und Tests

- ccfsm_p26_17_independent_certificate.py: Berichtserzeugung, kanonische Serialisierung, Fingerprint und unabhängige Prüfung.
- test_ccfsm_p26_17_independent_certificate.py: Tests für primalen Beleg, fehlerhaften Beleg, duale Neuberechnung, unresolved-Semantik und Integritätsprüfung.
- ccfsm_p26_17_certificate_study.py: reproduzierbarer Berichtsexport für die Referenzfälle.

Geltungsbereich: 1-D, feste nichtnegative Zellmittelwerte, quadratische Profile und globale Masse/erste/zweite Momente. Keine physikalische oder experimentelle Validierung.
