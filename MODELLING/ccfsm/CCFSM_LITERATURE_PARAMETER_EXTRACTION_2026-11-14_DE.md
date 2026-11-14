# Literatur-Parameterextraktion für CCFSM – Stand 2026-11-14

## Zweck und Abgrenzung

Diese Datei erfasst veröffentlichte Mess- und Modellwerte aus Wilhelm & Kind, Quarch, Schlomach & Kind sowie Sahabi & Kind. **Natürliche, mechanisch unbelastete Synärese** wird strikt von erzwungener Synärese/Oedometer-Konsolidierung und von gerührter Gelbildung/Fragmentierung getrennt. Werte aus den letztgenannten Versuchen dürfen nicht als direkte Kalibrierpunkte der natürlichen Synärese verwendet werden.

Kennzeichnung:
- **D**: im Text oder in einer Tabelle direkt berichtet.
- **G**: aus einer Abbildung zu digitalisieren; noch kein Rohmesswert.
- **A**: abgeleiteter bzw. modellangepasster Kennwert.
- **Q**: qualitativ berichtet, keine belastbare numerische Messreihe.
- **X**: anderer Prozess (z. B. erzwungene Konsolidierung), nicht in Natural-Syneresis-Fit aufnehmen.

## 1. Wilhelm & Kind (2015): natürliche Synärese

Quelle: S. Wilhelm & M. Kind, *Polymers* 7 (2015), 2504–2521, DOI 10.3390/polym7121528. Die Autoren passen die gemessene relative Volumenabnahme mit
\[
S(t)=S_{\max}\,[1-\exp(-t/\tau)]
\]
an. (S_{max}) und \(\tau\) sind somit **modellangepasste Kennwerte**, keine separat direkt gemessenen Materialkonstanten.

### Zylindrische Proben (D/A)
Geometrie: Durchmesser 12 mm, Gelvolumen ca. 3 mL.

| T (°C) | Katalyse | S_max (-) | tau (h) |
|---:|---|---:|---:|
| 20 | sauer | 0.20 | 21.3 |
| 20 | basisch | 0.30 | 50.1 |
| 40 | sauer | 0.20 | 11.7 |
| 40 | basisch | 0.39 | 32.0 |
| 60 | sauer | 0.20 | 5.0 |
| 60 | basisch | 0.51 | 27.5 |

### Geltröpfchen (D/A)
Geometrie: Durchmesser ca. 3 mm. Die Tröpfchen waren zunächst während der ersten 30 min bei 20 °C; danach wurde auf die Zieltemperatur eingestellt. Daher sind die Temperaturbedingungen keine idealen isothermen Startbedingungen.

| T (°C Ziel) | Katalyse | S_max (-) | tau (h) |
|---:|---|---:|---:|
| 20 | sauer | 0.37 | 0.40 |
| 20 | basisch | 0.30 | 0.67 |
| 40 | sauer | 0.41 | 0.64 |
| 40 | basisch | 0.39 | 0.57 |
| 60 | sauer | 0.48 | 0.77 |
| 60 | basisch | 0.51 | 0.95 |

### Weitere direkte Angaben
- Isoelectric point für das Schwefelsäure-System: pH_iso ca. 1.7–2.
- Für zylindrische natürliche Synärese: Monomer-Kieselsäure im ausgepressten Porenwasser ca. 0.2–0.4 mmol/L (sauer) und ca. 100–200 mmol/L (basisch). Das sind Messwerte der Porenflüssigkeit, nicht die gesamte gelbildende Si-Konzentration.
- Für die saure Zylinderprobe wird S_max = 0.20 unabhängig von 20/40/60 °C berichtet; die Temperatur beschleunigt vor allem die Kinetik.
- Kleinere Proben schrumpfen schneller und zeigen höhere maximale Schrumpfung. Die Porenflüssigkeit der kleinen Tröpfchen konnte wegen der geringen Menge nicht analysiert werden.
- Der Artikel weist selbst darauf hin, dass ein physikalisch begründetes Modell noch aussteht.

**CCFSM-Nutzung:** Zylinderwerte sind die bevorzugten natürlichen Makro-Synerese-Kalibrierpunkte. Tröpfchenwerte separat als Geometrie-/Längenskalen-Datensatz halten. Niemals beide Geometrien ohne Geometrievariable gemeinsam fitten.

## 2. Quarch (2010): Gelbildung, Alterung und qualitative Schrumpfung

Quelle: K. Quarch, *Produktgestaltung an kolloidalen Agglomeraten und Gelen – Gelierung und Fragmentierung anorganisch gefällten Siliciumdioxids*, KIT Dissertation, 2010.

### Für CCFSM verwertbare Angaben
- Ein basisches Gel gelierte im beschriebenen Vorversuch ca. 35 min nach Mischung; Entnahme nach 45 min. (D)
- Rezeptangabe für diesen Alterungsversuch: 0.084 g Silikat + 0.016 g H2SO4 je g H2O. (D; Bezugsbasis beachten, keine Konzentration ohne weitere Rezeptdetails ableiten.)
- Frische und 1 Tag gealterte basische Gele unterschieden sich deutlich; ab etwa einer Woche waren keine Unterschiede in der beschriebenen Partikelgrößen-/Dispergierkurve mehr feststellbar. (Q/D)
- Gegossene Gelkörper konnten erst ab dem zweiten Tag zerstörungsfrei entformt werden; die Schrumpfung unter den verwendeten Bedingungen war so klein, dass sie nur qualitativ beobachtet werden konnte. (Q)
- Bei 95 °C entstanden im Inneren der Gelkörper bleibende Blasen. Eine mögliche, ausdrücklich als Erklärung diskutierte Hypothese ist, dass Synärese so schnell abläuft, dass das Wasser nicht schnell genug aus dem Gelblock diffundieren kann. Das ist kein quantitatives S_max- oder tau-Datum. (Q)
- Höhere Na2SO4-Konzentration (45 g/kg H2O statt regulär 22.5 g/kg) und Absenkung des pH beeinflussten Partikelgrößen/Dispergierbarkeit; höhere Salzkonzentration beschleunigte die beobachtete Schrumpfung. Die Experimente beinhalteten Umgebungs-/Verdünnungsänderungen und sind nicht ohne Weiteres natürliche, geschlossene Synärese. (Q)
- Batch-Prozess-Kohäsionskräfte aus Tabelle 4.3: sauer 320 ± 263 nN; basisch 95 ± 37 nN; +20 g Na2SO4 170 ± 122 nN; 80 °C 712 ± 687 nN. **X:** aus gerührtem Batch-/Fragmentierungszusammenhang, nicht als natürliche Synerese-Parameter einsetzen.

**CCFSM-Nutzung:** Quarch liefert wertvolle Zeit- und Rezeptkontexte, Alterungs-/Salz-Einfluss und qualitative Mechanismushinweise. Die Dissertation liefert für die hier untersuchten gegossenen Körper keine belastbare quantitative natürliche Schrumpfkurve; daraus keine numerischen CCFSM-Synerese-Koeffizienten fitten.

## 3. Schlomach & Kind (2004): Primärpartikel und Aggregatstruktur

Quelle: J. Schlomach & M. Kind, *Investigations on the semi-batch precipitation of silica*, J. Colloid Interface Sci. 277 (2004), 316–326, DOI 10.1016/j.jcis.2004.04.051.

Direkt im Abstract berichtet:
- Primärpartikelgröße: 22.7 nm. (D)
- Fraktale Dimension der Gelcluster zunächst ca. 1.8, steigt rasch auf ca. 2.4 und bleibt anschließend ungefähr konstant. (D; Prozess-/Versuchsverlauf, nicht universelle Stoffkonstante)
- Spezifische Oberfläche sinkt von 480 auf 300 m²/g. (D)
- Aggregationskern-Koeffizient B'(t) liegt zwischen 3.4×10^-20 und 2.6×10^-20 1/min und ist nur schwach zeitabhängig; der Reaktions-limitierte Aggregationskern ist proportional zu B'(t)[q(p-q)]^(A/2), A=1. (D; nur für die dortige Aggregationsmodellierung und deren Definitionen verwenden)

**CCFSM-Nutzung:** (D_f\approx1.8\to2.4), Primärpartikelgröße und BET-Oberfläche können als Morphologie-/Strukturanker dienen. Sie sind keine direkte natürliche Synärese-Kinetik. Die (D_f)-Werte dürfen nicht ungeprüft mit den (D_f)-Definitionen anderer Mess-/Simulationsmethoden gleichgesetzt werden.

## 4. Sahabi & Kind (2011): MD-Modell und Oedometer-Konsolidierung

Quelle: H. Sahabi & M. Kind, *Experimentally Justified Model-Like Description of Consolidation of Precipitated Silica*, *Polymers* 3 (2011), 2156–2171, DOI 10.3390/polym3042156.

### MD-Modell (Modellparameter, nicht direkt gemessene Materialwerte)
- Gelcluster: 1,000 Primärpartikel; Lösungsmittelumgebung ca. 400,000 Lösungsmittelpartikel. (D)
- LAMMPS, Nosé–Hoover NPT bzw. konstante Spannung; dimensionslose Größen. (D)
- Partikelwechselwirkung über integrierte Lennard-Jones-12-6-Potentiale (Anziehung/van-der-Waals und Born/Pauli-Abstoßung); zusätzlich wird ein DLVO-artiger elektrostatischer Term diskutiert. (D)
- Die Übereinstimmung der MD-Zeitkurve mit dem Experiment erforderte eine Zeitgewichtung um Faktor 100 (1 min = 100 Simulationszeitschritte); die Autoren benennen verbleibende Modellunvollständigkeit. (D)

### Experimentelle Vergleichsdaten
- Die zeitabhängige Fraktaldimension stammt aus dem gerührten Schlomach-Versuch; Sahabi & Kind weisen ausdrücklich darauf hin, dass sie nur für diesen spezifischen Versuch gilt. (D)
- Die makroskopischen Konsolidierungskurven wurden mittels Oedometer unter verschiedenen pH-/Temperaturbedingungen erhoben. (X: mechanisch belastete/erzwungene Konsolidierung, keine natürliche Synerese.)
- Daher dürfen Oedometer-Kurven nicht in den natürlichen CCFSM-Shrinkage-Fit übernommen werden. Sie können separat zur Prüfung von Material-/Strukturmechanismen oder für ein eigenes erzwungenes Konsolidierungsmodell dienen.

## 5. Empfohlene Zuordnung zu CCFSM

| CCFSM-Größe / Teilmodell | Literaturanker | Status / Einschränkung |
|---|---|---|
| (S_{max},\tau) natürliche Synärese | Wilhelm & Kind 2015, Zylinder | quantitative Kalibrierwerte, modellangepasst |
| Geometrieabhängigkeit von (S_{max},\tau) | Wilhelm & Kind 2015, Tröpfchen | eigener Datensatz, andere Längenskala und Temperaturhistorie |
| (D_f) | Schlomach & Kind 2004 | Strukturanker, methodenspezifisch |
| Primärpartikelradius/-durchmesser | Schlomach & Kind 2004 | 22.7 nm Durchmesser |
| Spezifische Oberfläche | Schlomach & Kind 2004 | 480→300 m²/g |
| Gelierungs-/Alterungszeit | Quarch 2010 | ca. 35 min Gelierung, ca. 1 Woche bis Kurvenplateau im konkreten basischen Versuch |
| Salz-/pH-Einfluss | Quarch 2010 | qualitativ bzw. kontextgebunden; keine universelle Gesetzmäßigkeit |
| Interaktionspotentiale/MD-Setup | Sahabi & Kind 2011 | Modellarchitektur, nicht direkt kalibrierte CCFSM-Konstanten |
| Oedometer-Konsolidierung | Sahabi & Kind 2011 | getrennt halten; nicht Natural-Syneresis-Fit |

## 6. Offene Extraktionsarbeiten
1. Digitale Punkt-für-Punkt-Extraktion der natürlichen Synäresekurven aus Wilhelm & Kind 2015 (Abb. 8 und 10), mit Achsenkalibrierung, Pixel-/Digitalisierungsunsicherheit und getrenntem Geometrie-/Temperatur-Tag.
2. Vollständige Extraktion der Rezept-/Prozessbedingungen aus den Methoden und Tabellen von Quarch sowie Schlomach, inklusive Wasserglasmodul, Feststoffgehalt, Säurekonzentration, Dosierprofil, pH und Ionenstärke, soweit tatsächlich angegeben.
3. Tabellen-/Kurvenextraktion der Sahabi-Oedometerdaten in einen separaten Datensatz mit Kennzeichnung „erzwungen“.
4. Keine CCFSM-Koeffizienten aus einzelnen Endpunkten rückwärts konstruieren, wenn mehrere Parameter nicht identifizierbar sind. Fits mit Unsicherheiten und Parameterkorrelationen ausweisen.

## Quellen
- Wilhelm & Kind (2015): https://doi.org/10.3390/polym7121528
- Quarch (2010): https://doi.org/10.5445/KSP/1000073100
- Schlomach & Kind (2004): https://doi.org/10.1016/j.jcis.2004.04.051
- Sahabi & Kind (2011): https://doi.org/10.3390/polym3042156
