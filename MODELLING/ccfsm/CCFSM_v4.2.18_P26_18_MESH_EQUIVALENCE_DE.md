# P26.18 — Zertifikatsvergleich über rationale Darstellungen und Zellpartitionen

**Stand: 15. November 2026**

## Ziel

P26.18 ergänzt P26.17 um einen Vergleich bereits unabhängig geprüfter Zertifikatsberichte. Geprüft wird, ob zwei Berichte exakt dieselben globalen Zielmomente besitzen, denselben Belegstatus aufweisen und ihre jeweiligen Primär-/Dualbelege eigenständig bestehen.

## Exakte Signatur

Für jede Eingabe werden Kanten, Zellmittelwerte sowie lineare und quadratische Ausgangsmoden mit `Fraction` rationalisiert. Die Signatur ist das Tripel der exakten globalen Momente
[
(M_0,M_1,M_2),
]
berechnet aus den Zellpolynomen und den rationalen Zellgrenzen. Unterschiedliche Schreibweisen wie `0.5`, `1/2` und `Fraction(1,2)` werden auf denselben rationalen Wert abgebildet.

## Partitionen und Aussagegrenze

Der Referenzvergleich stellt eine Ein-Zellen-Partition einer Zweizellen-Partition gegenüber. Beide enthalten denselben konstanten positiven Profilzeugen und liefern exakt dieselben globalen Momente. Der Vergleich bestätigt damit die Gleichheit der globalen Momentenziele und die unabhängige Gültigkeit beider Zertifikate.

**Nicht** behauptet wird, dass beliebige verschiedene Partitionen denselben lokalen Funktionsraum, dieselben zulässigen Profile oder dieselbe Rekonstruktion besitzen. Gleiche drei globale Momente sind nur eine Momentenäquivalenz. Insbesondere kann eine Verfeinerung die diskrete Menge darstellbarer Profile ändern.

## Entscheidungslogik

- Ungültiger Hash oder ungültiger Einzelbeleg: Vergleich abgewiesen.
- Unterschiedliche globale Momententripel: `different_global_targets`.
- Unterschiedlicher Zertifikatsstatus: `inconclusive_status_mismatch`.
- Zwei unresolved-Berichte bleiben `same_target_but_unresolved`; sie werden nie zu einem Machbarkeitsbeweis hochgestuft.
- Nur zwei unabhängig verifizierte Belege mit gleichem Status und identischem rationalem Momententripel ergeben `equivalent_global_moment_certificates`.

Die Vergleichsfunktion behauptet keine physikalische Äquivalenz und ersetzt keinen vollständigen Machbarkeitsentscheid.

## Dateien und Reproduktion

- `ccfsm_p26_18_mesh_equivalence.py`: exakte Momentensignatur, Berichtsvergleich und rationale Kanonisierung.
- `test_ccfsm_p26_18_mesh_equivalence.py`: Partition, Dezimal-/Bruchalias, abweichende Ziele, unresolved-Semantik und Hashmanipulation.
- `ccfsm_p26_18_mesh_equivalence_study.py`: reproduzierbarer Ein-/Zweizellen-Referenzvergleich und JSON-Berichte.

Ausführung im Paketverzeichnis:
```bash
python ccfsm_p26_18_mesh_equivalence_study.py --output-dir ccfsm-p26-18-results
python -m unittest -v test_ccfsm_p26_18_mesh_equivalence.py
```

Geltungsbereich: 1-D, feste nichtnegative Zellmittelwerte, stückweise quadratische Profile und globale Masse/erste/zweite Momente. Softwareverifikation ist keine physikalische oder experimentelle Validierung.
