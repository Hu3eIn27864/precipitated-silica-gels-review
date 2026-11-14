# CCFSM — natural syneresis only

This folder contains the versioned CCFSM specifications and implementations for **unloaded natural syneresis of precipitated silica gels** (v0.1 empirical/poroelastic core and v0.2 two-timescale extension).

- CCFSM_NATURAL_SYNERESIS_v0.1.md — model definition, governing equations, empirical coefficient audit, identifiability limits, and mathematical propositions/energy proof.
- ccfsm_reduced.py — verified scalar natural-syneresis response and dimensionally checked hydraulic time-scale helper.
- test_ccfsm_reduced.py — unit tests for exact solution, bounds, monotonicity, semigroup property, volume balance, and input validation.
- natural_syneresis_empirical_coefficients_2026-11-14.csv — machine-readable copy of the seven current digitized primary fits and derived apparent rates.
- wilhelm_kind_natural_syneresis_source_table_coefficients_2026-11-14.csv — separate machine-readable copy of the 12 source-reported natural-syneresis Table 1/2 parameter combinations; the basic-droplet branch is explicitly flagged as conflicting with the dissertation source.
- wilhelm_2017_dissertation_basic_droplet_conflict_2026-11-14.csv — the separate natural-syneresis coefficient branch from dissertation Table 5.3 (A = 0.40/0.63/0.82; tau = 0.671/0.640/1.055 h at 20/40/60 °C). Do not average it with the journal Table 2 values.

## Reproduction

From this folder:

    python -m unittest -v

The seven parameter rows are sourced from the project's curated primary fit table for digitized Wilhelm & Kind (2015) natural-syneresis curves. These are figure-derived approximations, not author-supplied raw data. Excluded sensitivity/conflict branches remain excluded.

No oedometer, imposed-load, or forced-syneresis coefficient is used for the CCFSM natural-syneresis calibration. Unidentified chemical, fractal, eigenstrain, permeability, and modulus parameters are intentionally left unset.


## CCFSM v0.2 — two-timescale natural-syneresis closure

Added on 14 November 2026:

- CCFSM_v0.2_TWO_TIMESCALE.md — separation of intrinsic network contraction and observed hydraulic shrinkage; closed-form solutions; proofs of existence, invariant region, monotonicity and rate-label non-identifiability; finite-strain kinematics; silicon-balance caveat; natural-only experiment design.
- ccfsm_two_stage.py — exact two-state response, stable equal-rate limit, hydraulic-rate scaling, isotropic natural stretch, and unordered rate-pair recovery.
- test_ccfsm_two_stage.py — 12 regression tests.

The two new rates are not fitted to the current one-exponential tables or approximate digitized traces. The source-reported (A, tau) values from v0.1 remain unchanged. A single zero-start shrinkage curve only identifies an unordered pair of two rates and the endpoint product eta_a*q_infinity; assigning physical labels requires an independent chemical/structural or hydraulic measurement.

Local software verification: 12/12 v0.2 tests passed with python -m unittest -v. Hosted GitHub Actions run [43569636089](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43569636089) passed 22/22 tests in total (10 v0.1 and 12 v0.2). This is not physical validation. The natural-only exclusion remains in force: no oedometer, forced-syneresis or imposed-load coefficient is used.

The dedicated GitHub Actions workflow at .github/workflows/ccfsm-ci.yml runs all CCFSM unit tests on push/pull requests that touch this package.


## CCFSM v0.2a — prescribed temperature history

Added a protocol-aware piecewise-constant rate propagator:

- CCFSM_v0.2a_TEMPERATURE_HISTORY.md — source-level audit of the 20 °C droplet preparation period, the approximately 30-min initial curve overlap, sample heating lag, and exact segment propagator.
- ccfsm_thermal_history.py — Arrhenius helper with user-supplied parameters and exact piecewise rate switching for the two-state natural-syneresis ODE.
- test_ccfsm_thermal_history.py — seven tests including v0.2 recovery, semigroup composition, staged-rate history, invariant region, Arrhenius direction and validation.

The model holds q_infinity and natural-interface accessibility fixed within one specified protocol. The available article reports temperature-dependent endpoints, so one endpoint is not assumed to apply to all protocols. No activation energy, sample thermal time constant, permeability or modulus is estimated from nominal bath temperature. Local verification: 7/7 new tests passed; the dedicated CCFSM CI runs the full package test suite.


## CCFSM v0.3 — bridge / morphology / eigenstress / natural drainage
- CCFSM_v0.3_IDENTIFIABILITY_DE.md — structural and practical identifiability analysis; exact unobservable parameter blocks, bridge-scale symmetry, and measurement requirements.
- test_ccfsm_identifiability.py — regression tests demonstrating exact output invariance under bridge-scale, stress-relaxation-rate and morphology-parameter changes.
- CCFSM_v0.3_MATHEMATICAL_DERIVATION_DE.md — German step-by-step derivation, exact state solutions, contraction-inventory balance, dimensional check and conditional proofs of positivity, boundedness and monotonicity.

- CCFSM_v0.3_BRIDGE_MORPHOLOGY_STRESS.md — governing equations, parameter meanings, identifiability limits and synchronized natural-syneresis experiment design.
- ccfsm_v03.py — state model for load-bearing bridge inventory, fractal dimension, contact number, residual eigenstress, stress-relaxed contraction and observed natural shrinkage.
- test_ccfsm_v03.py — nine regression tests.

The bridge-to-morphology relations are explicit testable hypotheses, not established silica laws. Df/contact number are not used as unvalidated surrogates for permeability or modulus. All coefficients remain user-supplied/un-calibrated; no oedometer or forced-syneresis data enter the natural model.


## CCFSM v0.4 — vollständige Einflussparameter-Architektur

- CCFSM_v0.4_CHEMICAL_SUBMODEL_DE.md — chemische Teilbilanz mit Monomer-/Oligomer-/Netzwerk-Si, pH-/Ionenstärke-/Temperaturmodifikatoren, Brückenfraktion und Transfergrenzen.
- ccfsm_chemical_v04.py — SI-Sekunden-basierter chemischer ODE-Block; liefert effektive Brückendichte und deren Änderungsrate als Eingang für v0.3.
- test_ccfsm_chemical_v04.py — Regressionstests für Si-Erhaltung, Brückenschranken, pH-Kanäle, Arrhenius-Richtung und Integrator.
- CCFSM_v0.4_CHEMICAL_PARAMETER_REGISTER.csv — spezifisches Register der chemischen Zustände und kinetischen Parameter.

Das chemische Teilmodell ist mechanistisch modular, aber noch nicht an industriell gefällte Silica-Gele kalibriert. Die pH-/Ionenstärke-/Arrhenius-Funktionen sind identifizierbare Hypothesen; keine Literaturkoeffizienten werden ungeprüft als Zielsystemparameter eingesetzt.

- CCFSM_v0.4_PARAMETER_ARCHITECTURE_DE.md — kausale Parametergruppen von Rezeptur/Fällchemie über Temperatur, Mischung, Netzwerk, Porenraum und Mechanik bis Transport, Grenzfläche, Geometrie und Messunsicherheit; Freigabekriterien für vollständig grüne Gleichungen.
- CCFSM_v0.4_INFLUENCE_PARAMETER_REGISTER.csv — maschinenlesbares Register mit Symbol, Gruppe, Rolle, Einheit, Wirkpfad, Messbedarf und Identifizierbarkeitswarnung.
- CCFSM_v0.4_EQUATION_VERIFICATION_MATRIX_DE.md — 24 equation blocks with separate mathematical, physical and empirical readiness gates; explicit rejection rules for double counting and unsupported structure–permeability laws.
- test_ccfsm_v04_parameter_register.py — schema, unique-symbol and required-influence checks for the machine-readable parameter register.

v0.4 ist zunächst eine vollständige Parameterarchitektur, keine unkalibrierte Erweiterung aller ODEs. Insbesondere werden pH und Rezeptur nicht doppelt als unabhängige Ursachen gezählt; Gelkerntemperatur wird von Badtemperatur getrennt; D_f/z werden nicht ohne Porenhals- und Konnektivitätsdaten als Permeabilitätsersatz verwendet. Die natürliche, mechanisch unbelastete Synärese bleibt der einzige Geltungsbereich.

## CCFSM v0.4a — Rezeptur-zu-Speziation

- CCFSM_v0.4a_RECIPE_SPECIATION_DE.md — Rezeptur-Stoffbilanz, Speziationsgleichgewichte, Aktivitätsmodell und Gültigkeitsgrenzen.
- ccfsm_recipe_speciation_v04a.py — pH-Solver aus Natriumsilikatmodul, Gesamtsilicium, Schwefelsäure, NaOH/NaCl, Sulfat- und Natrium-Bilanz; Adapter zu ChemicalEnvironment mit expliziter Lösungsmittelmassen-Umrechnung.
- test_ccfsm_recipe_speciation_v04a.py — Regressionstests für Elektroneutralität, Stoffbilanzen, Säurewirkung, Ionenpaarbildung und Davies-Abbruch.

Der Solver ist ein vorläufiges Gleichgewichtsmodul. Davies wird oberhalb 0,5 mol/L Ionenstärke nicht extrapoliert. Für konzentrierte Prozessbrühen ist ein validiertes Pitzer/SIT-Modell bzw. eine experimentelle Aktivitätsbestimmung erforderlich. Die Temperaturabhängigkeit der Gleichgewichtskonstanten und zusätzliche Silica-Oligomer-/Oberflächenspezies sind noch nicht implementiert.

Der Rezeptur-Speziationsblock wurde mit dem bestehenden CCFSM-Kinetikmodul über einen Einheiten-sicheren Adapter verbunden. Der aktuelle CI-Lauf [43591288426](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43591288426) bestand 64/64 Tests. Dies ist numerische Softwareverifikation, keine Validierung an realen Prozessbrühen.


## Literaturdaten-Integration — 14 November 2026

- [CCFSM_LITERATURE_PARAMETER_EXTRACTION_2026-11-14_DE.md](CCFSM_LITERATURE_PARAMETER_EXTRACTION_2026-11-14_DE.md) — Quellenkritischer Bericht zu Wilhelm & Kind, Quarch, Schlomach & Kind sowie Sahabi & Kind.
- [ccfsm_literature_parameter_dataset_2026-11-14.csv](ccfsm_literature_parameter_dataset_2026-11-14.csv) — maschinenlesbare Extraktion mit Quellenjahr, Einheit, Datenklasse, Prozess-/Geometrie-Tag und zulässiger CCFSM-Verwendung.
- [test_ccfsm_literature_dataset.py](test_ccfsm_literature_dataset.py) — prüft CSV-Schema, eindeutige Datensatz-IDs, numerische Werte und den Ausschluss erzwungener/qualitativer Daten aus der natürlichen Kalibrierung.

**Kalibrierungsregel:** Nur die zwölf zylindrischen Wilhelm-&-Kind-Kennwerte (sechs (S_{max})- und sechs \\(\\tau\\)-Werte) sind im Datensatz als primäre natürliche CCFSM-Kalibrierwerte markiert. Tröpfchen bleiben ein separater Geometrie-/Temperaturhistorien-Datensatz. Quarch liefert überwiegend kontextuelle bzw. qualitative Angaben; Schlomach Morphologieanker; Sahabi & Kind MD-Setup und erzwungene Konsolidierung. Letztere werden nicht als natürliche Synäreseparameter gefittet.


## CCFSM v0.5 — explorativer Vergleich natürlicher Synäresekurven

- ccfsm_v05_calibration.py verwendet ausschließlich sieben primäre natürliche Näherungskurven aus LITERATURE/wilhelm_kind_approximate_measurement_points_curated.csv (Figures 8 und 10).
- DATA/Raw/kurvendigitalisierung.csv wird nur als Provenienz-Audit eingelesen: Die 21 Reihen enthalten Δp-Druckbedingungen und gehören zur erzwungenen Druckzell-Synärese; sie werden nicht zur natürlichen Kalibrierung verwendet.
- Verglichen werden exponentielle, gestreckt-exponentielle und zweistufige CCFSM-Antworten mit AICc, RMSE, chronologischem 80/20-Holdout und Residuen.
- CCFSM_v0.5_CALIBRATION_DE.md beschreibt den korrigierten Datenumfang und die Identifizierbarkeitsgrenzen.
- CCFSM_v0.5_FIRST_CI_RESULTS_2026-11-14_DE.md dokumentiert ausdrücklich die Rücknahme des ersten, falsch klassifizierten Laufs.
- test_ccfsm_v05_calibration.py prüft die Datenprovenienz, den Ausschluss von Druckzellkurven und die Fitfunktionen.

Die sieben natürlichen Kurven beruhen auf KI-gestützten ungeprüften Näherungsablesungen, nicht auf pixelkalibrierten Marker-Rohdaten. Die Ergebnisse bleiben explorativ; sie sind keine belastbare empirische Kalibrierung und keine physikalische Validierung.

- CCFSM_v0.5_CORRECTED_CI_RESULTS_2026-11-14_DE.md dokumentiert den korrigierten Lauf: 73/73 Tests, 7 natürliche Näherungskurven, 21 getrennt auditierte Druckzellkurven und die Identifizierbarkeitsgrenze des zweistufigen Fits.


## CCFSM v0.5 — zweiggetrennte Robustheitsanalyse (14.11.2026)

- `ccfsm_v05_branch_sensitivity.py` wertet alle 164 vorhandenen natürlichen Näherungsablesungen aus, getrennt nach primary, sensitivity-only und Figure-10b-Figure/Table-Konfliktzweig.
- `results_v0.5/wilhelm_kind_branch_sensitivity_2026-11-14.csv` enthält die getrennten Fits von Einzelexponential und gestrecktem Exponential samt AICc und Suchgrenzen.
- `CCFSM_v0.5_BRANCH_SENSITIVITY_2026-11-14_DE.md` ordnet die Ergebnisse den CCFSM-Aussagen und Identifizierbarkeitsgrenzen zu.
- Der CI-Workflow führt die Sensitivitätsanalyse jetzt zusätzlich aus und legt die CSV im Ergebnisartefakt ab.

Die 22 Sensitivitäts- und 44 Figure/Table-Konfliktpunkte bleiben getrennte Evidenzzweige; sie werden nicht in die primäre natürliche Kalibrierung eingemischt. Alle Kurvenwerte bleiben KI-gestützte, ungeprüfte Diagramm-Näherungsablesungen.
