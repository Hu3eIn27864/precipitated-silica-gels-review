# CCFSM – konservative Inventar- und Volumenbilanz für natürliche Synärese

**Datum:** 15.11.2026  
**Geltungsbereich:** natürliche, mechanisch unbelastete Synärese gefällter Silica-Gele; gesättigter Referenzfall ohne Verdunstung, Erosion oder Gasphase, sofern nicht ausdrücklich ergänzt.  
**Dokumenttyp:** versionsunabhängige Forschungsnotiz / Schnittstellenspezifikation. Sie ist kein neuer Modell- oder Release-Stand und gehört als querschnittlicher Bilanzbaustein zum bestehenden CCFSM-Entwicklungszweig (aktueller Stand: v4.2.57). Die Bilanzformen sind unter den jeweils genannten Annahmen Erhaltungssätze; Stoff- und Volumenübertragungskoeffizienten, Kapillargesetze, Materialgesetze und empirische Parameter sind damit noch nicht validiert. Keine Änderung oder Ersetzung der bestehenden v0.4-, P8- oder v1.0-Modelle.

## 1. Ziel und zentrale Entscheidung

Die bisherigen Modellgenerationen enthalten sinnvolle, aber nicht identische Zustandsgrößen:

- v0.4 führt mobile und kondensierte Silicium-Pools sowie eine daraus abgeleitete tragende Brückendichte.
- P8a verwendet eine hydraulische Speichergröße \(\theta\) und einen Drucklöser auf festem Referenzgebiet.
- P8b transportiert mobile Silicium-Inventare und bilanziert ihren Austrag an offenen Rändern.
- v1.0 verwendet die aktuelle Porosität \(\phi\), Skelettgeschwindigkeit \(\mathbf v_s\), relativen Darcy-Fluss \(\mathbf q\) und räumliche Spezieskonzentrationen.
- v1.1 führt den inkrementellen Fluidgehalt \(\zeta\) des linearen Biot-Referenzsystems ein.

Diese Größen sind nicht austauschbar. Insbesondere gilt im Allgemeinen weder \(\theta=\phi\) noch \(\zeta=\phi\). Die lineare Speicherbeziehung aus P8a ist eine reduzierte hydraulische Schließung; \(\phi\) ist ein tatsächlicher Flüssigkeitsvolumenanteil; \(\zeta\) ist eine inkrementelle Biot-Speichergröße.

**Entscheidung für die gemeinsame Bilanzschnittstelle:** Mobile Spezies werden über ihre Stoffmenge pro aktuellem Gesamt-Gelvolumen bilanziert, während ihre Konzentration weiterhin pro Flüssigkeitsvolumen angegeben wird. Netzwerk-Silicium wird als eigener immobilisierter Bestand pro aktuellem Gesamt-Gelvolumen geführt. Die Brückentragfähigkeit wird ausschließlich als abgeleitete Teilmenge dieses Netzwerkbestands modelliert und nicht nochmals als zusätzliche Silicium-Masse addiert.

## 2. Konfigurationen, Bezugsvolumina und Einheiten

Es werden zwei Darstellungen unterschieden.

### 2.1 Aktuelle Konfiguration

- \(\Omega(t)\): aktuelles Gelgebiet, Einheit \(\mathrm{m^3}\).
- \(\phi\in(0,1)\): Flüssigkeitsvolumenanteil am aktuellen Gesamt-Gelvolumen.
- \(\mathbf v_s\): Geschwindigkeit des Silica-Skeletts, \(\mathrm{m\,s^{-1}}\).
- \(\mathbf q\): Darcy-Volumenfluss relativ zum Skelett, bezogen auf die aktuelle Fläche, \(\mathrm{m\,s^{-1}}\).
- \(c_i\): Konzentration einer mobilen Spezies pro Flüssigkeitsvolumen, \(\mathrm{mol\,m^{-3}_{fluid}}\).
- \(N\): immobilisiertes Netzwerk-Silicium pro aktuellem Gesamt-Gelvolumen, \(\mathrm{mol\,m^{-3}_{gel}}\).
- \(\mathbf j_i\): diffusive/dispersionelle Stoffflussdichte relativ zum Skelett, \(\mathrm{mol\,m^{-2}\,s^{-1}}\).
- \(r_o,r_n,r_d\): Reaktionsfortschrittsraten pro aktuellem Gesamt-Gelvolumen, \(\mathrm{mol\,m^{-3}_{gel}\,s^{-1}}\).

Damit ist \(\phi c_i\) die mobile Stoffmenge pro aktuellem Gesamt-Gelvolumen. Diese Unterscheidung verhindert, dass eine Konzentration pro Flüssigkeitsvolumen mit einer Konzentration pro Gelvolumen verwechselt wird.

### 2.2 Referenzkonfiguration

Für die spätere mathematische Behandlung auf einem festen Gebiet \(\Omega_0\) seien
\[
\mathbf x=\boldsymbol\chi(\mathbf X,t),\qquad
\mathbf F=\nabla_X\boldsymbol\chi,\qquad J=\det\mathbf F>0.
\]
Ein aktuelles Inventar \(a\) pro aktuellem Volumen entspricht \(Ja\) pro Referenzvolumen. Ein aktueller Fluss \(\mathbf f\) wird als Piola-Fluss \(J\mathbf F^{-1}\mathbf f\) auf das Referenzgebiet transformiert.

Die Referenzdarstellung ist besonders zweckmäßig, wenn das Gel schrumpft und das Rechengebiet fest bleiben soll. Sie darf nicht mit einer aktuellen Konfiguration vermischt werden, ohne alle Volumen- und Flussterme zu transformieren.

## 3. Wasser- und Phasenbilanz

### 3.1 Gesättigter inkompressibler Referenzfall

Ohne Phasenwechsel-Volumenquellen, Verdunstung und Flüssigkeitskompressibilität lautet die Flüssigkeitsbilanz in aktueller Konfiguration:
\[
\boxed{\partial_t\phi+
\nabla\cdot(\phi\mathbf v_s+\mathbf q)=0.}
\tag{W1}
\]
Sie ist die lokale Bilanz des Flüssigkeitsvolumens. Der Fluss \(\mathbf q\) ist relativ zum Skelett; deshalb enthält der Gesamttransport zusätzlich \(\phi\mathbf v_s\).

Wenn auch die Feststoffphase inkompressibel ist und keine Feststoffmasse bzw. kein Feststoffvolumen zu- oder abgeführt wird:
\[
\boxed{\partial_t(1-\phi)+
\nabla\cdot[(1-\phi)\mathbf v_s]=0.}
\tag{W2}
\]
Addition ergibt:
\[
\boxed{\nabla\cdot(\mathbf v_s+\mathbf q)=0.}
\tag{W3}
\]
W3 ist eine Volumenkompatibilitätsbedingung für diesen speziellen inkompressiblen, gesättigten Fall. Sie ist keine allgemeine Gleichung für beliebige chemische Phasenwechsel.

### 3.2 Reaktive Phasenübertragung

Wenn gelöste Silica-Spezies in einen als Feststoffskelett gezählten Netzwerkbestand übergehen, muss festgelegt werden, ob dieser Übergang ein tatsächlicher Phasen-Volumentransfer ist oder lediglich eine Umklassifizierung innerhalb eines bereits vorhandenen kolloidalen Skeletts.

Falls ein physikalischer Phasen-Volumentransfer modelliert wird, sind Quellen \(s_f^V\) und \(s_s^V\) mit Einheit \(\mathrm{s^{-1}}\) einzuführen:
\[
\partial_t\phi+\nabla\cdot(\phi\mathbf v_s+\mathbf q)=s_f^V,
\]
\[
\partial_t(1-\phi)+\nabla\cdot[(1-\phi)\mathbf v_s]=s_s^V.
\]
Dann folgt
\[
\nabla\cdot(\mathbf v_s+\mathbf q)=s_f^V+s_s^V.
\]
Die Quellen müssen aus Reaktionsstöchiometrie und partiellen Molvolumina hergeleitet werden. Sie dürfen nicht allein aus einer Änderung der chemischen Poolbezeichnung abgeleitet werden. Für die erste konservative Referenzfassung werden \(s_f^V=s_s^V=0\) gesetzt und die Annahme explizit beibehalten. Die Frage, ob Netzwerkbildung im Zielmaterial eine zusätzliche Phasen-Volumenquelle erfordert, bleibt eine zu prüfende Materialfrage.

### 3.3 Referenzform

Mit \(Q=J\mathbf F^{-1}\mathbf q\) folgt aus W1:
\[
\boxed{\partial_t(J\phi)+
\operatorname{Div}_X\!\left(J\mathbf F^{-1}\mathbf q\right)=0.}
\tag{W1R}
\]
Diese Form ist die konservative Flüssigkeitsbilanz auf dem festen Referenzgebiet. Die entsprechende Feststoffbilanz lautet unter W2:
\[
\partial_t[J(1-\phi)]=0.
\tag{W2R}
\]
Bei Phasenübertragungsquellen sind die rechten Seiten entsprechend mit \(J s_f^V\) und \(J s_s^V\) zu ergänzen.

## 4. Konservative Siliciumbilanz ohne Doppelzählung

### 4.1 Zustände

Wir definieren zwei mobile Speziespools und einen immobilisierten Netzwerkpool:

- \(c_m\): mobiles Monomer-Silicium, pro Flüssigkeitsvolumen;
- \(c_o\): mobile lösliche Oligomer-Spezies, pro Flüssigkeitsvolumen;
- \(N\): gesamtes immobilisiertes Netzwerk-Silicium, pro aktuellem Gesamt-Gelvolumen.

Die mobile Inventardichte pro Gesamt-Gelvolumen ist damit \(\phi c_i\), nicht \(c_i\) allein.

Die effektive tragende Brückendichte ist eine abgeleitete Größe:
\[
\boxed{B=f_{\mathrm{load}}\,\beta\,N,\qquad
0\le f_{\mathrm{load}}\le1,\quad 0\le\beta\le1.}
\tag{Si0}
\]
\(B\) hat dieselbe Einheit wie \(N\), ist aber **kein zusätzlicher Stoffpool**. Eine Änderung von \(\beta\) ändert die Zuordnung des bereits im Netzwerk enthaltenen Siliciums zur tragenden Teilmenge; sie erzeugt oder vernichtet kein Silicium.

### 4.2 Lokale Transport-Reaktionsgleichungen

Für mobile Monomer- und Oligomerpools:
\[
\boxed{
\partial_t(\phi c_m)+
\nabla\cdot(\phi c_m\mathbf v_s+c_m\mathbf q+\mathbf j_m)
=-r_o+r_d,
}
\tag{Si1}
\]
\[
\boxed{
\partial_t(\phi c_o)+
\nabla\cdot(\phi c_o\mathbf v_s+c_o\mathbf q+\mathbf j_o)
=r_o-r_n.
}
\tag{Si2}
\]
Für das am Skelett gebundene Netzwerk-Silicium:
\[
\boxed{
\partial_tN+\nabla\cdot(N\mathbf v_s)=r_n-r_d.
}
\tag{Si3}
\]
Hier ist \(r_o\) der Transfer Monomer \(\to\) Oligomer, \(r_n\) der Transfer Oligomer \(\to\) Netzwerk und \(r_d\) der Rücktransfer/Auflösung Netzwerk \(\to\) Monomer. Alle drei Raten sind nichtnegativ, sofern sie als gerichtete Bruttoflüsse definiert werden. Allgemeinere reversible Reaktionsnetze benötigen eine explizite stöchiometrische Matrix.

Die Summe von Si1–Si3 liefert:
\[
\boxed{
\partial_t[\phi(c_m+c_o)+N]
+\nabla\cdot\left(
[\phi(c_m+c_o)+N]\mathbf v_s
+(c_m+c_o)\mathbf q
+\mathbf j_m+\mathbf j_o
\right)=0.
}
\tag{Si4}
\]
Damit ist die lokale Gesamt-Siliciumbilanz exakt konservativ. Die Reaktionsraten heben sich auf. Die Bilanz kann nur durch einen realen Randfluss oder einen ausdrücklich modellierten zusätzlichen Prozess geändert werden.

Die diffusive Flusskonvention ist hier relativ zum Skelett. Als einfache Fick-Näherung kann
\[
\mathbf j_i=-\phi\mathsf D_i\nabla c_i
\]
verwendet werden. Für konzentrierte Elektrolyte ist langfristig ein Fluss über chemische Potentiale und ein geeignetes Aktivitätsmodell vorzuziehen. Das Fick-Gesetz ist eine Transport-Schließung, nicht Teil der Erhaltungsaussage Si4.

### 4.3 Referenzform

Mit
\[
M_i=J\phi c_i,\qquad M_N=JN,\qquad
\mathcal J_i=J\mathbf F^{-1}(c_i\mathbf q+\mathbf j_i)
\]
lauten die Gleichungen auf \(\Omega_0\):
\[
\partial_t(J\phi c_m)+\operatorname{Div}_X\mathcal J_m
=J(-r_o+r_d),
\]
\[
\partial_t(J\phi c_o)+\operatorname{Div}_X\mathcal J_o
=J(r_o-r_n),
\]
\[
\partial_t(JN)=J(r_n-r_d).
\]
Dabei ist \(\mathbf v_s^{\,\mathrm{ref}}\) die auf dem Referenzgebiet dargestellte Skelettgeschwindigkeit. Alternativ kann die Materialableitung verwendet werden; beide Schreibweisen dürfen nicht doppelt konvektive Terme enthalten.

Die Referenz-Gesamtbilanz ist damit:
\[
\boxed{
\partial_t\{J[\phi(c_m+c_o)+N]\}
+\operatorname{Div}_X\left\{
J\mathbf F^{-1}[(c_m+c_o)\mathbf q+\mathbf j_m+\mathbf j_o]
\right\}=0.
}
\]
Die Skelettadvektion ist in der Zeitableitung des Referenzinventars enthalten und erscheint deshalb nicht nochmals als separater Referenzfluss.

## 5. Randfluss und kumulierter Austrag

Für die aktuelle Geloberfläche mit äußerer Normale \(\mathbf n\) ist der mobile Siliciumfluss relativ zur Oberfläche zu bilanzieren. Bei einer Oberfläche mit Geschwindigkeit \(\mathbf v_b\) lautet der Gesamtfluss der mobilen Spezies relativ zur bewegten Grenze:
\[
\boxed{
\mathcal F_i^{\,b}=
\left[
\phi c_i(\mathbf v_s-\mathbf v_b)
+c_i\mathbf q+\mathbf j_i
\right]\cdot\mathbf n.
}
\tag{B1}
\]
Für eine mit dem Skelett mitbewegte Materialoberfläche (\(\mathbf v_b=\mathbf v_s\)) reduziert sich dies auf
\[
\mathcal F_i^{\,b}=(c_i\mathbf q+\mathbf j_i)\cdot\mathbf n.
\]
Der kumulierte Si-Austrag ist:
\[
N_{\mathrm{Si,out}}(t)=
\int_0^t\int_{\partial\Omega(\tau)}
\sum_{i\in\{m,o\}}\mathcal F_i^{\,b}\,dA\,d\tau.
\]
Ein positiver Wert bezeichnet Netto-Austrag nach außen. Rückströmung ist durch das Vorzeichen zugelassen; die Außenkonzentration muss dann physikalisch vorgegeben sein.

Für das Gesamtinventar folgt:
\[
\boxed{
N_{\mathrm{Si,gel}}(t)+N_{\mathrm{Si,out}}(t)
=N_{\mathrm{Si,gel}}(0)
}
\tag{B2}
\]
sofern keine weiteren Si-Quellen, Feststofferosion, Partikelablösung oder Messverluste auftreten. Bei Erosion oder Partikelaustrag muss ein zusätzlicher Feststoff-Randfluss ergänzt werden.

Wasser und gelöstes Silicium müssen an denselben offenen Randflächen mit derselben hydraulischen Flussrichtung bilanziert werden. Ein hydraulischer Ausstrom ohne zugehörigen konvektiven Si-Austrag ist nur zulässig, wenn die betreffende Konzentration tatsächlich null oder ein anderer physikalisch begründeter Rückhalte-/Selektionsmechanismus vorhanden ist.

## 6. Gelvolumen, Schrumpfung und Syneresat

Die geometrische Gelvolumenänderung ist
\[
V_g(t)=\int_{\Omega(t)}1\,dV,\qquad
S_V(t)=\frac{V_g(0)-V_g(t)}{V_g(0)}.
\]
Für ein Materialgebiet mit Deformationsgradient:
\[
V_g(t)=\int_{\Omega_0}J(\mathbf X,t)\,dV_0.
\]
Der Flüssigkeitsaustritt wird separat über den Randfluss erfasst:
\[
V_{\mathrm{ex}}(t)=
\int_0^t\int_{\partial\Omega(\tau)}
\left[\phi(\mathbf v_s-\mathbf v_b)+\mathbf q\right]\cdot\mathbf n
\,dA\,d\tau.
\]
Bei einer mit dem Skelett mitbewegten Oberfläche vereinfacht sich der relative Flüssigkeitsaustritt auf \(\int\mathbf q\cdot\mathbf n\). Verdunstung ist ein zusätzlicher Wasserfluss über eine Gas-Flüssigkeits-Grenze und darf nicht als Darcy-Syneresat verbucht werden.

**Wichtige Einschränkung:** \(S_V(t)\) und \(V_{\mathrm{ex}}(t)/V_g(0)\) sind nicht definitionsgemäß identisch. Eine Gleichheit folgt nur unter zusätzlichen Annahmen über Sättigung, Phasenkompressibilität, Phasenwechsel, Randbewegung, Verdunstung, externe Flüssigkeitsaufnahme und Stoffverluste. Diese Annahmen sind für jede Messgeometrie einzeln zu prüfen.

Die reduzierte v0.2-Gleichung
\[
\dot S=k_h(\eta_aq-S)
\]
bleibt daher eine mögliche phänomenologische Gleichung für die beobachtete Volumenantwort. Sie ist nicht ohne Herleitung eine exakte Wasser-Austragsbilanz. \(S\) muss im jeweiligen Modell ausdrücklich als gemessene relative Gelvolumenabnahme oder als eine andere Observablen-Definition bezeichnet werden.

## 7. Schnittstellen zu den vorhandenen Modellgenerationen

| Vorhandener Block | Beibehaltener Inhalt | Erforderliche Schnittstellenregel |
|---|---|---|
| v0.4 Chemie | \(r_o,r_n,r_d\), pH-/I-/Temperaturmodifikatoren, \(\beta\) | \(c_m,c_o\) werden als Konzentrationen pro Flüssigkeitsvolumen interpretiert; \(N\) als Netzwerk-Si pro Gelvolumen. Reaktionsraten müssen auf dieselbe Gelvolumenbasis umgerechnet werden. |
| v0.4 Brücken | \(B=f_{\mathrm{load}}c_n\beta\) | \(B\) bleibt abgeleitete Tragfähigkeitsgröße und wird nicht als zusätzliche Si-Masse addiert. Der bisherige \(c_n\)-Bezugsraum muss explizit festgelegt und ggf. in \(N\) umgerechnet werden. |
| P8a | Druckspeicher, Darcy-Fluss, No-flow-Test | \(\theta=\theta_{\rm ref}+S_p(p-p_{\rm ref})\) bleibt eine reduzierte Speicher-Schließung. \(\theta\) ist nicht automatisch die Porosität \(\phi\) oder Biot-Fluidgehalt \(\zeta\). |
| P8b | offene hydraulische Ränder und mobiler Si-Austrag | P8b-M/O können auf \(\phi c_m,\phi c_o\) abgebildet werden. Die vorhandenen \(s_N,s_B\)-Variablen müssen auf Doppelzählung geprüft werden: Wenn \(s_B\) eine Teilmenge von \(s_N\) ist, darf die Summe nicht beide als disjunkte Inventare zählen. |
| v1.0 | aktuelle Phasenbilanzen, Biot-artige Mechanik, Speziestransport | W1–W2 und Si1–Si3 bilden die konservative gemeinsame Schnittstelle. Phasenquellen aus Reaktion nur bei begründetem Volumentransfer ergänzen. |
| v1.1 | Biot-Energie mit \(\zeta\), Darcy-Dissipation | Energievariablen und Stoffinventare müssen auf dieselbe Referenzbasis transformiert werden. P0-Energieidentität bleibt auf ihre linearen Annahmen begrenzt. |

### 7.1 Konkrete P8b-Doppelzählungsfrage

P8b führt immobilisierte Pools \(s_N\) und \(s_B\). v0.4 definiert \(B\) hingegen als tragende Teilmenge des Netzwerk-Siliciums und ausdrücklich nicht als zusätzlichen Si-Pool.

Daher ist vor einer Codekopplung eine eindeutige Wahl erforderlich:

1. **Bevorzugte Interpretation:** \(s_N\) repräsentiert das gesamte immobilisierte Netzwerk-Silicium; \(s_B\) wird als abgeleitete Größe \(f_{\rm load}\beta s_N\) geführt und nicht nochmals in der Gesamt-Si-Summe addiert.
2. **Alternative:** \(s_N\) und \(s_B\) sind nachweislich disjunkte chemische Siliciumbestände. Dann muss die Chemie eine stöchiometrisch konservative Aufteilung definieren; diese Interpretation ist nicht mit der bisherigen v0.4-Definition identisch.

Bis diese Frage geklärt ist, dürfen P8b und v0.4 nicht als bereits vollständig integrierte gemeinsame Chemie bezeichnet werden.

### 7.2 Konkrete v1.0-Phasenquellenfrage

v1.0 verwendet für die Feststoff- und Flüssigkeitsphase quellenfreie Bilanzen. Das ist konsistent, wenn die Reaktionsvariablen nur interne Umwandlungen innerhalb der gewählten Phasenbeschreibung darstellen oder wenn das Netzwerk bereits als Teil des Skeletts bilanziert wird. Wenn \(r_n\) tatsächlich gelöste Kieselsäure in eine separate Feststoffphase überführt, muss die Volumen-/Massenübertragung zwischen den Phasen explizit geprüft werden. Die Si-Erhaltung allein legt diese Volumenübertragung nicht fest; dafür werden Stöchiometrie, Dichten und partielle Molvolumina benötigt.

## 8. Was Bilanzidentität ist und was nicht

| Aussage | Status |
|---|---|
| Reaktionsraten heben sich in Si4 auf | Exakte algebraische Erhaltung bei den definierten Transferreaktionen |
| \(B=f_{\rm load}\beta N\) ist kein zusätzlicher Si-Pool | Definitionsentscheidung zur Vermeidung von Doppelzählung |
| W1 ist die gesättigte Flüssigkeitsbilanz | Etablierte Bilanzform unter den genannten Phasen-/Dichteannahmen |
| W2 gilt ohne Feststoffverlust und Phasenquellen | Bedingte Feststoffbilanz |
| \(\theta=\phi\) | Nicht zulässig ohne gesonderte Herleitung |
| \(S_V=V_{\rm ex}/V_0\) | Nicht allgemein gültig; nur unter zusätzlichen Voraussetzungen |
| \(\mathbf K=\mathbf K(\phi,D_f,z)\) | Nicht aus der Bilanz ableitbar; unabhängige konstitutive Schließung |
| \(B\) bestimmt unmittelbar Eigenstrain oder Modul | Nicht aus der Bilanz ableitbar; mechanische Schließung und Daten erforderlich |
| P8b-Randreservoir ist ein Kapillargesetz | Nein; \(p_{\rm ext}\) bleibt vorgegeben, solange keine Kapillarmodellierung ergänzt ist |
| P0-Energieidentität beweist die vollständige Chemie-Mechanik-Kopplung | Nein; sie gilt nur für den hergeleiteten linearen Referenzkern |

## 9. Mindestprüfungen vor einer Codekopplung

### 9.1 Algebraische Bilanztests

1. Summe der drei Si-Reaktionsquellen muss exakt null sein:
   \[
   (-r_o+r_d)+(r_o-r_n)+(r_n-r_d)=0.
   \]
2. Änderung von \(\beta\) darf das Gesamt-Si-Inventar nicht verändern.
3. Ein geschlossener No-flow-Rand muss das Gesamt-Si-Inventar erhalten.
4. Bei offenem Rand muss die Änderung des Gelinventars exakt dem integrierten Netto-Randfluss entsprechen.
5. Wasserbilanz und mobile Si-Advektion müssen denselben \(\mathbf q\)-Fluss verwenden.
6. Ein Wechsel zwischen aktueller und Referenzkonfiguration muss Inventare und Flüsse mit \(J\) und \(J\mathbf F^{-1}\) konsistent transformieren.

### 9.2 Grenzfalltests

- \(\mathbf q=0\), \(\mathbf j_i=0\): kein mobiler Randtransport.
- \(r_o=r_n=r_d=0\): jede Spezies wird nur transportiert; Gesamt-Si bleibt bis auf Randfluss erhalten.
- Geschlossene Grenzen: \(N_{\mathrm{Si,out}}=0\).
- \(\beta=0\) oder \(f_{\mathrm{load}}=0\): \(B=0\), aber \(N\) bleibt unverändert.
- \(\beta=1\), \(f_{\mathrm{load}}=1\): \(B=N\), ohne zusätzliche Masse.
- \(\mathbf v_b=\mathbf v_s\): Randfluss reduziert sich auf relativen Darcy- und Diffusionsfluss.
- Keine Deformation \(J=1\): Referenz- und aktuelle Inventare stimmen überein.

### 9.3 Empirische Gegenprüfungen

Für mindestens einen natürlichen Synäreseversuch sollten zeitlich synchron oder an zustandsangepassten Proben erfasst werden:

- Gelvolumen bzw. Geometrie \(V_g(t)\);
- Masse/Volumen des austretenden Syneresats;
- Verdunstungs-Leerkontrolle;
- Gesamt-Si im Ausgangsgel und im Syneresat;
- gelöstes Si im Syneresat;
- pH, Temperatur und Flüssigkeitszusammensetzung;
- soweit verfügbar: Porosität, Permeabilität und ein unabhängiger Netzwerk-/Tragfähigkeitsproxy.

Diese Messungen sind nicht alle Voraussetzung für den mathematischen Bilanzsatz. Sie sind nötig, um zu prüfen, ob die gewählte Bilanzgrenze und die Materialschließungen das reale Zielsystem angemessen beschreiben.

## 10. Empfohlene Implementierungsreihenfolge

1. **Definitions-Gate:** Bezugsvolumen und Einheiten für alle v0.4-/P8-Variablen verbindlich festlegen.
2. **Inventar-Gate:** P8b-\(s_N/s_B\) mit v0.4-\(c_n/\beta/B\) abgleichen; Doppelzählung ausschließen.
3. **Transport-Gate:** dieselbe hydraulische Flussvariable in Wasser- und mobilen Si-Bilanzen verwenden.
4. **Rand-Gate:** äußeren Druck, Außenkonzentration, Rückströmung und bewegte Grenze getrennt spezifizieren.
5. **Volumen-Gate:** Gelvolumenänderung, Flüssigkeitsaustritt und Verdunstung als getrennte Observablen behandeln.
6. **Mechanik-Gate:** erst danach die Volumen-/Phasenbilanz mit Eigenstrain, Biot-Kopplung, Permeabilität und freier Energie verbinden.

Die erste Implementierung soll nur die Bilanzschnittstelle und ihre Tests enthalten. Keine unkalibrierten Kapillar-, Permeabilitäts-, Modul- oder Reaktionsgesetze werden dabei stillschweigend ergänzt.

## 11. Ergebnis und Nicht-Ansprüche

Die hier formulierte Architektur verbindet die Erhaltungsaussagen aus v0.4, P8b und v1.0 auf einer einheitlichen aktuellen Volumenbasis und beschreibt die Transformation auf ein festes Referenzgebiet. Sie macht sichtbar, an welchen Stellen die vorhandenen Modellgenerationen unterschiedliche Variablen verwenden.

Sie ist noch kein vollständiges chemo-poroelastisches Modell und kein empirischer Nachweis für gefällte Silica-Gele. Insbesondere bleiben offen:

- die tatsächliche Phasen-Volumenänderung bei Kondensation/Auflösung;
- die chemische Identität und Bezugsbasis der P8b-Pools \(s_N,s_B\);
- ein validiertes Kapillar-/Benetzungsrandgesetz;
- freie Grenzflächenbewegung und gegebenenfalls Gasphase;
- Aktivitäts- und chemische Potentialmodelle konzentrierter Prozessbrühen;
- Permeabilitäts-, Modul- und Eigenstrain-Schließungen;
- die vollständige freie Energie des gekoppelten Systems.

**Kernaussage:** Erst die konservativen Inventare und Randflüsse werden festgelegt. Danach werden Materialgesetze ergänzt. Ein mathematisch exakter Bilanzsatz wird nicht mit einer experimentell validierten Silica-Konstitutivgleichung verwechselt.
