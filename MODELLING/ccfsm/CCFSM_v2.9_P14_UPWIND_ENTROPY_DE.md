# CCFSM P14 — Exakte Entropiebilanz des Upwind-Advektionsterms

**Status:** algebraisch hergeleitete und regressionstestete Teilidentität. Kein vollständiger Energie-/Entropiesatz des gekoppelten CCFSM.

## 1. Diskreter Operator

Für eine mobile Spezies sei (m_j=\theta_jc_j). Der Upwind-Stofffluss und die Fluidkapazitätsbilanz verwenden denselben Darcy-Fluss:

\[
F_{j+1/2}=q_{j+1/2}c^{up}_{j+1/2},\quad
\dot m_j=-\frac{F_{j+1/2}-F_{j-1/2}}{\Delta x},\quad
\dot\theta_j=-\frac{q_{j+1/2}-q_{j-1/2}}{\Delta x}.
\]

## 2. Entropie und innere Produktion

Wir betrachten die ideale mobile Mischungsentropie
\[
\eta(\theta,m)=m\left[\ln\left(\frac{m}{\theta c_*}\right)-1\right]
=\theta c[\ln(c/c_*)-1].
\]
Ihre konjugierten Ableitungen lauten
\[
\partial_m\eta=\ln(c/c_*),\qquad \partial_\theta\eta=-c.
\]
Der zweite Term ist entscheidend, damit die variable Fluidkapazität korrekt berücksichtigt wird.

Für eine innere Fläche mit (q_f>0) folgt durch Summation der Nachbarzellen
\[
\mathcal D_f^{up}=q_f[c_R-c_L-c_L\ln(c_R/c_L)]\geq0.
\]
Für (q_f<0):
\[
\mathcal D_f^{up}=|q_f|[c_L-c_R-c_R\ln(c_L/c_R)]\geq0.
\]
Die Nichtnegativität folgt aus (x-1-\ln x\geq0). Dies ist numerische Entropieproduktion des Upwind-Schemas, keine zusätzliche molekulare Diffusionskonstante.

## 3. Randfluss und Teilidentität

Mit (h(c)=c[\ln(c/c_*)-1]) und den tatsächlichen Upwind-Donorwerten gilt
\[
\mathcal P_{\partial\Omega}^{adv}=q_Lh(c_L^{up})-q_Rh(c_R^{up}).
\]
Damit ergibt sich exakt für den semidiskreten Advektions-/Kapazitätsoperator:
\[
\boxed{\dot E_h=\mathcal P_{\partial\Omega}^{adv}
-\sum_{f\in innen}\mathcal D_f^{up}},\qquad \mathcal D_f^{up}\geq0.
\]
Bei Einströmung ist die Reservoirkonzentration der Donor; bei Ausströmung die Gelkonzentration.

## 4. Implementierung und Tests

- `ccfsm_p14_upwind_entropy_audit.py`: berechnet Entropierate aus dem diskreten RHS, Rand-Entropieleistung, innere Upwind-Produktion und Identitätsresiduum.
- `test_ccfsm_p14_upwind_entropy_audit.py`: prüft Identität, beide Flussrichtungen, variable Fluidkapazität, homogene Zustände und Eingabevalidierung.

Die Tests sind Algebra-/Softwareverifikation, keine physikalische Validierung.

## 5. Noch nicht geschlossen

P14 schließt ausschließlich den idealen mobilen Mischungsentropieanteil des Upwind-Advektionsoperators samt variabler Fluidkapazität. Nicht enthalten sind Onsager-Diffusion einschließlich vollständiger chemischer Reservoirleistung, Reaktionsbeiträge, Darcy-/Druckreservoirarbeit, mechanische Lastarbeit und mögliche nichtideale Aktivitäten oder zusätzliche Strukturenergien. P13 plus P14 ist deshalb noch kein globaler Energiebeweis.

## 6. Nächster Schritt P15

P15 sollte Diffusion und Advektion in einer gemeinsamen chemischen Randbilanz zusammenführen: ein konsistenter diskreter Stofffluss, ein Reservoir-Chemiepotentialterm und eine gemeinsame Summationsidentität.
