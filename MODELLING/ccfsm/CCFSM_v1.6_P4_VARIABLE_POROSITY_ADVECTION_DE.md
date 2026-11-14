# CCFSM v1.6 – P4: variable Porosität und konservativer Advektions-Diffusions-Transport

**Datum:** 14.11.2026  
**Geltungsbereich:** natürliche, unbelastete Synärese; Referenzkonfiguration des Feststoffgerüsts; gesättigtes Porenfluid; vier Si-äquivalente Spezies aus P2/P3.  
**Status:** konsistente Bilanzformulierung und semidiskreter Referenzoperator. Kein vollständiger Existenzsatz für das gekoppelte nichtlineare Mehrfeldsystem und keine empirische Kalibrierung.

## 1. Ziel und Modellierungsentscheidung

P3 behandelte konstante Porosität und reine Diffusion. P4 ersetzt diese Vereinfachung durch eine variable Fluidkapazität und den relativen Transport mit dem Porenfluid. Um die Bilanzen nicht durch eine Mischung aus aktuellen und Referenzkoordinaten zu verfälschen, wird P4 in einer festen Referenzkonfiguration des Feststoffgerüsts formuliert.

Es sei \(\Omega_0\subset\mathbb R^3\) das Referenzgebiet. Die Deformation des Gerüsts ist
\[
x=\chi(X,t),\qquad F=\nabla_X\chi,\qquad J=\det F>0.
\]
Die aktuelle Porosität ist \(\phi(X,t)\). Die Fluidkapazität pro Referenzvolumen ist
\[
\theta(X,t)=J(X,t)\phi(X,t)>0.
\]
Die Konzentrationen \(c_i\) sind weiterhin pro aktuellem Porenfluidvolumen definiert (mol Si-Äquivalent/m³ Porenfluid). Die vier Pools sind \(M,O,N,B\).

**Wichtige Unterscheidung:** \(\phi\) ist ein Volumenanteil in der aktuellen Konfiguration; \(\theta=J\phi\) ist die für Referenzbilanzen benötigte Fluidmenge pro Referenzvolumen. In den Speziesbilanzen darf nicht \(\phi\) anstelle von \(J\phi\) eingesetzt werden.

## 2. Porosität und Feststoffbilanz

Für inkompressible Silica-Körner ohne Feststoffverlust gilt in der Referenzkonfiguration
\[
(1-\phi)J=1-\phi_0,
\qquad
\phi=1-\frac{1-\phi_0}{J},
\qquad
\theta=J-(1-\phi_0).
\tag{P4.1}
\]
Hier ist \(\phi_0(X)\in(0,1)\) die Referenzporosität. Die Formel gilt nur solange \(J>1-\phi_0\) und \(J>0\). Sie ist keine universelle Schließung für kompressible Primärpartikel, Auflösung, Fällung mit Feststoffmassenzuwachs oder Rissbildung.

Die Feststoffbilanz lautet
\[
\partial_t[J(1-\phi)]=0.
\tag{P4.2}
\]
Für kompressible Feststoffkörner oder Feststoffreaktionen ist (P4.2) durch eine eigene Feststoffmassenbilanz zu ersetzen.

## 3. Fluidbilanz und Darcy-Fluss

Sei \(Q(X,t)\) der Darcy-Volumenfluss relativ zum Feststoffgerüst, als Referenzflächenfluss (m/s) gemessen. Für inkompressibles Fluid ohne Fluidquellen gilt
\[
\partial_t\theta+\operatorname{Div}_X Q=0.
\tag{P4.3}
\]
Eine mögliche Pull-back-Darcy-Schließung lautet
\[
Q=-J\phi\,F^{-1}\mathbb L_p F^{-T}\nabla_X p.
\tag{P4.4}
\]
\(\mathbb L_p\) ist die aktuelle hydraulische Mobilität (m²/(Pa s)); die Transformation in (P4.4) ist die Piola-Transformation des aktuellen Darcy-Flusses. Bei symmetrisch positiv definitem \(\mathbb L_p\) und invertierbarem \(F\) ist der Referenzmobilitätstensor positiv definit.

(P4.3) ist eine Zwangsbedingung für die Deformation und den Darcy-Fluss. Man darf daher \(J,\phi\) und \(Q\) nicht unabhängig beliebig vorgeben. Ein numerisches Feldpaar \((\theta,Q)\) muss die Fluidbilanz erfüllen oder die Bilanzabweichung explizit als Fehler ausweisen.

## 4. Konservative Speziesbilanzen

Für jede Spezies \(i\in\{M,O,N,B\}\):
\[
\partial_t(\theta c_i)+
\operatorname{Div}_X\left(c_i Q+\mathcal J_i\right)
=\theta R_i(c).
\tag{P4.5}
\]
Der advective Fluss \(c_iQ\) transportiert gelöste Spezies relativ zum Gerüst. Der diffusive Referenzfluss ist
\[
\mathcal J_i=-\theta D_i F^{-1}F^{-T}\nabla_Xc_i.
\tag{P4.6}
\]
Für isotrope aktuelle Diffusion \(D_i>0\). Bei Anisotropie wird \(D_i\) durch einen symmetrischen positiven Diffusionstensor ersetzt. Die P2-Reaktionsterme bleiben
\[
R(c)=(-r_1,\ r_1-r_2,\ r_2-r_3,\ r_3),\qquad
\sum_iR_i=0.
\tag{P4.7}
\]
Damit folgt die lokale Si-Äquivalentbilanz
\[
\partial_t\left(\theta\sum_i c_i\right)+
\operatorname{Div}_X\left(Q\sum_i c_i+\sum_i\mathcal J_i\right)=0.
\tag{P4.8}
\]
Bei geschlossenen No-Flux-Rändern bleibt die gesamte Si-Äquivalentmenge exakt erhalten. Bei einer drainierenden freien Oberfläche ist der Randfluss dagegen Teil der physikalischen Bilanz; er darf nicht künstlich auf null gesetzt werden.

Aus (P4.3) und (P4.5) folgt die nichtkonservative Konzentrationsform
\[
\theta\,\partial_t c_i+
Q\cdot\nabla_Xc_i+
\operatorname{Div}_X\mathcal J_i
=\theta R_i(c),
\tag{P4.9}
\]
sofern die Produktregel für hinreichend reguläre Felder zulässig ist. Die konservative Form (P4.5) bleibt die maßgebliche schwache und numerische Form.

## 5. Reaktionskinetik und thermodynamische Grenze

Die lokalen Raten und Affinitäten werden unverändert aus P2 übernommen. Damit bleibt die Si-Erhaltung des Reaktionsblocks erhalten. P4 behauptet **keine** vollständige Energieungleichung für das gekoppelte System: variable \(\theta\), Advektion, Deformation und Druckarbeit müssen in einer gemeinsamen freien Energie mit konsistenten Randtermen hergeleitet werden. Die P2/P3-Dissipationsformel darf nicht unverändert als Gesamtenergiebeweis ausgegeben werden.

Ein thermodynamisch vollständiger nächster Schritt benötigt mindestens:
- eine freie Energie \(\Psi(F,\theta,c,T,\text{interne Variablen})\),
- konjugierte Spannung, Porendruck und chemische Potentiale aus derselben \(\Psi\),
- Onsager-konsistente Mobilitäts- und Diffusionstensoren,
- konsistente freie-Oberflächen-/Reservoir-Randbedingungen.

## 6. Schwache Form und mathematischer Status

Für vorgegebene Koeffizienten \(F,\theta,Q\), die
\[
0<\theta_*\le\theta\le\theta^*,\quad
F,F^{-1}\in L^\infty,\quad
\operatorname{Div}Q=-\partial_t\theta
\]
erfüllen, ist (P4.5) ein lineares bzw. quasi-positiv semilineares parabolisches Reaktions-Advektions-Diffusionssystem, sofern die P2-Raten lokal Lipschitz sind und die Diffusion gleichmäßig elliptisch bleibt. Bei geeigneter zeitlicher und räumlicher Regularität der vorgegebenen Felder kann die Standardtheorie parabolischer Systeme für lokale bzw. globale schwache Lösungen herangezogen werden; die globale Aussage benötigt zusätzlich eine nachgewiesene Invarianz-/Wachstumsabschätzung für die konkrete Reaktionsmatrix und Randbedingungen.

**Nicht bewiesen** ist hier ein Existenz-/Eindeutigkeitssatz für das bidirektional gekoppelte System, in dem \(F,\theta,Q,p,c\) und die Netzwerkvariablen gemeinsam unbekannt sind. Ebenso wenig wird ein klassischer Regularitätssatz für nichtlineare 3D-Gleichungen behauptet. P0s linearer Satz und P2s lokaler Reaktionssatz reichen dafür nicht aus.

## 7. Numerische Referenzimplementierung

ccfsm_p4_variable_porosity.py implementiert einen konservativen semidiskreten Finite-Volumen-Operator auf uniformen 1D/2D/3D-Referenzgittern:
- zellweise positive Fluidkapazität \(\theta\),
- innere orientierte Flächenflüsse \(Q\), äußere No-Flux-Flächen,
- Upwind-Advektion und symmetrische Zwei-Punkt-Diffusion,
- P2-Reaktion pro Zelle,
- gemeinsame diskrete Fluidbilanz \(\dot\theta=-\operatorname{Div}Q\),
- Konzentrationsableitung aus der konservativen Stoffmenge \(\theta c_i\).

Der Operator gibt \((\dot c,\dot\theta)\) zurück. Die Kombination erhält die diskrete Fluidbilanz und die globale Si-Menge (bis auf Rundungsfehler), wenn Reaktions- und Randflüsse die oben genannten Bedingungen erfüllen. Es ist kein Zeitintegrator. Für Zeitintegration sind konservative, positivity-preserving Verfahren und eine passende CFL-/Schrittweitenkontrolle erforderlich. Der Upwind-Anteil ist dissipativ; der Operator ersetzt keine Konvergenzstudie.

## 8. Annahmen, offene Parameter und Validierung

Noch nicht kalibriert sind insbesondere \(\phi_0\), \(F\) bzw. die Mechanik, \(\mathbb L_p\), \(D_i\), Tortuosität, P2-Kinetikparameter, Anfangsprofile und freie-Oberflächen-Randdaten. Die vorhandenen natürlichen Synäresekurven identifizieren diese Größen nicht getrennt. Druckzell-/Oedometerdaten bleiben ausgeschlossen aus der natürlichen Synäresekalibrierung.

P4 ist daher:
- **mathematisch:** konservative Bilanzstruktur und wohldefinierter semidiskreter Operator unter positiven Kapazitäten;
- **numerisch:** durch Unit-Tests auf Bilanz- und Grenzfälle geprüft, aber noch nicht durch Gitter-/Zeitschritt-Konvergenzstudien verifiziert;
- **physikalisch:** plausible Mischungstheorie-Schließung unter expliziten Annahmen;
- **empirisch:** nicht kalibriert und nicht validiert.

## 9. Anschluss P5

P5 sollte die Mechanik und Fluidbilanz bidirektional schließen: \(F\) aus quasistatischer Kraftbilanz, \(p\) aus Darcy-/Fluidbilanz, \(\theta\) aus Feststoff- und Fluidvolumenbilanz und die freie Energie aus Chemie plus Netzwerk-Eigenstrain. Erst danach ist ein gemeinsamer Energiebeweis für den vollständigen Mehrfeldblock sinnvoll. Die Wärme- und Elektrolyt-/Ladungsbilanz sollten als weitere konservative Felder ergänzt werden, nicht als empirische Korrekturfaktoren.
