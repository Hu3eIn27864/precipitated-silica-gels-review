# CCFSM v0.4 — chemisches Teilmodell der Silica-Netzwerkbildung

**Geltungsbereich:** natürliche, mechanisch unbelastete Synärese gefällter Silica-Gele aus Natriumsilikat und Schwefelsäure bzw. getrennt zu behandelnden alkalischen Rezepturen. Keine Parameterübernahme aus Oedometer- oder erzwungener Synärese.

**Status:** mechanistisch strukturierter, dimensionskonsistenter Modellvorschlag. Die kinetischen Parameter sind nicht an den Zielproben kalibriert. Die Gleichungen sind daher nicht empirisch grün.

## 1. Chemische Trennung der Zustände

Alle Konzentrationen werden als mol Si-Äquivalent pro m³ Flüssig-/Gelvolumen geführt:

- (c_m): monomere bzw. rasch austauschende gelöste Kieselsäure;
- (c_o): lösliche oligomere/poly(silicic-acid)-Spezies;
- (c_n): kondensiertes Netzwerk-Silicium;
- (etain[0,1]): Anteil des Netzwerk-Siliciums, der in der mesoskopischen Näherung zu effektiven tragenden Brücken beiträgt.

Die effektive tragende Brückendichte ist **abgeleitet**, nicht ein zusätzlicher Si-Massenpool:

[
B=f_{load},c_n,eta,qquad 0le f_{load}le1.
]

Damit wird vermieden, dieselben Siliciumatome sowohl als Netzwerk-Silicium als auch nochmals als unabhängige Brückenmasse zu zählen. (f_{load}) ist eine mesoskopische Topologie-/Tragfähigkeitsfraktion, keine universelle chemische Konstante.

## 2. Konservative Silicium-Bilanz

Wir verwenden drei Transferflüsse:

[
r_o: c_mightarrow c_o,qquad
r_n: c_oightarrow c_n,qquad
r_d: c_nightarrow c_m.
]

[
dot c_m=-r_o+r_d,
quad
dot c_o=r_o-r_n,
quad
dot c_n=r_n-r_d.
]

Addition ergibt exakt:

[
oxed{rac{d}{dt}(c_m+c_o+c_n)=0.}
]

Dies ist eine Bilanz für das betrachtete geschlossene Silicium-Teilvolumen. Bei Proben mit Flüssigkeitsaustritt, Waschung oder gelöstem Silicium im Syneresat muss ein gemessener Ausfluss-/Quellterm ergänzt werden; die geschlossene Bilanz darf dann nicht unkritisch verwendet werden.

### 2.1 Oligomerbildung

Mit (c_{ref}) als Konzentrationsskala und einer extern bereitgestellten Gleichgewichts-/Löslichkeitskonzentration (c_{eq}(pH,T,I)):

[
Omega=maxleft(rac{c_m}{c_{eq}}-1,0ight),
]

[
r_o=k_o(T)c_{ref}
left(rac{c_m}{c_{ref}}ight)^{n_o}
Omega^{m_o}
F_{pH}F_I.
]

Das ist eine bewusst modulare Netto-Wachstumsnäherung. Sie setzt voraus, dass (c_{eq}) für die aktuelle Zusammensetzung bekannt oder unabhängig modelliert ist. Sie ist keine universelle Elementarreaktionsgleichung und darf nicht ohne Anpassung auf alle hochkonzentrierten Fällungszustände übertragen werden.

### 2.2 Oligomer-zu-Netzwerk-Transfer

[
r_n=k_n(T)c_oF_{pH}F_I.
]

Dieser Term beschreibt den Transfer aus dem löslichen Oligomerpool in kondensiertes Netzwerk-Silicium. Er ist nicht mit dem Gelpunkt identisch. Perkolation und mechanische Tragfähigkeit werden erst über (eta), (f_{load}) und später die Struktur-/Kontaktkopplung abgebildet.

### 2.3 Auflösung/Hydrolyse

[
r_d=k_d(T)c_nF_d,
]

[
F_d=1+w_{d,H}F_H+w_{d,OH}F_{OH}.
]

Die Gewichte sind nichtnegative, zu kalibrierende Parameter. Die Form ist eine phänomenologische Möglichkeit, saure und alkalische Auflösung getrennt abzubilden; sie behauptet keine bekannte universelle Hydrolyseordnung.

## 3. pH- und Speziationsmodul

pH ist eine Aktivitätsgröße. Wir setzen:

\[
a_H=10^{-pH},\qquad a_{OH}=10^{pH-pK_w(T,I)}.
\]

Wir trennen die erste Dissoziation des Monomers von der Säure-Base-Chemie bereits gebildeter Oligomer-/Partikeloberflächen:

\[
\alpha_m=\frac{1}{1+10^{pK_{a,m}-pH}},\qquad
\alpha_s=\frac{1}{1+10^{pK_{a,s}-pH}}.
\]

\[
F_{pair,m}=4\alpha_m(1-\alpha_m),\qquad
F_{pair,s}=4\alpha_s(1-\alpha_s).
\]

Die erste Version verwendet zwei getrennte gewichtete Katalysefaktoren:

\[
F_{pH}^{(m)}=
w_H^{(m)}\left(\frac{a_H}{a_{H,ref}}\right)^{m_H^{(m)}}
+w_{pair}^{(m)}F_{pair,m}
+w_{OH}^{(m)}\left(\frac{a_{OH}}{a_{OH,ref}}\right)^{m_{OH}^{(m)}},
\]

\[
F_{pH}^{(s)}=
w_H^{(s)}\left(\frac{a_H}{a_{H,ref}}\right)^{m_H^{(s)}}
+w_{pair}^{(s)}F_{pair,s}
+w_{OH}^{(s)}\left(\frac{a_{OH}}{a_{OH,ref}}\right)^{m_{OH}^{(s)}}.
\]

\(F_{pH}^{(m)}\) moduliert die Monomer-Oligomer-Bildung \(r_o\); \(F_{pH}^{(s)}\) moduliert das Wachstum an Oligomer-/Partikeloberflächen \(r_n\) und die Entwicklung der tragenden Brückenfraktion. Die Gewichte und Reaktionsordnungen sind getrennt identifizierbar zu machen.

Die Trennung ist chemisch wichtig: Die scheinbare Säuredissoziation von Oligomer-/Partikeloberflächen ist nicht gleich der ersten Dissoziation des Monomers. In der Literatur wird für ionisierbare Polysilicic-acid-Oberflächen ein deutlich niedrigerer scheinbarer pKa-Wert (Größenordnung 6.8) diskutiert als für monomere Kieselsäure (Größenordnung 9–10). Diese Werte sind nur Orientierung; sie hängen von Spezies, Ionenstärke, Temperatur und Auswertungsmodell ab und sind nicht als feststehende Werte für unsere Prozessbrühen zu verwenden.

Das ist eine **additive Kanalhypothese**, kein vollständig hergeleiteter Elementarmechanismus. Die Speziation von Oligomeren und realen Partikeloberflächen ist breiter als ein einzelnes Henderson-Hasselbalch-Gleichgewicht. Säure- und Basenroute werden daher getrennt kalibriert.

\(pK_w\), \(p_{K,a,m}\) und \(p_{K,a,s}\) werden als zustandsabhängige Umweltgrößen behandelt. Die Code-Standardwerte dienen nur für Tests und sind keine universellen Werte für konzentrierte Prozessbrühen.

## 4. Ionenstärke und Temperatur

Erste empirische Korrektur:

[
F_I=left(1+rac{I}{I_{ref}}ight)^{m_I}.
]

Diese Form hält (F_I=1) bei (I=0) und lässt den Einfluss über (m_I) identifizieren. Sie ist eine flexible Korrektur, kein allgemeines Elektrolytgesetz. Spezifische Ionen (Na⁺, SO₄²⁻, HSO₄⁻ etc.) können über Hofmeister-/Aktivitäts-/Komplexierungseffekte nicht vollständig durch eine einzige Ionenstärke erfasst werden.

Jede elementare/effektive Rate erhält eine eigene Arrhenius-Funktion:

[
k_j(T_g)=k_{j,ref}
expleft[-rac{E_{a,j}}{R}
left(rac{1}{T_g}-rac{1}{T_{ref}}ight)ight].
]

(T_g) ist die Gelkerntemperatur. Aktivierungsenergien sind mechanismusspezifisch und nicht aus der Badtemperatur allein zu fitten.

## 5. Tragende Brücken als eigener mesoskopischer Zustand

[
doteta=k_{form}(T)F_{pH}F_I(1-eta)
-k_{b hyd}(T)F_{hyd}eta,
]

[
F_{hyd}=1+w_{hyd,H}F_H+w_{hyd,OH}F_{OH}.
]

Damit folgt:

[
B=f_{load}c_neta,
quad
dot B=f_{load}(dot c_neta+c_ndoteta).
]

Diese Definition trennt:
- chemische Kondensation ((c_n)),
- Anteil der Verknüpfungen, die effektiv tragend sind ((eta)),
- geometrisch/topologisch tragfähigen Anteil ((f_{load})).

Eine einzelne Siloxanbindung ist nicht automatisch eine load-bearing Brücke zwischen zwei unabhängigen Clustern. (f_{load}) muss später mit Kontakt-/Netzwerktopologie verknüpft werden. Bis dahin ist es ein zu identifizierender Closure-Parameter.

## 6. Mathematische Eigenschaften

Unter nichtnegativen Raten und positiven Referenzkonzentrationen gilt für das kontinuierliche ODE-System:

1. **Si-Erhaltung:** (dot c_m+dot c_o+dot c_n=0).
2. **Nichtnegative Si-Pools:** Die Transferflüsse sind an den jeweiligen Quellpool gekoppelt. Die kontinuierlichen Gleichungen sind auf dem nichtnegativen Orthanten vorwärtsinvariant.
3. **Brückenanteil:** Für (k_{form}F_{pH}F_Ige0) und (k_{b hyd}F_{hyd}ge0) ist ([0,1]) für (eta) invariant.
4. **Brückendichte:** (0le Ble f_{load}c_n).

Der RK4-Code prüft Zustandsadmissibilität und bricht bei zu großem Zeitschritt ab, statt negative Konzentrationen still zu beschneiden. Die Bilanzprüfung in Tests ist eine numerische Regression, kein Ersatz für den obigen analytischen Beweis.

## 7. Kopplung an CCFSM v0.3

Die chemische Komponente liefert (B(t)) und (dot B(t)). Diese Größen können die bisherige v0.3-Brückenkinetik ersetzen. Morphologie, Relaxation und hydraulische Schrumpfung bleiben zunächst getrennte Blöcke.

Wichtig für die Kopplung:
- Die v0.3 Zeitbasis ist Stunden; dieses chemische Modul verwendet SI-Sekunden. Vor Übergabe gilt (B_h=B_s) und (dot B|_{h^{-1}}=3600dot B|_{s^{-1}}).
- Anfangswerte müssen konsistent sein: (B_0=f_{load}c_{n,0}eta_0).
- Ein geschlossenes Siliciumsystem ist nur zulässig, solange keine relevante Si-Auswaschung/Abfuhr auftritt.
- Der pH-Verlauf ist eine gemessene Eingabe oder Ergebnis eines separaten Säure-Base-/Ladungsbilanzmodells, nicht ein unabhängiger freier Fitparameter neben der gesamten Rezeptur.

## 8. Was ist derzeit grün?

| Aussage | Mathematik | Physik | Empirie |
|---|---|---|---|
| Si-Poolbilanz | Grün | Grün als Bilanzdefinition im geschlossenen Teilvolumen | Gelb: Auswaschung messen |
| (F_{pair}=4alpha(1-alpha)) | Grün als mathematische Funktion | Gelb: Monomerproxy, Oberflächen-Spezies fehlen | Rot |
| Additiver (F_{pH})-Kanal | Grün als definierte Funktion | Gelb: Mechanismushypothese | Rot |
| (F_I) | Grün als definierte Funktion | Gelb: Elektrolytspezifität fehlt | Rot |
| Arrhenius (k_j(T_g)) | Grün als Temperaturfunktion | Gelb: Mechanismus-/Temperaturbereich prüfen | Rot |
| (eta)-Brückenfraktion | Grün: Intervall invariant | Gelb: load-bearing Closure | Rot |

## 9. Experimentelle Mindestdaten für Kalibrierung

Je Säure-/Basenroute getrennt:
1. Rezeptur, Silikatmodul, Gesamt-SiO₂, Säure-/Basen-Zugaberate und Zugabereihenfolge;
2. pH(t), Gelkerntemperatur (T_g(t)), Ionen-/Gegenionenbilanz;
3. gelöstes monomeres Si und lösliche Oligomerfraktion mit validierter Speziations-/Trennmethode;
4. Gesamt-Si im Gel und im austretenden Syneresat (Massenbilanz);
5. ein unabhängiger Proxy für tragende Brücken bzw. Netzwerk-Konnektivität;
6. Replikate und Unsicherheiten.

Ein bloßer Schrumpfungsverlauf (S(t)) reicht nicht, um (k_o,k_n,k_d,k_{form},k_{b hyd},f_{load}) getrennt zu identifizieren.

## 10. Literatur- und Transfergrenzen

- Icopini, Brantley & Heaney (2005), *Kinetics of silica oligomerization and nanocolloid formation as a function of pH and ionic strength at 25°C*, Geochimica et Cosmochimica Acta 69, 293–303, DOI: 10.1016/j.gca.2004.06.038. Untersucht verdünnte Lösungen (4.2–20.8 mmolal SiO₂; I=0.01 und 0.24 molal; pH 3–11). Mechanistische Orientierung, nicht direkte Kalibrierung konzentrierter gefällter Silica-Gele.
- *Silica polymerization and nanocolloid nucleation and growth kinetics in aqueous solutions* (2024), Geochimica et Cosmochimica Acta, DOI: 10.1016/j.gca.2024.02.017. Berichtet eine pH-/Ionenstärke-/Temperaturabhängigkeit in wässrigen Modelllösungen. Die berichtete (I^{0.65})- und Arrhenius-Parametrisierung wird nicht ungeprüft übernommen.
- Schlomach & Kind (2004), *Investigations on the semi-batch precipitation of silica*, Journal of Colloid and Interface Science 277, 316–326, DOI: 10.1016/j.jcis.2004.04.051. Direkter Zielmaterialkontext; unterscheidet Primärpartikelbildung, Aggregation bis zum Gelpunkt und post-gel Fragmentierung/Verdichtung. Liefert keine vollständige pH-/Speziationskinetik für unser Teilmodell.

## 11. Nächste Schritte

1. pH-/Ionen-/Temperaturkanäle anhand von Quarch/Kind und Primärquellen für die konkrete Rezeptur enger eingrenzen.
2. chemische Raten anhand zeitaufgelöster gelöster/oligomerer/Netzwerk-Si-Daten identifizieren.
3. Brückenfraktion (eta) und (f_{load}) separat durch Netzwerk-/Rheologie-/Strukturdaten identifizieren.
4. erst danach das chemische Modul mit v0.3 koppeln und eine hold-out Vorhersage natürlicher Synärese durchführen.
