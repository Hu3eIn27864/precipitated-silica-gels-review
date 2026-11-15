# CCFSM — P27-Pfad: Literaturbasierte physikalische Validierung

**Stand:** 15.11.2026  
**Ziel:** maximal belastbare externe Prüfung ohne neue Proben oder eigene Laborversuche.  
**Wichtige Abgrenzung:** Dieses Dokument definiert eine Validierungsstrategie und dokumentiert den gegenwärtig erreichbaren Evidenzstand. Es erklärt das CCFSM nicht für physikalisch validiert.

## 1. Ausgangsbefund

Die bisherige v0.5-Auswertung ist eine explorative Modellselektion auf sieben KI-gestützt approximativ digitalisierten natürlichen Kurven aus Wilhelm & Kind (2015). Sie ist weder eine unabhängige Validierung noch ein Test des vollständigen gekoppelten CCFSM. Der einfache Exponentialfit gewinnt 3/7, der gestreckte Exponentialfit 4/7; die zweistufige CCFSM-Antwort gewinnt 0/7 und trifft bei allen sieben Kurven eine Suchgrenze. Der Median-Holdout-RMSE beträgt 0.04207, 0.01755 bzw. 0.04207. Diese Befunde sind als negativer/neutraler Modellvergleich sichtbar zu halten und dürfen nicht durch nachträgliches Umdefinieren der Zielgröße verdeckt werden.

## 2. Evidenzhierarchie und Daten-Sperren

| Evidenz | Quelle/Status | Zulässige Rolle | Nicht zulässig |
|---|---|---|---|
| A: Originaltabellenwerte | Wilhelm & Kind 2015, Zylinder: sechs S_max- und sechs tau-Werte | Referenzwerte für natürliche Synärese im beschriebenen Protokoll | Als Rohmesswerte oder unabhängige Replikation bezeichnen |
| A, getrennt | Wilhelm & Kind 2015, Tröpfchenparameter | Geometrie-/Temperaturhistorien-Holdout nach Zylinderkalibrierung | Mit Zylindern ohne Geometrie-/Thermikmodell zusammenfitten |
| A, Konfliktzweig | Wilhelm 2017, basische Tröpfchen-Tabelle | Sensitivitäts-/Quellenkonfliktprüfung | Mit Artikel-Tabelle 2 mitteln |
| D: Abbildungsablesung | Sieben kuratierte natürliche Kurven | Explorative Kurvenformprüfung und Residuenanalyse | Konfidenzintervalle aus scheinbar unabhängigen Pixelpunkten ableiten |
| E/B nach Nacharbeit | Scherer 1989 II, TEOS-/Alkoxid-Silica | Unabhängige Mechanismenprüfung, ggf. externe Kurvenprüfung nach Volltextextraktion | Koeffizienten ungeprüft auf gefällte Natriumsilikat-Silica übertragen |
| E/C | Scherer 1989 I, 1989 G, Scherer & Swiatek | Theorie-/Permeabilitäts-/Modul-Plausibilität | Trocknungsbeziehungen als natürliche Synäresegesetze einsetzen |
| E/D | Quarch 2010; Schlomach & Kind 2004 | Fällungs-, Gelierungs-, Morphologie- und Prozesskontext | Als natürliche Post-Gel-Synärese-Zeitkurven ausgeben |
| X | Sahabi & Kind 2011, Druck-/Oedometerdaten; Wilhelm & Kind Druckzelle | Separater mechanischer/erzwungener Vergleich | Natürliche Synäreseparameter fitten |

Wilhelm 2017 ist quellenkritisch wertvoll, aber keine unabhängige Replikation des Artikels von 2015. Gleiches gilt für weitere Arbeiten derselben Forschungsgruppe. Ein unabhängiger Mechanismenvergleich ist nicht gleichbedeutend mit direkter Zielsystemvalidierung.

## 3. Konkretes Validierungsprotokoll

### V1 — Reproduktion der Quellenwerte

1. Alle zwölf Zylinderwerte (sechs Amplituden, sechs Zeitkonstanten) direkt aus der Originaltabelle als Klasse A führen.
2. Definitionen, Einheiten, Geometrie, Temperatur, pH/Katalyse und Randbedingungen unverändert übernehmen.
3. Die sieben Kurvenablesungen getrennt halten; Markerunsicherheit und Achsenkalibrierung dokumentieren.
4. Artikel/Dissertation-Konflikte als separate Datenzweige erhalten; niemals stillschweigend mitteln.

**Akzeptanz:** Jede Zahl hat Quellenstelle, Originaleinheit, Prozessklasse, Geometrie und Evidenzklasse; jede Umrechnung ist reproduzierbar.

### V2 — Geometrie- und Temperaturtransfer als interner Literatur-Holdout

1. Zylinderwerte sind der primäre Referenzzweig.
2. Tröpfchenwerte werden bis zur Festlegung eines geometrie-/thermisch konsistenten Vorhersageprotokolls gesperrt.
3. Vorhersage der Tröpfchen-Endwerte und Zeitkonstanten aus Zylinderparametern nur dann testen, wenn das Modell eine explizite Geometrie- und Temperaturhistorie enthält.
4. Keine Nachkalibrierung an Tröpfchen vor dem Holdout-Bericht.
5. Den Wilhelm-Dissertationskonflikt als getrennten Sensitivitätszweig ausweisen.

**Interpretation:** Dies ist ein strenger Cross-Protocol-Holdout innerhalb einer Forschungsquelle, aber keine unabhängige Laborreplikation.

### V3 — Kurvenform und Vorhersagefehler

Für jeden Holdout getrennt berichten:
- RMSE und MAE in der dimensionslosen Schrumpfungsgröße,
- Endwertfehler und Zeitmaßstabsfehler getrennt,
- Residuen gegen Zeit, Temperatur, pH/Katalyse und Geometrie,
- Fehler bei früher, mittlerer und später Phase,
- Parametergrenzen, Nichtidentifizierbarkeit und fehlende Beobachtbarkeit.

Bei digitalisierten Kurven sind Zeitpunkte korreliert und Ablesefehler nicht unabhängig. Deshalb keine naive i.i.d.-Signifikanzprüfung und keine künstlich engen Konfidenzintervalle. Sensitivitätsbänder müssen die Digitalisierungsunsicherheit abbilden.

### V4 — Unabhängiger Mechanismenvergleich

Scherer 1989 I/II ist die priorisierte externe Mechanismenprüfung: natürliche Synerese alkoxid-/TEOS-basierter Silicagele mit unabhängig gemessener Permeabilität, Modul und Viskosität. Vor jeder quantitativen Nutzung müssen Volltext, Materialrezeptur, Geometrie, Randbedingungen, Messgrößen und Kurvenmarker geprüft werden. Die chemische Herstellungsroute unterscheidet sich von gefälltem Natriumsilikat-Silica; daher getrennte Parameter und keine gepoolte Kalibrierung.

Quarch und Schlomach & Kind sind vorrangig für Gelierungs-/Struktur-/Morphologiehypothesen. Ein fehlender direkter natürlicher Synerese-Zeitverlauf darf nicht durch Strukturwerte ersetzt werden.

### V5 — Modellvergleich ohne Ergebnis-Selektion

Mindestens drei Modellklassen unverändert vergleichen:
1. exponentielle Baseline,
2. gestreckt-exponentielle Baseline,
3. zweistufige CCFSM-Antwort.

Gleiche Datenaufteilung, Zielfunktion und Nebenbedingungen verwenden. Komplexere Modelle erhalten keinen Vorteil durch zusätzliche freie Parameter oder nachträgliche Auswahl des Holdouts. Boundary-Hits und Nichtkonvergenz zählen als Ergebnis. Wenn eine einfachere Baseline besser vorhersagt, ist das als Befund zu berichten.

## 4. Was derzeit als physikalisch gestützt gelten kann

- Die publizierten natürlichen Zylinder-/Tröpfchenparameter belegen, dass Endschrumpfung und Zeitmaßstab mit Temperatur, Katalyse und Geometrie variieren; die konkrete Übertragbarkeit bleibt modellabhängig.
- Die Literatur stützt qualitativ die Relevanz von Netzwerkmechanik, Permeabilität und Porenflüssigkeitsbewegung für Synerese; Scherer ist dafür ein unabhängiger Mechanismenast, aber ein anderes Silicasystem.
- Das aktuelle CCFSM besitzt gekoppelte Reaktions-, FV-Transport-, Darcy- und Biot-Mechanik-Bausteine; die Kopplung allein ist kein empirischer Beleg für die Richtigkeit aller Terme.
- Die v0.5-Kurvenauswertung bevorzugt derzeit einfachere Kurvenformen. Das begrenzt jede Behauptung, dass die zusätzliche zweistufige Kinetik bereits empirisch erforderlich oder überlegen sei.

## 5. Offene Arbeiten mit höchstem Erkenntnisgewinn

1. Supplementary Materials S1–S7 und Figuren S1–S6 von Wilhelm & Kind 2015 abrufen und vollständig prüfen.
2. Scherer 1989 II Volltext und Zeitkurven extrahieren; erst danach entscheiden, ob markerbasierte externe Kurvenvalidierung möglich ist.
3. Scherer & Swiatek 1989 Permeabilitätswerte samt Messdefinition und Materialhistorie extrahieren.
4. Wilhelm-Zylinder als Kalibrierzweig und Tröpfchen als vorab gesperrten Cross-Protocol-Holdout implementieren.
5. Ein Quellen-/Daten-Audit mit maschinenlesbarer Herkunft, Messdefinition, Unsicherheit und Ausschlussgrund je Messpunkt bereitstellen.
6. Erst wenn unabhängige Material-/Transportgrößen tatsächlich verfügbar sind, die bisher nicht identifizierbaren chemischen, morphologischen und mechanischen Parameter schätzen.

## 6. Freigabestufen

- **L0 — Quellenreproduktion:** Originalwerte und Provenienz vollständig auditierbar.
- **L1 — interner Cross-Protocol-Test:** Geometrie-/Temperaturtransfer ohne Holdout-Leakage ausgewertet.
- **L2 — unabhängiger Mechanismenvergleich:** externe TEOS-/Alkoxid-Daten mit dokumentierter Systemtrennung geprüft.
- **L3 — unabhängige Zielsystemvalidierung:** unabhängige natürliche Synärese-Daten für gefällte Silica; derzeit nicht nachgewiesen.
- **L4 — gekoppelte Modellvalidierung:** mehrere unabhängige Observablen (Schrumpfung, Porendruck/Fluss, Struktur/Permeabilität/Mechanik) werden simultan und ohne freie Nachkalibrierung vorhergesagt.

**Aktueller Status:** L0 teilweise erreicht; L1 noch nicht ausgeführt; L2 bibliographisch/qualitativ vorbereitet, quantitative Extraktion offen; L3 und L4 nicht erreicht. Die wissenschaftlich korrekte Aussage lautet daher: CCFSM ist mathematisch und numerisch in Teilbereichen verifiziert und literaturbasiert plausibilisiert, aber noch nicht unabhängig physikalisch validiert.


## 7. Quellenkritischer Negativtest: erzwungene Synärese nicht als Ersatzvalidierung

Der Volltext von Wilhelm & Kind (2015) enthält einen besonders wichtigen Gegenbefund für jede naive Übertragung: Das aus erzwungener Synärese durch Extrapolation auf \(\Delta p=0\) abgeleitete korrelative Modell überschätzt bei basischer natürlicher Synärese die maximale Schrumpfung deutlich. Die extrapolierten Werte liegen bei etwa 0.52–0.75, während die natürlichen Zylinderwerte 0.30, 0.39 und 0.51 betragen; der Artikel beschreibt die Überschätzung als ungefähr Faktor zwei. Auch die Zuordnung der vorhergesagten Zeitkonstanten zu den Temperaturen ist teilweise falsch. Für saure Gele liegt die extrapolierte Amplitude dagegen bei etwa 0.19–0.30 und passt teilweise/in der Größenordnung zu den Messwerten.

Konsequenz für CCFSM: Druckzell-/Oedometerdaten dürfen nicht als einfacher Ersatz für natürliche Synerese oder als unabhängiger Bestätigungsdatensatz verwendet werden. Der Unterschied ist nicht bloß ein Datenformatproblem, sondern zeigt, dass die Randbedingung und der Prozesspfad den Transfer verändern können. Der Holdout muss daher Prozessklasse und Randbedingung strikt sperren.


## 8. Zusätzliche unabhängige Observable im Zielsystem: Silicium im Porenfluid

Figure 9 von Wilhelm & Kind (2015) enthält neben der Volumenschrumpfung eine zweite, chemisch relevante Observable: die Konzentration monomerer Kieselsäure im ausgetretenen Porenfluid natürlicher Zylinder. Berichtet werden für saure Gele etwa 0.2–0.4 mmol/L und für basische Gele etwa 100–200 mmol/L. Die Autoren weisen zugleich darauf hin, dass die Spektroskopie nicht bei der jeweiligen erhöhten Versuchstemperatur, sondern bei ungefähr 20 °C durchgeführt wurde; Nachpolymerisation und Temperaturabhängigkeit der Löslichkeit können die Interpretation beeinflussen.

**Validierungspotenzial:** Figure 9 sollte als eigener Datenzweig digitalisiert und mit Zeit, Katalyse, Temperatur und Messprotokoll erfasst werden. Diese Observable kann den chemischen Speziations-/Polymerisationsblock stärker prüfen als eine weitere Anpassung derselben Schrumpfungskurve. Sie ist aber keine direkte Messung der gesamten gelgebundenen Brückeninventare und identifiziert für sich allein keine Brückendichte.

**Priorität:** vor zusätzlichem Fitten chemischer Ratenparameter zuerst Figure 9 quellenkritisch digitalisieren, Einheiten/Probenahme und Messzeitpunkt klären und die bei 20 °C erfolgte Analyse als Messmodell abbilden. Tropfen besitzen laut Artikel zu wenig ausgetretenes Porenfluid für dieselbe Analyse; dieser Observable-Holdout ist deshalb auf die Zylinder beschränkt.


## 9. Figure 9 — Quellen- und Plot-Audit (15.11.2026)

Die Originalgrafik ist direkt unter [Figure 9 (MDPI image)](https://mdpi-res.com/polymers/polymers-07-01528/article_deploy/html/images/polymers-07-01528-g009-1024.png) einsehbar. Sie zeigt zwei Panels für natürliche Synärese in Zylindern: sauer (a) und basisch (b), jeweils mit Markern für 20, 40 und 60 °C. Die Zeitachse reicht ungefähr 0–250 h. Die Konzentrationsachse ist gebrochen; der bei etwa 1000 mmol/L eingezeichnete Anfangswert ist eine aus der eingesetzten Natriumsilikatmenge berechnete Konzentration und kein gemessener Porenfluid-Zeitpunkt.

### Kritischer Befund

Der Fließtext fasst die saure Reihe als 0.2–0.4 mmol/L zusammen. In der Grafik sind für die 60-°C-Reihe jedoch visuell auffällige Marker um ungefähr 0.8 mmol/L früh und ungefähr 0.6 mmol/L spät erkennbar. Diese Stellen sind noch nicht pixelgenau nachdigitalisiert; sie dürfen weder als gesicherte Messwerte behandelt noch stillschweigend verworfen werden. Der Text fasst die basische Reihe als 100–200 mmol/L zusammen, während einzelne Marker/Fehlerbalken visuell breit streuen.

### Messmodell und Freigabesperre

Die Autoren berichten, dass die spektroskopische Analyse nicht bei den Gelbadtemperaturen 40/60 °C, sondern bei Raumtemperatur (~20 °C) durchgeführt wurde. Sie diskutieren mögliche Nachpolymerisation nach dem Auspressen/Abtrennen des Porenfluids und eine daraus folgende Konzentrationsänderung. Die Messgröße ist deshalb nicht ohne Weiteres die in-situ-Konzentration im warmen Gel.

Die neue Datei \`LITERATURE/wilhelm_kind_fig9_pore_liquid_audit.csv\` ist ausdrücklich ein Quellen-Audit und **kein** digitalisierter Rohdatensatz. Sie trennt Textzusammenfassung, visuelle Auffälligkeit, Prozess-/Temperaturkontext und Fit-Freigabe. Alle Figure-9-Punkte bleiben bis zur pixelgenauen Digitalisierung, Fehlerbalkenklärung und Klärung der Probenahme-/Analyseverzögerung für eine quantitative CCFSM-Kalibrierung gesperrt.

**Validierungswert:** Figure 9 ist eine zusätzliche chemische Observable aus demselben Zielsystem und derselben Publikation, also ein unabhängiger Observable-Test, aber keine unabhängige Laborreplikation.


## 10. Assay-Spezifität: Molybdatreaktivität ist nicht automatisch Monomer-Spezifität

Ein zusätzlicher Quellencheck verändert die Interpretation von Figure 9 wesentlich. Wilhelm & Kind verwenden eine gelbe Silicomolybdat-Farbreaktion bei 400 nm und verweisen auf Alexander (1953). Alexander zeigte jedoch, dass die Reaktionsgeschwindigkeit mit Molybdänsäure vom Polymerisationsgrad abhängt: Monokieselsäure reagiert bei 20 °C in etwa 75 s vollständig, Disikieselsäure erst in ungefähr 10 min; höher polymerisierte Spezies reagieren noch langsamer. Die Methode misst daher abhängig von Reaktions-/Ablesezeit und Reagenzbedingungen eine operational definierte molybdatreaktive Siliciumfraktion, nicht ohne Weiteres ausschließlich Monomer.

Eine spätere methodische Übersicht zur Silica-Colorimetrie bestätigt, dass die molybdatreaktive Fraktion Monosilicic-, Disilicic- und niedrigmolekulare Polysilicic-Spezies umfassen kann. Deshalb ist die publizierte Bezeichnung „monomeric silicic acid“ als Autoreninterpretation zu kennzeichnen; ohne dokumentierte Reaktionszeit, pH-/Reagenzbedingungen und Matrixvalidierung dürfen die Figure-9-Werte nicht als eindeutige Monomerkonzentration in die CCFSM-Monomerbilanz übernommen werden.

**Konsequenz für das Messmodell:** zunächst eine Beobachtungsfunktion \(y_{Mo}(t)=\mathcal{A}_{Mo}[c_{M},c_{D},c_{P},pH,T_{assay},t_{reaction},\ldots]\) vorsehen. Erst wenn die Alexander-Kinetik und die konkrete Laborprozedur reproduzierbar spezifiziert sind, kann entschieden werden, ob ein vereinfachter Grenzfall \(y_{Mo}\approx c_M\) gerechtfertigt ist. Andernfalls bleibt Figure 9 ein Holdout für „molybdatreaktives niedrigmolekulares Silica“, nicht für reines Monomer.

Quellen: Alexander, G.B. (1953), *J. Am. Chem. Soc.* 75, 5655–5657, DOI 10.1021/ja01118a054; Berro et al. (2014), *Mineralogical Magazine* 78(6), 1417 ff., DOI 10.1180/minmag.2014.078.6.08.


## 11. Figure 9 — manuelle Ablese-Arbeitsdatei (15.11.2026)

Die Originalabbildung wurde direkt in der MDPI-Artikelseite geöffnet und visuell abgelesen. Die 39 geschätzten Markerzentren liegen in `LITERATURE/wilhelm_kind_fig9_digitized_approx_2026-11-15.csv`; die begleitende Methodik- und Unsicherheitsdokumentation steht in `CCFSM_P27_FIG9_DIGITIZATION_AUDIT_2026-11-15_DE.md`.

Diese Werte sind **keine pixelgenauen Rohdaten**. Zeit-/Konzentrationsableseunsicherheiten sind konservative visuelle Schätzungen; Fehlerbalken wurden nicht numerisch rekonstruiert. Die hohen sauren 60-°C-Marker wurden ausdrücklich beibehalten. Alle Punkte bleiben fitgesperrt. Die Abbildung enthält einen gebrochenen Konzentrationsmaßstab und einen berechneten Anfangswert (~1000 mmol/L), der kein gemessener Porenfluidpunkt ist und in der CSV fehlt.

Die Artikelbeschreibung bestätigt, dass das Porenfluid bei ca. 20 °C analysiert wurde, auch wenn die Gelbäder 40/60 °C hatten; Nachpolymerisation kann den Messwert beeinflussen. Der 400-nm-Molybdatassay ist bis zur Rekonstruktion von Reaktionszeit und Matrixbedingungen als operationale molybdatreaktive niedrigmolekulare Silica-Fraktion zu behandeln, nicht als gesicherte reine Monomerkonzentration. Figure 9 ist eine zusätzliche Observable aus derselben Studie, keine unabhängige Laborreplikation.
