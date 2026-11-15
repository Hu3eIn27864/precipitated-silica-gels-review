# CCFSM v4.2.41 — P27.21 Variationsaudit der gemeinsamen lokalen Energie

**Stand:** 15.11.2026  
**Status:** P9-Energiezerlegung und numerischer Konjugiertentest implementiert; gemeinsame P10/P13/P19-Energie noch nicht zertifiziert.

## Ergebnis des Audits

P27.21 nimmt die in P9 bereits vorhandene lokale gespeicherte Energiedichte auseinander:

\[
\psi_{P9}=\psi_{\rm el}+\psi_{\rm Biot}+\psi_{\rm chem}.
\]

Der neue Auditbaustein berechnet die Ableitungen dieser Energiedichte numerisch mit zentralen bzw. randnah einseitigen Differenzen und vergleicht sie mit den von P9 ausgegebenen Konjugierten:

\[
\partial_{n_i}\psi_{P9}\stackrel{?}{=}\mu_i^{\rm total},
\qquad
\partial_{\theta}\psi_{P9}\stackrel{?}{=}p-\Pi_{\rm osm}.
\]

Einheiten: `psi` in J/m³, Inventar-Konjugierte in J/mol, Fluidkapazitäts-Konjugierte in Pa. Das sind unabhängige Differenzenquotienten gegen die vorhandenen P9-Ausgaben, keine symbolische Identitätsbehauptung.

## Wichtige konzeptionelle Grenze: äußere Traktion

P9 gibt `free_energy_j_m3_reference` als gespeicherte innere Energie aus; der äußere Traktionspotentialterm ist ausdrücklich nicht enthalten. Bei kraft-/traktionsgesteuerter Mechanik muss für eine Variationsaussage das passende Gesamtpotential (innere Energie minus äußere Arbeit, mit konsistentem Vorzeichen und Lastpfad) differenziert werden. Daher gibt P27.21 bei nichtverschwindender axialer Traktion eine ausdrückliche Warnung aus. Ein gespeicherter Energiegradient und ein Gesamtpotentialgradient sind nicht ohne Weiteres identisch.

## Abgrenzung zu P10/P13/P19

- P10 und P13 verwenden die P9-Zellkonjugierten für Reaktion und Onsager-Transport; P13 prüft bereits die Diffusionsdissipation. P27.21 prüft nun unabhängig, ob diese Konjugierten tatsächlich Ableitungen der gemeldeten P9-Energiedichte sind.
- P19 verwendet eine räumliche 3D-Biot/Eigenstrain-Energie mit FE-Quadratur. Ihre Parameter, Geometrie, Eigenstrain-Abbildung und Referenzvolumen müssen mit der P9-Energie abgeglichen werden; die bloße Addition beider Energien wäre eine mögliche Doppelzählung.
- Die P9-Energie enthält chemische, elastische und Biot-Speicherterme gemeinsam. P19-Mechanik darf nicht nochmals addiert werden, wenn sie bereits dieselbe elastische/Biot-Energie repräsentiert.

## Implementierung und Tests

Modul: `ccfsm_p27_21_variational_audit.py`  
Tests: `test_ccfsm_p27_21_variational_audit.py` (fünf Regressionen).

Geprüft werden die fünf Konjugierten, die explizite Dreitermzerlegung, ungültige Zustände und der Traktionswarnpfad. Der Audit liefert numerische Defekte und toleranzbasierte Einzelstatus.

## Aussagegrenzen und nächste Schritte

Ein bestandener P9-Test ist ein lokaler Variationskonsistenztest unter den geprüften Parametern, kein Beweis einer gemeinsamen diskreten freien Energie für das gesamte P10/P13/P19/P21-System. Er zertifiziert weder Randarbeit noch Advektionsentropie, globalen Energieabschluss, PDE-Existenz, 3D-Positivität oder experimentelle Validierung.

**P27.22:** P19-Energie funktional mit P9 vergleichen (gleiche isotrope Elastizität, Biot-Speicherung, Eigenstrain und Quadratur); anschließend explizite Exklusivitätsregeln gegen Doppelzählung festlegen. Erst danach den P27.20-Zwei-Zustandsadapter und P27.19-Ledger verbinden.
