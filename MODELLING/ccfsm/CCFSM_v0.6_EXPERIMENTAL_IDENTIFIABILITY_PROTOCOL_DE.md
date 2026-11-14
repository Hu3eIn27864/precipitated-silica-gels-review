# CCFSM v0.6 — experimenteller Identifizierbarkeits- und Validierungsplan

**Datum:** 14.11.2026  
**Geltungsbereich:** ausschließlich natürliche, mechanisch unbelastete Synärese gefällter Silica-Gele.  
**Status:** präregistrierbarer Versuchsplan-Entwurf; noch keine experimentellen Messdaten und keine Freigabe unkalibrierter Stoffgesetze.

## 1. Ziel und wissenschaftliche Priorität

Die nächste Investition soll nicht in zusätzliche freie Fitparameter gehen. Sie soll die latenten Zustände und Transportgrößen unabhängig beobachten, die CCFSM bislang aus der äußeren Schrumpfungskurve S(t) nicht trennen kann.

**Primäre Forschungsfrage:** Lässt sich die beobachtete natürliche Schrumpfung als zeitlich gekoppelte Antwort aus (a) chemischer Netzwerkentwicklung, (b) Struktur-/Porenentwicklung und (c) hydraulisch-mechanischer Entwässerung vorhersagen, wenn die beteiligten Blöcke separat gemessen werden?

Die Versuche müssen drei Aussagen unterscheiden:

1. **Beobachtung:** Was wurde direkt gemessen (z. B. S(t), Temperatur, pH, Si im Überstand)?
2. **Proxy:** Welche Messung ist nur ein Stellvertreter (z. B. Qⁿ-Verteilung als Kondensationsproxy, D_f aus SAXS)?
3. **Modellzustand:** Welche Größe bleibt eine latente CCFSM-Variable (insbesondere effektive tragende Brückendichte B, Kontraktionsinventar X)?

Kein Proxy darf ohne Kalibrierung in eine direkte Messung umbenannt werden.

## 2. Harte Modellkorrekturen vor dem Experiment

### 2.1 B ist nicht die gesamte Si–O–Si-Bindungszahl

Quantitative Festkörper-29Si-MAS-NMR kann Q²/Q³/Q⁴-Spezies und damit den mittleren Kondensationszustand erfassen. Das ist ein chemischer Strukturproxy, aber kein direkter Zähler mechanisch tragender Brücken. Cross-polarization-MAS ist wegen unterschiedlicher Transferverstärkung nicht ohne Weiteres quantitativ; quantitative Auswertung benötigt geeignete direkte Anregung, Relaxations-/Recycle-Validierung und Standards.

**Konsequenz:** zunächst c_network/Qⁿ-Kondensation als gemessenen chemischen Block führen. B_eff bleibt latent, bis eine kalibrierte Beziehung zwischen Kondensation, Konnektivität und mechanischer Antwort vorliegt.

### 2.2 D_f, z und Permeabilität sind verschiedene Größen

SAXS/USAXS kann Fraktal-Skalierungen nur innerhalb des tatsächlich abgedeckten q-Fensters und einer angegebenen Längenskala liefern. D_f allein bestimmt weder Porenhalsverteilung noch Perkolation. Tomographie kann größere Poren und Konnektivität erfassen, aber nicht automatisch die Nanometer-Poren. Mehrskalige Messungen sind nötig; Auflösungsgrenzen müssen dokumentiert werden.

**Konsequenz:** D_f, Porosität, Porenhalsverteilung, Konnektivität und Tortuosität getrennt speichern. Keine Potenzfunktion kappa_eff(D_f) vor unabhängiger Prüfung.

### 2.3 K_eff ist nicht automatisch G' oder ein Oedometer-Modul

Ein Schermodul aus Oszillationsrheologie ist kein volumetrischer Kompressionsmodul. Für die hydraulische Closure muss der tatsächlich relevante, zeit- und frequenzabhängige Kompressions-/Konsolidierungsmodul des nahezu unbelasteten Gelzustands bestimmt oder die skalare k_h-Closure durch eine besser definierte poroelastische Gleichung ersetzt werden.

Oedometer- und Druckzellparameter werden nicht in die natürliche Synäresekalibrierung übernommen. Niedrigamplitudige Rheologie bzw. mechanische Charakterisierung erfolgt an separaten, zustandsangepassten Opferproben, nicht an der frei schrumpfenden Hauptprobe.

### 2.4 k_r ist durch gewöhnliche Rheologie nicht automatisch identifiziert

In v0.3 ist sigma ein dimensionsloses unrelaxiertes Kontraktionsinventar und keine Spannung in Pa. Ein gemessener Rheologie-Relaxationsmodul ist deshalb nicht ohne zusätzliche konstitutive Kopplung gleich sigma(t) oder k_r.

**Konsequenz:** bis eine solche Kopplung separat validiert ist, k_r nicht als identifizierte CCFSM-Rate ausgeben. Zunächst eine beobachtete Relaxationszeitverteilung als eigene Messgröße erfassen und prüfen, ob eine Ein-Rate-Näherung angemessen ist.

### 2.5 Modellstruktur vor Parameterfit

Aus S(t) allein ist eta_a q_infinity nur als Produkt zugänglich. Um eta_a und q zu trennen, braucht es eine unabhängige Operationalisierung von q (z. B. über einen validierten Netzwerk-/Eigenkontraktionsproxy) oder eine strukturell verbesserte Modellgleichung. Der Versuch darf q nicht zirkulär aus S zurückrechnen und anschließend als unabhängige Messung verwenden.

## 3. Messprogramm: was, wie, wann, wozu?

| Block | Primäre Messgröße und Methode | Zeitauflösung | Identifizierbare Aussage | Grenze / Kontrolle |
|---|---|---|---|---|
| Rezeptur | Gravimetrie, Feedstock-Assay, Dosier-/Mischprotokoll | je Ansatz | Reproduzierbare Eingangsbedingungen | Säure- und Basenroute getrennt |
| Chemie | pH und Gelkerntemperatur mit kalibrierten, möglichst wenig invasiven Sensoren; Parallel-/Opferproben | kontinuierlich bzw. dicht frühzeitig | pH(t), T_g(t), thermische Verzögerung | Badtemperatur nicht als Geltemperatur einsetzen |
| Si-Bilanz | ICP-OES/ICP-MS des Überstands und austretender Flüssigkeit; Gesamt-Si an Opferproben | frühe und späte Zeitpunkte | gelöstes, ausgetragenes und bilanziertes Si | Trennverfahren für kolloidales/gelöstes Si validieren |
| Kondensation | quantitative direkte Anregung 29Si-MAS-NMR an schock-/alterungsdefinierten Opferproben; Q²/Q³/Q⁴ | ausgewählte Zeitpunkte | chemischer Kondensationsproxy | kein direkter Lastbrückenzähler; CP-MAS allein nicht quantitativ |
| Fraktalstruktur | SAXS/USAXS mit dokumentiertem q-Fenster und Modellvergleich | ausgewählte Zeitpunkte | D_f im beobachteten Skalenbereich, charakteristische Längen | Poren-/Kontaktkonnektivität nicht allein ableitbar |
| Gröbere Poren | 3D-Röntgenmikro-/Nanotomographie, sofern Auflösung genügt; ergänzende Kryo-Bildgebung | ausgewählte Zeitpunkte | räumliche Poren-/Konnektivitätsinformation oberhalb Auflösungsgrenze | Einfrieren/Trocknen kann Artefakte erzeugen; keine unkritische Übertragung |
| Hydraulik | sehr niedriger Gradient an separaten, zustandsangepassten Opferproben; Darcy-Linearität und Geometrie prüfen | ausgewählte Zeitpunkte | kappa_eff(t) unter definierter Sättigung/Geometrie | nicht an Hauptprobe; mehrere kleine Gradienten, keine messbare Verdichtung |
| Mechanik | kleine Oszillationsamplitude innerhalb des linear-viskoelastischen Bereichs; ergänzend geeignete volumetrische Kompressibilität | ausgewählte Zeitpunkte | G*(omega,t) und ggf. separat K_eff | G' nicht als K_eff einsetzen; Opferproben |
| Relaxation | Stress-/Modulrelaxation an parallelen Opferproben mit dokumentierter Deformation und Erholungsphase | ausgewählte Zeitpunkte | beobachtetes Relaxationsspektrum | nur nach Modellkopplung auf k_r übertragbar |
| Natürliche Antwort | berührungsarme 3D-Volumenmessung plus Masse/ausgetretene Flüssigkeit | kontinuierlich, hohe Rate früh | S(t), Flüssigkeitsbilanz und Zeitmaßstab | Verdunstungsblank, geschlossene Feuchte-/Temperaturkontrolle |
| Grenzfläche | Kontaktmaterial, Rauheit, Benetzung, Drainagefläche und Interface-Widerstand dokumentieren | je Aufbau | reproduzierbare Randbedingungen | Kontaktwiderstand nicht in kappa_eff verstecken |

**Probenintegrität:** Die Hauptprobe für S(t) bleibt mechanisch unbelastet und wird nicht für NMR, Tomographie, Permeabilitäts- oder Rheologiemessungen manipuliert. Diese Messungen erfolgen an parallel hergestellten Opferproben, die aus demselben Ansatz und mit derselben Temperatur-/Alterungshistorie stammen.

## 4. Gestufter Versuchsplan

### Stufe 0 — Methoden- und Bilanzpilot

Ziel: zeigen, dass Zeitnullpunkt, Temperatur, Schrumpfung, Verdunstung und Si-Bilanz reproduzierbar erfasst werden.

- Säure- und Basenroute separat; zunächst je eine festgelegte, vollständig analytisch dokumentierte Rezeptur.
- Einheitlicher Misch-/Zugabeablauf, definierter Gelpunkt und operationaler Start t0.
- Mindestens drei unabhängig angesetzte Pilotchargen pro Route.
- Kontinuierliche T_g(t) und S(t); pH in Parallel-/Opfermessung.
- Verdunstungsblank und Gefäß-/Supportblank; Masse des austretenden Liquors.
- Abgleich Si_initial = Si_gel + Si_supernatant + Si_effluent innerhalb der vorab festgelegten analytischen Unsicherheit.

**Gate 0:** keine kinetische Parameteridentifikation, solange die Stoff-/Massenbilanz systematisch driftet oder t0/Temperatur nicht reproduzierbar sind.

### Stufe 1 — Minimaler identifizierender Faktorplan

Nach erfolgreichem Pilot wird ein blockierter faktorieller Plan vorgeschlagen:

- Route: Säure / Base (zwei getrennte Modellzweige).
- Geltemperatur: 20 / 40 / 60 °C, gemessen als T_g(t) und nicht nur als Bad-Sollwert.
- Drainagelänge: zwei klar definierte Werte bei ansonsten möglichst gleicher Proben- und Grenzflächengeometrie.
- Replikation: zunächst 4 unabhängig hergestellte Chargen je Zelle als Planungsstart; die endgültige Stichprobengröße nach Pilot-Varianz und Power-/Präzisionsziel festlegen.

Das ergibt 2 × 3 × 2 × 4 = 48 unabhängige Hauptproben. Die Zahl ist ein praktikabler Startpunkt, keine vorgetäuschte Power-Berechnung. Technische Wiederholungen derselben Charge zählen nicht als unabhängige Replikate.

**Wichtig:** Temperatur und Route werden nicht in einer einzigen universellen Parameterkurve zusammengeworfen. Die Säure- und Basenroute erhalten getrennte chemische Koeffizienten; gemeinsame hydraulische Koeffizienten sind erst nach einem formalen Modellvergleich zulässig.

Für jede Hauptprobe werden zustandsangepasste Opferproben aus derselben Charge zu vorab festgelegten Zeiten entnommen. Zeitpunkte müssen den schnellen Anfang und die langsame Spätphase abdecken; ein Pilot legt die endgültigen Zeitpunkte fest. Als Startgerüst: unmittelbar nach t0, 10 min, 30 min, 1 h, 2 h, 4 h, 8 h und 24 h; bei Zylinder-/Langzeitbedingungen gegebenenfalls 48–250 h. Nicht alle Methoden müssen an jedem Zeitpunkt laufen.

### Stufe 2 — gezielte mechanistische Teilstudien

Nur wenn Stufe 1 klare Signale zeigt:

1. **Chemie-/Brückenblock:** Qⁿ-NMR + Si-Bilanz + mechanischer Netzwerkproxy; prüfen, ob ein gemeinsamer B_eff(t)-Proxy überhaupt kalibrierbar ist.
2. **Morphologie-/Hydraulikblock:** SAXS/USAXS + Poren-/Konnektivitätsmessung + kappa_eff(t); konkurrierende Closure-Modelle vergleichen, nicht nur eine Potenzfunktion fitten.
3. **Mechanik-/Relaxationsblock:** K_eff(t) separat von G*(omega,t) bestimmen; prüfen, ob eine Ein-Rate-Relaxation genügt.
4. **Grenzflächenblock:** nur wenn Geometrie-/Drainage-Längen-Skalierung systematische Abweichungen zeigt, R_c und Benetzung gezielt variieren.

## 5. Welche Parameter werden womit identifiziert?

| CCFSM-Größe | Erforderliche Daten | Status nach Minimalprogramm |
|---|---|---|
| k_b | Zeitreihe eines validierten chemischen Netzwerk-/Brückenproxies | nur bedingt; B_eff braucht Kalibrierung |
| B_eff und Omega_b getrennt | absolute B_eff-Kalibrierung plus unabhängiges X | nicht automatisch durch Qⁿ-NMR |
| D_f(t) | SAXS/USAXS über angegebenes q-Fenster | identifizierbar im jeweiligen Skalenfenster |
| z(t) | 3D-Kontakt-/Koordinationsmessung mit Auflösungsnachweis | häufig schwierig; nicht aus D_f ableiten |
| Poren-/Konnektivitätsgrößen | mehrskalige Bildgebung/Porenanalyse | aufgelöstes Teilfenster, nicht alle Poren |
| kappa_eff(t) | unabhängige Niedriggradienten-Permeabilität an Opferproben | messbar unter spezifizierter Sättigung/Geometrie |
| K_eff(t) | volumetrische Kompressibilität am zustandsangepassten Gel | messbar, sofern methodisch definiert |
| k_h | kappa_eff, K_eff, mu, L_d und Randbedingungen | Closure testbar; C_g nicht ungeprüft universal |
| eta_a | unabhängiges q(t) und S(t) | bleibt unidentifiziert, solange q nur aus Modellgleichungen kommt |
| k_r | unabhängiges Relaxationssignal plus validierte Kopplung zu sigma | zunächst nur Relaxationsspektrum, nicht automatisch CCFSM-k_r |
| S(t) | berührungsarme Volumenmessung + Masse-/Verdunstungsbilanz | direkt messbar |

**Nichtidentifizierbarkeit offenlegen:** Falls B_eff, q oder sigma nicht unabhängig operationalisiert werden können, werden sie nicht durch mehr Fitparameter „identifiziert“. Das Modell wird dann auf messbare zusammengesetzte Parameter reduziert.

## 6. Präregistrierte Hypothesen und Falsifikationskriterien

- **H1 — chemischer Block:** Qⁿ-/Si-Bilanzänderungen laufen der Entwicklung von S(t) zeitlich voraus oder kovariieren reproduzierbar mit ihr. Widerlegt/geschwächt, wenn kein reproduzierbarer Zusammenhang über Chargen besteht oder der Zusammenhang nach Kontrolle von Temperatur/Geometrie verschwindet.
- **H2 — Struktur-Transport:** gemessene Poren-/Konnektivitätsänderungen erklären kappa_eff(t) besser als D_f(t) allein. Widerlegt/geschwächt, wenn kein reproduzierbarer Zusatznutzen gegenüber einem konstanten/chemieabhängigen kappa-Modell entsteht.
- **H3 — hydraulische Zeitkonstante:** die unabhängig gemessenen kappa_eff, K_eff, mu und L_d sagen die beobachtete Zeitantwort mit einer vorher festgelegten Geometrieclosure voraus. Widerlegt, wenn systematische Residuen nach unabhängiger Bestimmung der Faktoren bleiben oder ein nicht identifizierter Interface-Term dominiert.
- **H4 — Geometrieskalierung:** eine definierte Änderung von L_d führt in Richtung der vorhergesagten L_d^-2-Skalierung, sofern die erste-Moden-Annahmen erfüllt sind. Abweichungen sind Anlass, Rand-/Mehrmodenmodell zu prüfen, nicht die Daten nachträglich passend zu skalieren.
- **H5 — Ein-Rate-Relaxation:** ein einzelnes k_r genügt nur, wenn die Relaxationsdaten eine dominante Zeitskala zeigen und Vorhersagen an unabhängigen Proben bestehen. Sonst Relaxationsspektrum statt Ein-Rate-Modell.

Alle Hypothesen werden mit Chargen als unabhängigen Einheiten geprüft. Zeitpunkte innerhalb derselben Probe sind keine unabhängigen Replikate.

## 7. Daten- und Analyseprotokoll

Für jede Probe sind mindestens zu speichern:

- eindeutige Chargen-/Proben-ID, Route, Rohstoffchargen, Rezeptur und Dosiermassen;
- Zugabereihenfolge, Zugaberate, Mischgeometrie, Drehzahl/Leistung und Zeitstempel;
- t0-Definition, Gelpunktkriterium, Alterungsdauer;
- T_g(t), pH(t), Feuchte, Umgebungstemperatur;
- Probengeometrie, Drainageflächen, Material-/Oberflächenbehandlung, Entwässerungslänge;
- Rohdaten und Kalibrierdateien jeder Methode, Auflösung und Nachweisgrenzen;
- Massen-/Si-Bilanzen, Verdunstungsblank, Volumenmessung und Messunsicherheit;
- Abweichungen vom Protokoll und Ausschlussgründe vor Analyse.

Auswertung: hierarchisches Modell mit Charge als Zufallseffekt; Unsicherheit der Messmethoden propagieren; Modellvergleich über vorab definierte Hold-out-Chargen bzw. Bedingungen. Keine zufällige Aufteilung von Zeitpunkten derselben Probe in Training und Test. Für die Primärprüfung mindestens eine komplette Temperatur-/Geometriezelle oder unabhängige Chargen als externe Validierung zurückhalten.

## 8. Modellfreigabe-Gates

- **Gate A — Messqualität:** Reproduzierbarer t0, Temperaturhistorie, Volumen-/Massenbilanz, Verdunstungskontrolle und unabhängige Chargen.
- **Gate B — Einzelblöcke:** chemische, morphologische, hydraulische und mechanische Messgrößen mit Unsicherheit und Gültigkeitsbereich.
- **Gate C — Closure:** jede Struktur-Transport- und Mechanikgleichung muss gegen unabhängige Messungen getestet werden.
- **Gate D — gekoppelte Vorhersage:** Parameter werden auf Trainingschargen bestimmt; Vorhersage von S(t) in zurückgehaltenen Chargen ohne Nachfitten.
- **Gate E — Generalisierung:** getrennte Säure-/Basenroute und Temperatur-/Geometriebedingungen bestanden; erst dann Gleichung als empirisch GRÜN kennzeichnen.

## 9. Unmittelbare Priorität

1. Zuerst Stufe 0 und die Messdefinition von S, t0, T_g, Verdunstung und Si-Bilanz absichern.
2. Danach in Stufe 1 S(t), T_g(t), pH(t), Si-Bilanz und Opferprobenmessungen synchronisieren.
3. Erst nach Vorliegen der ersten Struktur-/Hydraulikdaten eine kappa_eff-Closure wählen.
4. B_eff, q, sigma und k_r bis zur unabhängigen Operationalisierung ausdrücklich als latent/unkalibriert markieren.

**Kernaussage:** Der wissenschaftliche Engpass ist nicht die Zahl der Fitparameter, sondern die fehlende unabhängige Beobachtung der inneren Zustände. Der vorgeschlagene Plan adressiert genau diese Lücke, ohne natürliche Synärese mit erzwungener Konsolidierung zu vermischen.
