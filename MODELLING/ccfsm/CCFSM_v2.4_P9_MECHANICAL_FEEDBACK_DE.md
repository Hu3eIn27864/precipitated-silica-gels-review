# CCFSM P9 — mechanische Rückkopplung, Brückeneigenverzerrung und Permeabilität

**Status:** konstitutiver Modellbaustein und algebraisch geschlossene lokale 1D-Bar-Kopplung; keine empirische Kalibrierung und noch kein räumlicher gekoppelter PDE-Löser.

## 1. Ziel und Abgrenzung

P9 schließt die in P5/P8c noch nicht räumlich-mechanisch gekoppelte Rückkopplung zwischen Netzwerkbrücken, Eigenverzerrung, Porendruck und intrinsischer Permeabilität. Der Geltungsbereich bleibt die natürliche, unbelastete Synärese; die implementierte Randtraktion ist ein mathematischer Kontrollparameter und keine Kalibrierung an erzwungener Konsolidierung.

Die Mechanik wird als 1D-Bar mit axialer Dehnung und verschwindenden lateralen Gesamtdehnungen reduziert. Die chemische Eigenverzerrung bleibt isotrop. Das ist eine explizite Reduktion, nicht die allgemeine 3D-Biot-Mechanik.

## 2. Zustände und Brückenfraktion

Für mobile Inventare (m_M,m_O), immobilisierte Netzwerk-Inventare (s_N,s_B) und Flüssigkeitskapazität (	heta) gilt

[
b=\frac{s_B}{s_N+s_B+\delta_B},\qquad
\varepsilon_{ch}=\beta_B(b-b_0).
]

Die Referenzvolumenänderung der Flüssigkeit ist
[
\zeta=\theta-\theta_{ref}.
]

## 3. Konsistente Biot-Mechanik unter axialer Traktion

Mit axialer Gesamtdehnung (e), Lamé-Konstante (\lambda), Schubmodul (G), Biot-Modul (M), Biot-Koeffizient (\alpha_B) und vorgegebener axialer Traktion (t):

[
H=\lambda+2G,\quad
p=M(\zeta-\alpha_B e),
]
[
t=H(e-\varepsilon_{ch})-\alpha_Bp.
]

Diese beiden Gleichungen werden analytisch gemeinsam gelöst:

[
p=\frac{M\left[\zeta-\alpha_B\varepsilon_{ch}
-\alpha_Bt/H\right]}{1+M\alpha_B^2/H},
\qquad
e=\varepsilon_{ch}+\frac{t+\alpha_Bp}{H}.
]

Damit gilt exakt die Fluidinhaltsidentität
[
\zeta=p/M+\alpha_Be
]
und das mechanische Gleichgewicht (\sigma_{11}=t). Für natürliche Synärese ist der Referenzfall (t=0); ein von null verschiedener Wert dient nur der Verifikation bzw. einer späteren Erweiterung.

## 4. Energie und chemische Rückwirkung

Die gespeicherte lokale Energie pro Referenzvolumen ist

[
\Psi=\frac12\lambda(\operatorname{tr}E)^2
+G E:E
+\frac12M(\zeta-\alpha_Be)^2
+\Psi_{mix},
]
wobei (E=\operatorname{diag}(e-\varepsilon_{ch},
-\varepsilon_{ch},-\varepsilon_{ch})) und (\Psi_{mix}) die P8c-Ideal-Mischungsenergie bezeichnet.

Die mechanische Ableitung nach (b) wird über das Hüllkurvenargument am quasistatischen Gleichgewicht gebildet:
[
\frac{\partial\Psi_{mech}}{\partial b}
=-\beta_B\operatorname{tr}\sigma_{el},
\quad
\operatorname{tr}\sigma_{el}
=(3\lambda+2G)(e-3\varepsilon_{ch}).
]
Mit
[
\frac{\partial b}{\partial s_N}
=-\frac{s_B}{(s_N+s_B+\delta_B)^2},\quad
\frac{\partial b}{\partial s_B}
=\frac{s_N+\delta_B}{(s_N+s_B+\delta_B)^2}
]
ergeben sich die mechanischen Beiträge zu den chemischen Potentialen von N und B. M und O erhalten in dieser lokalen Reduktion keinen direkten Eigenverzerrungsbeitrag. Die Reaktionsaffinitäten müssen in einer nachfolgenden gekoppelten Evolutionsimplementierung aus diesen totalen Potentialen gebildet werden.

**Keine Doppelzählung:** Die Brückeneigenverzerrung ist ein Argument der elastischen Energie. Es wird kein zusätzlicher empirischer „Brückenenergie“-Term addiert. Die externe Traktionsarbeit ist keine gespeicherte freie Energie; bei nichtverschwindender Traktion muss sie in einer globalen Energiebilanz als Randarbeit erscheinen.

## 5. Permeabilitätsrückkopplung — ausdrücklich Hypothese

Implementiert ist eine positive, exponentielle Schließung:
[
K=K_{ref}\exp\left[-\gamma_B(b-b_{ref})
+\gamma_e(e-e_{ref})\right].
]
(\gamma_B\ge0) kodiert die prüfbare Hypothese, dass zunehmender Brückenanteil die intrinsische Permeabilität senkt; (\gamma_e\ge0) kodiert die Hypothese, dass axiale Dehnung sie erhöht. Die Exponentialform garantiert (K>0), beweist aber weder die Vorzeichen noch die Materialgültigkeit. Die Koeffizienten sind unkalibriert. Insbesondere werden (D_f), Kontaktzahl oder BET-Oberfläche nicht ohne zusätzliche Porenhals-/Konnektivitätsdaten als Ersatz für (K) eingesetzt.

## 6. Implementierung und Tests

- `ccfsm_p9_mechanical_feedback.py`: lokale geschlossene Biot-/Eigenverzerrungsmechanik, Energie, mechanische chemische Potentialkorrektur, positive Permeabilität und feldweiser Adapter.
- `test_ccfsm_p9_mechanical_feedback.py`: Referenzzustand, Biot-Identität, Traktionsgleichgewicht, positive Permeabilität, Brücken-Monotonie der gewählten Hypothese, Feldordnung und Eingabevalidierung.

Die Implementierung ist eine lokale konstitutive Auswertung. Sie integriert noch keine Druck-/Flüssigkeitsbilanz, keinen Darcy-Fluss und keine mobile Speziestransportgleichung mit dem aktualisierten (K). Das ist die nächste Integrationsstufe; P8c bleibt bis dahin der eigenständige chemo-hydraulische Operator.

## 7. Was damit bewiesen bzw. nicht bewiesen ist

**Algebraisch exakt:** die geschlossene Lösung der zwei lokalen Biot-/Gleichgewichtsrelationen, (\sigma_{11}=t), die Fluidinhaltsidentität und (K>0) für endliche Parameter.

**Numerisch geprüft:** Regressionstests der obigen Eigenschaften und Eingabegrenzen.

**Nicht bewiesen:** globale Existenz/Regularität des nichtlinearen gekoppelten PDE-Systems, Energiedissipation des vollständigen P9-Systems, Eindeutigkeit bei nichtlinearer räumlicher Mechanik, oder Gültigkeit der gewählten (K(b,e))-Schließung.

**Nicht empirisch validiert:** (\beta_B,\gamma_B,\gamma_e,M,\lambda,G,\alpha_B). Die publizierten natürlichen Schrumpfkurven identifizieren diese Größen nicht getrennt. Erzwungene Druckzell-/Oedometerdaten werden nicht zur Kalibrierung der natürlichen Synärese herangezogen.

## 8. Nächster mathematischer Schritt

P10 sollte den P9-Zustand in einen konservativen räumlichen Operator überführen: aus (\theta,m_i,s_i) zunächst (p,e,b,K) zellweise bestimmen, dann (Q=-K\nabla p) mit konsistenten Randbedingungen berechnen und exakt denselben (Q) in Flüssigkeits- und mobile Si-Bilanzen verwenden. Die diskrete Energie muss dabei Randarbeit, mechanische Gleichgewichtsarbeit und chemische Reaktions-/Diffusionsdissipation gemeinsam bilanzieren.
