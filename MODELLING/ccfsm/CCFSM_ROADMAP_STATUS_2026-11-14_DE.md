# CCFSM — Statusaudit und priorisierte Roadmap

**Auditdatum:** 14.11.2026  
**Repository-Stand:** `main`, letzter geprüfter Commit `a5e8f066cb6a4e4ab700a3ace85763fa1f64dfb4`  
**Geltungsbereich:** CCFSM P0–P25.1, natürliche Synärese gefällter Silicagel-Systeme. Diese Roadmap ist ein Prüf- und Arbeitsplan, keine Behauptung physikalischer Validierung.

## 1. Kurzurteil

Der CCFSM-Prototyp hat sich von einer lokalen chemo-poroelastischen Schließung zu einer gekoppelten Kette aus Reaktionen, konservativem FV-Transport, räumlicher 3D-Biot-Mechanik, Druckrückkopplung und iteriertem Zeitschritt entwickelt. Die Architektur ist inzwischen mathematisch deutlich anspruchsvoller als ein reiner Kurvenfit.

Der aktuelle Engpass ist nicht das Hinzufügen weiterer physikalischer Terme, sondern die **Verifikation der tatsächlich gekoppelten diskreten Zeitschrittgleichungen** und danach die Identifizierbarkeit der Materialparameter.

### Gesicherter Softwarestand

- P0–P18: reduzierte/linearisierte Energie-, Reaktions-, Transport- und Variationsbausteine; P17 korrigiert die P9-Mechanik-Energie-Konsistenz für die dokumentierte 1D-Spezialisierung, P18 erweitert den Kern auf 3D.
- P19: quasistatischer räumlicher 3D-Biot-Eigenstrain-BVP-Assembler auf vom Aufrufer gelieferten FE-Quadraturdaten.
- P20: gestaffelte FV/FE-Kopplung.
- P21: FE-Druckprojektion zurück auf FV-Zellen und gemeinsamer Darcy-Fluss für Fluidbilanz und mobile M/O-Advektion.
- P22: gedämpfte Picard-Iteration für einen impliziten-Euler-Schritt.
- P23: diskreter Audit des akzeptierten P22-Schritts; globale FV-Siliciumbilanz plus getrennte P9-/P19-Energiediagnostik.
- P24: unabhängiger finite-difference Newton-Referenzlöser; P19 wird in jeder Residuumsauswertung neu gelöst.
- P25: Zeit-/Raumverfeinerungs- und Solverrobustheits-Harness implementiert; erster quantitativer Referenzlauf CI-grün (273 Tests), siehe CCFSM_v4.0_P25_RESULTS_DE.md.
- P25.1: konservative Cross-Mesh-Restriktion, netzunabhängige Anfangsprofile, L1/L2/Linf-Fehlernormen und erhöhter Druck-/Darcy-Gradient implementiert; CI #306 grün (278 Tests), quantitative Auswertung in `CCFSM_v4.1_P25_1_RESULTS_DE.md`.

GitHub Actions Lauf [#263](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43634688142) wurde geprüft: Job `ccfsm-tests` erfolgreich, 259 Unit-Tests bestanden. Im selben Lauf wurde die v0.5-Kalibrierung ausgeführt: 7 natürliche Kurven, 21 Fits; Exponentialmodell gewann 3/7, gestrecktes Exponentialmodell 4/7, zweistufiges CCFSM 0/7 und traf bei allen sieben Kurven eine Parametergrenze. Medianer Holdout-RMSE: 0.04207, 0.01755 bzw. 0.04207. Das ist ein begrenzter Vergleich auf approximierten/kuratierten Ablesepunkten, keine unabhängige physikalische Validierung. Der Druckzellen-Audit enthält 21 Druckzellkurven und 0 natürliche Kalibrierkurven; er dient der Trennung, nicht der Übernahme dieser Daten.

## 2. Historischer Auditbefund zu P22 (durch P22.1 behoben)

In `ccfsm_p22_iterated_implicit_coupling.py` wird das Zustandsresiduum aktuell aus dem **relaxierten Schritt** gebildet:

```python
state_residual = _relative_change(updated, current_flat)
```

Da `updated-current_flat = omega*(target-current_flat)` gilt, kann starke Unterrelaxation das gemeldete Residuum verkleinern, ohne den eigentlichen Fixpunktdefekt entsprechend zu reduzieren. Der Abbruchtest sollte stattdessen den unrelaxierten Defekt

[
r_{FP} = \frac{\|x^n+\Delta t F_{P21}(x^k)-x^k\|_\infty}
{\max(\epsilon,\|x^n+\Delta t F_{P21}(x^k)\|_\infty,\|x^k\|_\infty)}
]

oder eine äquivalente, sauber normierte Größe prüfen. Zusätzlich muss klar sein, dass der ausgegebene Druck-Snapshot zum akzeptierten Zustand gehört oder dessen Konsistenz explizit begrenzt wird.

Dies ist ein **Korrektur-/Verifikationspunkt**, kein Beleg für falsche bisherige Resultate. Die bestehenden vier P22-Tests prüfen den einfachen Konvergenzfall, Iterationslimit, ungültige Relaxation und Druckresiduum; ein Test auf Relaxationsunabhängigkeit des echten Fixpunktdefekts fehlt.

Weitere P22-Prüfpunkte:
- obere Schranke (\theta\leq1): derzeit Fehlerabbruch statt oberer admissibility-limited relaxation;
- Zeit-/Netzverfeinerung und Vergleich gegen eine unabhängige Lösung fehlen;
- die Picard-Konvergenz ist zustands- und zeitschrittabhängig; Unterrelaxation allein beweist keine Kontraktion;
- kein diskreter Gesamtenergie-Monotonienachweis.

## P22.1 completion update — 14 November 2026

P22.1 is implemented and its hosted CI is green.

- The state convergence criterion now measures the unrelaxed fixed-point defect \(x^n+\Delta t F_{P21}(x^k)-x^k\), not the damped update. Strong under-relaxation can no longer independently manufacture a small state residual.
- The accepted state is the current iterate for which the final P21 pressure snapshot was evaluated, so the returned pressure snapshot corresponds to the accepted iterate.
- The admissibility limiter constrains both strict positivity and the upper fluid-capacity bound \(\theta\leq1\), with a 5% safety margin when moving toward a bound.
- Regression coverage includes a deliberately tiny relaxation with a non-small fixed-point defect, the upper fluid-capacity bound, and accepted-state/pressure-snapshot consistency.
- Hosted workflow [#269](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43635230416) passed; the test log reports **262 tests in 0.708 s, OK**.
- This is a numerical acceptance-criterion correction, not a proof of Picard convergence, global energy stability, or physical validity.

**Gate A (P22.1) is complete. P23 is implemented as a partial accepted-step balance audit. P24 is now implemented:** an independent finite-difference Newton solver re-evaluates P19/P21 in every nonlinear residual and can be compared against P22 on identical data. Hosted CI status for P24 is pending verification. P25–P29 remain planned.

## 3. Priorisierte Roadmap und Freigabegates

### Gate A — P22.1: Fixpunktresiduum und Akzeptanzkriterien korrigieren

**Priorität: unmittelbar, vor jeder weiteren Modellphysik.**

1. Unrelaxierten Fixpunktdefekt unabhängig von der Relaxationszahl berechnen und als primäres Zustandskriterium verwenden.
2. Druckresiduum so definieren, dass es den Druck am akzeptierten/aktualisierten Zustand kontrolliert; gegebenenfalls nach dem letzten Update einen finalen P21-Snapshot berechnen.
3. Admissible relaxation für beide Grenzen (0<\theta\leq1) und positive Inventare implementieren oder die obere Schranke explizit und sicher als Abbruchbedingung behandeln.
4. Regressionstests: identischer Fixpunkt bei mehreren Relaxationswerten; kleine Relaxation darf nicht allein Konvergenz erzwingen; Druck-/Zustandskonsistenz; Grenzfälle bei \(\theta\to1\); Nichtkonvergenz ohne Zustandsannahme.
5. Dokumentation und CI-Logs aktualisieren.

**Freigabe:** P22 meldet nur dann Konvergenz, wenn unrelaxierter Fixpunktdefekt und Druckkonsistenz die Toleranzen erfüllen; Ergebnisse sind gegenüber vernünftigen Relaxationswerten konsistent.

### Gate B — P23: Diskrete Energie- und Siliziumbilanz des akzeptierten P22-Schritts

**Priorität: unmittelbar nach Gate A.**

- Bilanz der tatsächlich akzeptierten Zustandsänderung (E_h^{n+1}-E_h^n), nicht nur einer semidiskreten Energierate.
- Siliziuminventar (n_M+n_O+n_N+n_B) mit Reaktionsstöchiometrie, internen Flüssen und offenen Randflüssen getrennt auditieren.
- Mechanische Energiedifferenz und Dirichlet-Reaktionen/Randarbeit aus P19 berücksichtigen; Neumann-Traktionen und Reservoirarbeit mit konsistenten Vorzeichen erfassen.
- Darcy-, Onsager- und Reaktionsbeiträge als getrennte Dissipations-/Leistungsanteile ausweisen.
- Ein Bilanzresiduum berichten, nicht per Konstruktion auf null setzen. Bei offenen Systemen externe Arbeit/Materialleistung explizit bilanzieren.
- Geschlossene und offene Testfälle mit analytischen/konservativen Grenzfällen.

**Freigabe:** globale diskrete Stoffbilanz schließt bis zur Rundung; Energierest ist unabhängig berechnet, erklärbar und konvergiert mit Verfeinerung. Keine pauschale Energie-Monotonie behaupten, solange die Randarbeit/thermodynamische Struktur dies nicht trägt.

### Gate B — P23: diskrete Stoff-/Energiebilanz des akzeptierten P22-Schritts

**Status: implementiert als partieller Audit; vollständiger Energieabschluss noch offen.**

- P23 prüft die Änderung des gesamten FV-Siliciuminventars gegen den integrierten offenen M/O-Randfluss; Reaktionsstöchiometrie und interne Flüsse heben sich in der globalen Summe auf.
- P9-lokale FV-Energiedifferenz wird aus Anfangs- und akzeptiertem Zustand berechnet.
- P19-FE-Energie, Neumann-Traktionsarbeit und Dirichlet-Reaktionsresiduum werden am akzeptierten Zustand separat ausgegeben. Eine mechanische Energiedifferenz ist mangels P19-Anfangssnapshot noch nicht verfügbar.
- FE-Energie (J) und FV-Energie (J/m²) werden ohne dimensionsrichtige Geometrie-/Querschnittsabbildung nicht addiert.
- P16-semidiskrete Rate wird nicht als diskrete Energieänderung ausgegeben; kein globales Energieresiduum und keine Energie-Monotonie behauptet.
- Implementierung: `ccfsm_p23_discrete_balance.py`; Regressionen in `test_ccfsm_p23_discrete_balance.py`; Spezifikation: `CCFSM_v3.8_P23_DISCRETE_BALANCE_DE.md`.

**Freigabegrenze:** Die FV-Siliciumbilanz ist separat prüfbar. Der vollständige diskrete Energieabschluss bleibt ein offener Teil von Gate B.

### Gate C — P24: unabhängiger Newton-Referenzlöser für kleine gekoppelte Probleme

**Status: implementiert; hosted CI grün.** Workflows [#280](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43669701004) und [#283](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43669754294) sind erfolgreich; der aktuelle vollständige Testlog meldet **270 Tests bestanden**.

- `ccfsm_p24_newton_reference.py` löst (R(x)=x-x^n-\Delta t F_{P21}(x)=0) mit vorwärts-differenziertem Jacobian und gedämpftem Newton-Backtracking.
- Jede Residuumsauswertung löst P21 samt P19-Mechanik erneut; die FE-Freiheitsgrade werden durch den P19-Unterlöser statisch kondensiert.
- `p24_compare_with_p22` vergleicht FV-Zustand und projizierten Druck bei identischer Endzeit.
- Regressionen: Newton-Konvergenz/Admissibilität, P22-Vergleich, Nichtannahme bei Iterationslimit und Eingabeprüfung.
- Begrenzung: FD-Referenzsolver für kleine Netze, keine analytische Jacobimatrix, kein effizienter Produktionssolver und kein voll monolithischer FE-DOF-Newton.

**Freigabe:** Für den getesteten kleinen Referenzfall konvergieren P22 und P24 auf dieselbe diskrete Lösung innerhalb der Testtoleranzen. Zeit-/Raumverfeinerung und FD-Schrittweitenrobustheit bleiben Gate D/P25.

### Gate D — P25: Zeit- und Raumkonvergenz, Robustheit

- Zeitschrittfolge \(\Delta t,\Delta t/2,\Delta t/4\), räumliche FV-Verfeinerung und FE-Verfeinerung getrennt prüfen.
- Positivität, Stoffbilanz, Druckprojektion und Energieledger auf jeder Stufe berichten.
- Solver-Abbruch, Relaxationshistorie und Rechenkosten dokumentieren.
- Erst danach adaptive Zeitschrittsteuerung und ggf. adaptive Relaxation ergänzen.

**Implementierung und erster Lauf:** `ccfsm_p25_refinement_study.py`, Regressionen `test_ccfsm_p25_refinement_study.py`, Spezifikation `CCFSM_v4.0_P25_REFINEMENT_STUDY_DE.md`, Auswertung `CCFSM_v4.0_P25_RESULTS_DE.md`. CI [#295](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43670098385) erfolgreich; 273 Tests bestanden; Zeit-/Raum-/Robustheits-CSV und JSON-Artefakt hochgeladen.

- Zeitfolge T=10^-2 s, 1/2/4 Schritte: P22-Fehler gegen 4-Schritt-Referenz 1.547e-8, 5.150e-9, 0; P24 1.549e-8, 5.164e-9, 0. Trend ist mit Euler erster Ordnung vereinbar, formale Ordnungsfreigabe bleibt wegen nur zwei nichttrivialen Fehlerstufen offen.
- Raumfolge 1/2/4 Zellen: P22/P24 Zustandsabweichung höchstens 6.744e-12, Druckabweichung höchstens 6.664e-12; P23 relative Siliciumbilanzresiduen 8.85e-17 bis 3.28e-16.
- FD-Schritte 1e-4, 1e-6, 1e-8 konvergieren jeweils in 2 Newton-Iterationen; Residuum steigt von 2.84e-15 auf 4.72e-12 bei kleinerem FD-Schritt.
- Picard-Relaxation 0.2/0.5/1.0 benötigt 74/25/4 Iterationen; omega=1 ist in diesem Referenzfall am schnellsten, nicht allgemein als stabiler bewiesen.
- Der Raumvergleich ist Solverkonsistenz auf denselben Netzen, noch kein räumlicher Fehler gegen eine exakte/netzunabhängige Referenz. Alle Fälle synthetisch; keine physikalische Validierung.

**Freigabe:** Teilfreigabe für Softwareverifikation, Bilanzprüfung und Robustheit im Referenzfall. Beobachtete Konvergenzordnung und echte räumliche Konvergenz bleiben offen; keine scheinbare Konvergenz allein durch Relaxation oder grobe Diskretisierung.

### Gate D.1 — P25.1: konservative Cross-Mesh-Verfeinerung

- P25.1 vergleicht FV-Zellmittelwerte auf verschachtelten Netzen nach volumen-erhaltender Restriktion der Feinlösung auf das grobe Netz.
- Das Anfangsprofil ist als mesh-unabhängige kontinuierliche Referenz definiert; die Druckprojektion wird separat als nicht-konservierte Feldgröße verglichen.
- Zeitfolge 1/2/4/8/16 und Raumfolge 1/2/4/8; P23-Bilanz, P22/P24-Gleichnetzvergleich und Druck-/Darcy-Gradient werden separat ausgewiesen.
- Empirische Raten gegen die feinste numerische Referenz bleiben Diagnostik, kein mathematischer Konvergenzbeweis.

**Status:** Teilfreigabe nach CI-/Artefaktprüfung. Run [#306](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43670669824) erfolgreich; 278 Tests. Auf N=1/2/4 gegen N=8 sinken die relativen Zustands-L2-Fehler von 1.56e-7 auf 3.56e-8 und 9.70e-9; Druck-L2-Fehler von 1.35e-4 auf 2.91e-5 und 5.92e-6. Die ersten paarweisen Raumraten liegen bei ca. 1.9–2.3. P23-Siliciumbilanz in allen Fällen verifiziert; interner Druckgradient ab N=2 und Darcy-Fluss nachgewiesen. Siehe `CCFSM_v4.1_P25_1_RESULTS_DE.md`. Die Raten sind Diagnostik gegen eine numerische Referenz, kein Konvergenzbeweis.

### Gate E — P26: FE/FV-Abbildung und Geometrie

**Teilimplementierung abgeschlossen:**

- `ccfsm_p26_conservative_projection.py` projiziert Quellzellmittelwerte über exakte 1-D-Intervallüberlappungen auf nichtverschachtelte Zielnetze.
- FE-Quadraturwerte können mit positiven Gewichten zunächst zu Quellzellmitteln verdichtet werden.
- Konstanten- und Positivitätserhaltung sowie globale Integralerhaltung folgen aus nichtnegativen Überlappungslängen und identischer Gebietsabdeckung.
- Regressionen: `test_ccfsm_p26_conservative_projection.py`; CI führt zusätzlich einen reproduzierbaren CSV/JSON-Referenzlauf aus.

**Strikte Grenze:** Der Operator arbeitet mit stückweise konstanter Quellrekonstruktion in 1-D. Er ist keine allgemeine FE-Polynomprojektion und keine 2-D/3-D-Polyederintersection. Druck bleibt eine nicht-konservierte Feldgröße; ein Zielnetz-Druck für gekoppelte Mechanik erfordert eine erneute P19-Lösung. Zylindergeometrie und reale Abmessungen bleiben bis zu belastbaren Geometriedaten offen.

**P26.1-Erweiterung:** `ccfsm_p26_1_moment_projection.py` ergänzt eine stückweise lineare Minmod-Rekonstruktion und überträgt pro Zielzelle sowohl das nullte als auch das erste zentrierte Moment. Damit bleiben globale Masse und erstes räumliches Moment bei identischem Gebiet erhalten. Ein Positivitätsbegrenzer hält lineare Rekonstruktionen nichtnegativer Zellmittelwerte innerhalb der Zellränder nichtnegativ. Tests und separater CI-Referenzlauf sind ergänzt. Minmod kann nahe Extrema lokal Ordnung verlieren.

**Freigabe:** Teilfreigabe für den 1-D-Intervalloperator mit stückweise konstanter (P26) und linearer, momentenerhaltender (P26.1) Rekonstruktion nach grünem CI. Allgemeine 3-D-FE/FV-Konservativität, gekrümmte Geometrie und physikalische Validierung bleiben offen.

### Gate F — P27: Parameteridentifizierbarkeit und Datenmodell

- Parameter in drei Gruppen führen: direkt literaturberichtet, aus natürlichen Synäresekurven effektiv identifizierbar, nur mit unabhängigen Struktur-/Transportdaten identifizierbar.
- Natürliche Wilhelm-&-Kind-Kurven bleiben Kalibrierungszweig; Druckzellen/Oedometer bleiben separater erzwungener Konsolidierungszweig.
- Die sieben kuratierten natürlichen Kurven nicht als sieben unabhängige Materialreplikate behandeln, solange Forschungsfamilien-/Geometrieabhängigkeiten nicht geklärt sind.
- Profil-Likelihood/Bootstrap oder eine geeignete Unsicherheitsanalyse mit Digitisierungsunsicherheit und Datenfamilienstruktur ergänzen.
- \(K\), \(M\), Diffusivität, Brückenkinetik und Fraktalparameter nicht aus einem einzelnen Shrinkage-Zeitmaß rückwärts ableiten.

**Freigabe:** Rang/Unsicherheit der identifizierbaren Parameterkombinationen wird berichtet; nicht identifizierbare Größen bleiben als solche markiert.

### Gate G — P28: Externe/holdout Validierung

- Protokoll- und Geometrie-Holdouts vor dem Fit festlegen.
- Vorhersage gegen nicht zur Kalibrierung verwendete natürliche Syneresedaten prüfen.
- Getrennte Vergleiche mit unabhängigen Struktur- und Transportbeobachtungen nur bei übereinstimmender Materialklasse und passendem Zustand.
- Scherer/TEOS, reine kolloidale Kieselsäure, Oedometer und Filterkuchen bleiben Vergleichs-/Mechanismusdaten, keine stillschweigende Zielmaterialkalibrierung.

**Freigabe:** vorab definierte Vorhersagekriterien erfüllt oder Modellversagen transparent dokumentiert.

### Gate H — P29: Manuskript-/Reproduzierbarkeitspaket

- Modellgleichungen, Randbedingungen, Einheiten, Parameterregister und Datenprovenienz vollständig synchronisieren.
- Alle Abbildungen mit Roh-/abgeleiteten Datenstatus, Unsicherheiten und Fit-Holdout-Kennzeichnung versehen.
- Clean-checkout-Reproduktion der Tests, Kalibrierung und zentralen Figuren.
- Aussagen im Manuskript strikt nach mathematischem Beweis, numerischer Verifikation, empirischer Kalibrierung und unabhängiger physikalischer Validierung staffeln.

**Freigabe:** reproduzierbares Paket und vollständige Claim-Evidence-Matrix; Journal-Fit erst dann final entscheiden.

## 4. Parallel laufender Literatur-/Datenstrang

Dieser Strang kann parallel zu Gates A–E laufen, ohne unkalibrierte Materialgesetze in den Solver einzubauen:

1. Originalabbildungen von Wilhelm & Kind (2015) panelweise neu digitalisieren: Markerzentren, Achsenkalibrierung, Unsicherheit, Modellkurven und überlappende Spuren getrennt.
2. Abweichungen zwischen Artikel, Dissertation und Tabellen explizit erhalten; keine stille Harmonisierung.
3. Quarch (2010) und Schlomach & Kind (2004) als Alterungs-/Morphologie-/Prozesshistorienanker nutzen, nicht als quantitative natürliche Synerese-Kinetik.
4. Sahabi & Kind (2011) und Druckzell-/Oedometerwerte ausschließlich im erzwungenen Konsolidierungszweig führen.
5. Für direkte Zielmaterialparameter matched-state Paare aus Permeabilität und mechanischer Kompressibilität suchen; Filterkuchenwerte und freie Shrinkage-Zeitkonstanten nicht substituieren.

## 5. Empfohlene Ausführungsreihenfolge

| Reihenfolge | Paket | Abhängigkeit | Ergebnis |
|---|---|---|---|
| 1 | P22.1 Fixpunktresiduum korrigieren | keine | verlässliches Akzeptanzkriterium |
| 2 | P23 diskretes Stoff-/Energiebudget | P22.1 | FV-Siliciumbilanz geschlossen prüfbar; Energiebilanz partiell |
| 3 | P24 unabhängiger Newton-Referenzfall | P22.1 | FD-Newton-Referenz; P22/P24-Vergleich im kleinen Testfall, 270 Tests grün |
| 4 | P25 Raum-/Zeitverfeinerung | P23, P24 | numerische Robustheit |
| 5 | P26 konservative FE/FV-Projektion | P24, P25 | Netzübertragbarkeit |
| 6 | P27 Identifizierbarkeit | belastbare Solverbasis + Datenaudit | Parameterunsicherheiten |
| 7 | P28 Holdout-Validierung | P27 | Vorhersageprüfung |
| 8 | P29 Manuskriptpaket | P23–P28 | submission-orientierte Reproduzierbarkeit |

## 6. Explizite Stop-Regeln

- Keine weitere Modellkomplexität, solange P22.1 nicht behoben und P23/P24 nicht geprüft sind.
- Keine Permeabilitäts-/Modulkalibrierung aus \(S(t)\), \(A\) oder \(\tau\) allein.
- Keine Vermischung natürlicher Synärese mit Druckzell-, Zentrifugal- oder Oedometerkonsolidierung.
- Keine Übertragung von Kolloid-/TEOS-/Filterkuchenparametern als gemessene Parameter gefällter Silica-Nassgele.
- CI-Erfolg ist Softwareverifikation, nicht physikalische Validierung.
- Fehlende Daten werden als Datenlücke dokumentiert, nicht durch plausible Zahlen ersetzt.

## 7. P26.2 — quadratische Momentenprojektion

**Implementiert; CI-Lauf #357 erfolgreich (315/315 Tests).**

- ccfsm_p26_2_quadratic_projection.py überträgt stückweise quadratische Quellfelder auf nichtverschachtelte 1-D-Zielnetze.
- Pro Zielzelle werden die Momente nullter, erster und zweiter Ordnung projiziert; damit bleiben bei identischer Gebietsabdeckung die globalen rohen Momente ∫u dx, ∫xu dx und ∫x²u dx erhalten.
- Drei-Punkt-Gaußquadratur ist für die Polynomprodukte bis Grad vier exakt.
- Der optionale Positivitätsbegrenzer skaliert beide Moden gemeinsam und erhält den Mittelwert, kann aber lokale Ordnung/Form reduzieren.
- Regressionen prüfen quadratische Exaktheit, Momentenerhaltung, lokale Krümmung/Extrema, Positivität, Identität und Konstanten.
- Die Koeffizienten werden vorgegeben; eine automatische robuste quadratische FE/FV-Rekonstruktion ist nicht Teil dieses Pakets.

**Geltungsgrenze:** 1-D-Intervalle, synthetische Verifikation; keine 2-D/3-D-Intersection-Geometrie, keine Druck-/Energieerhaltung und keine physikalische Validierung. P19-Druck muss nach Netztransfer mechanisch neu gelöst werden.

## 8. P26.3 — Verfeinerungs-, Positivitäts- und Sensitivitätsstudie

**Implementiert; CI-Lauf #345 erfolgreich (306/306 Tests).**

- Vier Profiltypen (glatt, steile Front, lokale Extrema, nahezu Nullinventar), Quellnetze N=16/32/64/128 und nichtpassende gradierte Zielnetze.
- Relative L1/L2- und abgetastete L-infinity-Feldfehler, Minimum des Zielpolynoms, Residuen der drei globalen Momente sowie empirische Störungsverstärkung.
- Limiter an/aus wird getrennt verglichen. Der Quelllimiter garantiert keine Positivität des Zielpolynoms.
- Störungsverstärkung maximal 6.923 (empirischer Sensitivitätsindikator, keine Matrix-Konditionszahl); maximales relatives Momentenresiduum 6.45e-16.
- Bei N=128 relative L2-Fehler: glatt 5.68e-7, steile Front 4.41e-6, lokale Extrema 3.09e-5, nahezu Nullinventar 3.32e-5.
- Zielpolynom-Minimum ohne Limiter -6.81e-3, mit Quelllimiter -9.43e-11. Der Quelllimiter garantiert also keine strikt positive Zielrekonstruktion.
- Limiterbedingte relative Verschiebung des zweiten Moments maximal 6.36e-5 (lokale Extrema); Masse bleibt erhalten.

## 9. P26.4 — positivitätserhaltende Zielrekonstruktion

**Implementiert; CI-/Artefaktprüfung ausstehend.**

- Nach P26.2 werden die Zielzellmoden mit dem größtmöglichen gemeinsamen Faktor theta in [0,1] kontrahiert, so dass das quadratische Zielpolynom auf dem vollständigen Intervall nichtnegativ ist.
- Der Zielzellmittelwert bleibt exakt erhalten; dadurch bleiben jede Zellmasse und die globale Masse erhalten.
- Erstes und zweites räumliches Moment dürfen sich ändern; absolute und relative Abweichungen werden berichtet.
- Der Limiter ist eine radiale Modenkontraktion, kein globaler konvexer Projektionsoptimierer. Negative Zielmittelwerte werden abgewiesen.
- Regressionen umfassen Rand- und Scheitelpunkt-Unterschwinger, Nullmittelwerte, unveränderte positive Felder, Massenerhaltung und Momentenänderungen. Fünf synthetische Referenzfälle: zwei begrenzt, Zielminimum nach Begrenzung 0, maximale absolute Massenänderung 0; erste und zweite Momente änderten sich in den Stressfällen um bis zu ca. 1/6. Ergebnisartefakt: [P26.4 CI #357](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43673207806/artifacts/14145520449).

**Geltungsgrenze:** 1-D-Intervalle und quadratische Felder; keine 2-D/3-D-Geometrie, keine Druck-/Energieerhaltung und keine physikalische Validierung.

**P26.5 implementiert; CI-Lauf #374 erfolgreich (324/324 Tests).** Lokale gewichtete Nächstpunktprojektion der zwei höheren Moden unter kontinuierlicher Nichtnegativitätsbedingung bei festem Zellmittelwert. Der Solver projiziert auf die beiden Endpunkt-Halbräume und den elliptischen Innenminimum-Bogen; die Bogen-Zielfunktion wird eindimensional geklammert minimiert. Keine externe Optimierungsbibliothek. Erstes und zweites Moment werden gemessen, aber nicht global erzwungen. In fünf synthetischen Fällen sank die Summe der absoluten Änderungen des ersten Moments gegenüber P26.4 von 0.2328275 auf 0.2157950 und die des zweiten Moments von 0.2439617 auf 0.2215272; je Moment gab es in zwei von fünf Fällen eine Verbesserung. Massenänderung 0; Zielminimum 0. [CI-/Artefaktlauf #374](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43673736847). Details: CCFSM_v4.2.5_P26_5_OPTIMAL_POSITIVE_PROJECTION_DE.md.

**Nächster Schritt:** Ergebnisse gegen P26.4 prüfen. Bei Bedarf P26.6 als global gekoppeltes Optimierungsproblem mit expliziten Nebenbedingungen für erstes/zweites Moment formulieren. Den vollständigen P23-Energieabschluss separat weiterführen.


## P26.6 completion update — 15 November 2026

P26.6 implementiert die global gekoppelte Projektion mit Dykstras Algorithmus: feste Zellmittelwerte (damit Gesamtmasse), globale erste und zweite Momente sowie kontinuierliche Nichtnegativität jeder quadratischen Zielzelle. Die affine Projektion nutzt ein gewichtetes 2x2-Gram-System; die lokale Positivitätsprojektion delegiert an P26.5. Regressionen und CI-Studienlauf sind ergänzt. Nichtkonvergenz bleibt ein offenes Machbarkeitsresultat, kein Beweis der Unzulässigkeit. Nur 1-D/quadratisch; keine physikalische Validierung.


## P26.6.1 — feasibility diagnostics

Added a three-way feasibility classification: converged numerical feasible witness; exact single-cell infeasibility certificate from the unique moment-to-mode map; unresolved multi-cell nonconvergence. Generic multi-cell nonconvergence is not treated as proof of infeasibility. Regression coverage updated.


## P26.7 — dualer Machbarkeitstest

P26.7 ergänzt eine Supportfunktionsdiagnose: erreichbare globale Modenmomente bilden eine Minkowski-Summe zellweiser konvexer Positivitätsmengen. Ein gefundener positiver Trennungsabstand wird als numerischer dualer Zeuge ausgegeben. Gleitkommaarithmetik und endliche Winkel-/Randoptimierung bedeuten, dass noch kein formal intervallverifiziertes Unzulässigkeitszertifikat vorliegt. Kein Separator ist kein Machbarkeitsbeweis.


## P26.8 — verifizierte duale Unzulässigkeitszertifikate

P26.8 ersetzt die numerische Supportfunktionsdiagnose durch eine geschlossene Zell-Supportfunktion und rationale obere Schranken für Quadratwurzeln. Ein strikt positiver rationaler Abstand liefert ein unabhängig nachprüfbares Unzulässigkeitszertifikat für die exakt aus den Dezimalstrings gebildeten Eingabedaten. Ein endliches Richtungsraster kann bestehende Separatoren übersehen; fehlendes Zertifikat ist daher kein Machbarkeitsbeweis. Geltungsbereich: 1-D, feste Zellmittelwerte, quadratische Rekonstruktion.



## P26.9 — primal-duale Machbarkeitsentscheidung

P26.9 kombiniert P26.8 und P26.6 in einer dreistufigen Entscheidung. Ein strikt positiver rationaler dualer Abstand liefert certified_infeasible. Andernfalls wird eine primale Dykstra-Projektion versucht; der resultierende Dezimalzeuge wird unabhängig mit rationaler Arithmetik auf kontinuierliche Zellpositivität und explizit begrenzte globale Momentenresiduen geprüft. Nur dann gilt feasible_verified_primal_witness. Fehlschlag oder Nichtkonvergenz bleibt unresolved. Die primale Momentenerhaltung ist daher toleranzbehaftet und nicht pauschal ein exakter Gleichheitsbeweis. Geltungsbereich bleibt 1-D mit festen Zellmitteln und quadratischen Rekonstruktionen; keine physikalische Validierung.


## P26.10 — exakte rationale Momentenkorrektur

P26.10 ergänzt P26.9 um eine exakte rationale Nachkorrektur. Für einen numerischen Projektionskandidaten werden die Nicht-Pivot-Koeffizienten rationalisiert; zwei Koeffizienten einer Pivotzelle werden so bestimmt, dass globale Masse, erstes und zweites Moment exakt erfüllt sind. Kontinuierliche Zellpositivität wird danach exakt geprüft. Erfolgreiche Zeugen erfüllen somit alle drei Momente als rationale Gleichheiten. Eine endliche Suche über Rundungsgenauigkeiten und Pivotzellen kann jedoch vorhandene Zeugen übersehen; Fehlschlag bleibt unresolved und beweist keine Unzulässigkeit. Geltungsbereich: 1-D, feste Zellmittelwerte, quadratische Rekonstruktion; keine physikalische Validierung.


## P26.11 — allgemeine exakte Zwei-Koordinaten-Momentkorrektur

P26.11 verallgemeinert die P26.10-Pivotkorrektur von einer Pivotzelle auf beliebige zwei Koordinaten unter allen 2N linearen/quadratischen Zellmoden. Für jede ausgewählte Dezimalpräzision werden alle nichtsingulären Paare enumeriert; die beiden Pivotkoeffizienten werden durch rationale 2x2-Elimination exakt aus den globalen Erst-/Zweitmomentbedingungen bestimmt. Ein Kandidat wird nur akzeptiert, wenn Masse, erstes und zweites Moment exakt übereinstimmen und jedes quadratische Zellpolynom auf dem vollständigen Intervall exakt nichtnegativ ist. Die endliche Präzisionsliste ist kein vollständiger rationaler oder reeller Machbarkeitsalgorithmus; kein gefundener Zeuge bedeutet unresolved, nicht certified_infeasible. Geltungsbereich: 1-D, feste Zellmittelwerte, quadratische Rekonstruktionen; keine physikalische Validierung.


## P26.12 — exakte affine Parametrisierung des Momentenraums

P26.12 stellt den vollständigen affinen Lösungsraum der globalen Erst-/Zweitmomentbedingungen dar. Für N Zellen sind 2N Modenkoordinaten vorhanden; bei Rang zwei der Momentenmatrix werden zwei unabhängige Pivotkoordinaten exakt aus den verbleibenden 2N−2 freien Koordinaten rekonstruiert. Die affine Parametrisierung ist bijektiv und rational. Eine rationale Gittersuche im freien Raum liefert bei Erfolg exakte positive Primärzeugen, ist aber endlich und kein vollständiger Positivitäts-Machbarkeitsalgorithmus. Kein Treffer bleibt unresolved; Unzulässigkeit darf nur durch ein gültiges Dualzertifikat behauptet werden. Geltungsbereich: 1-D, feste Zellmittelwerte, quadratische Rekonstruktionen; keine physikalische Validierung.


## P26.13 — exakte Markov-Lukács-Zertifikate und konvexe Kegelformulierung

P26.13 stellt die kontinuierliche Nichtnegativität eines quadratischen Zellpolynoms auf \\([-1/2,1/2]\\) exakt als
\\[
u(x)=[1,x]Q[1,x]^T+\\lambda(1/4-x^2),\\quad Q\\succeq0,\\;\\lambda\\ge0
\\]
dar. Für 2x2-Matrizen wird PSD durch drei rationale Ungleichungen geprüft. Die optimale Intervallvariable \\(\\lambda\\) wird analytisch aus einer konkaven quadratischen Funktion gewählt; der resultierende Zellzeuge ist exakt rational. In Verbindung mit P26.12 entsteht eine endlichdimensionale konvexe SOCP-/2x2-PSD-Machbarkeitsformulierung. Implementiert ist die exakte Zertifikatskonstruktion und Kandidatenprüfung, **noch kein globaler SOCP-Optimierer**. Der CI-Lauf deckte in P26.12 einen tatsächlichen Präzisionsverlust auf: die Netzkanten wurden zur Validierung in Floats umgewandelt, bevor die exakte Parametrisierung sie übernahm. Die Implementierung validiert nun die Kantenfolge separat und behält anschließend die ursprünglichen rationalen Kanten exakt bei. Softwareprüfung läuft; keine physikalische Validierung.


## P26.14 — globaler konvexer Machbarkeitslöser (15. November 2026)

P26.14 verbindet die Dykstra-Projektion aus P26.6 mit der vollständigen affinen Momentenparametrisierung aus P26.12 und den exakten Markov-Lukács-Zellzertifikaten aus P26.13. Die numerische konvexe Projektion dient ausschließlich als Kandidatengenerator. Anschließend werden die freien Koordinaten rationalisiert, zwei Pivotkoordinaten exakt rekonstruiert und alle drei globalen Momente sowie die kontinuierliche Nichtnegativität jeder Zelle exakt geprüft. Nur ein vollständig geprüfter rationaler Zeuge erhält den Status `feasible_exact_primal_witness`. Nichtkonvergenz oder erfolglose endliche Nachsuche bleibt `unresolved`; P26.14 behauptet daraus keine Unzulässigkeit und erzeugt kein duales Zertifikat (P26.8/P26.9 bleiben dafür zuständig). Geltungsbereich: 1-D, feste nichtnegative Zellmittelwerte, quadratische Profile. Keine physikalische Validierung.


## P26.15 — globaler rationaler Primär-/Dualentscheid (15. November 2026)

P26.15 verbindet eine systematische Dualsuche mit P26.14. Primitive ganzzahlige Richtungen werden in wachsenden L-infinity-Schalen enumeriert; jeder Kandidat wird mit P26.8 und dessen rationalen Support-Obergrenzen unabhängig exakt geprüft. Ein strikt positiver rationaler Abstand ergibt `certified_infeasible`. Ohne Separator wird P26.14 ausgeführt; nur dessen exakt rationaler Primärzeuge mit globalen Momentengleichheiten und kontinuierlichen Markov-Lukács-Zellzertifikaten ergibt `feasible_exact_primal_witness`. Endliche erfolglose Dual-/Primärsuche bleibt `unresolved`. Die endliche Richtungsmenge ist kein vollständiger Unzulässigkeitsentscheid. Geltungsbereich: 1-D, feste nichtnegative Zellmittelwerte, quadratische Profile; keine physikalische Validierung.


## P26.16 — Stabilität und Vollständigkeit der dualen Suche (15. November 2026)

P26.16 prüft P26.15 über verschachtelte L-infinity-Richtungsradien und mehrere Genauigkeiten der rationalen Quadratwurzel-Obergrenze. Die Support-Obergrenze konvergiert monoton von oben; für eine feste Richtung nimmt die zertifizierte untere Trennungslücke daher monoton nicht ab. Der zusätzliche Support-Überhang ist durch (6\,10^{-d}\sum_jm_j) beschränkt.

Mathematisch ist die unendliche Enumeration primitiver ganzzahliger Richtungen vollständig für strikte Unzulässigkeit: Außerhalb der kompakten konvexen erreichbaren Momentenmenge existiert ein strikter Separator; wegen Stetigkeit bleibt er in einer offenen Richtungsumgebung gültig, die eine rationale und damit nach Skalierung eine primitive ganzzahlige Richtung enthält. Kein endlicher Radius garantiert jedoch, diese Richtung bereits zu erfassen. Kein Treffer bleibt daher ohne Machbarkeitsaussage.

Geltungsbereich: 1-D, feste nichtnegative Zellmittelwerte, quadratische Profile; rationale Zertifikate beziehen sich auf exakt rationalisierte Eingabedaten. Keine physikalische oder experimentelle Validierung.


## P26.17 — reproduzierbarer Zertifikatsbericht und unabhängige Prüfung (15. November 2026)

P26.17 ergänzt ein portables JSON-Format für exakte Primär- und Dualbelege. Der eigenständige Verifikator nutzt ausschließlich die Python-Standardbibliothek und Fraction-Arithmetik; er importiert keine P26.8/P26.13/P26.14/P26.15-Solver. Primärberichte werden anhand der drei globalen Momente und der Markov-Lukács-SOS-Identität einschließlich PSD-Bedingungen pro Zelle geprüft. Dualberichte werden durch erneute Supportfunktionsauswertung und strikt positive rationale Gap-Schranke geprüft. Ein SHA-256-Fingerabdruck schützt gegen unbeabsichtigte Berichtsmutationen, ist aber keine Signatur. Berichte ohne Beleg bleiben unresolved.

Geltungsbereich bleibt 1-D, feste nichtnegative Zellmittelwerte und quadratische Profile; Softwareverifikation ist keine physikalische Validierung.


## P26.18 — exakte Zertifikatsäquivalenz über rationale Darstellungen und Partitionen (15. November 2026)

P26.18 ergänzt P26.17 um einen unabhängigen Vergleich zweier Zertifikatsberichte anhand ihrer exakt rational berechneten globalen Momente (Masse, erstes und zweites Moment). Dezimal- und Bruchschreibweisen desselben rationalen Werts werden kanonisiert. Eine Einzellen- und eine Zweizellenpartition mit demselben konstanten positiven Profil werden verglichen; beide Primärzertifikate werden separat durch P26.17 geprüft. Ungültige Hashes/Belege, unterschiedliche Zielmomente und Statuskonflikte werden zurückgewiesen. Zwei unresolved-Berichte bleiben unresolved.

**Aussagegrenze:** Identische globale Momente beweisen weder identische lokale Profile noch identische stückweise-polynomiale zulässige Mengen auf unterschiedlichen Partitionen. Die Referenzstudie prüft die Vergleichslogik mit konstruierten exakten Zeugen, nicht einen neuen globalen Solver. Geltungsbereich: 1-D, feste nichtnegative Zellmittelwerte, quadratische Profile, globale Masse/erste/zweite Momente. Keine physikalische oder experimentelle Validierung.


## P26.19 — exakte lokale Profilrestriktion und Rückkoarsenierung (15. November 2026)

P26.19 geht über P26.18-Momentenäquivalenz hinaus. Für die normierte Zellquadratik (u(\xi)=m+a\xi+b(\xi^2-1/12)) werden Restriktionskoeffizienten auf jeder Kindzelle durch exakte rationale affine Koordinatentransformation berechnet. Die Rückkoarsenierung gewinnt die Elternkoeffizienten aus den exakten Kindmomenten zurück und restringiert anschließend erneut. Ein Round-trip gilt nur dann als exakt, wenn sämtliche Kindmittelwerte sowie linearen und quadratischen Koeffizienten übereinstimmen. Tests decken nichtuniforme Verfeinerung, mehrere Elternzellen, nicht geschachtelte Netze, lokale Abweichungen und globale Momentenerhaltung ab.

**Aussagegrenze:** Exakte Restriktion erhält das lokale Polynom punktweise. Beliebige Feinprofile müssen nicht aus einer Elternquadratik stammen; dann wird die lokale Gleichheitsprüfung negativ. Nur 1-D, stückweise quadratische Profile und geschachtelte Netze; keine allgemeine nichtpassende Projektion, keine 2-D/3-D- oder physikalische Validierung.

## P26.20 — Positivitätserhalt und unabhängige SOS-Zertifikatsprüfung (15. November 2026)

P26.20 verbindet die exakte Profilrestriktion aus P26.19 mit den lokalen Markov-Lukács-Zertifikaten aus P26.13. Da die Restriktion auf einer Kindzelle eine affine Koordinatentransformation desselben Elternpolynoms ist, bleibt dessen Nichtnegativität punktweise erhalten. Für strikt positive, randberührende und Nullprofile werden Kindzellenzertifikate erzeugt und anschließend von einem separaten P26.20-Verifikator mit exakter rationaler Arithmetik geprüft. Der Verifikator kontrolliert die Koeffizientenidentität, den nichtnegativen Multiplikator sowie Diagonaleinträge und Determinante der symmetrischen 2×2-Gram-Matrix; er importiert den P26.13-Konstruktor nicht.

**Korrektur aus dem P26.19-CI-Lauf:** Ein Regressionstest übergab zuvor die von P26.19 ausgegebenen rationalen Zeichenketten direkt an den P26.17-Momentenprüfer. Die Profilroutine war nicht betroffen; der Test wurde auf exakte Fraction-Konvertierung vor dem Momentenvergleich umgestellt und nutzt nun den P26.19-Momentenintegrator.

**Aussagegrenze:** Die Positivitätsaussage gilt für exakte geschachtelte 1-D-Restriktion desselben quadratischen Polynoms. Sie garantiert keine Positivität nach beliebiger nichtkonformer Projektion. Keine 2-D/3-D-Verallgemeinerung, keine physikalische oder experimentelle Validierung; kein globaler SOCP-Optimierer.


## P27 — Parallelpfad: Literaturvalidierung und 3-D-Positivität (15.11.2026)

### P27-V — Literaturbasierte physikalische Validierung

**Status: Prüfprotokoll angelegt; externe Zielsystemvalidierung weiterhin offen.**

- Neue Spezifikation: CCFSM_P27_PHYSICAL_VALIDATION_PROTOCOL_DE.md.
- L0–L4 trennen Quellenreproduktion, internen Cross-Protocol-Test, unabhängigen Mechanismenvergleich, unabhängige Zielsystemvalidierung und gekoppelte Mehr-Observablen-Validierung.
- Wilhelm-&-Kind-Zylinderwerte bleiben der primäre Quellenzweig; Tröpfchenwerte sind ein gesperrter Geometrie-/Temperatur-Holdout. Die Dissertation-Abweichung bleibt eigener Sensitivitätszweig.
- Scherer 1989 II ist als externer Mechanismenast priorisiert, aber wegen TEOS-/Alkoxid-System nicht mit gefällter Silica zu poolen. Volltext-/Kurvenextraktion steht aus.
- Der aktuelle v0.5-Befund (Exponential 3/7, gestreckt-exponentiell 4/7, zweistufiges CCFSM 0/7; alle zweistufigen Fits an Suchgrenzen) wird als Gegenbefund beibehalten.
- Status: L0 teilweise, L1 nicht ausgeführt, L2 qualitativ/bibliographisch vorbereitet, L3/L4 nicht erreicht.

### P27.1 — Exakte 3-D-Tetraedergeometrie und P1-Positivität

**Status: implementiert; CI-Prüfung ausstehend.**

- Exakte rationale Berechnung von sechsfacher Tetraedervolumina und Entartungstest.
- Für affine P1-Skalarfelder ist die Positivität auf einem Tetraeder äquivalent zu vier nichtnegativen Eckwerten, da die baryzentrischen Koordinaten nichtnegative konvexe Gewichte sind.
- Mesh-Prüfer akzeptiert nur dann, wenn jedes gelistete Element die lokale Prüfung besteht.
- Testfälle umfassen positive und randberührende Profile, negative nodale Werte, umgekehrte Orientierung, degenerierte Elemente, fehlerhafte Konnektivität und rationale Geometrie.

**Grenze:** Das ist eine exakte lokale 3-D-Aussage für P1-Skalarfelder. Keine P2-/höhergradige Positivität, keine Erhaltung im gekoppelten CCFSM-Zeitschritt, keine globale Netzkonformitätsgarantie und keine physikalische Validierung. P27.2 muss die Elementordnung und das für P19/P20 tatsächlich verwendete FE-Interpolationsschema adressieren; danach erst Transport-/Reaktions-Invariantenbereich und 3-D-Zeitschrittkopplung.


### P27.2 — Hinreichende P2-Bernstein-Positivität auf Tetraedern

**Status: implementiert; CI-Prüfung ausstehend.**

- Aus vier Eck- und sechs Kantenmittelpunktwerten werden zehn quadratische Simplex-Bernstein-Koeffizienten exakt rational rekonstruiert.
- Weil die Bernstein-Basisfunktionen nichtnegativ sind und eine Partition der Eins bilden, zertifizieren zehn nichtnegative Koeffizienten die punktweise Nichtnegativität.
- Ein bewusstes Gegenbeispiel \((\lambda_0-\lambda_1)^2\) zeigt: Ein nichtpositiver Bernstein-Koeffizient kann trotz nichtnegativem Polynom auftreten. Der Prüfer meldet dann „nicht zertifiziert“, niemals „negativ“.
- P27.2 ist ein hinreichender lokaler Zertifikatsbaustein, kein vollständiger P2-Positivitätstest.

**Nächster mathematischer Schritt:** adaptive Tetraeder-Subdivision und erneute Bernstein-Zertifizierung; danach Abgleich mit dem tatsächlichen Interpolationsschema und den Quadraturdaten des P19-Mechanikblocks. Erst danach kann ein diskreter Positivitätslimiter für die gekoppelten Transport-/Reaktionszustände entworfen werden.


### P27.3 — Adaptive P2-Bernstein-Zertifizierung auf Tetraedern

**Status: implementiert; CI-Prüfung ausstehend.**

- Exakte Unterteilung des Referenztetraeders in vier Eck- und vier zentrale Tetraeder, mit zentraler Oktaederdiagonale \(m_{01}\)--\(m_{23}\).
- Kindpolynome werden durch exakte Auswertung an Kind-Ecken und Kantenmittelpunkten rekonstruiert.
- Positivitätszertifikat nur dann, wenn jedes Blatt ausschließlich nichtnegative Bernstein-Koeffizienten besitzt.
- Ein exakt negativer Kindknotenwert liefert einen echten Negativitätszeugen. Negative Bernstein-Koeffizienten allein liefern niemals einen solchen Zeugen.
- Tests umfassen den positiven Fall \((\lambda_0-\lambda_1)^2+1/16\), dessen Ausgangs-Bernstein-Koeffizient negativ ist, die exakte Achtfach-Volumenaufteilung und einen negativen Punktzeugen.

**Grenze:** endliche Unterteilung ist ein hinreichendes Verfahren; nicht zertifizierte Fälle bleiben unentschieden. Keine globale Netzkonformität und keine gekoppelte 3-D-Zeitschrittgarantie.

### P27-V — Figure-9-Porenfluid-Audit

**Status: Quellen-Audit erstellt; quantitative Digitalisierung gesperrt.**

- `LITERATURE/wilhelm_kind_fig9_pore_liquid_audit.csv` trennt Artikeltext, visuelle Auffälligkeiten und Messstatus.
- Der Text nennt für saure Gele 0.2–0.4 mmol/L, die Grafik zeigt aber visuell auffällige 60-°C-Punkte nahe 0.8 und 0.6 mmol/L; pixelgenaue Nachprüfung erforderlich.
- Der bei ungefähr 1000 mmol/L eingezeichnete Anfangswert ist berechnet und darf nicht als Messpunkt gefittet werden.
- Die Spektroskopie erfolgte bei ungefähr 20 °C, auch bei warmen Gelversuchen; mögliche Nachpolymerisation nach Probenahme ist ein expliziter Messmodellfehlerpfad.
- Figure 9 ist eine zusätzliche Observable im Zielsystem, aber keine unabhängige Laborreplikation.

**Nächster Schritt:** hochauflösende Pixel-Digitalisierung mit Unsicherheitsintervallen und Prüfung der Fehlerbalken-/Probenahmedefinition; erst dann ein eigener chemischer Holdout.


## P27.4 — unabhängige Verifikation und Figure-9-Ablese-Audit (15.11.2026)

**P27.4 implementiert:** Ein separates Modul ohne Import des P27.3-Konstruktors/P27.2-Umrechners rekonstruiert die exakten lokalen Bernstein-Koeffizienten, prüft vollständige Blattpfade, Mutationsfälle und exakte Negativpunktzeugen. Die P27.3-Ausgabe enthält dazu Blattdatensätze. Die neue Prüfschicht bestätigt nur das vorgelegte Zertifikat; sie macht aus dem hinreichenden Bernstein-Kriterium keinen vollständigen Positivitätstest.

**Figure 9:** 39 Markerzentren wurden als manuelle, grobe Arbeitsablesung in `LITERATURE/wilhelm_kind_fig9_digitized_approx_2026-11-15.csv` erfasst. Markerableseunsicherheit ist ausgewiesen; publizierte Fehlerbalken wurden nicht separat digitalisiert. Die hoch liegenden sauren 60-°C-Marker bleiben erhalten. Alle Punkte sind weiterhin für quantitative Fits gesperrt, bis eine pixelkalibrierte Zweitablesung und das chemische Beobachtungsmodell vorliegen.

**Freigabegrenze:** P27.4 ist Software-Verifikation, nicht physikalische Validierung. Figure 9 ist ein zusätzlicher Observable-Zweig innerhalb derselben Studie, keine unabhängige Replikation.


## P27.5 — Mesh-Konformität (15.11.2026)

Ein exakter rationaler Audit-Prüfer rekonstruiert die auf gemeinsamen groben Tetraederflächen induzierten Dreieckszerlegungen aus den P27.3-Blattpartitionen. Übereinstimmung beider Seiten wird als konform ausgewiesen; abweichende Triangulierungen werden als nichtkonform erkannt. Tests decken unverfeinerte, beidseitig gleich verfeinerte und einseitig verfeinerte Flächen sowie nicht-manifold und fehlerhafte Eingaben ab. Der Prüfer erzeugt noch keine konforme Verfeinerung und prüft nicht die vollständige globale Knoten-/Kantenstruktur.


## P27.6 — konservativer Verfeinerungstiefen-Abschluss (15.11.2026)

**Status: implementiert; CI-Prüfung ausstehend.** Der neue Tiefenabschluss baut die Face-Nachbarschaft der groben Tetraeder auf und hebt alle Elemente einer face-zusammenhängenden Komponente auf deren maximale angeforderte P27.3-Verfeinerungstiefe. Damit werden unterschiedliche Tiefen auf gemeinsamen groben Flächen konservativ vermieden. Die Regel kann eine ganze Komponente uniform verfeinern und ist ausdrücklich nicht minimal. Ressourcenlimits liefern unresolved ohne partielle Meshänderung. P27.6 erzeugt selbst keine Kind-Tetraeder; nach realer Subdivision bleibt der exakte P27.5-Audit verpflichtend. Keine Aussage über globale Knoten-/Kantenkonformität, Elementqualität oder physikalische CCFSM-Positivität.


## P27.7 — tatsächliche konforme rote Tetraederverfeinerung (15.11.2026)

**Status: implementiert; CI-Prüfung ausstehend.** P27.7 wendet P27.6-Tiefenabschluss an, erzeugt die Achtfach-Unterteilung rekursiv mit exakten rationalen Koordinaten und dedupliziert globale Knoten. Der P27.5-Audit prüft die induzierten Dreieckszerlegungen auf jeder gemeinsamen groben Fläche; nur bei `conforming` wird ein erfolgreiches Netzobjekt zurückgegeben. Ressourcenabbruch und fehlgeschlagene Prüfungen liefern keinen Erfolg. Keine Garantie für globale Kanten-/Knotenmannigfaltigkeit, Elementqualität, Orientierungsnormalisierung oder CCFSM-Positivität.

## Figure 9 — zweite visuelle Ableserunde (15.11.2026)

Die Original-PNG wurde über die Artikelabbildung erneut geöffnet. Eine zweite visuelle CSV enthält Zeitablesung und grobe visuelle Fehlerbalken-Unter-/Obergrenzen für alle 39 Marker. Ein früher saurer 60-°C-Marker wurde dabei zeitlich auf ungefähr 22 h statt 7 h eingeordnet; der hohe Konzentrationswert bleibt erhalten. Es ist ausdrücklich keine maschinelle Pixelkalibrierung. Die zweite CSV ist ein visueller Prüfdatensatz; beide CSV-Dateien bleiben für Fits gesperrt. Die Assay-Observable wird wegen fehlender Reaktionszeit-/Selektivitätsangaben nicht ungeprüft mit monomerem (c_M) gleichgesetzt.


## P27.8 — exakte Orientierung und Elementformqualität (15.11.2026)

**Status: implementiert; CI-Prüfung ausstehend.** Der Geometrie-Audit berechnet das signierte sechsfache Volumen jedes Tetraeders exakt rational. Negative Orientierung wird durch Vertauschung zweier lokaler Knoten normalisiert; degenerierte Elemente werden abgewiesen. Als dimensionsloser skaleninvarianter Formindikator wird Q=432 D²/S³ verwendet, wobei D das orientierte Determinantenvolumen und S die Summe der sechs quadrierten Kantenlängen ist. Ein optionaler rationaler Mindestwert wirkt als harte Netzfreigabeschwelle; bei Unterschreitung wird kein Mesh ausgegeben.

**Grenze:** Der Indikator misst Formverzerrung, ist aber kein vollständiges FE-Konditionierungszertifikat. P27.8 beweist weder globale Knoten-/Kantenmannigfaltigkeit noch CCFSM-Zustandspositivität oder physikalische Validität.
