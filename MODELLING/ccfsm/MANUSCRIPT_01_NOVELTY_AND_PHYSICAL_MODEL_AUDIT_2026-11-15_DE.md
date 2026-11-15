# Manuskript 1 — Neuheits- und physikalischer Modell-Audit

**Stand:** 15.11.2026  
**Zweck:** Überzogene Neuheitsbehauptungen vermeiden; mathematische Korrektheit der ODE von physikalischer Herleitung trennen.  
**Status:** vorläufige Literaturprüfung anhand öffentlich zugänglicher Abstracts/Volltexte; keine systematische Review und keine Volltextprüfung aller historischen Arbeiten.

## 1. Zentrale Schlussfolgerung

Die v0.2-Gleichungen sind als lineares, dreieckiges Zwei-Zustands-ODE-System mathematisch konsistent. Daraus folgt jedoch nicht, dass sie bereits eine physikalisch hergeleitete oder experimentell bestätigte Naturgesetzbeschreibung der Synärese gefällter Silica darstellen.

Die Grundidee, dass die spontane Schrumpfung durch Netzwerkmechanik/viskoelastische Kontraktion und den Transport der Porenflüssigkeit gemeinsam bestimmt wird, ist spätestens durch Scherers Arbeiten von 1989 bekannt. Die Vertauschungssymmetrie der zwei Raten in einem linearen Zwei-Kompartiment-/Kaskadenmodell ist ebenfalls klassische Identifizierbarkeitstheorie und darf nicht als neue allgemeine mathematische Entdeckung dargestellt werden.

Daher wird der bisherige Neuheitsanspruch deutlich zurückgenommen.

## 2. Literaturbefund und Konsequenz für Claims

### 2.1 Scherer (1989), Mechanics of Syneresis I–II

Scherer beschreibt spontane Gelkontraktion mit Flüssigkeitsexpulsion, die Abhängigkeit der Schrumpfungsrate von Probengröße und Porenflusswiderstand sowie eine anfängliche Verzögerung, die mit dem Druckaufbau der Porenflüssigkeit in einem viskoelastischen Netzwerk erklärt wird. Die experimentelle Folgearbeit vergleicht Silica-Schrumpfkurven mit Berechnungen, die unabhängig gemessene Permeabilität, Modul und Viskosität verwenden.

**Konsequenz:** Nicht beanspruchen:
- erstmalige Trennung von Netzwerkmechanik und Flüssigkeitstransport;
- erstmalige mechanistische Erklärung zweier zeitlicher Prozesse der Synärese;
- erstmalige Herleitung einer Größenabhängigkeit der Schrumpfung;
- erstmalige Kopplung von viskoelastischer Antwort und Darcy-Transport.

Scherers Modell ist allerdings ein räumlich-mechanistischer poro-viskoelastischer Ansatz; es ist nicht ohne vollständigen Gleichungs- und Annahmenvergleich identisch mit der hier verwendeten lumped ODE.

### 2.2 Wilhelm & Kind (2014/2015), natürliche und erzwungene Synärese gefällter Silica

Die öffentlich zugängliche Arbeit von Wilhelm & Kind (2014) beschreibt die Fortsetzung der Polymerisation/Netzwerkrestrukturierung nach Gelbildung, natürliche Synärese und Flüssigkeitsexpulsion. Die natürliche Schrumpfung wird empirisch mit

\[
S_{emp}(t)=S_{max}\left[1-\exp\left(-(t/\tau)^n\right)\right]
\]

beschrieben; für die untersuchten natürlichen Proben wird ein Exponent um 1.23 berichtet. Die Arbeit entwickelt außerdem eine Korrelation, um natürliche Synärese aus erzwungener Synärese zu prognostizieren. Diese erzwungenen Daten sind nicht mit unbelasteter natürlicher Synärese gleichzusetzen.

**Konsequenz:** Nicht beanspruchen:
- erstmalige quantitative Beschreibung natürlicher Synärese von gefällter Silica;
- erstmalige Bestimmung einer empirischen Schrumpfkurve oder charakteristischen Zeitskala;
- erstmalige Untersuchung von Temperatur-/pH-/Prozessabhängigkeit;
- direkte Übernahme von Parametern aus erzwungener Synärese als Naturparameter.

Eine mögliche Differenz des v0.2-Ansatzes ist die Interpretation einer beobachteten Kurve durch zwei interne Zustände statt durch eine empirische gestreckte Exponentialfunktion. Das ist zunächst eine alternative reduzierte Parametrisierung, kein nachgewiesener physikalischer Fortschritt.

### 2.3 Klassische Identifizierbarkeit linearer Kompartimentmodelle

Die Literatur zu linearen Kompartimentmodellen behandelt bereits die strukturelle Identifizierbarkeit von Zwei-Kompartiment-Systemen, Transferfunktionssymmetrien, Parametervertauschung sowie die Verbesserung durch zusätzliche Ausgänge oder Eingangsperturbationen. Eine Arbeit von 1979 untersucht explizit die Identifizierbarkeit von Zwei-Kompartiment-Systemen; spätere Arbeiten analysieren Ununterscheidbarkeit und Identifizierbarkeit ebenfalls algebraisch.

**Konsequenz:** Nicht beanspruchen:
- erstmalige Entdeckung der Ratenvertauschungssymmetrie;
- neue allgemeine Theorie der strukturellen Identifizierbarkeit;
- neue allgemeine Rückgewinnung zweier Raten aus Summe und Produkt.

Der v0.2-Satz kann als transparente, anwendungsbezogene Ableitung für die konkrete Zustandsdefinition nützlich sein. Seine mathematische Struktur ist aber ein Spezialfall klassischer Kaskaden-/Kompartimentmodelle.

## 3. Mathematische Korrektheit versus physikalische Gültigkeit

### 3.1 Was derzeit mathematisch abgesichert ist

Für konstante Parameter und die expliziten Anfangsbedingungen ist das System

\[
\dot q=k_n(q_\infty-q),\qquad
\dot S=k_h(\eta_aq-S)
\]

eine affine, global Lipschitz-stetige ODE. Die exakte Lösung, das Gleichratenlimit, die bedingte Invarianz-/Monotonieaussage und die Nullstart-Transferfunktion folgen korrekt aus dieser Modelldefinition. Die Einheiten sind konsistent, wenn q, S, eta_a dimensionslos sind und k_n, k_h inverse Zeit besitzen.

### 3.2 Was nicht aus der Mathematik folgt

Die ODE-Herleitung beweist nicht:
- dass die Netzwerk-Kontraktionspotenzialdynamik erster Ordnung ist;
- dass hydraulische Relaxation durch genau einen konstanten Rateparameter beschrieben werden kann;
- dass eta_a zeitlich konstant oder als skalarer Faktor physikalisch ausreichend ist;
- dass q eine direkt messbare stressfreie Volumenkontraktion ist;
- dass q und S die vollständigen relevanten Zustände eines gefällten Silica-Gels darstellen;
- dass die Reduktion mit Silizium-, Wasser- und Flüssigkeitsbilanzen vereinbar ist;
- dass das Modell die räumlichen Biot-/Darcy-/viskoelastischen Gleichungen Scherers oder ein allgemeines Poroelastizitätsmodell herleitet.

### 3.3 Noch offene physikalische Modellprüfung

Vor einer physikalischen Behauptung müssen wir insbesondere prüfen:

1. **Zustandsdefinition:** Ist q eine latente interne Variable, ein stressfreies Eigenvolumen, ein chemisches Kontraktionspotential oder nur ein mathematischer Hilfszustand? Diese Bedeutungen sind nicht automatisch äquivalent.
2. **Kopplung:** Ist \(\dot S=k_h(\eta_aq-S)\) eine sinnvolle reduzierte Relaxationsgleichung aus einer kontrollierten Darcy-/poroelastischen Grenzfallanalyse? Bis dahin ist sie eine phänomenologische Schließung.
3. **Erhaltung:** Welche Beziehung besteht zwischen Volumenschrumpfung, Porenflüssigkeitsabgabe, Feststoffvolumen und fortlaufender Kondensation gelöster Kieselsäure? Die ODE enthält diese Bilanzen nicht explizit.
4. **Geometrie:** Die Skalierung \(k_h\propto L_d^{-2}\) ist nur unter einer geeigneten homogenen, gesättigten linearen Diffusions-/First-mode-Reduktion plausibel; sie muss aus dem zugrunde liegenden Randwertproblem hergeleitet werden.
5. **Parameterbedeutung:** \(k_n\), \(k_h\) und \(\eta_a\) sind effektive Modellparameter. Ohne unabhängige Messungen dürfen sie nicht als elementare Reaktionskonstante, direkt gemessene hydraulische Rate oder echte Grenzflächenfläche ausgegeben werden.

## 4. Neuheitsmatrix

| Aussage | Status | Zulässige Formulierung |
|---|---|---|
| Netzwerkmechanik und Porenflüssigkeitstransport beeinflussen gemeinsam Synärese | etablierte Vorarbeit | „im Anschluss an die poro-viskoelastische Syneresemechanik“ |
| Natürliche Synärese gefällter Silica wurde experimentell und empirisch untersucht | etablierte Vorarbeit | „für die untersuchte Formulierung an bestehende Messungen anknüpfend“ |
| Zwei Raten in einer linearen Kaskade sind aus einem Ausgang nur bis auf Vertauschung bestimmbar | klassische Theorie | „wir leiten die bekannte Symmetrie für die hier verwendete Modellparametrisierung explizit her“ |
| Exakte Lösung und Invarianzregion für die konkrete v0.2-ODE | korrekte anwendungsbezogene Ableitung | „analytische Eigenschaften der vorgeschlagenen reduzierten Schließung“ |
| Die ODE ist eine physikalisch abgeleitete Silica-Konstitutivgleichung | nicht belegt | nicht behaupten |
| Die ODE ist experimentell validiert | nicht belegt | nicht behaupten |
| Der Ansatz ist gegenüber Scherer neuartig | nicht belegt | erst nach Gleichungs-/Grenzfallvergleich entscheiden |
| Ein neuer, publikationswürdiger mathematischer Satz liegt vor | derzeit nicht belegt | Neuheitsprüfung offen; klassische Kaskadenstruktur beachten |

## 5. Empfohlener, zurückhaltender Manuskriptbeitrag

Bis weitere Herleitung und Daten vorliegen, sollte Manuskript 1 nicht als neue Theorie der Silica-Synärese und nicht als neue Identifizierbarkeitstheorie positioniert werden.

Eine vertretbare Arbeitsbeschreibung lautet:

> We examine a low-order, two-state phenomenological closure for unloaded natural syneresis of precipitated silica. The model is motivated by the established coupling between network contraction and pore-liquid transport, but is not derived from the full poro-viscoelastic field equations. We provide its exact response and conditional state bounds, and make explicit the parameter-exchange ambiguity that follows from observing shrinkage alone. The closure is presented as a testable reduced model whose physical interpretation and predictive value require independent measurements and comparison with established syneresis theories.

Der Beitrag kann erst stärker werden, wenn mindestens einer der folgenden Punkte erfüllt ist:
- eine nachvollziehbare asymptotische Reduktion aus einem anerkannten poro-viskoelastischen PDE-Modell;
- ein mathematisch nichttriviales Resultat, das nicht nur Standardfolgen einer linearen Kaskade wiedergibt;
- eine klar definierte, reproduzierbare Verbesserung gegenüber der bestehenden empirischen Einraten-/Stretched-Exponential-Beschreibung;
- eine experimentell gestützte Trennung von Netzwerk- und hydraulischer Observable.

## 6. Konsequenz für die Publikationsstrategie

EJDE ist für die derzeitige ODE allein kein realistischer Anspruch, solange keine substanzielle neue mathematische Theorie hinzukommt. Ein mathematisch korrekt gelöstes lineares Zweizustandssystem plus bekannte Ratenvertauschung reicht voraussichtlich nicht als eigenständiger Beitrag in einem Differentialgleichungsjournal.

Die nächste sinnvolle Arbeit ist daher nicht, den Titel oder Abstract zu polieren, sondern:
1. v0.2 als phänomenologische Hypothese zu kennzeichnen;
2. die Gleichungen gegen Scherers Feldmodell und Wilhelm/Kind's empirische Beschreibung abzugleichen;
3. die Reduktion physikalisch herzuleiten oder die Modellbehauptung enger zu halten;
4. erst dann über Manuskriptumfang und Zieljournal zu entscheiden.

## 7. Quellen, die in der ersten Prüfung berücksichtigt wurden

- Scherer, G. W. (1989). “Mechanics of Syneresis I. Theory.” *Journal of Non-Crystalline Solids* 108(1), 18–27. DOI: 10.1016/0022-3093(89)90328-1.
- Scherer, G. W. (1989). “Mechanics of Syneresis II. Experimental Study.” *Journal of Non-Crystalline Solids* 108(1), 28–36. DOI: 10.1016/0022-3093(89)90329-3.
- Wilhelm, S.; Kind, M. (2014). “On the Relation between Natural and Enforced Syneresis of Acidic Precipitated Silica.” *Polymers* 6(12), 2896–2911. DOI: 10.3390/polym6122896.
- Bellman, R.; Åström, K. J. (1970). “On structural identifiability.” *Mathematical Biosciences* 7, 329–339. DOI: 10.1016/0025-5564(70)90132-X. (Classical general framework; detailed equation-by-equation comparison remains pending.)
- “The Identifiability of Linear Compartmental Models.” IFAC Proceedings Volumes 12(8), 1979, 719–726. DOI: 10.1016/S1474-6670(17)65484-3.
- Godfrey, K. R.; Jones, R. P.; Brown, R. F.; Norton, J. P. (1982). “Factors affecting the identifiability of compartmental models.” *Automatica* 18(3), 285–293. DOI: 10.1016/0005-1098(82)90088-7.

**Prüfgrenze:** Die Web-/Metadatenprüfung belegt die Existenz und grobe Inhalte der genannten Vorarbeiten. Für eine finale Prior-Art-Aussage sind Volltextlektüre, Gleichungsvergleich, Zitationsketten und eine breitere Suche notwendig.
