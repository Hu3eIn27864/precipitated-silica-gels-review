# CCFSM — Statusaudit und priorisierte Roadmap

**Auditdatum:** 14.11.2026  
**Repository-Stand:** `main`, letzter geprüfter Commit `a5e8f066cb6a4e4ab700a3ace85763fa1f64dfb4`  
**Geltungsbereich:** CCFSM P0–P25, natürliche Synärese gefällter Silicagel-Systeme. Diese Roadmap ist ein Prüf- und Arbeitsplan, keine Behauptung physikalischer Validierung.

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

### Gate E — P26: FE/FV-Abbildung und Geometrie

- Die derzeitige quadraturgewichtete Zellmittelung ist nur für die explizit zugeordneten Quadraturpunkte abgesichert.
- Für nicht deckungsgleiche Netze eine konservative Projektion mit Erhaltungsnachweis implementieren.
- Zylindergeometrie, radiale/axiale Randbedingungen und physikalische Abmessungen erst mit nachvollziehbaren Geometriedaten spezifizieren.
- Netzabhängigkeit der Projektion und Randreaktionen untersuchen.

**Freigabe:** Projektion erhält die relevanten Integrale und ist unter Netzverfeinerung konsistent. Bis dahin keine allgemeine FE→FV-Konservativität behaupten.

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

## 7. Nächster konkreter Arbeitsschritt

**P25 als Nächstes:** Zeit- und Raumverfeinerung getrennt durchführen, zuerst am kleinen P22/P24-Referenzfall. Newton-FD-Schrittweite, Solverfehler, Positivität und Stoffbilanz über die Verfeinerungsfolge protokollieren. Den offenen vollständigen P23-Energieabschluss als Teil des Folgeaudits beibehalten.
