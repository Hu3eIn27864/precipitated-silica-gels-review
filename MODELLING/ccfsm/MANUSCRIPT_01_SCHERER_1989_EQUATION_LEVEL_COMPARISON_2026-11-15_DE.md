# Scherer (1989) und das v0.2-Zweizeitenmodell – Gleichungs- und Reduktionsaudit

**Stand:** 15. November 2026  
**Status:** Literaturgestützte Strukturprüfung; noch keine Gleichung-für-Gleichung-Rekonstruktion des vollständigen Originalartikels.

## 1. Ziel und Quellenlage

Verglichen wird das phänomenologische Modell

\[
\dot q=k_n(q_\infty-q),\qquad
\dot S=k_h(\eta_a q-S)
\tag{V0.2}
\]

mit George W. Scherer, *Mechanics of Syneresis I. Theory*, Journal of Non-Crystalline Solids 108 (1989), 18–27, DOI: 10.1016/0022-3093(89)90328-1, und Teil II, *Experimental Study*, S. 28–36, DOI: 10.1016/0022-3093(89)90329-3.

Die zugänglichen Verlags- und Princeton-Nachweise geben Abstract, bibliographische Daten und die Kernaussagen wieder, aber nicht den vollständigen Gleichungstext von Teil I. Der Verlagsvolltext war in der Recherche nicht zugänglich. Deshalb werden hier **keine angeblichen Originalgleichungsnummern oder wörtlichen Formeln Scherers rekonstruiert**. Eine exakte Reduktion darf erst nach Prüfung einer rechtmäßig zugänglichen vollständigen Kopie behauptet werden.

## 2. Was Scherer nachweislich modelliert

Aus dem Abstract von Teil I ergeben sich folgende physikalische Bestandteile:

1. Synärese ist spontane Gelkontraktion mit gleichzeitiger Auspressung von Flüssigkeit aus den Poren; sie kann auch ohne Verdunstung und bei Eintauchen des Gels in Flüssigkeit auftreten.
2. Die Kontraktionsgeschwindigkeit hängt von der Probengröße ab, weil die kleinen Poren den Flüssigkeitsstrom aus dem Gel behindern.
3. Die Theorie behandelt Platten und Zylinder.
4. Eine anfänglich langsame Kontraktion wird durch den allmählichen Druckanstieg in der Porenflüssigkeit erklärt, während das viskoelastische Netzwerk diese Flüssigkeit komprimiert.
5. Teil II wendet die Theorie auf Silicagel-Schrumpfdaten an. Kurvenform und Rate hängen laut Abstract von Permeabilität sowie viskoelastischen Eigenschaften ab; die gemessenen Kurven stimmten vernünftig mit Berechnungen unter Verwendung unabhängig gemessener Permeabilität, Modul und Viskosität überein.

Diese Punkte sind bereits eine klare mechanistische Vorarbeit. Eine Behauptung, die Kopplung von Netzwerkmechanik und Porenflüssigkeitstransport sei neu, wäre daher unhaltbar.

## 3. Strukturvergleich

| Physikalische Rolle | Scherer (1989), nach zugänglichem Abstract | v0.2 |
|---|---|---|
| Netzwerkmechanik | viskoelastische Gelmatrix komprimiert Porenflüssigkeit | latent gebündelt in q |
| Porenflüssigkeit | Druckaufbau und Flüssigkeitsausstrom | nicht explizit als Druck oder Flüssigkeitsvolumen modelliert |
| Transportwiderstand | Permeabilität und Probengröße | in k_h nur als effektive Rate repräsentierbar |
| Geometrie | explizit Platten und Zylinder | keine räumliche Geometrie |
| Messgröße | makroskopische Kontraktion/Shrinkage | S |
| zeitliche Struktur | anfängliche Verzögerung durch Druckaufbau; Kurvenform aus gekoppelter Mechanik und Transport | zwei gekoppelte Relaxationsstufen |

**Zwischenbefund:** V0.2 ist keine nachgewiesene algebraische oder asymptotische Reduktion von Scherer. Es ist zunächst ein niedrigdimensionales Ersatzmodell, das zwei zeitliche Rollen unterscheidet. Ob diese Rollen genau den Eigenmoden oder den physikalischen Zuständen des Scherer-Modells entsprechen, ist offen.

## 4. Was eine legitime Reduktion mindestens benötigen würde

Eine belastbare Herleitung müsste in nachvollziehbarer Reihenfolge zeigen:

1. **Ausgangssystem:** vollständige Impuls-/Gleichgewichtsbeziehung für das Netzwerk, viskoelastisches Stoffgesetz, Flüssigkeitsbilanz und Darcy-Gesetz mit den bei Scherer verwendeten Annahmen.
2. **Geometrie und Randbedingungen:** Platte oder Zylinder, Symmetrie-/Zentrumsbedingung und Flüssigkeitsdruck bzw. Fluss am Rand. Die Randbedingungen sind entscheidend für die räumlichen Eigenwerte.
3. **Linearisation:** Angabe des Referenzzustands und der Größenordnung, in der Materialparameter und Geometrie als konstant behandelt werden dürfen.
4. **Räumliche Reduktion:** Herleitung einer dominanten Druck-/Transportmode oder eines kontrollierten Einmodenansatzes. Die zugehörige Rate muss aus Permeabilität, Kompressibilität/Modul, Viskosität und charakteristischer Länge folgen.
5. **Netzwerkzustand:** eigenständige Definition einer inneren Netzwerk-Kontraktionsvariable q samt konstitutiver Relaxationsgleichung. Ein solcher Zustand folgt nicht allein aus der Existenz einer viskoelastischen Matrix; er muss aus dem konkreten Stoffgesetz abgeleitet werden.
6. **Ausgangsgröße:** Herleitung, wie die gemessene Schrumpfung S aus Netzwerkdeformation, Porenflüssigkeitsabfluss und ggf. Probengeometrie berechnet wird.
7. **Fehlerkontrolle:** Vergleich der reduzierten Lösung mit dem räumlichen Ausgangsmodell über den beanspruchten Parameter- und Zeitbereich.

Ohne diese Schritte wäre die Formulierung „aus Scherer hergeleitet“ zu stark.

## 5. Mathematische Plausibilität von v0.2 als Ersatzmodell

V0.2 hat die Form einer linearen Kaskade:

\[
q(t)=q_\infty+(q_0-q_\infty)e^{-k_nt},
\]

und S relaxiert mit Rate k_h gegen den zeitabhängigen Zielwert \(\eta_aq(t)\). Für \(k_h\ne k_n\) ergibt sich

\[
S(t)=\eta_aq_\infty+(S_0-\eta_aq_\infty)e^{-k_ht}
+\frac{\eta_a k_h(q_0-q_\infty)}{k_h-k_n}
(e^{-k_nt}-e^{-k_ht}).
\]

Damit enthält die Antwort zwei exponentielle Zeitanteile. Das ist als kompakte Beschreibung einer zweistufigen Dynamik plausibel. Es beweist aber nicht, dass die beiden Exponenten mit zwei physikalisch eindeutig getrennten Prozessen Scherers identisch sind.

Wichtige Interpretationsgrenzen:

- q ist derzeit eine **latente effektive Kontraktionsvariable**, kein direkt gemessener Netzwerkdehnungs-, Spannungs- oder Reaktionsfortschrittsparameter.
- S ist eine dimensionslose Schrumpfungsgröße; die genaue experimentelle Definition (linear, radial, volumetrisch oder normiert) muss im Manuskript festgelegt werden.
- k_n und k_h haben die Dimension Zeit⁻¹. Ihre physikalischen Bedeutungen sind erst nach Herleitung oder unabhängiger Messung abgesichert.
- η_a ist dimensionslos und skaliert den auf S wirksamen Anteil des latenten Zustands. „Accessibility“ ist bisher eine Modellinterpretation, keine aus Scherer abgeleitete Materialkonstante.
- Ein einfacher erster räumlicher Diffusions-/Konsolidierungsmodus kann eine Rate proportional zu einer effektiven Diffusivität geteilt durch L² liefern. Daher ist k_h ∝ L⁻² nur unter expliziten Annahmen über Geometrie, Randbedingungen, konstante Koeffizienten und Modendominanz zulässig. Es ist keine universelle Aussage über Scherers vollständige Lösung.

## 6. Ein entscheidender Unterschied: Druckaufbau ist nicht automatisch eine Netzwerkkinetik

Scherers Abstract beschreibt eine Verzögerung, weil der Porenflüssigkeitsdruck während der Kompression durch das viskoelastische Netzwerk allmählich ansteigt. In v0.2 entwickelt sich dagegen q gegen q∞, und S folgt verzögert dem Wert η_a q.

Diese beiden Beschreibungen können qualitativ ähnliche Kurven erzeugen, sind aber nicht ohne Weiteres dieselbe Physik:

- Bei Scherer ist der Porenflüssigkeitsdruck eine zentrale dynamische Größe.
- In v0.2 ist kein Porenflüssigkeitsdruck vorhanden.
- Bei Scherer hängt der Transport explizit von Permeabilität und Geometrie ab.
- In v0.2 ist dieser Einfluss bislang in k_h verborgen.
- Die Gleichung für q setzt eine eigene Relaxationskinetik voraus; deren Identifikation mit der viskoelastischen Antwort muss erst bewiesen werden.

**Konsequenz:** Eine physikalisch ehrlichere Interpretation von v0.2 lautet vorläufig „phänomenologische Zweizeiten-Reduktion mit latenter Netzwerk-Kontraktionsvariable und verzögerter makroskopischer Schrumpfungsantwort“. Nicht: „Scherers Modell in reduzierter Form“.

## 7. Konkrete nächste Prüfungen

### 7.1 Volltext-Rekonstruktion

Vor einer formalen Reduktionsbehauptung müssen aus Scherer (1989), Teil I, extrahiert werden:
- Definitionen aller Feld- und Materialvariablen;
- konstitutive Gleichungen für viskoelastisches Netzwerk und Flüssigkeit;
- gekoppelte Feldgleichungen;
- Randbedingungen für Platte und Zylinder;
- analytische/numerische Lösung und Definition der gemessenen Schrumpfung.

Bis dahin bleibt die vorliegende Analyse ausdrücklich eine Abstract-basierte Strukturprüfung.

### 7.2 Zwei mögliche Modellpfade

**Pfad A – v0.2 beibehalten:** als phänomenologisches Minimalmodell. Dann muss es gegen die Scherer-Kurvenform und gegen die Wilhelm-Kind-Daten geprüft werden; Parameter sind zunächst effektiv und nicht automatisch mikrophysikalisch.

**Pfad B – physikalische Reduktion entwickeln:** aus einem poro-viskoelastischen Kontinuumsmodell eine reduzierte Zustandsdynamik ableiten. Dabei kann sich herausstellen, dass v0.2 modifiziert werden muss, etwa durch eine Druckvariable, eine andere Kopplungsstruktur oder mehrere räumliche Moden. Frühere v0.2-Arbeit bleibt als dokumentierter Modellstand erhalten.

## 8. Konsequenz für Neuheits- und Geltungsansprüche

Nicht zulässig:
- „Erstes physikalisches Modell der Synärese von Silicagelen“;
- „Erste Kopplung von Netzwerkrelaxation und Flüssigkeitstransport“;
- „V0.2 ist eine bewiesene Reduktion von Scherer (1989)“;
- „k_h ist generell proportional zu L⁻²“.

Derzeit vertretbar:
- v0.2 ist eine explizite, analytisch lösbare phänomenologische Zweizustandsbeschreibung;
- es macht die Austausch-Symmetrie der beiden Raten und die daraus folgende strukturelle Identifizierbarkeitsgrenze sichtbar;
- sein zusätzlicher physikalischer Nutzen gegenüber bestehenden poro-viskoelastischen Modellen ist noch durch Modellvergleich und Daten zu belegen.

## 9. Quellen

1. G. W. Scherer, “Mechanics of Syneresis I. Theory,” *Journal of Non-Crystalline Solids* 108 (1989), 18–27. DOI: [10.1016/0022-3093(89)90328-1](https://doi.org/10.1016/0022-3093(89)90328-1). Verlagsnachweis und Abstract: https://www.sciencedirect.com/science/article/abs/pii/0022309389903281
2. G. W. Scherer, “Mechanics of Syneresis II. Experimental Study,” *Journal of Non-Crystalline Solids* 108 (1989), 28–36. DOI: [10.1016/0022-3093(89)90329-3](https://doi.org/10.1016/0022-3093(89)90329-3).
3. Princeton Materials Research Group, Scherer publications list: https://gwsgroup.princeton.edu/publications/papers-by-george-scherer/

## 10. Auditentscheidung

**Ergebnis: V0.2 bleibt mathematisch als phänomenologisches Modell verwendbar; eine physikalische Ableitung aus Scherer ist nicht nachgewiesen.** Der nächste wissenschaftlich sinnvolle Schritt ist die Beschaffung und Prüfung des vollständigen Gleichungstextes von Scherer (1989), Teil I. Erst danach entscheiden wir, ob eine kontrollierte Reduktion möglich ist oder ob v0.2 als eigenständige empirisch zu prüfende Modellklasse stehen bleiben soll.

Diese Datei ergänzt die bestehende Dokumentation. Sie ersetzt oder löscht keine frühere Fassung.
