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
