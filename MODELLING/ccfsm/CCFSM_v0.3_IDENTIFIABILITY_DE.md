# CCFSM v0.3 — strukturelle und praktische Identifizierbarkeit

**Geltungsbereich:** natürliche, mechanisch unbelastete Synärese gefällter Silica-Gele.  
**Fragestellung:** Welche Modellparameter lassen sich aus welcher Messgröße bestimmen?  
**Status:** analytische Aussagen über die derzeitige v0.3-Gleichungsstruktur; keine empirische Parameterschätzung.

## 1. Ergebnis vorweg

Eine einzelne ideale, rauschfreie Schrumpfungskurve `S(t)` kann nicht alle v0.3-Parameter bestimmen. Einige Parameter sind aus dieser Ausgabe **strukturell nicht identifizierbar**, weil sie in der Ausgangsgleichung nach analytischer Reduktion überhaupt nicht vorkommen.

Insbesondere sind aus `S(t)` allein nicht identifizierbar:

- die Relaxationsrate `k_r`, solange nur die Summe aus residualer und relaxierter Kontraktion die Schrumpfung antreibt;
- die Morphologieparameter `k_m,D_{f,0},\Delta D_f,z_0,\Delta z`, weil `D_f` und `z` derzeit keinen Rückkopplungsterm auf `q` oder `S` besitzen;
- die absolute Brückendichteskala und `\Omega_b` getrennt voneinander, wenn keine unabhängige absolute Brückendichtemessung vorliegt.

Das ist stärker als eine bloß schlechte Parameterschätzung: Selbst perfekte, kontinuierliche und rauschfreie `S(t)`-Daten können diese Größen in der aktuellen Modellstruktur nicht einzeln festlegen.

## 2. Analytische Reduktion des Brücken- und Kontraktionsblocks

Die Brückenkinetik lautet:

\[
\dot B=k_b(B_\infty-B),\qquad B(0)=B_0.
\]

Daraus folgt exakt:

\[
B(t)=B_\infty-(B_\infty-B_0)e^{-k_bt}.
\]

Wir setzen `X(t)=\sigma(t)+\epsilon_r(t)`. Aus den beiden Relaxationsgleichungen folgt:

\[
\dot X=\Omega_b\dot B.
\]

Mit `X_0=\sigma_0+\epsilon_{r,0}` erhalten wir:

\[
X(t)=X_0+\Omega_b[B(t)-B_0].
\]

Einsetzen der Lösung für `B(t)` liefert:

\[
\boxed{X(t)=X_0+A(1-e^{-k_bt}),\qquad
A:=\Omega_b(B_\infty-B_0).}
\]

Das innere Schrumpfungspotenzial ist:

\[
\boxed{q(t)=1-\exp[-X_0-A(1-e^{-k_bt})].}
\]

Die beobachtete Schrumpfung erfüllt:

\[
\boxed{\dot S=k_h[\eta_aq(t)-S].}
\]

Damit hängt die Ausgabe `S(t)` nur von den fünf zusammengesetzten Größen

\[
\boxed{(X_0,\ A,\ k_b,\ k_h,\ \eta_a)}
\]

sowie dem Anfangswert `S_0` ab. Die Einzelgrößen `B_0,B_\infty,\Omega_b,k_r,k_m,D_{f,0},\Delta D_f,z_0,\Delta z` sind in dieser reduzierten Ausgangsgleichung nicht alle separat enthalten.

Das ist zunächst eine notwendige Einschränkung der Identifizierbarkeit. Es ist **kein** Beweis, dass jedes der fünf zusammengesetzten Parameter aus einem endlichen verrauschten Datensatz zuverlässig geschätzt werden kann.

## 3. Exakte Nichtidentifizierbarkeit I: Brückendichteskala

Sei `c>0` beliebig. Wir transformieren:

\[
B_0'=cB_0,\qquad B_\infty'=cB_\infty,\qquad
B'(t)=cB(t),\qquad \Omega_b'=\Omega_b/c.
\]

Dann bleibt:

\[
\Omega_b'[B'(t)-B_0']
=\frac{\Omega_b}{c}[cB(t)-cB_0]
=\Omega_b[B(t)-B_0].
\]

Folglich bleiben `X(t),q(t),S(t)` exakt unverändert. Auch die dimensionslose Brückenfraktion bleibt gleich:

\[
B'(t)/B_\infty'=B(t)/B_\infty.
\]

Daher bleiben sogar die in v0.3 berechneten Morphologie-Zielwerte unverändert.

**Schluss:** Ohne eine unabhängige Messung der absoluten Brückendichte kann `\Omega_b` nicht von der Brückendichteskala getrennt werden. Identifizierbar ist höchstens das Produkt `A=\Omega_b(B_\infty-B_0)`.

## 4. Exakte Nichtidentifizierbarkeit II: Relaxationsrate

Die Relaxationsgleichungen lauten:

\[
\dot\\sigma=\Omega_b\dot B-k_r\\sigma,
\qquad
\dot\\epsilon_r=k_r\\sigma.
\]

Ihre Summe ist unabhängig von `k_r`:

\[
\frac{d}{dt}(\\sigma+\\epsilon_r)=\Omega_b\dot B.
\]

Die Schrumpfungsausgabe verwendet nur `q=1-e^{-(\sigma+\epsilon_r)}`. Deshalb erzeugt jede positive Wahl von `k_r` dieselbe `q(t)`- und `S(t)`-Kurve, wenn alle anderen zusammengesetzten Größen gleich bleiben.

**Schluss:** `k_r` ist aus `S(t)` exakt nicht identifizierbar. Sie wird erst durch eine zusätzliche Messung der Partition, beispielsweise residualer Spannung/Relaxation oder eines geeigneten rheologischen Signals, zugänglich.

## 5. Exakte Nichtidentifizierbarkeit III: Morphologieblock

Im Modell gilt:

\[
\dot D_f=k_m(D_{f,eq}-D_f),\qquad
\dot z=k_m(z_{eq}-z),
\]

aber weder `D_f` noch `z` tritt in `\dot X`, `q` oder `\dot S` auf.

Somit kann man bei unveränderten übrigen Parametern `k_m,D_{f,0},\Delta D_f,z_0,\Delta z` variieren, ohne `S(t)` zu verändern.

**Schluss:** Diese Parameter sind aus der Schrumpfungskurve allein strukturell nicht identifizierbar. Dafür sind zeitaufgelöste, skalenklar definierte Morphologie- und Kontaktmessungen erforderlich.

Das ist auch eine wichtige Modellkritik: In v0.3 ist Morphologie derzeit ein parallel laufender Zustandsblock, noch keine mechanistisch rückgekoppelte Ursache der Permeabilität oder des Moduls.

## 6. Was verrät die Endschrumpfung?

Für `t\to\infty` gilt:

\[
q_\\infty=1-e^{-(X_0+A)},\qquad
S_\\infty=\\eta_a[1-e^{-(X_0+A)}].
\]

Die Endschrumpfung allein identifiziert also nur die Kombination:

\[
\boxed{S_\\infty=\\eta_a q_\\infty.}
\]

Sie trennt den zugänglichen Anteil `\eta_a` nicht vom intrinsischen Endpotenzial `q_\infty`.

Die vollständige ideale Zeitkurve kann zusätzliche Forminformation enthalten. Daraus folgt aber nicht automatisch eine robuste Identifizierbarkeit unter realem Messrauschen. Eine formale globale Identifizierbarkeitsanalyse der verbleibenden fünf Parameter ist ein eigener Schritt; hier wird sie nicht vorgetäuscht.

## 7. Praktische Korrelation im Klein-Schrumpfungsbereich

Wenn `X\ll1`, gilt:

\[
q=1-e^{-X}=X+O(X^2).
\]

Dann näherungsweise:

\[
q(t)\\approx X_0+A(1-e^{-k_bt}).
\]

In diesem Bereich erscheint die Schrumpfung hauptsächlich über die Produkte `\eta_aX_0` und `\eta_aA`. `\eta_a` und die Kontraktionsamplituden können daher stark korreliert sein. Bei ausreichend großem Kontraktionsbereich kann die Nichtlinearität theoretisch zusätzliche Information liefern; praktisch entscheidet die Messpräzision und der beobachtete Zeitbereich.

Weiterhin gilt:

- Ist `k_b` sehr schnell gegenüber `k_h`, sieht man die Netzwerkbildung kaum zeitaufgelöst; sie erscheint nahezu als schneller Sprung im inneren Potenzial.
- Ist `k_h` sehr schnell gegenüber `k_b`, folgt `S` dem zugänglichen Potenzial nahezu unmittelbar; die hydraulische Rate ist dann schlecht begrenzt.
- Wird nur der frühe oder nur der späte Zeitbereich gemessen, können Raten und Amplituden stark korreliert sein.

Diese Aussagen beschreiben praktische Identifizierbarkeitsrisiken, nicht zusätzliche exakte Symmetrien.

## 8. Welche Zusatzmessung identifiziert welchen Block?

| Gesuchte Größe | Erforderliche unabhängige Information |
|---|---|
| `B_0,B_\infty,k_b` | zeitaufgelöste absolute Messung tragfähiger Brücken oder ein validierter chemischer Proxy |
| `\Omega_b` | Brückendichte **und** unabhängige Messung des Kontraktionsinventars `X` |
| `k_r` | residualer Anteil `\sigma` oder unabhängige Stress-/Relaxationsmessung |
| `k_m,D_{f,0},\Delta D_f` | zeitaufgelöste `D_f(t)`-Messung mit deklarierter Auswertungsskala |
| `k_m,z_0,\Delta z` | zeitaufgelöste Kontakt-/Koordinationsmessung |
| `k_h,\eta_a` | unabhängiges `q(t)` plus `S(t)`; dann Regression von `\dot S= (k_h\eta_a)q-k_hS` |
| `\kappa_{eff},K_{eff},\mu,L_d` | unabhängige hydraulische, rheologische und geometrische Messungen; aus `k_h` allein ist nur die Kombination `C_g\kappa K/(\mu L_d^2)` bekannt |

Für die letzte Zeile ist wichtig: Selbst wenn `k_h` perfekt bekannt wäre, trennt es die Faktoren `C_g,\kappa_{eff},K_{eff},\mu,L_d` nicht voneinander.

## 9. Empfohlene Identifikationsreihenfolge

1. **Chemie/Brücken:** `B(t)` oder ein unabhängig kalibrierter Proxy, getrennt für Säure- und Basenroute.
2. **Kontraktionsinventar:** unabhängige Bestimmung von `X(t)` oder einer direkt damit verknüpften Netzwerkgröße.
3. **Relaxation:** `\sigma(t)` bzw. ein geeignetes rheologisches Relaxationssignal, um `k_r` zu bestimmen.
4. **Morphologie:** `D_f(t)` und `z(t)` zeitaufgelöst und mit festgelegter Messskala.
5. **Hydraulik:** `\kappa_{eff}`, `K_{eff}`, `\mu` und `L_d` separat erfassen.
6. **Gesamtschrumpfung:** erst dann `S(t)` als gekoppelte Modellprüfung verwenden.

Alle Versuche müssen natürliche, mechanisch unbelastete Synärese abbilden. Erzwungene Synärese und Oedometerdaten sind keine direkte Kalibrierung dieses Datensatzes.

## 10. Konsequenz für die nächste Modellversion

Die aktuelle v0.3 ist als Zustandsbuchhaltung nützlich, aber die Morphologie ist noch nicht kausal an die hydraulische Antwort gekoppelt. Eine spätere Version sollte eine messbar begründete Beziehung zwischen Morphologie/Kontaktstruktur und `\kappa_{eff}` bzw. `K_{eff}` entwickeln. Sie darf nicht einfach `\kappa\propto D_f^n` postulieren: Porenkonnektivität, Porenhalsverteilung, Kontakt-Topologie und Bindungsstärke müssen berücksichtigt werden.

**Wichtig:** Diese Rückkopplung sollte erst nach Auswertung geeigneter Struktur- und Transportdaten ergänzt werden. Andernfalls würden nicht identifizierbare Parameter nur durch zusätzliche Annahmen verdeckt.

## 11. Kernaussage

Eine Schrumpfungskurve ist eine Messung der äußeren Antwort, keine direkte Messung aller inneren Zustände. In CCFSM v0.3 sieht `S(t)` nur eine reduzierte Kombination aus Netzwerk-Kontraktionsinventar, dessen Bildungsrate, hydraulischer Antwort und Zugänglichkeit. Morphologie, Relaxationspartition und absolute Brückendichteskala benötigen jeweils unabhängige Beobachtungen.
