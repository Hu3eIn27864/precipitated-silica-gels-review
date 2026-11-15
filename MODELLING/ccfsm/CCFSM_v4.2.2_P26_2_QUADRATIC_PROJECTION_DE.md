# CCFSM v4.2.2 — P26.2 quadratische Momentenprojektion

**Status:** 1-D-Referenzmethode; Freigabe vorbehaltlich CI-Prüfung.  
**Ziel:** Übertragung stückweise quadratischer Felder zwischen nichtverschachtelten Intervallnetzen unter Erhaltung des nullten, ersten und zweiten räumlichen Moments.

## 1. Rekonstruktion

Auf einer Quellzelle \(I_i=[x_i,x_{i+1}]\) mit Breite \(h_i\), Zentrum \(c_i\) und Zellmittelwert \(\bar u_i\) wird verwendet:

\[
u_i(x)=\bar u_i+a_i\xi+b_i(\xi^2-1/12),\qquad
\xi=(x-c_i)/h_i.
\]

Damit ist der Zellmittelwert exakt \(\bar u_i\), weil beide Zusatzmoden auf \([-1/2,1/2]\) Mittelwert null besitzen. \(a_i,b_i\) sind dimensionslose Modalkoeffizienten und werden explizit übergeben. P26.2 behauptet **keinen automatischen, universell stabilen quadratischen Rekonstruktor**.

## 2. Zielzellprojektion

Für eine Zielzelle \(J_j\) mit Zentrum \(d_j\) und Breite \(H_j\), \(\eta=(x-d_j)/H_j\):

\[
\bar u_j^T=H_j^{-1}\int_{J_j}u_h(x)\,dx,
\]
\[
a_j^T=12H_j^{-1}\int_{J_j}\eta u_h(x)\,dx,\qquad
b_j^T=180H_j^{-1}\int_{J_j}(\eta^2-1/12)u_h(x)\,dx.
\]

Die Faktoren folgen aus \(\int_{-1/2}^{1/2}\eta^2d\eta=1/12\) und
\(\int_{-1/2}^{1/2}(\eta^2-1/12)^2d\eta=1/180\). Drei-Punkt-Gaußquadratur integriert die auftretenden Polynome bis Grad vier exakt. Damit werden drei lokale Momente pro Zielzelle bis auf Rundungsfehler übertragen.

Die globalen rohen Momente \(\int u\,dx,\int xu\,dx,\int x^2u\,dx\) bleiben bei gleicher Gebietsabdeckung erhalten.

## 3. Extrema und Positivität

Die Minimumsfunktion prüft Endpunkte und – falls vorhanden – den inneren Scheitelpunkt des quadratischen Polynoms. Der optionale Positivitätsbegrenzer skaliert beide Moden mit demselben Faktor \(0\leq\lambda\leq1\), bis die Rekonstruktion nichtnegativ ist. Der Mittelwert und damit die Zellmasse bleiben unverändert. Die Begrenzung kann lokale Forminformation und formale Ordnung reduzieren; sie ist keine allgemeine TVD-Garantie.

Ein positiver Zellmittelwert allein garantiert keine überall positive quadratische Rekonstruktion. Positivität ist daher standardmäßig ausgeschaltet und muss für geeignete nichtnegative Inventare ausdrücklich aktiviert werden.

## 4. Verifikation

Regressionen decken ab: exakte Übertragung eines globalen quadratischen Polynoms auf ein nichtpassendes Netz; Erhaltung der globalen Momente nullter, erster und zweiter Ordnung; Identitäts- und Konstantenfall; konkave/konvexe Krümmung (Maxima/Minima); Positivitätsbegrenzung bei unverändertem Zellmittelwert; ungültige Gebietsabdeckung und Koeffizientenformen.

Der CI-Referenzlauf erzeugt die Dateien p26_2_quadratic_projection.csv und summary.json.

## 5. Geltungsgrenzen

- Nur eindimensionale Intervalle und stückweise quadratische Quellfelder.
- Koeffizienten \(a_i,b_i\) werden vorgegeben; keine automatische WENO-/DG-/FE-Rekonstruktion.
- Keine 2-D/3-D-Polyederintersection, keine gekrümmte Zylindergeometrie.
- Die Erhaltung räumlicher Momente ist keine Erhaltung mechanischer Energie, Druck oder beliebiger nichtlinearer Funktionen.
- Ein übertragener Druck ist kein mechanisch konsistenter P19-Druck; für gekoppelte Mechanik ist P19 erneut zu lösen.
- Synthetische Polynomtests sind Softwareverifikation, keine physikalische Validierung gefällter Silicagel-Gele.

## 6. Nächste Schritte

P26.3 sollte eine unabhängige Verfeinerungsstudie der Momentenfehler, Konditionierung und Positivitätsverluste ergänzen. Danach sind 2-D/3-D-Intersection-Geometrien und eine belastbare FE-Quadratur-zu-Polynom-Rekonstruktion separate Entwicklungspakete.
