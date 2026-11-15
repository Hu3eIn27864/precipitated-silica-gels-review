# Manuskript 1 — strukturelle Identifizierbarkeit und praktische Grenzen

**Stand:** 15.11.2026  
**Bezug:** CCFSM v0.2, Nullstart-Spezialfall des Zwei-Zustands-Modells  
**Status:** mathematische Charakterisierung unter idealisierten Annahmen; keine empirische Parameterschätzung

## 1. Modell und Geltungsbereich

Betrachtet wird

\[
\dot q=k_n(q_\infty-q),\qquad
\dot S=k_h(\eta_a q-S),
\]

mit positiven Raten \(k_n,k_h>0\), \(q_\infty>0\), \(\eta_a>0\). Für die folgende Identifizierbarkeitsaussage wird ausdrücklich der Nullstart

\[
q(0)=0,\qquad S(0)=0
\]

vorausgesetzt. Beobachtet wird ausschließlich die skalare Ausgangsgröße \(S(t)\). Die Größen \(\eta_a\) und \(q_\infty\) werden zunächst nicht separat als bekannt vorausgesetzt.

Die Aussage gilt für die vollständige ideale, kontinuierliche und rauschfreie Ausgangskurve für alle $t\\ge0$ sowie für exakte Kenntnis der Modellklasse. Der Endwert wird dabei als Langzeitgrenze der Kurve bestimmt. Sie ist keine Aussage über endliche, diskrete oder verrauschte Messreihen.

## 2. Exakte Ausgangsantwort

Aus der ersten Gleichung folgt

\[
q(t)=q_\infty(1-e^{-k_nt}).
\]

Einsetzen in die zweite Gleichung und Lösung mit \(S(0)=0\) ergibt für \(k_n\ne k_h\)

\[
S(t)=C\left[
1-\frac{k_h e^{-k_nt}-k_n e^{-k_ht}}{k_h-k_n}
\right],
\qquad C:=\eta_aq_\infty.
\]

Für gleiche Raten \(k_n=k_h=k\) ergibt der stetige Grenzwert

\[
S(t)=C\left[1-(1+kt)e^{-kt}\right].
\]

In beiden Fällen gilt bei den genannten positiven Parametern \(S(t)\to C\) für \(t\to\infty\). Der Endwert identifiziert daher nur das Produkt \(C=\eta_aq_\infty\), nicht dessen Faktoren einzeln.

## 3. Satz — strukturelle Identifizierbarkeit des ungeordneten Ratenpaars

**Satz.** Seien \(k_n,k_h,C>0\). Unter Nullstart und idealer kontinuierlicher Beobachtung von \(S(t)\) ist die Abbildung von den Parametern auf die vollständige Ausgangskurve invariant unter Vertauschung \(k_n\leftrightarrow k_h\). Sofern die Modellklasse exakt gilt, ist aus der vollständigen idealen Kurve der Endwert \(C\) sowie das ungeordnete Ratenpaar \(\{k_n,k_h\}\) eindeutig bestimmbar. Eine Zuordnung, welche der beiden Raten physikalisch die Netzwerkkinetik und welche die hydraulische Relaxation repräsentiert, ist aus \(S(t)\) allein nicht identifizierbar.

### Beweis

Die Laplace-Transformation der Nullstart-Lösung liefert

\[
\widehat S(s)=\frac{C k_nk_h}{s(s+k_n)(s+k_h)}.
\]

Mit dem aus dem Kurvenendwert bestimmten \(C>0\) folgt

\[
\frac{s\widehat S(s)}{C}
=\frac{k_nk_h}{s^2+(k_n+k_h)s+k_nk_h}.
\]

Damit sind die symmetrischen Koeffizienten

\[
a:=k_n+k_h,\qquad b:=k_nk_h
\]

eindeutig durch die rationale Ausgangsantwort festgelegt. Die beiden Raten sind folglich genau die Nullstellen des Polynoms

\[
z^2-az+b=0,
\]

also

\[
\{k_n,k_h\}
=\left\{
\frac{a+\sqrt{a^2-4b}}{2},
\frac{a-\sqrt{a^2-4b}}{2}
\right\}.
\]

Da \(a^2-4b=(k_n-k_h)^2\ge0\), sind die Wurzeln reell und positiv. Die Rekonstruktion bestimmt nur die Menge der beiden Raten; die rationale Antwort ist unter ihrer Vertauschung unverändert. Daher ist eine physikalische Label-Zuordnung aus dem skalaren Ausgang allein unmöglich. Für \(k_n=k_h\) liegt eine doppelte Wurzel vor; das ungeordnete Paar ist dann \(\{k,k\}\). \(\square\)

### Präzisierung der Voraussetzungen

- \(C>0\) ist notwendig. Für \(C=0\) ist die Ausgangskurve im Nullstartfall identisch null und enthält keinerlei Information über die Raten.
- Beide Raten müssen strikt positiv sein. Grenzfälle mit einer Rate null gehören zu einer degenerierten Modellklasse und sind gesondert zu behandeln.
- Die Kurve muss die Modellantwort eindeutig festlegen. In der idealen kontinuierlichen Form bedeutet dies Kenntnis der exakten Ausgangsfunktion; praktisch ist das keine direkt verfügbare Operation.
- Bei unbekanntem oder nicht-null Anfangszustand gilt diese konkrete Transferfunktionsargumentation nicht unverändert. Dann müssen Anfangszustände als zusätzliche Parameter mitanalysiert werden.
- Sind \(\eta_a\) und \(q_\infty\) beide unbekannt, bleiben sie selbst bei perfekter Kenntnis von \(S(t)\) durch die Transformation \((\eta_a,q_\infty)\mapsto(c\eta_a,q_\infty/c)\) mit zulässigem \(c>0\) ununterscheidbar, solange nur ihr Produkt beobachtbar ist.

## 4. Was der Satz nicht behauptet

Der Satz ist ein strukturelles Ergebnis innerhalb einer festgelegten Modellklasse. Er besagt nicht, dass zwei Raten aus einer realen Messreihe stabil geschätzt werden können. Er beweist auch nicht, dass die physikalischen Prozesse im Gel tatsächlich exakt zwei lineare Zeitskalen besitzen. Ebenso wenig liefert er eine separate Schätzung von \(\eta_a\) und \(q_\infty\).

## 5. Praktische Identifizierbarkeit — kritische Regime

### 5.1 Nahezu gleiche Raten

Die Rate-Rekonstruktion verwendet die Diskriminante

\[
\Delta=a^2-4b=(k_n-k_h)^2.
\]

Wenn die beiden Raten nahe beieinanderliegen, ist \(\Delta\) klein. Kleine Fehler in den geschätzten Koeffizienten \(a,b\) können dann relativ große Fehler in der Ratenaufspaltung verursachen. Im Grenzfall gleicher Raten entsteht eine doppelte Wurzel. Die getrennte Schätzung zweier fast gleicher Raten ist daher typischerweise schlecht konditioniert, auch wenn das ungeordnete Paar im idealen mathematischen Sinn eindeutig ist.

### 5.2 Zu grobe frühe Abtastung

Die schnellere Mode klingt auf einer Zeitskala von ungefähr \(1/k_{fast}\) ab. Liegt die erste Messung erst deutlich nach dieser Zeitskala oder ist das Abtastintervall zu groß, wird die frühe Dynamik nur schwach erfasst. Die Daten können dann praktisch kaum zwischen einer schnellen Mode und einem effektiven Anfangsversatz unterscheiden.

### 5.3 Zu kurzes Beobachtungsfenster

Wenn das Beobachtungsfenster deutlich kürzer als die langsamere Zeitskala \(1/k_{slow}\) ist, wird der Endwert \(C\) nicht ausreichend erreicht. Dann sind Endwert und langsame Rate stark korreliert. Eine formal identifizierbare Langzeitinformation kann im verfügbaren Zeitfenster faktisch fehlen.

### 5.4 Rauschen und diskrete Messungen

Bei endlichen verrauschten Daten werden \(a\) und \(b\) nicht direkt beobachtet, sondern müssen über eine Parameterschätzung aus der Kurve gewonnen werden. Korrelationen, ungleichmäßige Messfehler, unbekannte Messoffsets und Unsicherheit des Zeitnullpunkts können die Schätzung zusätzlich destabilisieren. Die idealisierte Eindeutigkeit des Satzes ist deshalb nicht mit statistischer Präzision gleichzusetzen.

### 5.5 Amplituden- und Parameterkonfundierung

Die Ausgangskurve enthält den Endwert \(C=\eta_aq_\infty\). Ohne zusätzliche unabhängige Messung lassen sich \(\eta_a\) und \(q_\infty\) nicht separat aus dieser Kurve bestimmen. Eine gute Schätzung von \(C\) löst diese Konfundierung nicht.

## 6. Konsequenzen für das Versuchsdesign

Um die physikalischen Labels der Raten aufzulösen, ist mindestens eine zusätzliche, zeitaufgelöste Observable erforderlich, die selektiv auf einen der beiden Zustände reagiert. Denkbare, vorab zu validierende Kandidaten sind:

1. eine unabhängige Struktur-/Netzwerkobservable für \(q(t)\) (z. B. eine geeignete zeitaufgelöste Streuungs- oder spektroskopische Kenngröße);
2. eine hydraulische Observable (z. B. Flüssigkeitsabgabe, lokale Feuchte-/Sättigungsverteilung oder ein geeigneter Druck-/Drainageindikator);
3. eine kontrollierte Variation der charakteristischen Drainagelänge, sofern die Geometrie und die Annahme einer dominanten linearen hydraulischen Mode gerechtfertigt sind.

Die Messmethoden sind nicht automatisch direkte Messungen von \(q\) oder \(k_h\). Ihre Beziehung zu den Modellzuständen muss kalibriert und separat begründet werden. Eine zweite Messgröße hilft nur dann bei der Label-Zuordnung, wenn ihre Beobachtungsgleichung die beiden Zustände tatsächlich unterschiedlich koppelt.

**Mindestanforderung an die Zeitplanung:** frühe Messpunkte müssen die schnellere Dynamik auflösen; die Messdauer muss zugleich mehrere langsame Zeitskalen umfassen. Konkrete Abtastzeiten können erst nach einer Größenordnungsabschätzung der erwarteten Raten festgelegt werden.

## 7. Numerische Prüfstrategie für den nächsten Schritt

Vor einer Auswertung experimenteller Daten soll ein reproduzierbares synthetisches Benchmark-Skript erstellt werden. Es soll:

- gleich verteilte und logarithmisch verteilte Ratenpaare einschließlich nahezu gleicher Raten abdecken;
- mehrere Beobachtungsfenster und Abtastintervalle vergleichen;
- kontrollierte Messrauschstufen und Messoffsets untersuchen;
- Profil-Likelihood oder eine andere begründete Unsicherheitsanalyse ergänzen;
- die Konditionierung bzw. Unsicherheit der sortierten Raten \((k_{slow},k_{fast})\) berichten;
- den Unterschied zwischen struktureller Eindeutigkeit und praktischer Schätzbarkeit sichtbar machen.

Eine Fisher-Informationsmatrix kann ergänzend verwendet werden, muss aber mit dem gewählten Messfehlermodell und der Parameterskalierung interpretiert werden. Eine singuläre oder schlecht konditionierte lokale Matrix ist ein Warnsignal, kein universeller Beweis globaler Nichtidentifizierbarkeit.

## 8. Publikationsrelevante Schlussfolgerung

Der belastbare mathematische Kern lautet derzeit:

> Under zero initial conditions and for a positive nonzero endpoint, an ideal continuous shrinkage response uniquely determines the unordered pair of positive kinetic rates and the endpoint product, but it cannot assign the two physical rate labels or separate the accessibility and intrinsic endpoint factors.

Die praktische Identifizierbarkeit bleibt eine offene quantitative Frage. Sie muss mit synthetischen Benchmarks und anschließend — sofern geeignete Primärdaten verfügbar sind — mit transparent dokumentierten Messdaten untersucht werden.

**Claim–Evidence-Einstufung:** Der Satz in Abschnitt 3 ist ein analytisches Resultat unter expliziten Modellannahmen. Die Aussagen in Abschnitt 5 sind qualitative Konditionierungsdiagnosen, noch keine numerisch quantifizierten Grenzen. Die Versuchsdesignpunkte sind Vorschläge, keine bereits experimentell validierten Messprotokolle.
