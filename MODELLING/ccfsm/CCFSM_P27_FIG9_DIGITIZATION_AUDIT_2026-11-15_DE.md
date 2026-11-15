# Figure 9 — erste manuelle Markerablesung und Unsicherheits-Audit

**Quelle:** Wilhelm & Kind (2015), *Polymers* 7(12), 2504–2521, Fig. 9, DOI 10.3390/polym7121528.  
**Originalabbildung:** https://mdpi-res.com/polymers/polymers-07-01528/article_deploy/html/images/polymers-07-01528-g009-1024.png  
**Ablesestatus:** manuelle Näherungsablesung aus der im Artikel gerenderten 1000-px-Abbildung; nicht aus Rohdaten, nicht pixelkalibriert und nicht unabhängig gegengeprüft.

## Ergebnis

Die neue CSV `wilhelm_kind_fig9_digitized_approx_2026-11-15.csv` enthält 39 geschätzte Markerzentren aus beiden Panels (sauer/basisch; 20/40/60 °C). Zeit- und Konzentrationswerte sind absichtlich grob gerundet. Die Spalte `visual_uncertainty_mmol_L` ist eine konservative Schätzunsicherheit der Markerablesung, **nicht** der publizierte Fehlerbalken. Die Fehlerbalken wurden nicht digitalisiert. Für jeden Punkt bleibt `fit_eligibility=hold_for_pixel_validation`.

## Achsen und getrennte Bereiche

- Beide Panels: Zeit ungefähr 0–250 h.
- Sauer (a): unterer Ast 0–0.9 mmol/L; oberer, gebrochener Ast zeigt den berechneten Anfangswert um 1000 mmol/L. Dieser Anfangswert ist keine Messung des ausgeschiedenen Porenfluids und ist nicht in der Punkt-CSV enthalten.
- Basisch (b): unterer Ast 0–250 mmol/L; ebenfalls berechneter Anfangswert um 1000 mmol/L, nicht als Messpunkt übernommen.
- Zeitablesung: visuelle Unsicherheit typischerweise ca. ±3–4 h. Konzentrationsablesung: grob ±0.04–0.06 mmol/L (sauer) und ±12–15 mmol/L (basisch), zusätzlich zu nicht rekonstruierten experimentellen Fehlerbalken.

## Quellenkritische Beobachtungen

1. Im sauren 60-°C-Zweig sind zwei visuell hohe Marker um ca. 0.83 mmol/L früh und ca. 0.60 mmol/L spät zu sehen. Sie bleiben enthalten und werden nicht als Ausreißer entfernt. Das steht in Spannung zur Textzusammenfassung 0.2–0.4 mmol/L; der Artikel erwähnt später selbst, dass Messwerte über der berechneten Löslichkeit liegen können.
2. Die basischen Marker streuen breit; einige Fehlerbalken sind groß. Eine Regressionskurve über Markerzentren ohne Fehlerbalkenmodell wäre nicht gerechtfertigt.
3. Die Analyse wurde bei ungefähr 20 °C durchgeführt, auch für Gelproben aus 40/60-°C-Bädern. Die Probe kann während Trennung und Analyse nachpolymerisieren.
4. Die Farbreaktion bei 400 nm ist nach dem referenzierten Molybdatverfahren nicht automatisch monomerspezifisch. Bis Reaktionszeit, pH und Reagenzprotokoll geklärt sind, ist die Observable operational als molybdatreaktive niedrigmolekulare Silica-Fraktion zu führen.

## Verwendungsregel

Die CSV ist eine **Ablese-Arbeitsdatei**, keine freigegebene Messdatentabelle. Keine Parameterkalibrierung, keine Konfidenzintervalle und kein Fit der Monomerbilanz, bevor die Bildpixel mit festgelegten Achsenkoordinaten und Markerzentren unabhängig digitalisiert, Fehlerbalken getrennt rekonstruiert und die chemische Messfunktion spezifiziert sind. Die sechs Temperatur-/Katalyse-Serien gehören alle zur selben Publikation und sind keine unabhängigen Replikate.

## Reproduzierbare nächste Stufe

Eine pixelgenaue Zweitablesung sollte die Plot-Rahmenkoordinaten und Achsen-Ticks aus der Original-PNG erfassen, Markerfarben/-formen segmentieren, überlagerte Fehlerbalken separat maskieren und eine manuelle Korrekturtabelle mit Screenshot-Koordinaten bereitstellen. Die derzeitige Webansicht lieferte die Grafik, aber kein lokal verfügbares Original-PNG für eine reproduzierbare Pixelanalyse; deshalb wird kein Pixelpräzisionsanspruch erhoben.


## Quellenabgleich und quantitative Sperre (15.11.2026)

Der Volltext des Artikels wurde erneut gegen die Figure-9-Beschreibung geprüft. Er bestätigt ausdrücklich: saurer Zweig 0.2–0.4 mmol/L als Textzusammenfassung; basischer Zweig 100–200 mmol/L; die Proben wurden auch bei 40/60-°C-Geltemperatur bei ungefähr 20 °C spektroskopisch analysiert, sodass Nachpolymerisation möglich ist. Die Messung beruht auf gelbem Silicomolybdat bei 400 nm nach Alexander. Die Autoren weisen außerdem darauf hin, dass einzelne Messwerte über der aus Gleichung (1) berechneten Löslichkeit liegen und dass sich das Porenfluid bei Lagerung eintrüben kann.

**Wichtige Präzisierung:** Die vorhandenen 39 CSV-Punkte bleiben eine manuelle Näherungsablesung. Ein erneuter Abruf der 1024-px-Abbildung über die verfügbare Laufzeitumgebung war nicht erfolgreich; deshalb konnte in diesem Durchgang keine reproduzierbare Pixelkoordinaten-Zweitablesung und keine separate Fehlerbalkendigitalisierung erstellt werden. Es werden keine künstlich präzisen Pixelwerte ergänzt. fit_eligibility=hold_for_pixel_validation bleibt für alle Punkte bestehen.

**Interpretation:** Die Diskrepanz der sauren 60-°C-Marker zur Textspanne wird nicht durch Entfernen der Marker „gelöst“. Sie bleibt ein dokumentierter Quellenkonflikt, der anhand der Originalpixel und der Messunsicherheit zu klären ist. Die Observable wird bis zur Klärung des Reaktionszeit-/pH-Protokolls weiterhin nicht als streng monomerspezifische Konzentration in die CCFSM-Kinetik eingespeist.

Quelle: Wilhelm & Kind (2015), Polymers 7(12), 2504–2521, DOI: 10.3390/polym7121528, Abschnitt 4.1 und Fig. 9. https://www.mdpi.com/2073-4360/7/12/2504
