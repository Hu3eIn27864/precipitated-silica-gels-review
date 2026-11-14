# CCFSM v1.5 – P3: räumliches 3D-Reaktions-Diffusions-Darcy-System

**Datum:** 14.11.2026  
**Bezug:** P0 Biot–Darcy, P1 beschränkte Brücken-/Mobilitätskopplung, P2 reversible Si-Pool-Kinetik.  
**Geltungsbereich:** natürliche, mechanisch unbelastete Synärese gefällter Silica-Gele.  
**Status:** mathematisch spezifizierter, dreidimensionaler, dreieckig gekoppelter PDE-Block; analytische Stoffbilanz-, Positivitäts- und Dissipationsresultate; Referenz-Finite-Volume-Operator. Keine empirische Kalibrierung.

## 1. Ziel und Modellhierarchie

P3 ersetzt die räumlich homogene P2-Kinetik durch ein Reaktions-Diffusions-System. Die vier Si-Äquivalent-Pools werden orts- und zeitabhängig:
\[
c=(c_M,c_O,c_N,c_B):\Omega\times(0,T)\to[0,\infty)^4.
\]
Der lokale Reaktionsmechanismus bleibt
\[
M\rightleftharpoons O\rightleftharpoons N\rightleftharpoons B,
\]
mit den P2-Aktivitäten, Gleichgewichtskonstanten und Reaktionsraten. Die Spezies diffundieren im Porenraum. Der entstehende Netzwerk-/Brückenanteil bestimmt anschließend die hydraulische Darcy-Mobilität.

**Dreieckige Kopplung:** Chemie \(\to b_\delta(c)\to\mathbb L_p\to p\). Der Druck wirkt in P3 noch nicht auf die Reaktionsraten oder Diffusionskoeffizienten zurück. Das ist ein bewusst abgegrenzter Zwischenschritt, keine Behauptung vollständiger physikalischer Rückkopplung.

## 2. Geometrie, Porosität und Zustände

\(\Omega\subset\mathbb R^3\) sei ein beschränktes Lipschitz-Gebiet. Die Porosität \(\phi\) ist zunächst konstant mit \(0<\phi\le1\). Konzentrationen sind mol Si-Äquivalent pro m³ Porenflüssigkeit. \(D_i>0\) sind effektive Diffusionskoeffizienten (m²/s), bereits einschließlich einer vorläufigen Tortuositätskorrektur, sofern diese unabhängig bekannt ist.

Die konservative Bilanz für jede Spezies lautet:
\[
\boxed{\partial_t(\phi c_i)+\nabla\cdot J_i=\phi R_i(c)}
\quad\text{in }\Omega\times(0,T),
\]
\[
J_i=-\phi D_i\nabla c_i,\qquad J_i\cdot n=0\quad\text{auf }\partial\Omega.
\]
Bei konstanter Porosität ergibt sich nach Division durch \(\phi\):
\[
\partial_t c_i-D_i\Delta c_i=R_i(c).
\]
Mit \(r_1,r_2,r_3\) aus P2 gilt
\[
R(c)=(-r_1,\ r_1-r_2,\ r_2-r_3,\ r_3).
\tag{P3-RD}
\]
Für variable Porosität ist die konservative Form beizubehalten; dann dürfen weder \(\phi\) noch die Flussfaktoren aus der Bilanz herausgekürzt werden.

## 3. Reaktionsraten und Aktivität

Für \(i=M,O,N,B\) sei
\[
a_i=\gamma_i c_i/c_*,
\]
und
\[
r_1=k_1c_*(a_M-a_O/K_1),\quad
r_2=k_2c_*(a_O-a_N/K_2),\quad
r_3=k_3c_*(a_N-a_B/K_3).
\]
Alle Parameter sind zunächst räumlich konstant und zeitlich konstant. Räumlich veränderliche, messbare Parameter können später als beschränkte Koeffizienten zugelassen werden. pH- und Temperaturabhängigkeit wird nicht durch unbelegte Potenzgesetze ersetzt: Sie muss über unabhängig begründete \(\gamma_i(x,t)\), \(K_j(T)\) und \(k_j(T)\) eingebracht werden. Die P2-Gültigkeitsgrenzen für Aktivitätsmodelle gelten unverändert.

## 4. Exakte globale Siliciumbilanz

Durch Summation der vier Reaktionsquellen gilt punktweise
\[
\sum_iR_i(c)=0.
\]
Daher
\[
\partial_t\left(\phi\sum_i c_i\right)
+\nabla\cdot\left(\sum_iJ_i\right)=0.
\]
Integration über \(\Omega\) und Anwendung der No-Flux-Randbedingung liefert
\[
\boxed{\int_\Omega\phi\sum_i c_i(x,t)\,dx
=\int_\Omega\phi\sum_i c_i(x,0)\,dx.}
\]
Dies ist die globale Si-Äquivalent-Erhaltung. Einzelne Speziesmengen sind wegen Reaktion und Diffusion nicht erhalten. Bei offenen Rändern oder Probenkontakt mit einer Flüssigkeitsphase muss der gemessene Randfluss explizit eingesetzt werden.

## 5. Positivität und Beschränktheit

Das Reaktionsnetzwerk ist quasi-positiv: Ist eine Spezieskonzentration null, zeigen die Reaktionsbeiträge der angrenzenden Reaktionen nicht aus dem nichtnegativen Kegel heraus. Der Diffusionsoperator mit No-Flux-Randbedingung erhält ebenfalls Nichtnegativität. Für nichtnegative Anfangsdaten folgt daher
\[
c_i(x,t)\ge0.
\]
Aus der globalen Bilanz folgt eine \(L^1\)-Schranke. Bei konstanten positiven Diffusionskoeffizienten und linearen P2-Raten ist das System ein kooperatives lineares Reaktions-Diffusions-System; auf endlichen Zeitintervallen liefert die Maximum-Prinzip-/Semigruppenstruktur zusätzlich \(L^\infty\)-Schranken aus den Anfangsdaten. Es wird keine Konzentration über die Gesamt-Si-Menge hinaus erzeugt.

## 6. Chemische freie Energie und räumliche Dissipation

Bei konstantem \(T,\gamma_i,\phi,D_i\) definieren wir die P2-freie Energiedichte
\[
g(c)=\sum_i\left[\mu_i^0c_i+RTc_i(\ln a_i-1)\right],
\]
mit \(0\ln0:=0\). Die Gesamtenergie des chemischen Blocks ist
\[
\mathcal G(t)=\int_\Omega\phi g(c(x,t))\,dx.
\]
Die chemischen Potentiale sind \(\mu_i=\partial g/\partial c_i=\mu_i^0+RT\ln a_i\). Wegen \(J_i=-\phi D_i\nabla c_i\) gilt im positiven Inneren
\[
J_i\cdot\nabla\mu_i
=-\phi D_iRT\frac{|\nabla c_i|^2}{c_i}\le0.
\]
Integration partiell, No-Flux und P2-Affinitäten ergeben
\[
\boxed{
\frac{d\mathcal G}{dt}
=-\int_\Omega\phi\left[
RT\sum_iD_i\frac{|\nabla c_i|^2}{c_i}
+\sum_{j=1}^3r_j\mathcal A_j
\right]dx\le0,
}
\]
wobei \(\mathcal A_j=RT\ln(K_ja_j/a_{j+1})\). Die Identität gilt für hinreichend glatte, strikt positive Lösungen; für schwache Lösungen ist die entsprechende Energieungleichung der natürliche Zielbegriff. An Nullstellen sind die Terme durch Approximation/untere Halbstetigkeit zu interpretieren. Für variable Aktivitätskoeffizienten, Temperatur oder Porosität entstehen zusätzliche Terme; die obige Formel darf dann nicht unverändert verwendet werden.

Die Diffusionsdissipation ist proportional zu \(|\nabla c_i|^2/c_i\), nicht zu \(|\nabla c_i|^2\). Diese Gewichtung folgt aus der idealen chemischen Potentialform \(\mu_i\sim\ln c_i\).

## 7. Brückenanteil und Darcy-Kopplung

Die rohe Netzwerkfraktion \(c_B/(c_N+c_B)\) ist bei leerem Netzwerk nicht definiert und nahe \(c_N+c_B=0\) numerisch schlecht konditioniert. Für die gekoppelte PDE verwenden wir deshalb die explizite Regularisierung
\[
\boxed{b_\delta(c)=\frac{c_B}{c_N+c_B+\delta_B}},
\qquad\delta_B>0.
\]
Dann \(0\le b_\delta\le1\), und die Abbildung ist auf dem nichtnegativen Kegel glatt/beschränkt differenzierbar. \(\delta_B\) hat Konzentrationseinheit und ist eine numerische/konstitutive Regularisierung, kein aus Daten bestimmter Materialparameter. Für \(c_N+c_B\gg\delta_B\) nähert sich \(b_\delta\) der P2-Brückenfraktion. Der Grenzübergang \(\delta_B\downarrow0\) ist ein eigener Analyse- und Konvergenzschritt.

Die P1-Mobilität wird
\[
\mathbb L_p(c)=
(1-b_\delta(c))\mathbb L_0+b_\delta(c)\mathbb L_1.
\]
Sind \(\mathbb L_0,\mathbb L_1\) symmetrisch und gleichmäßig positiv definit, bleibt \(\mathbb L_p(c)\) gleichmäßig elliptisch. Der P0-Druckblock lautet in schwacher Form
\[
m(\partial_t p,v)+
\int_\Omega\mathbb L_p(c)\nabla p\cdot\nabla v\,dx
=\langle s_f,v\rangle.
\]
Die P0-Speicherform \(m\), Randbedingungen und mechanische Eliminierung bleiben unverändert. Die Kopplung ist aktuell einseitig: \(c\) bestimmt den Druckoperator, \(p\) ändert \(c\) noch nicht.

## 8. Schwache Form des chemischen PDE-Blocks

Setze \(V=H^1(\Omega)\), \(H=L^2(\Omega)^4\). Für jede Testfunktion \(\psi_i\in H^1(\Omega)\):
\[
\langle\partial_t(\phi c_i),\psi_i\rangle
+\int_\Omega\phi D_i\nabla c_i\cdot\nabla\psi_i\,dx
=\int_\Omega\phi R_i(c)\psi_i\,dx.
\]
No-Flux ist damit natürlich eingebaut. Für konstantes \(\phi\) und \(D_i\) sowie lineare Reaktionsraten ist dies ein lineares parabolisches System. Die Reaktionsmatrix ist durch die P2-Raten bestimmt; Quasi-Positivität, Erhaltung und Diffusionselliptizität liefern die invarianten Schranken.

## 9. Existenz und Eindeutigkeit – präziser Satzumfang

**Satz (chemischer P3-Block).** Sei \(\Omega\) beschränkt und Lipschitz, \(\phi\in(0,1]\) konstant, \(D_i>0\), \(k_j\ge0\), \(K_j,\gamma_i,c_*,T>0\) konstant. Für \(c_i^0\in L^2(\Omega)\), \(c_i^0\ge0\), existiert eine eindeutige globale schwache Lösung des linearen Reaktions-Diffusions-Systems mit No-Flux-Randbedingung. Sie erfüllt Nichtnegativität, globale Si-Erhaltung und eine chemische Energieungleichung. Für beschränkte Anfangsdaten bleibt die Lösung auf endlichen Zeitintervallen beschränkt.

*Beweisskizze:* Schreibe das System als \(\partial_t c-\mathcal D\Delta c=Ac\), wobei \(\mathcal D=\operatorname{diag}(D_i)\) strikt positiv und \(A\) die konstante P2-Reaktionsmatrix ist. Die Neumann-Laplaceoperatoren erzeugen analytische Kontraktionshalbgruppen; die konstante Matrix \(A\) ist eine beschränkte lineare Störung. Galerkin-Approximation liefert die \(L^2(0,T;H^1)\)- und \(H^1(0,T;H^{-1})\)-Schranken. Eindeutigkeit folgt aus der Energieabschätzung für die Differenz zweier Lösungen. Quasi-Positivität bzw. das Maximumprinzip erhält den nichtnegativen Kegel; Summation der Gleichungen ergibt die Erhaltung. Die Energieungleichung folgt durch Testen mit chemischen Potentialen, zunächst regularisiert und anschließendem Grenzübergang.

**Druck-Unterproblem:** Für eine gegebene chemische Lösung \(c\) ist \(b_\delta(c)\) messbar und beschränkt. Damit ist \(\mathbb L_p(c)\) messbar, beschränkt und gleichmäßig elliptisch. Die nichtautonome lineare P0-Druckgleichung besitzt unter den P0-Rand- und Speicherannahmen eine eindeutige schwache Lösung.

**Gekoppeltes System:** Da die Chemie nicht vom Druck abhängt, ist die Gesamtlösung durch Hintereinanderausführung beider Teilprobleme eindeutig. Das ist kein Existenzbeweis für eine voll bidirektionale, nichtlineare Chemie-Poroelastizitäts-Kopplung. Auch klassische Glattheit wird nicht behauptet.

## 10. Numerische Diskretisierung

Der Referenzoperator verwendet zellzentrierte Finite Volumes auf einem gleichmäßigen kartesischen Gitter. Diffusionsflüsse werden paarweise über gemeinsame Zellflächen berechnet; dadurch heben sich innere Flüsse in der globalen Summe exakt auf. Außenflächen tragen bei No-Flux null bei. Reaktionsquellen werden zellweise aus P2 ausgewertet und summieren sich exakt zu null.

Für produktive Zeitintegration sind implizite oder positivity-preserving Verfahren zu bevorzugen (z. B. implizite Diffusion plus geeigneter Reaktionsschritt). Ein explizites Euler-Verfahren ist nur unter einer gitter- und ratenabhängigen CFL-/Positivitätsbedingung zulässig. Die Referenzimplementierung stellt den semidiskreten Operator bereit und behauptet keine unbedingte Positivität eines beliebigen Zeitschritts.

## 11. Parameter- und Validierungsstatus

Noch nicht identifiziert sind insbesondere \(D_i\), Tortuosität, \(\delta_B\), \(k_j\), \(K_j\), \(\gamma_i\), \(\mathbb L_0,\mathbb L_1\), Porosität und die räumlichen Anfangsprofile. Natürliche makroskopische Synäresekurven allein identifizieren diese Größen nicht getrennt. Erforderlich wären räumliche Konzentrations-/Speziesprofile, Diffusions- oder Tracerexperimente, unabhängige Porositäts-/Permeabilitätsmessungen und zeitaufgelöste Struktur-/Brückeninformationen.

Die bestehenden Wilhelm-&-Kind-Daten bleiben für die natürliche Makro-Synärese. Die erzwungenen Druckzell-/Oedometerdaten und Trocknungsdaten bleiben separate Zweige. P3 führt keine dieser Daten unzulässig in eine neue chemische Parameterkalibrierung ein.

## 12. P4 – nächste mathematische Erweiterung

1. variable Porosität \(\phi(x,t)\) mit Feststoff-/Flüssigkeitsbilanz und ALE-/Mischungsformulierung,
2. advektiver Speziestransport durch Porenwasserbewegung, konservativ mit Relativfluss,
3. Wärmegleichung für tatsächliche Gelkerntemperatur \(T(x,t)\),
4. vollständige Elektrolyt-, Wasser- und Ladungsbilanz einschließlich Oberflächenladung,
5. Rückkopplung von Porendruck/chemischen Potentialen auf Reaktionsaffinitäten und Netzwerk-Eigenstrain,
6. thermodynamisch konsistente Gesamtenergie für Chemie + Porenfluid + Festkörper,
7. Existenz-/Eindeutigkeit für den bidirektionalen nichtlinearen Mehrfeldblock.
