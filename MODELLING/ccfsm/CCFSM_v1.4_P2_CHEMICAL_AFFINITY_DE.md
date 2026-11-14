# CCFSM v1.4 – P2: chemische Affinität, reversible Si-Umwandlung und Brückenbildung

**Datum:** 14.11.2026  
**Bezug:** P0 (Biot–Darcy), P1 (beschränkte Brücken-/Mobilitätskopplung), v0.4/v0.4a (chemische Zustände und Rezeptur-Speziation).  
**Geltungsbereich:** lokale chemische Referenzkinetik für natürliche, mechanisch unbelastete Synärese gefällter Silica-Gele.  
**Status:** thermodynamisch strukturierter Modellblock mit analytischem Dissipationsresultat und Referenzimplementierung. Keine empirische Kalibrierung, keine Validierung und noch kein vollständiger räumlicher 3D-PDE-Existenzsatz.

## 1. Ziel von P2

P1 verwendete ein zeitlich festes (b_{eq}) und eine Relaxationskinetik. P2 ersetzt diesen Zielwert durch eine reversible, stoffbilanzierte Reaktionskette. Die chemische Triebkraft wird aus chemischen Potentialen und Reaktionsaffinitäten berechnet. Die resultierende Netzwerk-Brückenfraktion kann anschließend in die P1-Mobilität eingesetzt werden.

P2 ist bewusst ein **lokaler Reaktionsblock**. Räumlicher Stofftransport, Grenzflächenreaktionen, Wasseraktivität und eine vollständige Elektrolyt-/Silica-Spezierung werden nicht stillschweigend als gelöst ausgegeben.

## 2. Zustände und Stoffbilanz

Alle Konzentrationen sind mol Si-Äquivalent pro m³ Flüssig-/Gelvolumen:
- (c_M): monomeres gelöstes Silicium,
- (c_O): lösliche oligomere Silica-Spezies,
- (c_N): nicht-lasttragendes Netzwerk-Silicium,
- (c_B): effektives lasttragendes Brücken-Silicium.

Die Reaktionskette lautet
[
M\rightleftharpoons O\rightleftharpoons N\rightleftharpoons B.
]
Jeder Pool zählt dieselbe Zahl an Si-Äquivalenten. Die Reaktionsraten (r_j) sind positiv in Vorwärtsrichtung:
[
r_1=k_1c_*\left(a_M-a_O/K_1\right),\quad
r_2=k_2c_*\left(a_O-a_N/K_2\right),\quad
r_3=k_3c_*\left(a_N-a_B/K_3\right),
]
mit (a_i=\gamma_i c_i/c_*), (k_j\ge0), (K_j>0). (c_*>0) ist eine Referenzkonzentration und (gamma_i>0) sind Aktivitätskoeffizienten. Die ODEs lauten
[
\dot c_M=-r_1,\quad
\dot c_O=r_1-r_2,\quad
\dot c_N=r_2-r_3,\quad
\dot c_B=r_3.
\tag{P2-Si}
]
Daraus folgt exakt
[
\frac{d}{dt}(c_M+c_O+c_N+c_B)=0.
\]
Es gibt in diesem geschlossenen lokalen Block weder eine externe Siliciumquelle noch einen Siliciumverlust. Ein realer Austrag/Eintrag muss später als expliziter Fluss oder Quellterm ergänzt werden.

## 3. Chemische Potentiale und Affinitäten

Für den idealisierten Aktivitätsansatz definieren wir
[
\mu_i=\mu_i^0+RT\ln a_i.
]
Die Gleichgewichtskonstanten sind nicht frei unabhängig von den Standardpotentialen:
[
K_j=\exp[(\mu_j^0-\mu_{j+1}^0)/(RT)].
]
Damit ist die Vorwärtsaffinität
[
\mathcal A_j=\mu_j-\mu_{j+1}
=RT\ln\left(\frac{K_j a_j}{a_{j+1}}\right).
]
Das Vorzeichen von (r_j) stimmt mit dem von \(\mathcal A_j\) überein. Insbesondere gilt
[
r_j\mathcal A_j\ge0,
]
weil ((x-y)\ln(x/y)\ge0) für (x,y>0). Die chemische Dissipation \(\mathcal D=\sum_j r_j\mathcal A_j\) ist somit nichtnegativ (Einheit W m⁻³); die Entropieproduktionsrate ist \(\mathcal D/T\) (W m⁻³ K⁻¹).

Die gewählte lineare Aktivitätsdifferenz ist eine Onsager-nahe, detailliert-bilanzierte Referenzschließung. Sie ist keine universelle Elementarreaktionskinetik. Für konzentrierte Natriumsilikat-/Sulfatbrühen können nichtideale Aktivitäten, Ionenpaare, Oligomerverteilungen, Wasseraktivität und Oberflächenzustände wesentlich sein.

## 4. Brückenfraktion und P1-Kopplung

Für (c_N+c_B>0) definieren wir
[
b=\frac{c_B}{c_N+c_B},\qquad 0\le b\le1.
]
Wenn der Netzwerkpool leer ist, wird (b) als nicht definiert behandelt; numerisch darf dann kein willkürlicher positiver Netzwerkbestand erfunden werden. Für (c_N+c_B>0) ist die Brückenfraktion durch die nichtnegativen Si-Pools beschränkt.

Die P1-Mobilität kann damit geschlossen werden:
[
\mathbb L_p(b)=(1-b)\mathbb L_0+b\mathbb L_1.
]
Die Elliptizität bleibt erhalten, sofern beide Endtensoren gleichmäßig positiv definit sind. Wie bereits in P1 ist die affine Abhängigkeit nur eine mathematisch zulässige Platzhalterhypothese. Ein empirisches Vorzeichen oder eine lineare Permeabilitäts-Brücken-Beziehung ist nicht belegt.

Wichtig: (b) ist hier eine **effektive Poolfraktion**, keine direkte spektroskopisch messbare Anzahl chemisch eindeutig definierter Si–O–Si-Brücken. Die Umrechnung in eine absolute Brückendichte benötigt eine unabhängig definierte Netzwerk-/Brückenzählkonvention.

## 5. Freie Energie und Dissipation

Bei konstantem (T), konstanten (gamma_i) und konstantem Flüssigkeitsvolumen betrachten wir
[
\mathcal G(c)=\sum_i\left[
\mu_i^0c_i+RTc_i(\ln a_i-1)
\right].
]
Bis auf additive lineare Konstanten gilt
[
\frac{d\mathcal G}{dt}
=\sum_{j=1}^3(\mu_j-\mu_{j+1})r_j
=\sum_{j=1}^3\mathcal A_jr_j\ge0.
]
Mit der üblichen Konvention für chemische freie Energie muss das Vorzeichen sorgfältig interpretiert werden: Bei der hier gewählten Vorwärtsaffinität (mathcal A_j=\mu_j-\mu_{j+1}) und (r_j>0) fließt Material vom höheren zum niedrigeren Potential; daher ist die dissipierende freie Energie
[
\boxed{\frac{d\mathcal G}{dt}=-\sum_j r_j\mathcal A_j\le0.}
]
Die Identität folgt direkt aus (dot c=S r) und der Definition der Affinität. Sie gilt im positiven Inneren; Randzustände werden durch stetige Grenzwerte behandelt.

Dies ist ein **Modell-internes thermodynamisches Resultat**. Es beweist weder, dass die vier Pools die reale Silica-Chemie vollständig repräsentieren, noch dass die gewählte lineare Rate empirisch korrekt ist.

## 6. Kopplung an pH, Temperatur und Ionenaktivität

Die Abhängigkeiten werden nicht durch frei erfundene Universal-Potenzgesetze festgelegt:
- (T) tritt über (RT), temperaturabhängige Standardpotentiale/Gleichgewichtskonstanten und die bei tatsächlicher Geltemperatur geltenden (k_j(T)) ein.
- pH und Elektrolytzusammensetzung beeinflussen (a_i), (gamma_i), die Speziesverteilung und gegebenenfalls die effektiven (K_j) und (k_j).
- Die v0.4a-Rezeptur-Speziation liefert einen ersten Ansatz für Monomer-/Säure-Base-/Sulfat-/Natriumzustände, ist aber keine vollständige Oligomer- oder Geloberflächen-Speziation.
- Davies darf nicht außerhalb seiner dokumentierten Gültigkeitsgrenze verwendet werden; konzentrierte Prozessbrühen erfordern validierte SIT/Pitzer-Aktivitäten oder Messwerte.

Die P2-Implementierung nimmt deshalb (\gamma_i), (K_j), (k_j) und (T) explizit als Eingaben entgegen. Sie berechnet keine nicht belegten pH- oder Temperaturkoeffizienten.

## 7. Mathematische Eigenschaften

Für nichtnegative Anfangskonzentrationen und positive Parameter ist das Reaktionssystem:
1. **Silicium-erhaltend:** Summe der vier Pools ist konstant.
2. **Quasi-positiv:** Wenn ein Pool null ist, zeigen die benachbarten Reaktionen keinen auswärts gerichteten Fluss aus diesem leeren Pool.
3. **Beschränkt:** Jeder Pool liegt zwischen null und der konstanten Gesamtsiliciumkonzentration.
4. **Lokal eindeutig lösbar:** Auf dem kompakten nichtnegativen Simplex ist die rechte Seite stetig und lokal Lipschitz; damit existiert eine eindeutige Lösung für alle endlichen Zeiten. Die Gesamtmassen-Erhaltung verhindert endliches Entweichen aus dem Simplex.
5. **Dissipativ:** Die freie Energie ist nicht zunehmend, solange (T), Aktivitätenkoeffizienten und Volumen konstant sind.

Diese Aussagen betreffen den endlichen-dimensionalen lokalen Reaktionsblock. Für räumliche Diffusion-Reaktion, variable Porosität, freie Oberflächen und die volle nichtlineare Biot-Darcy-Kopplung ist ein eigener PDE-Beweis nötig.

## 8. Grenzen und Identifizierbarkeit

Die vorhandenen natürlichen Synäresekurven messen primär makroskopische Volumenänderung. Sie identifizieren nicht separat:
- (c_M,c_O,c_N,c_B) oder deren absolute Anfangswerte,
- (K_j), (k_j), Aktivitätskoeffizienten und Standardpotentiale,
- die Zuordnung des effektiven (c_B) zu chemisch definierten Brückentypen,
- die Funktion (\mathbb L_p(b)).

Die P2-Parameter bleiben deshalb unkalibriert. Die natürlichen Wilhelm-&-Kind-Kurven werden nicht als Ersatz für Speziesanalytik behandelt. Druckzell-/Oedometerdaten und Trocknungsdaten bleiben separate Zweige und fließen nicht in eine natürliche Synärese-Kalibrierung ein.

## 9. P3 – notwendige nächste Erweiterung

Für den räumlichen 3D-Block sind als Nächstes erforderlich:
1. konservative Speziesflüsse (J_i=-D_i\nabla c_i) mit Porositäts-/Tortuositätsbezug,
2. Reaktions-Diffusions-PDE mit no-flux bzw. gemessenen Randflüssen,
3. variable Geltemperatur (T(x,t)), nicht bloß Badtemperatur,
4. konsistente Wasser-/Elektrolyt-/Ladungsbilanz und Oberflächenladung,
5. Kopplung der chemischen freien Energie an Netzwerk-Eigenkontraktion und mechanische Energie,
6. Existenz-/Eindeutigkeitssatz für den tatsächlich gewählten gekoppelten PDE-Block.

Erst nach unabhängigen Spezies-, Aktivitäts-, Poren- und Transportmessungen kann die Konstitutivseite als empirisch geprüft gelten.
