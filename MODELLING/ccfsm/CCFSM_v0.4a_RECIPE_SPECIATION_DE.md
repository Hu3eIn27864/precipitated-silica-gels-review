# CCFSM v0.4a — Rezeptur-zu-Speziation-Modell

**Ziel:** aus analytischen Rezepturgrößen eine erste überprüfbare Gleichgewichts-Speziation für Natriumsilikat/Schwefelsäure berechnen. Dies ist ein vorgeschalteter Chemieblock, kein vollständiges Modell industrieller Fällung oder Gelierung.

## Geltungsbereich

Enthalten sind analytisches Silicium aus Natriumsilikat, Natrium aus dem Silikatmodul, Gesamtsulfat aus Schwefelsäure, optionale NaOH- und NaCl-Zugaben, zwei Dissoziationsstufen der monomeren Kieselsäure, HSO4-/SO4--, NaSO4- Ionenpaar, Wasserautoprotolyse, Aktivitätskorrektur und Elektroneutralität.

Nicht enthalten sind oligomere Spezies, geladene Silica-Partikeloberflächen, Na-Silikat-Ionenpaare, Wasseraktivität, spezifische Ioneneffekte jenseits von NaSO4-, Feststoff-/Gelgleichgewichte und Alterungskinetik. Der nicht gelöste Siliciumanteil wird in der Ladungsbilanz vorläufig als neutraler Feststoff behandelt; reale Oberflächenladung kann diese Annahme verletzen.

## 1. Rezeptur in analytische Gesamtkonzentrationen

Für Natriumsilikat mit Modul M = n(SiO2)/n(Na2O):

\[
C_{Na,waterglass}=\frac{2C_{Si,total}}{M}.
\]

Mit NaOH und NaCl:

\[
C_{Na,T}=\frac{2C_{Si,total}}{M}+C_{NaOH}+C_{NaCl}.
\]

Für Schwefelsäure und NaCl gilt:

\[
C_{S(VI),T}=C_{H_2SO_4},\qquad C_{Cl,T}=C_{NaCl}.
\]

Die Stocklösungsfunktion rechnet Stoffmengen über das Endvolumen um. Additive Volumina sind nur eine Näherung; bei Volumenkontraktion ist das gemessene Endvolumen einzusetzen.

## 2. Gleichgewichte

Referenzwerte bei 25 °C aus der PHREEQC-Datenbank:
- H4SiO4 = H3SiO4- + H+, log10 K = -9.83;
- H4SiO4 = H2SiO4-- + 2 H+, log10 K = -23.00 (Gesamtreaktion);
- H+ + SO4-- = HSO4-, log10 K = 1.988;
- Na+ + SO4-- = NaSO4-, log10 K = 0.94.

Massenwirkung mit Aktivitäten a_i = gamma_i [i]:

\[
a_{H_3SiO_4^-}=K_1\frac{a_{H_4SiO_4}}{a_H},\quad
a_{H_2SiO_4^{2-}}=K_{1,overall}\frac{a_{H_4SiO_4}}{a_H^2}.
\]

\[
a_{HSO_4^-}=K_{assoc}a_Ha_{SO_4^{2-}},\quad
a_{NaSO_4^-}=K_{pair}a_{Na^+}a_{SO_4^{2-}}.
\]

Die erste Dissoziation der Schwefelsäure wird als vollständig angenommen. Die Konstanten sind Referenzwerte und nicht automatisch für konzentrierte Prozessbrühen oder alle Temperaturen gültig.

## 3. Aktivitätsmodell

Die Davies-Näherung:

\[
\log_{10}\gamma_i=-Az_i^2\left(\frac{\sqrt I}{1+\sqrt I}-0.3I\right).
\]

Bei der pH-Intervallsuche werden Aktivitätskoeffizienten extremer Probewerte nur bis zur Davies-Grenze ausgewertet, damit die Nullstelle eingegrenzt werden kann. Die endgültige selbstkonsistente Lösung wird verworfen, sobald I > 0.5 mol/L ist. Der Solver verweigert damit jede ausgegebene Davies-Lösung außerhalb dieses Bereichs. Diese Grenze ist eine praktische Obergrenze, keine Genauigkeitsgarantie. Bei konzentrierten Prozessbrühen ist ein Pitzer- oder geeignetes SIT-Modell mit Parametern für das tatsächliche Na-H-SO4-Silikat-System erforderlich. Das ideale Aktivitätsmodell ist nur ein expliziter Vergleichs-/Grenzfall.

## 4. Numerische Lösung

Für jeden Test-pH werden Aktivitätskoeffizienten und Ionenstärke iteriert, das NaSO4-Ionenpaar aus Natrium- und Sulfatbilanz berechnet, die Spezies nach Massenwirkung bestimmt und die Ladungsbilanz ausgewertet. Eine Intervallsuche mit anschließender Bisektion löst die Elektroneutralität. Bilanzresiduen werden ausgegeben; fehlende Gegenionen oder nicht eingeschlossene Stoffe führen zum Abbruch, wenn keine Nullstelle gefunden wird.

## 5. Übergabe an CCFSM

Der Solver liefert pH, I und monomere Silicium-Spezies. Der Adapter to_ccfsm_chemical_environment übergibt diese Größen an den bestehenden kinetischen CCFSM-Block. Dafür sind Lösungsmittelmasse pro Liter Endlösung und eine unabhängig bestimmte Silica-Löslichkeit erforderlich; die molare Ionenstärke wird nicht ungeprüft als Molalität behandelt. Für das bestehende kinetische Modul werden zusätzlich Löslichkeit c_eq(pH,T,I,Festphase), Gelkerntemperatur und Oligomer-/Oberflächenspeziation benötigt. Diese Größen werden nicht aus einer einzelnen Monomer-Gleichgewichtsrechnung erfunden. Die Löslichkeit amorpher frisch gefällter Silica ist nicht identisch mit der Quarzlöslichkeit.

I wird zunächst in mol/L ausgegeben. Es darf nicht ungeprüft als mol/kg an ChemicalEnvironment übergeben werden; die Umrechnung benötigt Lösungsmittelmasse bzw. Dichte und Zusammensetzung.

## 6. Verifikation und benötigte Daten

Tests prüfen alkalische Natriumsilikatlösung, pH-Absenkung durch Säure, Elektroneutralität, Si-/Na-/Sulfatbilanzen, NaSO4-Paarung, Stocklösungsverdünnung und Davies-Abbruch. Empirische Freigabe benötigt Silikatmodul und Feedstockanalyse, Stockkonzentrationen, Endvolumen/Dichte, Säure-/Basendosierprotokoll, pH-Zeitreihe, Leitfähigkeit, Na-/Sulfatanalyse sowie gelöstes Silicium nach validierter Feststoff-/Kolloidtrennung. Säure- und Basenroute sind getrennt zu validieren.

## Quellen

- PHREEQC-Datenbank phreeqc.dat: https://github.com/phreeqc-dev/iphreeqc/blob/master/database/phreeqc.dat
- USGS, PHREEQC-Datenbankkonstanten: https://wwwbrr.cr.usgs.gov/projects/GWC_coupled/phreeqc.v1/html/phqc_66.htm
- USGS, PHREEQC-Gültigkeitsgrenzen und Pitzer-Hinweis: https://wwwbrr.cr.usgs.gov/projects/GWC_coupled/phreeqc/html/final-4.html
- EPA Method 1627, Davies-Gleichung und ungefähre 0.5-M-Grenze: https://www.epa.gov/sites/default/files/2015-08/documents/method_1627_2011.pdf
- SCCS (2019), Solubility of Synthetic Amorphous Silica: https://health.ec.europa.eu/document/download/5dfad02b-e1da-405e-8ad0-4ca8d91112a8_en?filename=sccs_o_228.pdf

**Status:** Bilanz- und Gleichgewichtsstruktur sind numerisch testbar. Physikalische Validierung im Zielsystem steht aus.
