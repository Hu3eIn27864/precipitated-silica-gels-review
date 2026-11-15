# CCFSM — konsolidierte Beweis-, Verifikations- und Publikationsroadmap

**Auditdatum:** 15.11.2026  
**Bezug:** Repository `main`; CCFSM-Entwicklungsstand bis P27.37 sowie analytische Modellstände v0.1–v0.4 und PDE-Referenzstände v1.0–v1.3.  
**Zweck:** Klare Trennung von Implementierung, Softwareverifikation, mathematischem Beweis, Zertifikat, empirischer Identifikation und unabhängiger physikalischer Validierung.

Diese Roadmap ist ein Arbeits- und Freigabeplan. Ein grüner CI-Lauf beweist weder die physikalische Gültigkeit einer Modellannahme noch einen mathematischen Satz.

## 1. Gesamturteil

Das Projekt besitzt inzwischen mehrere unterschiedlich weit entwickelte Ebenen, die nicht zu einem einzigen „CCFSM bewiesen“-Status zusammengezogen werden dürfen:

1. **Reduzierte natürliche-Synärese-Modelle v0.1/v0.2:** geschlossene Lösungen und bedingte mathematische Aussagen zu Existenz/Eindeutigkeit, Invarianz, Positivität, Monotonie, Langzeitgrenze und struktureller Nichtidentifizierbarkeit. Das sind die am klarsten abgrenzbaren analytischen Resultate.
2. **P0/P1-PDE-Referenzsystem v1.1–v1.3:** ein schwacher Existenz-/Eindeutigkeitsbeweis für eng definierte lineare bzw. zeitabhängig-koerzive Biot-Darcy-Referenzsysteme und eine beschränkte Netzwerkvariable. Diese Beweise gelten ausdrücklich nicht für das volle CCFSM.
3. **P22–P27 numerischer CCFSM-Zweig:** ein umfangreicher implementierter gekoppelter Prototyp mit partiellen Stoff-/Energieaudits, Referenzlösern, Projektions- und Intervallverfahren. Die Gesamtvalidierung und mehrere Beweisziele bleiben offen.
4. **P26 rationale Zertifikate:** exakte rationale Primär-/Dualbelege für ein eng begrenztes eindimensionales quadratisches Projektions-/Machbarkeitsproblem. Das ist ein echtes mathematisches Zertifikat, aber kein Beweis für die CCFSM-PDEs.
5. **Empirischer Status:** natürliche Syneresedaten aus Wilhelm & Kind (2015) sind verfügbar; ein Teil der Projektauswertung basiert auf diagramm-digitalisierten Näherungswerten. Unabhängige matched-state Messungen und Holdout-Validierung fehlen.

## 2. Claim–Evidence-Matrix

| Aussage / Modul | Implementiert | Software geprüft | Mathematisch bewiesen / zertifiziert | Empirisch validiert | Freigabe |
|---|---|---|---|---|---|
| v0.1 Einzelexponentialgesetz | Ja | Unit-Tests vorhanden | Exakte ODE-Lösung und elementare Schranken unter Konstantkoeffizientenannahmen | Effektive Literaturparameter berichtet; keine universelle Materialkonstante | Als reduzierte empirische Beschreibung verwendbar |
| v0.2 Zwei-Zeitskalen-ODE | Ja | 12/12 v0.2-Tests; historischer CI-Lauf 22/22 Pakettests | Exakte Lösung inkl. Gleichratenlimit; bedingte globale Existenz/Eindeutigkeit, Invarianz, Positivität, Monotonie, Grenzwert und Raten-Label-Symmetrie | Noch keine unabhängige Zweiraten-Identifikation am Zielmaterial | Kandidat für Manuskript 1 nach unabhängiger mathematischer Prüfung |
| v0.2 hydraulische Skalierung | Spezifiziert | Einheiten-/Regressionstests | Dimensionsanalyse und bedingte First-mode-Skalierung | Noch keine matched-state Längen-/Permeabilitätsvalidierung | Als falsifizierbare Hypothese, nicht als bestätigtes Gesetz |
| v0.3 Brücken/Morphologie/Eigenstress | Ja, Hypothesenschließung | Regressionstests | Teilresultate für definierte ODEs | Keine silica-spezifische Identifikation der Kopplungsfunktionen | Hypothesen klar markieren |
| v0.4 Chemie/Speziation | Module vorhanden | Teilweise CI-geprüft | Einzelne Bilanz-/Gleichgewichtseigenschaften, abhängig vom Modul | Keine validierte Modellierung konzentrierter Prozessbrühen | Nicht als validierte chemische Schließung präsentieren |
| v1.1–v1.2 P0 Biot-Darcy | Spezifiziert | Strukturtests | Schwacher Existenz-/Eindeutigkeitssatz unter expliziten Koerzivitäts-, Raum- und Randannahmen | Keine silica-spezifische Validierung | Separater mathematischer Referenzsatz |
| v1.3 P1 Brückenvariable | Spezifiziert/implementiert | Regressionstests | Bedingter schwacher Existenz-/Eindeutigkeitssatz für affine, gleichmäßig elliptische Mobilitätsinterpolation und festes Gleichgewicht | Mobilitätsgesetz ist Platzhalter, nicht gemessen | Nicht auf reales CCFSM verallgemeinern |
| P19 3D Biot-Eigenstrain-BVP | Implementiert | Unit-/Integrationsprüfungen | Kein allgemeiner Beweis der gesamten gekoppelten Diskretisierung | Keine reale Geometrie-/Materialvalidierung | Numerischer Baustein |
| P20–P22 Kopplung / impliziter Schritt | Implementiert | P22.1 behebt Fixpunktdefekt; CI dokumentiert | Kein allgemeiner Existenz-/Eindeutigkeitsbeweis für jeden diskreten Zeitschritt; Picard-Kontraktion nicht allgemein gezeigt | Nicht unabhängig validiert | Referenzfälle und Akzeptanzgrenzen ausbauen |
| P23 Stoff-/Energiebilanz | Teilweise | Audit vorhanden | Globale FV-Siliciumbilanz prüfbar; vollständiger diskreter Energieabschluss fehlt | Keine experimentelle Energiebilanz | Kritisches offenes Gate |
| P24 Newton-Referenz | Implementiert | begrenzte Vergleichstests | Numerischer Referenzlöser, kein mathematischer Lösungsbeweis | Keine physikalische Validierung | Robustheit weiter testen |
| P25 Verfeinerung | Implementiert | quantitative synthetische Referenzläufe vorhanden | Noch kein allgemeiner Konsistenz-/Stabilitäts-/Konvergenzbeweis | Keine Holdout-Validierung | Verfeinerungsstudie vervollständigen |
| P26.0–P26.18 Projektion | Weit entwickelt | mehrere dokumentierte CI-Läufe | Exakte rationale Zertifikate für bestimmte 1-D/quadratische Momenten- und Positivitätsprobleme; endliche Suche bleibt ggf. unresolved | Keine physikalische Validierung | Als eigenständige numerisch-mathematische Methode beschreibbar |
| P27.25–P27.37 Randarbeit/Ereignisse/Intervalle | Implementiert | CI-Status je Lauf einzeln prüfen; P27.37 jüngste Läufe nicht als grün behaupten, solange nicht verifiziert | Bedingte Aussagen bei gültigen Intervall-Einschließungen; P27.37 polynomialer Spezialfall, ungelöste Rand-/Tangentialwurzeln möglich | Keine physikalische Validierung | Kein Vollständigkeitsbeweis für beliebige Flüsse |
| P27 Parameteridentifizierbarkeit (ursprüngliches Gate) | Teilweise konzeptionell bearbeitet | Datenaudits vorhanden | Strukturidentifizierbarkeit einzelner reduzierter Modelle; umfassende praktische Identifizierbarkeit offen | Unsicherheiten/Datengruppen nicht vollständig analysiert | Eigenes Gate I-1 |
| P28 Holdout-Validierung | Plan vorhanden | Noch nicht freigegeben | Nicht anwendbar | Unabhängige, vorab definierte Holdouts fehlen | Offen |
| P29 Reproduzierbares Manuskriptpaket | In Vorbereitung | Clean-checkout-Gesamtlauf und Figurenpipeline offen | Claim-Evidence-Prüfung ausstehend | Datenprovenienz-/Rechteaudit offen | Offen |

**Wichtige Statusregel:** „Zertifiziert“ ist nur dort zu verwenden, wo ein explizit nachprüfbarer mathematischer Beleg vorliegt (z. B. rationale P26-Zeugen oder ein vollständig formulierter Satz mit geprüftem Beweis). Unit-Tests und Strukturtests sind keine mathematischen Beweise.

## 3. Neue, kollisionsfreie Roadmap-Gates

Die historischen Paketnummern P27.x bleiben erhalten. Die übergeordneten Forschungs-/Publikations-Gates erhalten ab jetzt eindeutige Bezeichnungen.

### Gate M — Manuskript 1: reduziertes Zwei-Zeitskalen-Modell

**Ziel:** Eine eigenständige, mathematisch saubere Arbeit über natürliche Synärese mit zwei dynamischen Zuständen.

Inhalt:
- präzise Modellannahmen und dimensionslose Form;
- vollständige Herleitung der exakten Lösung für (k_n\ne k_h) und (k_n=k_h);
- Invarianzregion, Positivität, Monotonie und asymptotischer Grenzwert;
- strukturelle Nichtidentifizierbarkeit der physischen Ratenlabels aus (S(t)) allein;
- exakte Rückgewinnung der ungeordneten Ratenkombinationen im idealen, rauschfreien Fall;
- Trennung struktureller und praktischer Identifizierbarkeit;
- hydraulische (L_d^{-2})-Skalierung als klar konditionierte First-mode-Hypothese;
- konkrete Mess-/Falsifikationsstrategie;
- Vergleich zum Einzelexponentialgesetz ohne überzogene Datenanpassung.

**Freigabe:** unabhängige mathematische Prüfung jeder Proposition, numerische Reproduktion aller Formeln, nachvollziehbare Literaturabgrenzung, menschlich geprüfter Manuskripttext und vollständige Offenlegung von Daten-/KI-Unterstützung.

### Gate E — diskreter Energieabschluss P23

1. Tatsächliche Energieänderung des akzeptierten Schritts bilanzieren.
2. Mechanische Randarbeit, Dirichlet-Reaktionen und Neumann-Traktionen mit konsistentem Vorzeichen erfassen.
3. Darcy-, Onsager- und Reaktionsanteile getrennt ausweisen.
4. Geschlossene und offene Referenzfälle testen.
5. Bilanzrest unabhängig berechnen; nicht per Konstruktion auf null setzen.

**Freigabe:** Stoffbilanz schließt bis Rundungsfehler; Energieabweichung ist unabhängig erklärt und zeigt erwartete Verfeinerung. Keine pauschale Energie-Monotonie ohne passende Annahmen.

### Gate N — numerische Stabilität und Konvergenz P24/P25

1. P22 und P24 auf identischen Referenzfällen vergleichen.
2. Raum- und Zeitverfeinerung getrennt untersuchen.
3. Beobachtete Ordnungen nur für hinreichend asymptotische Regime berichten.
4. Solverfehler, Abbruch, Positivitätsverletzungen und Sensitivität dokumentieren.
5. Beweisziele für Konsistenz, Stabilität und Konvergenz separat formulieren.

**Freigabe:** reproduzierbare quantitative Studie; allgemeiner Konvergenzsatz nur nach eigenständigem Beweis.

### Gate I — Parameteridentifizierbarkeit

1. Literaturberichtete Parameter, effektiv identifizierbare Kombinationen und nicht identifizierbare Größen trennen.
2. Diagramm-Digitalisierungsunsicherheit und Datenfamilienabhängigkeit erfassen.
3. Profil-Likelihood/Bootstrap nur bei geeigneter Datenqualität und Modellstruktur.
4. Natürliche Synärese und erzwungene Konsolidierung strikt getrennt halten.
5. Keine Rückrechnung von (K), (M), Diffusivität oder Brückenkinetik aus einem einzelnen Shrinkage-Zeitmaß.

**Freigabe:** Rang-/Unsicherheitsbericht; unidentifizierte Größen bleiben explizit unidentifiziert.

### Gate V — unabhängige Validierung

1. Holdout-Protokolle und Geometrien vor dem Fit festlegen.
2. Nicht zur Kalibrierung verwendete natürliche Syneresedaten verwenden.
3. Materialklassen und Zustände matched halten.
4. Abweichungen und Modellversagen vollständig berichten.

**Freigabe:** vorab definierte Kriterien erfüllt oder klare Falsifikation/Begrenzung.

### Gate P — mathematische PDE-Beweisroute

- **PDE-P0/P1:** bereits formulierte schwache Sätze gelten nur für die dokumentierten linearen/affin-koerziven Referenzschließungen.
- **PDE-P2:** chemische Reaktionen mit stöchiometrischer Erhaltung und dissipativer Affinität einführen.
- **PDE-P3:** beschränkte interne Variablen, Positivität und gleichmäßige Mobilitäts-/Elastizitätskoerzivität unter Rückkopplung beweisen.
- **PDE-P4:** natürliche Drainage-/Kapillarrandbedingungen, freie Oberfläche/Reservoir und Randenergien ergänzen.
- **PDE-P5:** Eigenkontraktion, finite Kinematik und nichtlineare Mechanik konsistent koppeln.
- Erst danach: Existenz, Eindeutigkeit (falls erreichbar), Energieabschätzung, Regularität und Grenzübergang für das vollständige System untersuchen.

**Freigabe:** kein „vollständiges CCFSM bewiesen“, bevor sämtliche im jeweiligen Satz enthaltenen Kopplungen und Randbedingungen tatsächlich erfasst sind.

### Gate R — reproduzierbare Veröffentlichung

- Clean checkout auf frischer Umgebung;
- reproduzierbare Tests, Datenaufbereitung, Fits und Figuren;
- vollständiges Quellen-/Lizenz-/Provenienzregister;
- Claim–Evidence-Matrix im Supplement;
- Autorenbeiträge, Affiliation, Finanzierung und KI-Einsatz korrekt;
- Journalrichtlinien unmittelbar vor Einreichung erneut prüfen.

## 4. Manuskriptstrategie

Die erste Arbeit wird bewusst auf v0.2 begrenzt. Sie behauptet weder den mathematischen Beweis des gesamten CCFSM noch eine experimentell identifizierte Zweiraten-Schließung.

**Arbeitsname:** *A two-timescale dynamical model for natural syneresis of precipitated silica gels: exact response, invariant-region analysis, and structural identifiability.*

Der v0.2-Ansatz ist die mathematische Hauptsache. v0.1 liefert die empirische Ein-Zeitskalen-Baseline. v0.3/v0.4, P19–P27 und die P26-Zertifikate werden nicht als vermeintliche Belege für v0.2 verwendet und nur im Ausblick eingeordnet, falls nötig.

Die vollständige Aufgabenliste, Journalprüfung und Manuskriptgliederung stehen in:
- [Manuskript 1 — Arbeitsplan und Einreichungsstrategie](MANUSCRIPT_01_TWO_TIMESCALE_SYNERESIS_PLAN_DE.md)
- [Claim–Evidence-Matrix](CCFSM_CLAIM_EVIDENCE_MATRIX_2026-11-15_DE.md)

## 5. Unmittelbare Ausführungsreihenfolge

1. v0.2-Formeln, Beweise und Grenzfälle unabhängig nachrechnen.
2. Neue Proposition zur idealen Parameter-Rückgewinnung sauber formulieren und beweisen; strukturelle von praktischer Identifizierbarkeit trennen.
3. Alle Abbildungen synthetisch und reproduzierbar erzeugen; keine Diagramm-Digitalisierung als Rohdaten darstellen.
4. Quellenkritik und Prior-Art-Abgrenzung vertiefen.
5. Manuskript auf Englisch schreiben und fachlich extern gegenlesen lassen.
6. Zieljournal anhand der tatsächlichen Manuskriptfassung und aktuellen Gebühren-/OA-Regeln final festlegen.
7. Erst nach Rechte-, Autorenschafts- und Reproduzierbarkeitsprüfung einreichen.

## 6. Nicht-Ziele und Stop-Regeln

- Kein Claim „vollständiges CCFSM mathematisch bewiesen“.
- Keine universelle Materialgesetz-Aussage aus einem reduzierten ODE-Modell.
- Keine getrennte Schätzung von (q_\infty) und (\eta_a) oder Zuordnung von (k_n,k_h) allein aus einer einzigen idealen (S(t))-Kurve.
- Keine Übernahme von Druckzell-/Oedometerparametern in natürliche Synerese.
- Keine Veröffentlichung KI-generierter Literaturangaben ohne menschliche Quellenprüfung.
- Keine Behauptung experimenteller Validierung aufgrund synthetischer Referenzfälle oder Diagramm-Näherungsablesungen.
- Kein Autorenschafts-/Affiliation-/Förderclaim ohne dokumentierte Grundlage.

## 7. Journalauswahl — vorläufig, nicht als Annahmeversprechen

**Primäre OA-Kandidatur: Electronic Journal of Differential Equations (EJDE).** Die offizielle Journalinformation nennt offene Einreichung zu ODE/PDE und Anwendungen, uneingeschränkten kostenlosen Lesezugang, CC BY 4.0 und keine Seiten-/Zugangsgebühren. Die Arbeit muss dafür jedoch echte, nichttriviale mathematische Ergebnisse für Differentialgleichungen liefern. Eine bloße Umbenennung zweier linearer ODEs in ein „CCFSM“ reicht nicht. Vor Einreichung ist zu prüfen, ob die mathematische Neuheit und Breite den Qualitätsanspruch des EJDE erfüllen.

**Fachlich-methodischer Alternativkandidat: Mathematics and Mechanics of Complex Systems (MEMOCS).** Der Scope verlangt rigorose mathematische Methoden mit Schwerpunkt Mechanik und passt thematisch zur Modellierung. Es erhebt keine Autorengebühren, ist aber ein Subskriptionsjournal; der reguläre Artikelzugang wird erst sechs Jahre nach Veröffentlichung frei. Es erfüllt daher nicht das Ziel sofortigen Diamond Open Access. Eine zulässige Preprint-/Repository-Strategie ist gesondert zu prüfen.

**Kein endgültiger Journalentscheid:** Die endgültige Wahl erfolgt erst, wenn der tatsächliche Manuskriptbeitrag, die Beweise und die Datenlage feststehen. Keine Annahmewahrscheinlichkeit oder Reputation wird garantiert.
