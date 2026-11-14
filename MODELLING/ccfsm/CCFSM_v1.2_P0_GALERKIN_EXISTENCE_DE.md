# CCFSM v1.2 – P0-Galerkin-Existenz- und Eindeutigkeitssatz

**Datum:** 14.11.2026  
**Geltungsbereich:** lineares, isothermes, gesättigtes Biot-Darcy-Referenzproblem in 3D; natürliche Synärese wird hier noch nicht durch silica-spezifische interne Variablen modelliert.  
**Status:** schwacher Existenz- und Eindeutigkeitsbeweis unter den unten genannten Annahmen. Kein klassischer Regularitäts- oder P1–P5-Beweis.

## 1. Geometrie, Räume und Koeffizienten

Sei \(\Omega\subset\mathbb R^3\) ein beschränktes Lipschitz-Gebiet und \(T>0\). Wir setzen
\[
V=H^1_0(\Omega;\mathbb R^3),\qquad Q=H^1(\Omega),\qquad H=L^2(\Omega).
\]
Die homogene Dirichlet-Bedingung für die Verschiebung entfernt starre Bewegungen. Für den Fluidfluss gilt die homogene natürliche No-Flow-Bedingung \(\mathbf q\cdot\mathbf n=0\) auf dem gesamten Rand. Der Druck wird nicht auf Mittelwert null festgelegt: der positive Speicherterm kontrolliert auch seine räumlich konstante Komponente.

Die Elastizitätsform und Darcy-Form lauten
\[
a(u,w)=\int_\Omega \mathbb C\varepsilon(u):\varepsilon(w)\,dx,
\qquad
\ell(p,r)=\int_\Omega \mathbb L_p\nabla p\cdot\nabla r\,dx.
\]
Es gebe Konstanten \(c_C,C_C,\lambda_L,\Lambda_L>0\), so dass für fast alle \(x\)
\[
c_C|E|^2\le (\mathbb C(x)E):E,\quad
|\mathbb C(x)E|\le C_C|E|,\quad
\lambda_L|\xi|^2\le \mathbb L_p(x)\xi\cdot\xi,\quad
|\mathbb L_p(x)\xi|\le\Lambda_L|\xi|.
\]
\(\mathbb C\) besitzt die übliche Minor-/Major-Symmetrie; \(\mathbb L_p\) ist symmetrisch. Ferner seien \(M>0\) und \(\alpha_B\in\mathbb R\) konstant. Für variable Koeffizienten genügt dieselbe messbare, gleichmäßige Beschränktheits- und Koerzivitätsannahme.

Wir betrachten zunächst keine mechanische Volumenkraft oder Traktion und eine Fluidquelle
\[
s_f\in L^2(0,T;Q').
\]
Der Anfangsdruck sei \(p_0\in H\). Das Weglassen mechanischer Lasten ist eine bewusste Referenzannahme; zeitabhängige Lasten erfordern zusätzliche Arbeits-/Ableitungsterme.

## 2. Reduktion auf eine parabolische Gleichung

Für jedes \(p\in H\) definiere \(Tp\in V\) eindeutig durch
\[
a(Tp,w)=\alpha_B\int_\Omega p\,\nabla\cdot w\,dx
\quad\forall w\in V.
\]
Lax–Milgram und Korn liefern
\[
\|Tp\|_V\le C_T\|p\|_H.
\]
Die quasistatische mechanische Gleichung ist damit für fast alle Zeiten erfüllt durch
\[
u(t)=Tp(t).
\]

Definiere auf \(H\) die symmetrische Bilinearform
\[
m(p,r)=M^{-1}(p,r)_H+a(Tp,Tr).
\]
Sie ist stetig und positiv definit. Insbesondere
\[
M^{-1}\|p\|_H^2\le m(p,p)
\le (M^{-1}+C_T^2)\|p\|_H^2,
\]
nach Anpassung der Konstanten. Somit ist \(m\) ein zugehöriges Skalarprodukt, dessen Norm zur \(L^2\)-Norm äquivalent ist.

Die reduzierte schwache Fluidgleichung lautet
\[
m(\partial_t p,r)+\ell(p,r)=\langle s_f,r\rangle
\quad\forall r\in Q.
\tag{P0-R}
\]
Tatsächlich gilt wegen der Symmetrie von \(a\)
\[
a(T\partial_t p,Tr)
=\alpha_B\int_\Omega r\,\nabla\cdot(T\partial_t p)\,dx,
\]
also genau der mechanische Speicher-Kopplungsanteil
\(\alpha_B(\partial_t\nabla\cdot u,r)\). Die Reduktion ist daher algebraisch äquivalent zur gekoppelten schwachen Form.

## 3. Existenzsatz

**Satz (schwache P0-Existenz).** Unter den Annahmen aus Abschnitt 1 existiert eine Lösung
\[
p\in L^2(0,T;Q)\cap C([0,T];H),\qquad
\partial_t p\in L^2(0,T;Q'),
\]
mit \(p(0)=p_0\) in \(H\), so dass (P0-R) für fast alle Zeiten und alle \(r\in Q\) gilt. Mit \(u=Tp\) erhält man
\[
u\in L^\infty(0,T;V)\cap C([0,T];V)
\]
und das Paar \((u,p)\) löst die ursprüngliche quasistatische Biot-Darcy-Schwachform.

**Beweis.** Aus der Koerzivität von \(\mathbb C\), Korn und der Beschränktheit des Kopplungsoperators folgt, dass \(m\) ein stetiges Skalarprodukt auf \(H\) mit zu \(L^2\) äquivalenter Norm ist. Auf \(Q=H^1(\Omega)\) ist \(\ell\) stetig und nichtnegativ. Die Einbettungen
\[
Q\hookrightarrow (H,m)\hookrightarrow Q'
\]
sind dicht und stetig. Zusätzlich ist
\[
m(v,v)+\ell(v,v)\ge c\|v\|_{H^1}^2
\]
mit einem \(c>0\): der erste Term kontrolliert \(\|v\|_{L^2}^2\), der zweite den Gradienten. Damit ist die Standardtheorie linearer parabolischer Evolutionsgleichungen auf einem Gelfand-Tripel (Galerkin-Verfahren plus Energieabschätzung, äquivalent zum Lions-Existenzsatz) anwendbar.

Zur expliziten Galerkin-Skizze wählt man eine in \(Q\) dichte Folge endlichdimensionaler Räume \(Q_n\subset Q\), die zugleich in \(H\) dicht ist, und löst
\[
m(\dot p_n,r_n)+\ell(p_n,r_n)=\langle s_f,r_n\rangle
\quad\forall r_n\in Q_n,
\]
mit \(p_n(0)\) als \(m\)-orthogonaler Projektion von \(p_0\). Das ist ein endlichdimensionales lineares ODE-System mit positiv definiter Massenmatrix und besitzt eine globale Lösung auf \([0,T]\). Testen mit \(r_n=p_n\) ergibt
\[
\frac12\frac d{dt}m(p_n,p_n)+\ell(p_n,p_n)
=\langle s_f,p_n\rangle.
\]
Youngs Ungleichung und die Koerzivität von \(m+\ell\) liefern, nach Integration und Gronwall,
\[
\sup_{0\le t\le T}\|p_n(t)\|_H^2+
\int_0^T\|p_n(t)\|_{H^1}^2\,dt
\le C\left(\|p_0\|_H^2+
\|s_f\|_{L^2(0,T;Q')}^2\right),
\]
wobei \(C\) unabhängig von \(n\) ist. Die Evolutionsgleichung liefert außerdem die übliche Schranke für \(\dot p_n\) in \(L^2(0,T;Q')\) (in der abstrakten Galerkin-Konstruktion bzw. über die zugehörige Evolutionsformulierung). Schwache Teilfolgen konvergieren; durch Testen zunächst gegen Elemente der Vereinigung der \(Q_n\), anschließend durch Dichte, gehen die linearen Terme in (P0-R) über. Die Anfangsbedingung folgt aus der schwachen Zeitstetigkeit und der Energieabschätzung. Die abstrakte parabolische Theorie liefert die stärkere Aussage \(p\in C([0,T];H)\). Schließlich ist \(T:H\to V\) stetig, also \(u=Tp\in C([0,T];V)\cap L^\infty(0,T;V)\). Einsetzen der Definition von \(T\) und von \(m\) zeigt beide ursprünglichen schwachen Gleichungen. \(\square\)

**Präzisierung der Galerkin-Schranke.** Die Zeitderivierten-Schranke ist im Standardbeweis als Schranke in \(L^2(0,T;Q')\) für die Grenzlösung zu lesen; bei beliebigen Galerkin-Räumen ist die gleichmäßige Stabilität der \(Q'\)-Projektionen nicht automatisch. Man verwendet daher entweder eine geeignete stabile Galerkin-Basis oder direkt den abstrakten Evolutionssatz. Diese technische Wahl ist Teil eines vollständig ausgeschriebenen konstruktiven Galerkin-Beweises und wird nicht durch die formale Energieidentität ersetzt.

## 4. Energieungleichung und Eindeutigkeit

Für die Lösung gilt für fast alle \(t\in[0,T]\)
\[
\frac12m(p(t),p(t))+
\int_0^t\ell(p(s),p(s))\,ds
=
\frac12m(p_0,p_0)+
\int_0^t\langle s_f(s),p(s)\rangle\,ds.
\tag{E-P0}
\]
Mit \(u=Tp\) ist
\[
\frac12m(p,p)=
\frac12\int_\Omega\left[
\varepsilon(u):\mathbb C:\varepsilon(u)+M^{-1}p^2
\right]dx,
\]
also exakt die P0-Energie aus v1.1. Für \(s_f=0\) folgt Energieerhaltung bis auf Darcy-Dissipation:
\[
\mathcal F_0(t)+
\int_0^t\!\int_\Omega\nabla p\cdot\mathbb L_p\nabla p\,dx\,ds
=\mathcal F_0(0).
\]

**Eindeutigkeit.** Seien \((u_1,p_1)\) und \((u_2,p_2)\) zwei Lösungen mit denselben Daten. Ihre Differenz erfüllt die homogene reduzierte Gleichung mit Anfangswert null. Einsetzen der Differenz \(p=p_1-p_2\) als Testfunktion ergibt
\[
\frac12m(p(t),p(t))+\int_0^t\ell(p,p)\,ds=0.
\]
Beide Terme sind nichtnegativ und \(m\) positiv definit; daher \(p=0\), und aus \(u=Tp\) folgt \(u=0\). Die Lösung ist eindeutig.

## 5. Was der Satz nicht behauptet

1. Er beweist schwache Existenz und Eindeutigkeit für den linearen P0-Referenzkern, nicht für das nichtlineare CCFSM P1–P5.
2. Er liefert keine klassische Glattheit, keine punktweisen Schranken für Gradienten und keinen globalen Regularitätssatz für nichtlineare 3D-Systeme.
3. Er identifiziert keine silica-spezifischen Materialgesetze für Permeabilität, Netzwerkbrücken, Fraktaldimension, Kontraktion oder Relaxation.
4. Die homogene No-Flow-Randbedingung ist eine geschlossene Referenzgrenze. Natürliche Synärese mit drainierender freier Oberfläche braucht eine eigene Randbilanz einschließlich möglicher Reservoir-/Kapillarterme.
5. Für nichtverschwindende zeitabhängige mechanische Lasten, gemischte Drainageränder oder variable Speicherkoeffizienten sind die Energie- und Datenannahmen entsprechend zu erweitern.

## 6. Nächster mathematischer Schritt

P1 sollte zunächst eine einzelne beschränkte Netzwerkvariable \(B\) mit einer explizit gewählten, nichtnegativen freien Energie und einer zustandsrauminvarianten Mobilität ergänzen. Vor einem gekoppelten Existenzbeweis müssen die Energieabhängigkeit, Randbedingungen und Kopplung an \(\mathbb L_p\) festgelegt sein. Eine Mobilität allein proportional zu \(B(B_\infty-B)\) sichert ohne passende Rand- und Quellterme noch nicht automatisch alle gewünschten Invarianz- und Regularitätseigenschaften.
