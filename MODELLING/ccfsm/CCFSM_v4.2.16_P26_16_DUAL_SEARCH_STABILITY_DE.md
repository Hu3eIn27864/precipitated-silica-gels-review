# P26.16 — Stabilität und Vollständigkeit der dualen Suche

**Stand: 15. November 2026**

## Ziel

P26.15 findet strikte rationale Dualseparatoren durch primitive ganzzahlige Richtungen in wachsenden L-infinity-Schalen. P26.16 prüft den Richtungsradius und die Dezimalgenauigkeit der rationalen Quadratwurzel-Obergrenzen getrennt.

Ein gefundenes Zertifikat bleibt ein exakter rationaler Beweis. Ein endlicher Suchlauf wird ausdrücklich nicht zu einem vollständigen Entscheid erklärt.

## 1. Richtungs-Vollständigkeit im Grenzfall

Sei \(K\subset\mathbb R^2\) die Menge der durch feste Zellmittelwerte und zellweise Nichtnegativität erreichbaren beiden globalen Modenmomente. Jede zellweise Koeffizientenmenge ist kompakt und konvex; lineare Abbildung und endliche Minkowski-Summe erhalten Kompaktheit und Konvexität. Daher ist \(K\) kompakt und konvex.

Liegt der Zielvektor \(t\notin K\), liefert der strikte Trennungssatz einen Vektor \(y\in\mathbb R^2\) mit
\[
y\cdot t-h_K(y)>0.
\]
Die Supportfunktion \(h_K\) ist stetig. Wegen des strikt positiven Abstands bleibt die Ungleichung in einer offenen Umgebung von \(y\) erfüllt. Diese Umgebung enthält einen rationalen Vektor. Durch Multiplikation mit dem gemeinsamen Nenner und anschließende Kürzung des ggT erhält man eine primitive ganzzahlige Richtung.

**Folgerung:** Die unendliche Enumeration aller primitiven ganzzahligen Richtungen ist im exakten mathematischen Sinn vollständig für die Erkennung strikter Unzulässigkeit.

**Wichtige Grenze:** Für jeden endlichen Radius kann ein Separator außerhalb des untersuchten Rasters liegen. 'no_certificate_found' bei endlichem Radius ist weder ein Machbarkeitsbeweis noch ein Unzulässigkeitsbeweis. Liegt \(t\in K\), existiert kein strikter Separator.

## 2. Quadratwurzel-Obergrenze

P26.8 verwendet für \(x\ge0\) eine rationale Obergrenze \(s_d\) mit
\[
\sqrt{x}\le s_d<\sqrt{x}+10^{-d},
\]
wobei \(d\) die Dezimalstellenzahl ist. Die Konstruktion erfolgt ausschließlich mit ganzzahliger Quadratwurzel und rationaler Arithmetik.

Für eine Zell-Supportfunktion ist der Quadratwurzelterm mit \(6m\) multipliziert. Da die äußere Maximumsbildung 1-Lipschitz bezüglich des jeweiligen Arguments ist, gilt für den gesamten Support:
\[
0\le h_K^{(d)}(y)-h_K(y)
\le 6\,10^{-d}\sum_jm_j.
\]
Der zertifizierte Abstand \(g_d=y\cdot t-h_K^{(d)}(y)\) ist eine untere Schranke des wahren Abstands. Bei höherer Dezimalgenauigkeit kann diese untere Schranke nicht kleiner werden. Ein positiver Wert ist bereits bei grober Genauigkeit ein gültiger Beweis; ein nichtpositiver Wert kann durch höhere Genauigkeit positiv werden.

## 3. Stabilitätsaudit

Das Modul ccfsm_p26_16_dual_search_stability.py:
- prüft verschachtelte Richtungsradien und dokumentiert den ersten zertifizierenden Shell-Radius;
- vergleicht die beste verifizierte Lücke über verschachtelte Suchmengen;
- prüft die monotone Verschärfung der rationalen Quadratwurzel-Obergrenzen;
- prüft für eine feste Richtung die monotone Nichtabnahme der zertifizierten unteren Abstandsschranke;
- gibt die explizite Schranke \(6\,10^{-d}\sum_jm_j\) für den Support-Überhang aus.

Alle Vergleiche der Zertifikatsabstände erfolgen als Fraction, nicht mit Float-Toleranzen.

## 4. Statussemantik

| Ergebnis | Zulässige Aussage |
|---|---|
| certified_infeasible | Ein strikt positiver rationaler unterer Dualabstand beweist Unzulässigkeit. |
| no_certificate_found | Im endlichen Richtungsraster wurde kein Separator zertifiziert. |
| Höhere Quadratwurzelgenauigkeit findet Separator | Der vorherige Lauf war hinsichtlich der Support-Obergrenze zu grob; das neue Zertifikat ist gültig. |
| Auch größeres endliches Raster findet keinen Separator | Weiterhin keine Machbarkeitsaussage. |

## 5. Verifikation und Grenzen

Die Regressionen prüfen die verschachtelte Quadratwurzel-Obergrenze, monotone Gap-Schranken, verschachtelte Richtungsraster und die analytische Support-Fehlerschranke.

Geltungsbereich bleibt 1-D, feste nichtnegative Zellmittelwerte und quadratische Zellprofile mit globalen ersten/zweiten Momenten. Die Vollständigkeitsbehauptung betrifft nur die unendliche rationale Richtungsmenge, nicht die Laufzeit oder Vollständigkeit eines endlichen Programmlaufs. Die Zertifikate gelten für die exakt rationalisierten Eingabedaten. Keine experimentelle oder physikalische Validierung.
