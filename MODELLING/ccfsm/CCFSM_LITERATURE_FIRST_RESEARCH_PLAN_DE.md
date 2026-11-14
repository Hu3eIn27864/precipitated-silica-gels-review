# CCFSM — Literaturdatenstrategie ohne neue Laborversuche

**Stand:** 14.11.2026  
**Geltungsbereich des Kernmodells:** natürliche, mechanisch unbelastete Synärese gefällter Silica-Gele.  
**Arbeitsmodus:** Sekundäranalyse publizierter Daten; keine neuen Proben und keine eigenen Messungen werden vorausgesetzt.

## 1. Konsequenz für die Forschungsstrategie

Die experimentelle Identifizierbarkeitsmatrix v0.6 bleibt als Referenz dafür nützlich, welche Größen ein vollständiges Modell unabhängig messen müsste. Sie ist aber **kein notwendiger Arbeitsauftrag an den Nutzer**. Da keine Probenherstellung mehr möglich ist, wird die operative Forschungsroute auf Literaturdaten umgestellt:

1. publizierte Tabellenwerte und ausdrücklich berichtete Messwerte transkribieren;
2. Supplementary Materials und institutionelle Repositorien systematisch prüfen;
3. Diagramme nur mit dokumentierter Achsenkalibrierung und manuell geprüften Markern digitalisieren;
4. Daten unterschiedlicher Silica-Herstellungsrouten und Prozessarten getrennt halten;
5. Modellblöcke nur mit Daten prüfen, die die betreffende Größe tatsächlich beobachten;
6. fehlende Zustände als nicht identifiziert ausweisen, statt sie durch zusätzliche freie Parameter zu ersetzen.

Es wird keine neue Laborarbeit unterstellt. Die wissenschaftliche Leistung kann in einer quellenkritischen, reproduzierbaren Datenrekonstruktion, einer identifizierbaren Modellreduktion und einer externen Literaturprüfung liegen.

## 2. Evidenzklassen und Zulassungsregeln

| Klasse | Bedeutung | Verwendung |
|---|---|---|
| A | Original veröffentlichte Zahlenwerte (Tabelle/Text) | quantitative Referenz; Herkunft und Definition exakt übernehmen |
| B | Originaldiagramm mit reproduzierbarer Achsenkalibrierung und geprüften Markern | quantitative Kurvendaten mit Digitalisierungsunsicherheit |
| C | Originaldiagramm visuell geprüft, aber nicht vollständig pixelkalibriert | qualitative/halbquantitative Plausibilitätsprüfung |
| D | KI-gestützte oder nicht unabhängig geprüfte Näherungsablesung | explorative Sensitivität, nicht primäre Kalibrierung |
| E | Sekundärzitat, Abstract, Review oder qualitative Aussage | Kontext und Hypothesen, keine Rohdatenbehauptung |
| X | Andere Prozessphysik (Trocknung, Druckkonsolidierung, Oedometer, erzwungene Synärese) | separater Vergleichs-/Mechanismenast; keine Kalibrierung der natürlichen Synärese |

**Wichtige Trennung:** Eine in einem Paper angegebene Fit-Amplitude oder Zeitkonstante ist ein publizierter empirischer Fitparameter, keine Rohmessung. Eine aus einer Abbildung rekonstruierte Kurve ist ebenfalls keine Original-Rohdatenreihe.

## 3. Quelleninventar und konkrete Verwendbarkeit

### 3.1 Primäre Zielsystemquelle: gefällte Silica

**Wilhelm, S.; Kind, M. (2015).** *Influence of pH, Temperature and Sample Size on Natural and Enforced Syneresis of Precipitated Silica*. Polymers 7(12), 2504–2521. DOI: [10.3390/polym7121528](https://doi.org/10.3390/polym7121528).  
Volltext: https://www.mdpi.com/2073-4360/7/12/2504

- Direkte Zielsystemquelle für natürliche Synärese aus Natriumsilikat/Schwefelsäure.
- Tabellen 1 und 2 enthalten empirische Fitparameter für Zylinder und Tropfen; Figuren 8 und 10 zeigen Zeitverläufe.
- Tabelle 1 ist bereits als Evidenzklasse A transkribiert; Tabelle 2 bleibt wegen der bekannten Figure-10b-Diskrepanz ausdrücklich getrennt von der Abbildungsablesung.
- Der Artikel enthält auch Informationen zur Siliciumsäure im ausgepressten Porenfluid (Figur 9) und zum Prozess-/Geometrieaufbau.
- Supplementary Materials sind verlinkt. Der Supplement-Link wurde im Recherchelauf identifiziert, ließ sich mit dem verwendeten Abruf jedoch nicht dekodieren. Die dortigen Tabellen S1–S7 und Figuren S1–S6 sind daher **noch nicht inhaltlich geprüft**. Sie sind ein priorisierter nächster Abrufpunkt.
- Zylinder- und Tropfenbedingungen nicht ohne explizite thermische und geometrische Randbedingungen zusammenwerfen. Druckzell-/erzwungene Daten bleiben Klasse X.

### 3.2 Dissertation und KIT-Repositorium

**Wilhelm, S. (2017).** *Über die Synärese kolloidaler Strukturen am Beispiel von Siliciumdioxid*. KIT Scientific Publishing. DOI: [10.5445/KSP/1000073100](https://doi.org/10.5445/KSP/1000073100).  
Institutioneller Volltext/Datensatz: https://publikationen.bibliothek.kit.edu/1000052536/3796774

- Dient zum Gegenprüfen der 2015er Artikelwerte, Methoden und Figuren.
- Die Dissertation enthält für basische Tropfen eine von Tabelle 2 des Artikels abweichende Tabelle. Diese Abweichung ist als separater Quellenzweig zu erhalten, nicht zu mitteln.
- Keine unabhängige Replikation von Wilhelm & Kind (2015): gleiche Forschungsgruppe und eng verwandter Datensatz.

### 3.3 Mechanik natürlicher Synärese — verwandtes, aber nicht identisches Silicasystem

**Scherer, G. W. (1989).** *Mechanics of syneresis I. Theory*. Journal of Non-Crystalline Solids 108(1), 18–27. DOI: [10.1016/0022-3093(89)90328-1](https://doi.org/10.1016/0022-3093(89)90328-1).

- Theoretischer Beitrag: Größeneffekt, Porenflüssigkeitsströmung und viskoelastisches Netzwerk.
- Geeignet als unabhängige theoretische Strukturprüfung des hydraulisch-mechanischen CCFSM-Blocks.
- Keine direkte Parameterquelle für gefällte Silica aus Natriumsilikat.

**Scherer, G. W. (1989).** *Mechanics of syneresis II. Experimental study*. Journal of Non-Crystalline Solids 108(1), 28–36. DOI: [10.1016/0022-3093(89)90329-3](https://doi.org/10.1016/0022-3093(89)90329-3).  
Bibliographischer Nachweis/Abstract: https://collaborate.princeton.edu/en/publications/mechanics-of-syneresis-ii-experimental-study/

- Experimentelle Schrumpfungsverläufe von Silicagelen; der Abstract berichtet eine Übereinstimmung mit Rechnungen, in denen Permeabilität, Modul und Viskosität unabhängig gemessen wurden.
- Sehr relevant für die Frage, ob ein gekoppeltes poro-viskoelastisches Modell prinzipiell durch unabhängige Materialparameter gestützt werden kann.
- Das Gel ist alkoxid-/TEOS-basiert und daher chemisch nicht gleich dem gefällten Natriumsilikat-Silica-Zielsystem.
- Zeitkurven und gegebenenfalls Parameter aus dem Volltext müssen erst originalgetreu extrahiert werden. Bis dahin keine Zahlenwerte in die Zielsystemkalibrierung übernehmen.

### 3.4 Struktur- und Modulentwicklung in TEOS-Silicagelen

**Scherer, G. W. (1989).** *Effect of shrinkage on the modulus of silica gel*. Journal of Non-Crystalline Solids 109, 183–190. DOI: [10.1016/0022-3093(89)90030-6](https://doi.org/10.1016/0022-3093(89)90030-6).  
Volltext-PDF: https://belinra.inrae.fr/doc_num.php?explnum_id=3120

- Volltext geprüft. TEOS-abgeleitete Gele; 6-mm-Stäbe; Säure- und Basenkatalyse; Modul gegen Alter und lineare Schrumpfung.
- Der Text berichtet z. B. eine empirische Beziehung für getrocknete B2-Gele: G(MPa) = 0.13 exp(0.17 ε[%]). Diese Beziehung gilt für die beschriebenen Trocknungsdaten und darf **nicht** als Natur-Synäresegesetz oder als gefällte-Silica-Koeffizient verwendet werden.
- Der Autor unterscheidet Alterung im Porenfluid von Trocknung; Alterung kann den Modul ohne proportionale Schrumpfung erhöhen. Das ist ein wertvoller qualitativer Hinweis gegen eine einfache Eins-zu-eins-Kopplung von Schrumpfung und Steifigkeit.
- Figuren 1–7 enthalten diagrammatische Daten. Eine Pixel-Digitalisierung wäre möglich, aber zunächst nur als TEOS-Mechanismen-/Vergleichsdatensatz (Klasse B nach erfolgter Kalibrierung).
- Der Artikel verweist auf ²⁹Si-NMR-Befunde einer früheren Arbeit, nicht auf einen direkt verfügbaren Lastbrückenzähler.

### 3.5 Permeabilität

**Scherer, G. W.; Swiatek, R. M. (1989).** *Measurement of permeability II. Silica gel*. Journal of Non-Crystalline Solids 113(2–3), 119–129. DOI: [10.1016/0022-3093(89)90002-1](https://doi.org/10.1016/0022-3093(89)90002-1).

- Der publizierte Abstract beschreibt eine Druckgradientenmessung in dünnen Gelplatten (~2 mm), um viskoelastische Effekte zu minimieren.
- Für ein homogenes säurekatalysiertes Gel stimmt die Größenordnung mit Carman–Kozeny überein; für ein inhomogenes basenkatalysiertes Gel ist die gemessene Permeabilität größer als vorhergesagt. Teilweises Trocknen senkt die Permeabilität um ungefähr zwei Größenordnungen.
- Das ist ein mechanistisch relevanter Permeabilitätsdatensatz, aber TEOS-/Alkoxid-System, nicht gefällte Silica. Zahlenwerte aus dem Volltext und deren Einheiten/Definition müssen vor Verwendung geprüft werden.
- Nicht aus dem Abstract eine numerische Permeabilität erfinden.

### 3.6 Review-/Kontextquelle für viskoelastische und hydraulische Kopplung

**Scherer, G. W. (1996).** *Influence of Viscoelasticity and Permeability on the Stress Response of Silica Gel*. Langmuir 12(5), 1109–1116. DOI: [10.1021/la9503111](https://doi.org/10.1021/la9503111).

- Review/Mechanismenbeitrag zu Alterung, Temperatur, Deformation und Trocknung.
- Unterstützt die qualitative Aussage, dass die Antwortzeiten von Permeabilität und Netzwerkmodul abhängen.
- Kein eigenständiger neuer Datensatz ohne Prüfung des Volltexts; keine automatische Übertragung auf gefällte Silica.

**Scherer, G. W. (1997).** *Effect of drying on properties of silica gel*. Journal of Non-Crystalline Solids 215(2–3), 155–168. DOI: [10.1016/S0022-3093(97)00079-3](https://doi.org/10.1016/S0022-3093(97)00079-3).

- Permeabilität und viskoelastische Eigenschaften werden während der Trocknung verfolgt.
- Prozessklasse X (Trocknung); hilfreich für mögliche Dichte-/Porositätsabhängigkeit, nicht als natürliche Synäresekalibrierung.

### 3.7 Gefällte Silica: Gelbildung und Morphologie

**Quarch, K.; Kind, M. (2010).** *Inorganic Precipitated Silica Gel. Part 1: Gelation Kinetics and Gel Properties*. Chemical Engineering & Technology 33(6), 1034–1039. DOI: [10.1002/ceat.201000080](https://doi.org/10.1002/ceat.201000080). KITopen: https://publikationen.bibliothek.kit.edu/1000033921

- Zielsystemnah für Gelbildung und Gel-Eigenschaften.
- Im derzeit erschlossenen Quellenstand kein gleichwertiger Satz vollständiger natürlicher S(t)-Kurven identifiziert.
- Als Rezeptur-/Gelbildungs-/Strukturkontext verwenden; konkrete Tabellen/Figuren separat prüfen, bevor Zahlen in Register übernommen werden.

**Quarch, K. (2010).** *Produktgestaltung an kolloidalen Agglomeraten und Gelen – Gelierung und Fragmentierung anorganisch gefällten Siliciumdioxids*. KIT Scientific Publishing. ISBN 978-3-86644-503-1.

- Dissertation; ergänzende Prozess-, Gelierungs- und Strukturinformationen.
- Qualitative Synäresehinweise nicht als quantitative Zeitkurven behandeln, sofern keine expliziten Messwerte gefunden werden.

**Schlomach, J.; Kind, M. (2004).** *Investigations on the semi-batch precipitation of silica*. Journal of Colloid and Interface Science 277(2), 316–326. DOI: [10.1016/j.jcis.2004.04.051](https://doi.org/10.1016/j.jcis.2004.04.051).
- Zielsystemnah: Fällung aus Natriumsilikat und Schwefelsäure im 5-L-Rührkessel bei 83 °C; Photonenkorrelationsspektroskopie für Aggregationsentwicklung.
- Der Abstract berichtet einen reaktionslimitierten Aggregationskernel mit A = 1 und B′(t) = 3,4×10⁻²⁰ bis 2,6×10⁻²⁰ L/min, eine Fraktaldimension der Gelcluster von zunächst etwa 1,8, rasch ansteigend auf etwa 2,4, eine spezifische Oberfläche von 480 auf 300 m²/g sowie Primärpartikel mit 22,7 nm.
- Diese Werte sind wertvolle Struktur-/Fällungsanker für die chemisch-morphologische Vorgeschichte des CCFSM. Sie sind **keine** Messungen der zeitabhängigen natürlichen Synärese nach Gelpunkt und identifizieren weder Porenpermeabilität noch tragende Brückendichte.
- Abstractdaten sind Evidenzklasse E, bis die Originaltabellen/Figuren und Messdefinitionen aus dem Volltext geprüft sind.

### 3.8 Ausschluss-/Vergleichsquelle: erzwungene Konsolidierung

**Sahabi, H.; Kind, M. (2011).** *Consolidation of Inorganic Precipitated Silica Gel*. Polymers 3(3), 1423–1432. DOI: [10.3390/polym3031423](https://doi.org/10.3390/polym3031423).

- Oedometer-/mechanische Konsolidierung; nicht natürliche, unbelastete Synärese.
- Nur als separater Vergleichsast für mechanische Antwort/Modellgrenzen; keine Kalibrierung von natürlichem k_h, S_max oder τ.

## 4. Was die Literatur bereits quantitativ trägt

### Zielsystem (gefällte Silica)

1. Wilhelm & Kind (2015) liefern publizierte natürliche Zylinder- und Tropfen-Fitparameter (A/ΔV/V₀,max und τ) für Säure-/Basenbedingungen und 20/40/60 °C.
2. Für Zylinder sind die zwölf Kennwerte (sechs Amplituden, sechs Zeitkonstanten) die robusteste bisherige quantitative Basis im Projekt.
3. Tropfen bleiben wegen thermischer Vorgeschichte und ungelöster Figure-10b-Tabellen-Diskrepanz ein eigener Prüfzweig.
4. Die 164 KI-gestützten Kurvenablesungen sind nur Klasse D und bleiben von den Tabellenwerten getrennt.
5. Die publizierte Porenflüssigkeits-Siliciumsäurekonzentration aus Figur 9 ist ein zusätzlicher chemischer Anker, jedoch keine direkte Messung von tragender Brückendichte.

### Verwandte TEOS-Silicagel-Systeme

1. Scherer (1989) bietet direkte experimentelle Hinweise, dass Synereseantworten mit unabhängig gemessenen Permeabilitäts- und viskoelastischen Größen verknüpft werden können.
2. Scherer (1989) liefert Diagrammdaten zur Modul-/Schrumpfungs-/Alterungsentwicklung und zeigt, dass Alterung den Modul auch ohne proportionale Schrumpfung verändern kann.
3. Scherer & Swiatek (1989) liefert eine eigenständige Permeabilitätsmethodik und qualitative Größenordnungs-/Trendinformation.
4. Diese Daten können die mathematisch-physikalische Struktur des CCFSM prüfen, aber nicht ohne Transfermodell die Koeffizienten der gefällten Silica ersetzen.

## 5. Konsequenz für die CCFSM-Parameter

| CCFSM-Größe | Was vorhandene Literatur tatsächlich liefert | Status |
|---|---|---|
| S(t), S_max, τ | Wilhelm & Kind Tabellen/Figuren; Scherer-Synerese-Figuren für anderes Gel | Zielsystem teilweise quantifizierbar |
| Temperatur-/pH-Effekt | Wilhelm & Kind Bedingungen und Fitparameter | empirisch beschreibbar; Mechanismus nicht eindeutig identifiziert |
| Geometrie-/Drainageeffekt | Zylinder/Tropfen bei Wilhelm & Kind; Scherer-Größeneffekt | Randbedingungen kritisch; kein universelles L_d^-2 ungeprüft |
| gelöstes Si im Porenfluid | Wilhelm & Kind Figur 9 | chemischer Proxy/Teilinformation |
| Kondensation/Netzwerkentwicklung | Quarch-/Schlomach-Kontext; Scherer-NMR-Zitate und Modultrends | kein direkter, gemeinsamer Zeitverlauf von Qⁿ und S(t) gefunden |
| G oder viskoelastische Antwort | Scherer (1989) für TEOS-Gele | mechanistischer Vergleich, kein gefällte-Silica-Koeffizient |
| Permeabilität | Scherer & Swiatek (1989), TEOS-Gel | Methodik/Mechanismusvergleich; Volltextwerte noch zu extrahieren |
| D_f, Porenhals/Konnektivität | einzelne Strukturarbeiten möglich, aber kein synchroner Zielsystemdatensatz gesichert | nicht ausreichend identifiziert |
| B_eff, z, σ, q, η_a, k_r | keine direkte vollständige unabhängige Messung in den derzeit erschlossenen Zielsystemdaten | latent/nicht identifiziert; nicht aus S(t) rückrechnen |

**Kernschluss:** Wir können eine belastbare empirische Beschreibung der äußeren natürlichen Schrumpfung und einen physikalisch begründeten Modellrahmen entwickeln. Die vorhandene Literatur rechtfertigt derzeit aber keine eindeutige Identifikation aller chemischen, strukturellen und mechanischen Zustände des vollständigen CCFSM.

## 6. Priorisierte nächste Literaturarbeit

1. **Supplementary Materials Wilhelm & Kind (2015):** Tabellen S1–S7 und Figuren S1–S6 sichern, lokal/maschinenlesbar erfassen und nur die natürlich-synereserelevanten Inhalte markieren.
2. **Scherer (1989) Part II:** Volltext sichern, Geometrie/Rezeptur/Alterung/Drainagebedingungen rekonstruieren, natürliche Syneresekurven mit Pixelkalibrierung extrahieren.
3. **Scherer & Swiatek (1989):** Volltextzahlen und Einheiten für Permeabilität prüfen; Materialzustand und Messprotokoll erfassen.
4. **Schlomach & Kind (2004):** Strukturanker (D_f, Primärpartikelgröße, spezifische Oberfläche und Aggregationskinetik) aus Originalfiguren/-tabellen mit Messdefinitionen absichern; strikt als Fällungs-/Gelpunkt-Vorgeschichte behandeln.
5. **Scherer (1989) Modulpaper:** Figuren 1–7 reproduzierbar digitalisieren, aber in separater TEOS-Datenklasse.
6. **Quarch/KITopen:** konkrete struktur- und gelbildungsbezogene Messgrößen und Quellenstellen ergänzen.
7. **Datenbank erweitern:** jeden extrahierten Zahlenwert mit Quelle, Seite/Figur/Tabelle, Originaleinheit, Umrechnung, Evidenzklasse, Prozessklasse und Freigabestatus dokumentieren.
8. **Modellvergleich:** zunächst ein reduziertes, identifizierbares Modell an Wilhelm & Kind; Scherer-Daten als externe Mechanismenprüfung, nicht als gepoolte Kalibrierung.

## 7. Publikationsethik und Claim-Grenzen

- Keine Behauptung eigener Experimente.
- Keine KI-Ablesung als Rohdaten ausgeben.
- Keine aus Diagrammen rekonstruierten Punkte ohne Pixelkoordinaten, Achsenkalibrierung und Unsicherheiten als Klasse B deklarieren.
- Keine unabhängige Replikation behaupten, wenn mehrere Arbeiten aus derselben Arbeitsgruppe oder Datenlinie stammen.
- Keine Zwangs-/Druckzell-/Oedometerdaten als natürliche Synärese fitten.
- Keine TEOS-/Alkoxid-Daten als gleichwertige gefällte-Silica-Daten poolen.
- Softwaretests belegen Softwareverifikation, nicht physikalische Validierung.
- Mathematische Eigenschaften der Gleichungen sind keine empirischen Beweise der Stoffgesetze.

## Quellenzugriff im Recherchelauf

- Wilhelm & Kind (2015), Volltext und Tabellen 1/2: MDPI-Seite erfolgreich geprüft.
- Supplement-Link auf der MDPI-Seite gefunden, automatischer Abruf des Supplement-Pakets jedoch fehlgeschlagen; Inhalte bleiben offen.
- Scherer (1989), *Effect of shrinkage on the modulus*: vollständiger INRAE-PDF-Text erfolgreich geprüft.
- Scherer (1989), *Mechanics of syneresis II*: bibliographischer Nachweis und Abstract über Princeton geprüft; Volltextzahlen noch nicht extrahiert.
- Scherer & Swiatek (1989) und Scherer (1996): bibliographische Angaben und Abstracts geprüft; Verlagsvolltexte nicht direkt abrufbar.
