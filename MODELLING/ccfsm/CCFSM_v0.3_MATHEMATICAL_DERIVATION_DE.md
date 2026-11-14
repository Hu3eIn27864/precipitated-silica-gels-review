# CCFSM v0.3 – mathematische Herleitung und verständliche Beweise

**Geltungsbereich:** natürliche, mechanisch unbelastete Synärese gefällter Silica-Gele.  
**Status:** mathematische Eigenschaften des formulierten Modells; keine empirische Validierung der konstitutiven Ansätze.

## 1. Modellidee in einem Satz

Das Gelnetzwerk bildet tragfähige Brücken, reorganisiert dabei seine Morphologie und entwickelt ein inneres Schrumpfungspotenzial. Die Flüssigkeit kann dieses Potenzial nur mit einer endlichen hydraulisch-mechanischen Geschwindigkeit als äußere Volumenabnahme sichtbar machen.

Wir unterscheiden deshalb strikt zwischen dem inneren Potenzial `q(t)` und der beobachteten Schrumpfung `S(t)`.

## 2. Zustände und Einheiten

| Symbol | Bedeutung | Einheit |
|---|---|---|
| `B` | effektive Dichte tragfähiger Siloxanbrücken | mol m`^{-3}` |
| `D_f` | fraktale Dimension | dimensionslos |
| `z` | mittlere Kontaktzahl | dimensionslos |
| `\sigma` | noch nicht relaxierter logarithmischer Kontraktionsanteil | dimensionslos |
| `\epsilon_r` | relaxierter/akkommodierter logarithmischer Kontraktionsanteil | dimensionslos |
| `q` | intrinsisches Schrumpfungspotenzial | dimensionslos |
| `S` | beobachtete relative natürliche Schrumpfung | dimensionslos |

Die Größe `\sigma` ist in dieser reduzierten Fassung keine Spannung in Pa. Der Name „Eigenstress-Kontraktion“ bezeichnet einen nicht relaxierten Kontraktionsanteil. Eine Spannung in Pa müsste durch eine zusätzliche konstitutive Beziehung mit einem Modul eingeführt werden.

## 3. Brückenbildung

\[
\dot B=k_b(B_\infty-B),\qquad k_b>0.
\]

Für konstante Parameter und Anfangswert `B(0)=B_0` gilt:

\[
B(t)=B_\infty-(B_\infty-B_0)e^{-k_bt}.
\]

**Folgerung:** Falls `0\le B_0\le B_\infty`, dann gilt für alle `t\ge0`:

\[
0\le B(t)\le B_\infty,\qquad \dot B(t)\ge0.
\]

Der Grenzwert ist `B_\infty`. Das ist eine sättigende Modellkinetik. Ob reale Brückenbildung für eine gegebene Rezeptur tatsächlich durch eine Kinetik erster Ordnung ausreichend beschrieben wird, ist experimentell zu prüfen.

## 4. Morphologische Nachführung

\[
D_{f,eq}=D_{f,0}+\Delta D_f B/B_\infty,
\qquad
\dot D_f=k_m(D_{f,eq}-D_f),
\]
\[
z_{eq}=z_0+\Delta z B/B_\infty,
\qquad
\dot z=k_m(z_{eq}-z).
\]

Die Zielwerte ändern sich mit `B(t)`, während die tatsächlichen Morphologiegrößen ihnen mit Verzögerung folgen. `k_m` ist daher eine morphologische Nachführungsrate und nicht die Brückenbildungsrate.

Da `B(t)` bekannt ist, kann man die erste Gleichung auch explizit lösen. Mit
`a=1-B_0/B_\infty` und `D_{f,\infty}=D_{f,0}+\Delta D_f` ist der Zielwert
`D_{f,eq}=D_{f,\infty}-\Delta D_f a e^{-k_bt}`. Für `k_m\ne k_b`:

\[
D_f(t)=D_{f,\\infty}
+\left(D_f(0)-D_{f,\\infty}
+\frac{k_m\\Delta D_f a}{k_m-k_b}\right)e^{-k_mt}
-\frac{k_m\\Delta D_f a}{k_m-k_b}e^{-k_bt}.
\]

Für `k_m=k_b` ergibt sich der stetige Grenzfall:

\[
D_f(t)=D_{f,\\infty}
+\left[D_f(0)-D_{f,\\infty}-k_m\\Delta D_f a\,t\right]e^{-k_mt}.
\]

Für `z(t)` gilt dieselbe Formel mit `D_{f,0},\Delta D_f,D_f(0)` ersetzt durch `z_0,\Delta z,z(0)`.

Diese Gleichungen zeigen ausdrücklich, dass Morphologie und Chemie zwei verschiedene Zeitskalen besitzen können.

## 5. Kontraktionsinventar und Relaxation

Die Brückenbildung erzeugt einen logarithmischen Kontraktionszuwachs:

\[
\dot\\chi_b=\\Omega_b\\dot B.
\]

Der noch nicht relaxierte Anteil und der bereits akkommodierte Anteil entwickeln sich gemäß:

\[
\dot\\sigma=\\Omega_b\\dot B-k_r\\sigma,
\qquad
\dot\\epsilon_r=k_r\\sigma,
\qquad k_r>0.
\]

Addition liefert:

\[
\frac{d}{dt}(\\sigma+\\epsilon_r)=\\Omega_b\\dot B.
\]

Integration zwischen `0` und `t` ergibt die exakte Bilanz:

\[
\boxed{X(t):=\\sigma(t)+\\epsilon_r(t)
=X_0+\\Omega_b[B(t)-B_0].}
\]

Das ist die zentrale Invariante des Relaxations-Teils. Relaxation verschiebt Kontraktion zwischen `\sigma` und `\epsilon_r`; sie löscht das Gesamtinventar `X` nicht.

**Wichtige Anfangsbedingung:** Nur wenn `X_0=\Omega_b B_0` gilt, vereinfacht sich die Bilanz zu `X(t)=\Omega_b B(t)`. Bei einem vorgealterten Gel müssen die Anfangswerte `B_0,\sigma_0,\epsilon_{r,0}` daher konsistent beschrieben werden. Die allgemein gültige Bilanz ist die Gleichung mit `X_0`.

Für konstante Raten ist auch `\sigma` explizit lösbar. Mit `\Delta B_0=B_\infty-B_0` gilt für `k_r\ne k_b`:

\[
\\sigma(t)=\\sigma_0e^{-k_rt}
+\\Omega_b k_b\\Delta B_0
\\frac{e^{-k_bt}-e^{-k_rt}}{k_r-k_b}.
\]

Für `k_r=k_b`:

\[
\\sigma(t)=e^{-k_rt}
[\\sigma_0+\\Omega_b k_b\\Delta B_0t].
\]

Danach folgt `\epsilon_r(t)=X(t)-\sigma(t)`.

## 6. Inneres Schrumpfungspotenzial

Wir definieren:

\[
q(t)=1-e^{-X(t)},\qquad X=\\sigma+\\epsilon_r.
\]

Wenn `X_0\ge0`, `\Omega_b>0` und `\dot B\ge0` gelten, dann:

\[
\\dot X=\\Omega_b\\dot B\\ge0,
\qquad
\\dot q=e^{-X}\\dot X\\ge0.
\]

Damit ist `q` monoton nicht fallend. Außerdem gilt für endliches `X\ge0`:

\[
0\\le q<1.
\]

Dies ist ein mathematischer Satz über die gewählte Definition von `q`, kein experimenteller Nachweis, dass reale Gel-Schrumpfung exakt dieser Exponentialfunktion folgt.

## 7. Äußerlich beobachtete natürliche Synärese

\[
\dot S=k_h(\\eta_a q-S),
\qquad k_h>0,\quad 0<\\eta_a\\le1.
\]

`\eta_a` ist der zugängliche Anteil des inneren Potenzials unter den natürlichen Entwässerungs- und Grenzflächenbedingungen. `k_h` beschreibt die Geschwindigkeit, mit der `S` dem zugänglichen Zielwert `\eta_a q` folgt.

Die exakte Integralform lautet:

\[
S(t)=S_0e^{-k_ht}
+k_h\\eta_a\\int_0^t e^{-k_h(t-s)}q(s)\\,ds.
\]

Das ist eine gewichtete Vorgeschichte von `q`: Die beobachtete Schrumpfung hängt nicht nur vom momentanen Potenzial, sondern auch von dessen zeitlichem Verlauf ab.

### Satz: Positivität, Schrumpfungsgrenze und Monotonie

Angenommen:

1. `k_h>0` und `0<\eta_a\le1`,
2. `q(t)` ist stetig und monoton nicht fallend,
3. `0\le S_0\le\eta_a q(0)`.

Dann gilt für alle `t\ge0`:

\[
0\\le S(t)\\le\\eta_a q(t)<1,
\qquad \\dot S(t)\\ge0.
\]

**Beweis:** Setze `g(t)=\eta_a q(t)-S(t)`. Dann folgt aus der Modellgleichung:

\[
\\dot g=\\eta_a\\dot q-k_hg.
\]

Mit dem integrierenden Faktor `e^{k_ht}` erhält man:

\[
g(t)=g(0)e^{-k_ht}
+\\eta_a\\int_0^t e^{-k_h(t-s)}\\dot q(s)\\,ds.
\]

Beide Terme sind nichtnegativ, weil `g(0)\ge0` und `\dot q\ge0`. Also ist `g(t)\ge0`. Damit gilt `\dot S=k_hg\ge0` und `S\le\eta_a q`. Aus `S_0\ge0` und der Lösung der linearen Gleichung folgt außerdem `S(t)\ge0`. Zusammen mit `q<1` folgt die Behauptung. `\square`

Der Satz ist bewusst bedingt: Wenn ein Anfangswert `S_0>\eta_a q(0)` gewählt wird oder das Potenzial später sinkt, ist Monotonie nicht automatisch garantiert.

## 8. Hydraulische Zeitskala und Dimensionsprüfung

Als reduzierte erste-Moden-Näherung verwenden wir:

\[
k_h=3600\\,C_g
\\frac{\\kappa_{eff}K_{eff}}{\\mu L_d^2}
\\quad [\\mathrm{h}^{-1}].
\]

Dabei sind `\kappa_{eff}` die effektive Permeabilität in m², `K_{eff}` ein effektiver Netzwerk-/Kompressionsmodul in Pa, `\mu` die dynamische Viskosität in Pa s und `L_d` eine charakteristische Entwässerungslänge in m. `C_g` ist ein dimensionsloser Geometrie-/Randbedingungsfaktor; 3600 wandelt s⁻¹ in h⁻¹ um.

Dimensionsprüfung:

\[
\\frac{\\mathrm{m}^2\\,\\mathrm{Pa}}
{(\\mathrm{Pa}\\,\\mathrm{s})\\,\\mathrm{m}^2}
=\\mathrm{s}^{-1}.
\]

Daraus folgen die Modellskalierungen `k_h\propto\kappa_{eff}`, `k_h\propto K_{eff}`, `k_h\propto1/\mu` und `k_h\propto1/L_d^2`. Diese sind Konsequenzen der reduzierten hydraulischen Näherung. Insbesondere muss `K_{eff}` für natürliche freie Synärese experimentell passend definiert und bestimmt werden; ein Oedometer-Modul darf nicht ungeprüft eingesetzt werden.

## 9. Was ist mathematisch bewiesen – und was noch nicht?

**Innerhalb des Modells bewiesen:**

- die Brückendichte bleibt im zulässigen Intervall und steigt monoton;
- Morphologiegrößen folgen ihren zeitabhängigen Zielwerten mit einer eigenen Relaxationszeit;
- die Summe `\sigma+\epsilon_r` erfüllt eine exakte Bilanz;
- bei nichtnegativem Kontraktionsinventar steigt `q` monoton und bleibt kleiner als eins;
- unter den genannten Anfangsbedingungen steigt `S` monoton und bleibt unter `\eta_a q`.

**Nicht bewiesen:**

- dass Brückenbildung in realen Silica-Gelen erster Ordnung folgt;
- dass `D_f` und `z` linear mit `B/B_\infty` gekoppelt sind;
- dass die gewählte Exponentialabbildung `q=1-e^{-X}` die reale Kontraktion quantitativ trifft;
- dass die hydraulische Ein-Moden-Näherung alle Geometrie-, Grenzflächen- und Porenstruktureffekte erfasst;
- dass die Parameter aus einer einzelnen Schrumpfungskurve identifizierbar sind.

Diese offenen Punkte benötigen unabhängige, zeitaufgelöste Messungen. Insbesondere müssen Säure- und Basenroute separat untersucht werden. Daten aus erzwungener Synärese oder Oedometer-Versuchen sind keine direkte Kalibrierung der hier betrachteten natürlichen Synärese.

## 10. Empfohlene nächste mathematische Schritte

1. Die Anfangszustände vorgealterter Gele und die Bilanz `X_0+\Omega_b(B-B_0)` formal und im Code durchgängig prüfen.
2. Die exakten Lösungen für `B,D_f,z,\sigma` als Referenz gegen den RK4-Integrator testen.
3. Für `S` die Integralform numerisch unabhängig auswerten und mit RK4 vergleichen.
4. Danach strukturelle Identifizierbarkeit analysieren: Welche Parameter lassen sich aus `S(t)` allein überhaupt bestimmen, und welche erfordern unabhängige Messungen von `B,D_f,z,\kappa,K,\mu`?

Erst nach diesen Schritten sollte eine Parameterschätzung an experimentellen Kurven erfolgen.
