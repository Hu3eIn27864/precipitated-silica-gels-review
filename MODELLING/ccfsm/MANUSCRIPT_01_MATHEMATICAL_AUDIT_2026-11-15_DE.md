# Manuskript 1 — erster mathematischer Audit von CCFSM v0.2

**Datum:** 15.11.2026  
**Prüfumfang:** Modellgleichungen, explizite Lösung, Gleichratenlimit, Invarianzargument, Transferfunktion und Abgleich mit `ccfsm_two_stage.py`.  
**Status:** interner unabhängiger Rechenaudit; noch keine externe mathematische Begutachtung und keine endgültige Manuskriptfreigabe.

## 1. Modell

[
\dot q=k_n(q_\infty-q),\qquad
\dot S=k_h(\eta_aq-S),
]
mit
[
k_n,k_h>0,\quad 0<\eta_a\le1,\quad
0\le S_0\le\eta_aq_0\le\eta_aq_\infty<1.
]

## 2. Explizite Lösung — algebraisch bestätigt

[
q(t)=q_\infty+(q_0-q_\infty)e^{-k_nt}.
]

Für (k_h\ne k_n):
[
S(t)=\eta_aq_\infty+(S_0-\eta_aq_\infty)e^{-k_ht}
+\frac{\eta_ak_h(q_0-q_\infty)}{k_h-k_n}
(e^{-k_nt}-e^{-k_ht}).
]

Für (k_h=k_n=k):
[
S(t)=\eta_aq_\infty+
[S_0-\eta_aq_\infty+\eta_ak(q_0-q_\infty)t]e^{-kt}.
]

Der Gleichratenfall folgt als stetiger Grenzwert der ungleichen Formel. Die Implementierung verwendet für die Differenz der Exponentialfunktionen eine `expm1`-basierte dividierte Differenz und den exakten Grenzwert (t e^{-kt}). Das ist numerisch sinnvoller als eine direkte Division durch (k_h-k_n).

Ein zusätzlicher interner numerischer Quercheck verglich die geschlossene Formel für 30 zufällig gewählte zulässige Parametersätze mit einer RK4-Integration. Maximale absolute Abweichung im Testlauf: ca. (1.0\times10^{-15}). Dies ist ein Implementierungsquercheck, kein Beweis.

## 3. Invarianz und Monotonie — Beweisstruktur bestätigt

Setze (d(t)=\eta_aq(t)-S(t)). Dann
[
\dot d=\eta_ak_n(q_\infty-q)-k_hd.
]
Die Variation-der-Konstanten-Formel lautet
[
d(t)=d(0)e^{-k_ht}
+\eta_ak_n\int_0^t e^{-k_h(t-r)}
[q_\infty-q(r)]\,dr.
]
Aus (q_0\le q_\infty) folgt (q(r)\le q_\infty), und aus (d(0)\ge0) folgt (d(t)\ge0). Somit
[
\dot S=k_hd\ge0,\qquad
0\le S_0\le S(t)\le\eta_aq(t)\le\eta_aq_\infty<1.
]
Da (q(t)\to q_\infty) und die hydraulische Relaxation stabil ist, gilt (S(t)\to\eta_aq_\infty).

**Grenze:** Die Monotonie folgt nicht für beliebige Anfangsdaten. Die geordnete Anfangsbedingung muss im Satz und Abstract ausdrücklich stehen.

## 4. Strukturelle Nichtidentifizierbarkeit — bestätigt

Für (q_0=S_0=0) ergibt die Laplace-Transformation
[
\mathcal L\{S\}(s)=
\frac{\eta_aq_\infty k_nk_h}
{s(s+k_n)(s+k_h)}.
]
Der Ausdruck ist invariant unter (k_n\leftrightarrow k_h). Aus einer idealen einzelnen Nullstart-Kurve können daher die physikalischen Ratenlabels nicht zugeordnet werden. Ebenso erscheint der Endpunkt nur als Produkt (\eta_aq_\infty).

Dies bedeutet **nicht**, dass das ungeordnete Ratenpaar prinzipiell unidentifizierbar wäre.

## 5. Ergänzung für Manuskript 1: inverse Rückgewinnung des ungeordneten Ratenpaars

Für (C=\eta_aq_\infty>0) und eine ideal bekannte Antwort für alle (t\ge0) gilt
[
\frac{s\,\mathcal L\{S\}(s)}{C}
=\frac{k_nk_h}{s^2+(k_n+k_h)s+k_nk_h}.
]
Die normierte rationale Übertragungsfunktion bestimmt die Koeffizienten
[
a=k_n+k_h,\qquad b=k_nk_h.
]
Damit sind die beiden Raten als ungeordnete Wurzeln
[
\{k_n,k_h\}
=\left\{
\frac{a-\sqrt{a^2-4b}}2,
\frac{a+\sqrt{a^2-4b}}2
\right\}
]
bestimmt, sofern (a>0), (b>0) und (a^2-4b\ge0). Bei (a^2=4b) fallen beide Raten zusammen. Die Zuordnung „Netzwerk“ versus „hydraulisch“ bleibt ohne zusätzliche unabhängige Beobachtung unbestimmt.

**Noch zu präzisieren:** Identifizierbarkeit bei (C=0), Messfenster (0\le t\le T<\infty), verrauschten/diskreten Beobachtungen und nahezu gleichen Raten. Diese Fälle gehören zur praktischen Identifizierbarkeit, nicht zum idealen strukturellen Satz.

## 6. Codeabgleich

`ccfsm_two_stage.py` implementiert:
- (q(t)) korrekt;
- (S(t)) mit stabiler dividierter Differenz und Gleichratenlimit;
- (\dot S=k_h(\eta_aq-S)), mit kleiner Rundungs-Toleranzkorrektur;
- (k_h=3600 C_g\kappa K/(\mu L_d^2)) in h(^{-1});
- isotrope finite Kinematik (\lambda=(1-q)^{1/3});
- numerische Rückgewinnung des ungeordneten Ratenpaars aus Summe und Produkt.

Die zwölf vorhandenen Tests decken Anfangszustände, Nullstart-Lag, gleiche/nahe gleiche Raten, Invarianz/Monotonie als numerische Regression, Langzeitgrenze, Zugänglichkeit, Ratenvertauschung, Ratenrückgewinnung, (L_d^{-2})-Skalierung, finite Kinematik und ungültige Eingaben ab.

**Zusätzliche Tests empfohlen:**
1. geschlossene Lösung für zufällige zulässige Anfangsdaten gegen unabhängige numerische Integration;
2. Residuen der beiden ODEs aus der analytischen Lösung;
3. Grenzübergang (k_h\to k_n) über mehrere Größenordnungen;
4. numerische Stabilität bei sehr kleinem/großem (k t);
5. Rückgewinnung bei exakt gleichen Raten und nahe zusammenliegenden Raten;
6. explizite Behandlung von (C=0) und degenerierten Beobachtungen.

## 7. Offene wissenschaftliche Punkte vor Einreichung

- Vollständiger Prior-Art-Abgleich: insbesondere Scherer (1989) und weitere Synerese-/Kompartimentmodelle. Die bloße Zwei-Exponential-Form ist nicht automatisch neu.
- Begründung, weshalb die Zustandsgröße (q) und die Grenzflächenzugänglichkeit (\eta_a) für natürliche gefällte Silica-Gele sinnvolle, falsifizierbare Größen sind.
- Praktische Identifizierbarkeit: Sensitivitäts-/Konditionsanalyse für endliche, verrauschte Zeitreihen.
- Beleg der hydraulischen (L_d^{-2})-Skalierung nur unter den genannten First-mode-Annahmen.
- Unabhängiges mathematisches Gegenlesen durch eine fachkundige Person.
- Keine Zwei-Raten-Parameteranpassung an die vorhandenen approximativen Digitalisate ohne unabhängige Zustandsmessung.

## 8. Ergebnis des ersten Audits

**Kein algebraischer Widerspruch** in der zentralen v0.2-Lösung, im Gleichratenlimit oder im Invarianzargument gefunden. Die Codeformel stimmt mit der geschlossenen Lösung überein. Die Ratenvertauschungs-Symmetrie ist korrekt.

Der wichtigste nächste mathematische Ausbau ist die rigorose inverse Charakterisierung des ungeordneten Ratenpaars und danach eine praktische Identifizierbarkeitsanalyse. Das ist noch keine externe Prüfung und kein Beleg dafür, dass die reale Silica-Synerese exakt dem Zweizustandsmodell folgt.
