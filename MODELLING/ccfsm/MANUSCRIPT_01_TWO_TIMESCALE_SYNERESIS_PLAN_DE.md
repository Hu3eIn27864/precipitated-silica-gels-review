# Manuskript 1 — Zwei-Zeitskalen-Modell der natürlichen Synärese

**Arbeitsstand:** 15.11.2026  
**Status:** Konzept und Einreichungsstrategie festgelegt; Manuskript noch nicht einreichungsfertig.  
**Repository-Basis:** CCFSM v0.2 und die zugehörige Implementierung/Tests.  
**Primärziel:** eine eng abgegrenzte mathematisch-modellierende Arbeit, nicht die Veröffentlichung des gesamten CCFSM.

## 14. Neuheits- und physikalischer Modell-Audit — wichtige Einschränkung

Die erste Literaturprüfung ist in [MANUSCRIPT_01_NOVELTY_AND_PHYSICAL_MODEL_AUDIT_2026-11-15_DE.md](MANUSCRIPT_01_NOVELTY_AND_PHYSICAL_MODEL_AUDIT_2026-11-15_DE.md) dokumentiert. Scherer (1989) hat die Kopplung von viskoelastischer Netzwerkmechanik und Porenflüssigkeitstransport für Silica-Synerese bereits mechanistisch behandelt; Wilhelm & Kind haben natürliche Synärese gefällter Silica empirisch modelliert; die Ratenvertauschung in linearen Zwei-Kompartiment-Systemen ist klassische Identifizierbarkeitstheorie.

Daher ist die Zwei-Zustands-ODE derzeit als **phänomenologische, testbare reduzierte Schließung** zu bezeichnen, nicht als erstmalige physikalische Trennung der Prozesse oder als aus Biot-Darcy hergeleitetes Silica-Gesetz. Die ODE ist mathematisch konsistent unter ihren Annahmen; ihre physikalische Gültigkeit, Erhaltungsbilanz und Reduktion aus einem etablierten Feldmodell sind noch zu prüfen. EJDE wird bis dahin nicht als realistisches Ziel für die ODE allein behandelt.

## 15. Prior-Art-Korrektur: Wilhelm & Kind 2015

Die 2015er Arbeit von Wilhelm & Kind verwendet für natürliche Synärese ebenfalls eine empirische Einratenform \\(S(t)=S_{max}[1-\\exp(-t/\\tau)]\\), untersucht aber pH, Temperatur und Probengröße. Sie erklärt diese Gleichung als empirischen Ansatz und hält ein physikalisch basiertes Modell für noch ausstehend. Dies ist eine mögliche Anwendungslücke, aber kein Beleg dafür, dass es keine frühere physikalische Syneresetheorie gibt: Scherer (1989) hat bereits eine poro-viskoelastische Theorie samt experimenteller Anwendung auf Silica-Gele publiziert. Die zentrale Aufgabe ist nun der Gleichungs-/Grenzfallvergleich zwischen Scherer und v0.2, nicht die bloße Gegenüberstellung mit der empirischen Einratenkurve.

## 1. Arbeitstitel

**A two-timescale dynamical model for natural syneresis of precipitated silica gels: exact response, invariant-region analysis, and structural identifiability**

Alternativ, etwas zurückhaltender:

**Separating network contraction and hydraulic relaxation in natural syneresis: a reduced two-state model**

## 2. Zentraler wissenschaftlicher Beitrag

Das Modell trennt zwei Prozesse, die eine einzelne beobachtete Schrumpfkurve sonst zu einer scheinbaren Zeitkonstante zusammenfasst:

\[
\dot q=k_n(q_\infty-q),\qquad
\dot S=k_h(\eta_a q-S).
\]

(q) ist das intrinsische Netzwerk-Kontraktionspotential, (S) die beobachtete makroskopische Volumenschrumpfung, (k_n) die effektive Netzwerkbildungs-/Kontraktionsrate, (k_h) die effektive hydraulisch-poroelastische Relaxationsrate und (\eta_a) die effektive natürliche Grenzflächenzugänglichkeit.

**Kernbeitrag:** exakte Antwort einschließlich des Gleichratenlimits, zulässiger Zustandsbereich und Monotonie, strukturelle Symmetrie der beiden Ratenlabels aus einer einzelnen Nullstart-S(t)-Kurve, und ein Versuchsdesign, das die beiden Prozesse mit unabhängigen Observablen trennen kann.

Das ist eine reduzierte, falsifizierbare Modellhypothese. Es ist kein Nachweis, dass jedes gefällte Silicagel exakt dieser ODE folgt.

## 3. Klare Forschungsfragen

1. Welche geschlossene Lösung ergibt sich für beliebige zulässige Anfangszustände und für gleiche bzw. ungleiche Raten?
2. Unter welchen Anfangsdaten bleibt der Zustandsbereich invariant und die beobachtete Schrumpfung monoton?
3. Welche Parameterkombinationen sind aus einer idealen Nullstart-S(t)-Kurve strukturell identifizierbar?
4. Welche unabhängigen Messungen sind minimal erforderlich, um (k_n), (k_h), (q_\infty) und (\eta_a) physikalisch zuzuordnen?
5. Unter welchen klar benannten Annahmen folgt die (L_d^{-2})-Skalierung des hydraulischen Zeitmaßes?

## 4. Geplanter Satzapparat

Die vorhandenen v0.2-Propositionen werden unabhängig nachgerechnet und in publikationsreifer Form neu formuliert.

- **Theorem 1 — globale Existenz und Eindeutigkeit:** affine global Lipschitz ODE, explizite globale Lösung.
- **Theorem 2 — Invarianz und Monotonie:** für (0\le S_0\le\eta_aq_0\le\eta_aq_\infty<1) gilt (0\le S_0\le S(t)\le\eta_aq(t)\le\eta_aq_\infty<1), (\dot S\ge0) und (S(t)\to\eta_aq_\infty).
- **Theorem 3 — strukturelle Nichtidentifizierbarkeit:** die Nullstart-Transferfunktion ist invariant unter (k_n\leftrightarrow k_h); nur das ungeordnete Ratenpaar und das Endpunktprodukt sind aus idealem S(t) identifizierbar.
- **Proposition 4 — Parameter-Rückgewinnung:** präzise notwendige/ausreichende Bedingungen, unter denen die zwei positiven Raten aus idealen noisefreien Kurvendaten als ungeordnetes Paar rekonstruierbar sind. Diese Aussage muss noch formal bewiesen und auf Sonderfälle (gleiche Raten, verschwindende Amplitude, endliches Beobachtungsfenster) geprüft werden.
- **Proposition 5 — hydraulische Längenskalierung:** (k_h\propto L_d^{-2}) nur für die spezifizierte homogene gesättigte lineare First-mode-Reduktion mit konstantem (C_g,\kappa_{eff},K_{eff},\mu). Nicht als universelles Gesetz formulieren.

**Zusätzliche Pflichtprüfung:** Die Gleichratenlösung muss als stetiger Grenzwert der ungleichen Ratenformel gezeigt werden; Einheiten und Zeitursprung werden vollständig geprüft. Die Monotonieaussage gilt nur unter den genannten geordneten Anfangsdaten.

## 5. Empfohlene Gliederung

1. Introduction: natürliche vs. erzwungene Synerese; Lücke zwischen Netzwerk-Kontraktion und Drainage.
2. Scope and relation to prior models: Wilhelm & Kind (2015), Scherer (1989), Wu et al. (2020) als jeweils klar abgegrenzte Vergleichssysteme.
3. Model definition and assumptions: Variablen, Einheiten, Zeitursprung, Anfangsdaten.
4. Exact solution: allgemeine Anfangsdaten, ungleiche und gleiche Raten, Nullstart-Spezialfall.
5. Mathematical analysis: Existenz/Eindeutigkeit, Invarianz, Positivität, Monotonie, Grenzwert, Raten-Label-Symmetrie.
6. Identifiability and experimental design: identifizierbare Kombinationen, zusätzliche Messungen, Längenvariation.
7. Relation to the one-timescale empirical law: Grenzfälle (k_n\gg k_h) und (k_h\gg k_n).
8. Limitations and falsifiable predictions.
9. Conclusions.

## 6. Was ausdrücklich NICHT in Manuskript 1 gehört

- Vollständige P19–P27-3D-FE/FV-Implementierung;
- Behauptung eines Existenzsatzes für das vollständige gekoppelte CCFSM;
- P26-Projektionszertifikate als vermeintlicher Beweis der Synerese-ODE;
- P0/P1-PDE-Sätze, außer höchstens einem kurzen Ausblick, weil sie ein anderes Referenzsystem behandeln;
- ungeprüfte KI-Digitalisate als inferenzstatistische Datenbasis;
- Fits der zwei neuen Raten aus einer einzigen Shrinkagekurve ohne zusätzliche Observablen;
- Oedometer-, Druckzellen- oder erzwungene Konsolidierungsdaten als natürliche Synerese.

## 7. Daten- und Abbildungsstrategie

Die Arbeit ist zunächst eine mathematisch-modellierende Arbeit mit Literaturmotivation, keine neue experimentelle Validierungsarbeit.

Vorgesehene Figuren:
1. Zustandsdiagramm (q\to S) mit Netzwerk- und hydraulischem Zeitskalenpfad.
2. Exakte Modellantworten für (k_n<k_h), (k_n=k_h), (k_n>k_h), dimensionslos und mit gleichen Endwerten.
3. Invarianzregion im ((q,S))-Zustandsraum.
4. Vertauschung der Ratenlabels: identische S(t)-Kurve für ((k_n,k_h)) und ((k_h,k_n)).
5. Hydraulische Skalierung (k_h\sim L_d^{-2}), klar als Modellvorhersage, nicht Messfit.

Alle Figuren aus offen dokumentierten Gleichungen und synthetischen Parameterwerten generieren. Synthetische Werte ausdrücklich als Illustration kennzeichnen. Literaturwerte aus Wilhelm & Kind nur als Kontexttabelle mit Originaleinheiten, Geometrie, Temperatur und Quellenprovenienz verwenden; Konfliktwerte aus Dissertation und Journalartikel getrennt halten.

## 8. Journalentscheidung — vorläufige Rangfolge

### 1. Electronic Journal of Differential Equations (EJDE) — primärer Diamond-OA-Kandidat, bedingt

Offizielle Journalinformation: ODE/PDE und Anwendungen sind im Scope; freie Lektüre, CC BY 4.0, keine Seiten- oder Zugangsgebühren. Die Indexierung umfasst laut Journal Math Reviews, zbMATH und Web of Knowledge. Ein aktueller DOAJ-Datensatz bestätigt keine APCs.

**Bedingung:** Das Manuskript muss mathematisch deutlich über eine elementare lineare Zwei-Zustands-ODE hinausgehen. Die strukturelle Identifizierbarkeitsanalyse, inverse Parameterrekonstruktion, scharfe Anfangsdatenbedingungen und eine nichttriviale Verallgemeinerung müssen rigoros ausgearbeitet sein. Wenn das Ergebnis zu anwendungsorientiert oder mathematisch zu elementar bleibt, ist EJDE kein guter Fit.

Offizielle Seiten:
- https://ejde.math.txstate.edu/indexright.html
- https://ejde.math.txstate.edu/
- https://doaj.org/toc/1072-6691

### 2. Mathematics and Mechanics of Complex Systems (MEMOCS) — starker fachlicher Fallback, nicht Diamond OA

Der Scope fordert rigorose mathematische Methoden und betont Mechanik; das passt zur mechanistisch-hydraulischen Modellierung. Das Journal ist in MathSciNet, zbMATH, Scopus und Web of Science gelistet. Es erhebt keine Autorengebühren, ist jedoch subskriptionsbasiert; der Artikel wird regulär erst sechs Jahre nach Veröffentlichung frei zugänglich. Daher kein unmittelbarer Diamond-OA-Kanal.

Offizielle Seiten:
- https://msp.org/memocs/about/journal/about.html
- https://msp.org/memocs/about/journal/submissions.html

### 3. Weitere angewandte Mathematik-/Kolloid-/Materialjournale

Erst nach Manuskriptfertigstellung erneut prüfen. Bei Hybrid-/Subskriptionsjournalen kann eine kostenfreie traditionelle Publikation möglich sein, aber sie ist nicht sofort Open Access. Eine Green-OA-Preprint-Version ist nur im Rahmen der dann aktuellen Journalrichtlinien zu nutzen.

**Entscheidung:** EJDE ist unser vorläufiges Ziel, nicht eine Zusage der Annahme. Nach einem vollständigen Manuskript und externer mathematischer Begutachtung wird ein Scope-Check vorgenommen; bei zu geringer mathematischer Neuheit wechseln wir zu einem besser passenden Modellierungsjournal.

## 9. Schritt-für-Schritt-Arbeitsliste

### Phase 1 — mathematische Verifikation
- [ ] Jede Formel aus v0.2 unabhängig nachrechnen.
- [ ] Gleichratenlimit symbolisch und numerisch prüfen.
- [ ] Invarianz-/Monotoniebeweis Zeile für Zeile prüfen.
- [ ] Transferfunktion und Raten-Symmetrie prüfen.
- [ ] Identifizierbare Koeffizientenkombinationen vollständig charakterisieren.
- [ ] Endliches Beobachtungsfenster, Rauschen, gleiche Raten und Amplitudengrenzen analysieren.
- [ ] Unabhängige fachmathematische Prüfung organisieren.

### Phase 2 — Literatur und Neuheit
- [ ] Scherer (1989) Theorie und Experiment im Volltext gegen Modellgleichungen abgleichen.
- [ ] Wilhelm & Kind (2015) genaue Natur-/erzwungene Trennung, Geometrie und Protokolle prüfen.
- [ ] Wu et al. (2020) als kolloidaler Mechanismusvergleich, nicht als Silica-Koeffizientenquelle.
- [ ] Weitere Zwei-Zeitskalen-/lineare Kompartiment-/Synerese-Modelle recherchieren.
- [ ] Präzise Abgrenzung zu existierenden Transferfunktions-/Identifizierbarkeitsresultaten erstellen.

### Phase 3 — reproduzierbare Ergebnisse
- [ ] Python-Skript für analytische Kurven und Figuren erstellen.
- [ ] unabhängige symbolische/numerische Checks dokumentieren.
- [ ] Einheiten- und Grenzfalltests ergänzen.
- [ ] Keine statistischen Fits an Näherungsdigitalisaten behaupten.
- [ ] Clean-checkout-Test und versionierte Daten-/Code-Freigabe.

### Phase 4 — Manuskript
- [ ] vollständigen englischen Entwurf erstellen;
- [ ] Abstract (zunächst maximal 150 Wörter für EJDE/MEMOCS-Format prüfen);
- [ ] Einleitung und Prior-Art-Vergleich;
- [ ] Modell-/Satz-/Beweisabschnitte;
- [ ] Figuren, Tabellen und Supplement;
- [ ] Claim–Evidence- und Limitationen-Audit;
- [ ] menschliche fachliche Überarbeitung und unabhängiges Gegenlesen.

### Phase 5 — Ethik, Autorenschaft, Rechte
- [ ] tatsächliche Autorinnen-/Autorenbeiträge klären;
- [ ] frühere TVT-Affiliation korrekt historisch einordnen, keine aktuelle KIT-Affiliation suggerieren;
- [ ] Matthias Kind nur unverbindlich um fachlichen Austausch bitten; Koautorenschaft ausschließlich nach tatsächlichem substanziellen Beitrag und Zustimmung;
- [ ] Herkunft/Lizenz aller Daten und Abbildungen prüfen;
- [ ] KI-Unterstützung nach Journalvorgaben transparent offenlegen; KI nicht als Autor;
- [ ] Finanzierung und unentgeltliche Eigeninitiative nur sachlich und korrekt deklarieren.

### Phase 6 — Einreichung
- [ ] Journal-Scope unmittelbar vor Einreichung erneut prüfen;
- [ ] Format, MSC-Codes, Keywords, Referenzen, PDF und Quellen-Dateien vorbereiten;
- [ ] bei EJDE drei fachlich passende, unabhängige Gutachter vorschlagen;
- [ ] genau ein Journal gleichzeitig;
- [ ] Preprint- und Lizenzstrategie anhand aktueller Richtlinien prüfen;
- [ ] erst nach ausdrücklicher menschlicher Freigabe einreichen.

## 10. Manuskript-Reifegrad

Aktuell: **Konzept und mathematische Basis vorhanden; Manuskript nicht einreichungsreif.**

Einreichungsreif erst, wenn:
- die mathematischen Aussagen unabhängig geprüft sind;
- die zusätzliche inverse Identifizierbarkeitsanalyse einen klaren nichttrivialen Beitrag liefert;
- der Literaturvergleich die Neuheit belegt;
- alle Abbildungen/Code reproduzierbar sind;
- Daten-/Rechte-/Autorenschaftsfragen geklärt sind;
- das Journal den Beitrag fachlich passend einordnen kann.

Es wird kein Zeitplan mit fingierter Sicherheit angegeben. Der Fortschritt wird über abgeschlossene Gates statt Kalenderprognosen gemessen.

## 13. Praktische Identifizierbarkeit — erster synthetischer Benchmark

Ein reproduzierbarer synthetischer Benchmark wurde ergänzt: [Bericht](MANUSCRIPT_01_PRACTICAL_IDENTIFIABILITY_BENCHMARK_2026-11-15_DE.md) und [Python-Skript](MANUSCRIPT_01_PRACTICAL_IDENTIFIABILITY_BENCHMARK.py). In vier Szenarien werden nahe bzw. getrennte Raten mit dicht/langem und grob/kurzem Messplan verglichen. Die Simulation verwendet 100 Wiederholungen je Szenario und additives gaußsches Messrauschen.

Der Benchmark illustriert erwartungsgemäß: nahe Raten und kurze/grobe Messfenster verschlechtern die Schätzung deutlich. Er ist ausdrücklich synthetisch, nutzt dieselbe Modellklasse zur Simulation und Anpassung und stellt keine experimentelle Validierung dar. Nächste methodische Ergänzungen: Profil-Likelihood/Bootstrap, Messoffsets und Modellfehlanpassung.

## 12. Strukturelle Identifizierbarkeit — zweiter Audit

Die formale Nullstart-Aussage und ihre Voraussetzungen sind in [MANUSCRIPT_01_STRUCTURAL_IDENTIFIABILITY_AND_PRACTICAL_LIMITS_2026-11-15_DE.md](MANUSCRIPT_01_STRUCTURAL_IDENTIFIABILITY_AND_PRACTICAL_LIMITS_2026-11-15_DE.md) ausgearbeitet. Unter \(k_n,k_h,C>0\), Nullstart und idealer kontinuierlicher Beobachtung bestimmt die Kurve das ungeordnete Ratenpaar über Summe und Produkt der Raten. Eine physikalische Zuordnung der beiden Ratenlabels bleibt unmöglich; ebenso ist \(\eta_a\) von \(q_\infty\) nur über das Produkt \(C=\eta_aq_\infty\) beobachtbar.

Der Satz ist ausdrücklich nicht auf unbekannte Anfangszustände oder reale verrauschte endliche Messreihen übertragen. Nahezu gleiche Raten, unzureichende frühe Abtastung und ein zu kurzes Beobachtungsfenster können die praktische Schätzung stark destabilisieren. Der nächste quantitative Schritt ist ein synthetischer Benchmark mit Rauschen, Messzeitplänen und Unsicherheitsanalyse.

## 11. Erster mathematischer Audit

Der erste interne Rechenaudit ist in [MANUSCRIPT_01_MATHEMATICAL_AUDIT_2026-11-15_DE.md](MANUSCRIPT_01_MATHEMATICAL_AUDIT_2026-11-15_DE.md) dokumentiert. Die zentrale geschlossene Lösung, das Gleichratenlimit, die Invarianzargumentation und die Raten-Label-Symmetrie wurden algebraisch nachgerechnet und mit dem Code abgeglichen. Kein algebraischer Widerspruch wurde gefunden. Der inverse Satz zur Rückgewinnung des ungeordneten Ratenpaars sowie die praktische Identifizierbarkeit sind als nächste Arbeit markiert.
