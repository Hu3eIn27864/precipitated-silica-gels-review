# CCFSM P15 — Gemeinsame Randbilanz für mobile Advektion und Onsager-Diffusion

**Status:** algebraisch hergeleitete und implementierte semidiskrete Teilidentität; Regressionstests prüfen die diskrete Bilanz. Kein vollständiger Energie-/Entropiesatz des gekoppelten CCFSM und keine empirische Validierung.

## 1. Ziel und Geltungsbereich

P13 formuliert mobile Diffusion als Onsager-Fluss entlang des chemischen Potentialgradienten. P14 weist für Upwind-Advektion zusammen mit der variablen Fluidkapazität eine exakte Entropieidentität nach. P15 verbindet beide Beiträge für die mobilen Spezies M und O, verwendet dabei unverändert die P13-Gesamtflächenflüsse und denselben Darcy-Fluss für Fluidkapazität und Advektion.

Für eine Spezies gelten (m_j=\theta_jc_j), (q>0) von links nach rechts und
\[
F_{j+1/2}=q_{j+1/2}c^{up}_{j+1/2}+J^{diff}_{j+1/2},\quad
\dot m_j=-\frac{F_{j+1/2}-F_{j-1/2}}{\Delta x},\quad
\dot\theta_j=-\frac{q_{j+1/2}-q_{j-1/2}}{\Delta x}.
\]

Die mobile freie Energiedichte pro Referenzvolumen lautet für konstante Aktivitätskoeffizienten
\[
f_i(\theta,m)=m\left[\mu_i^0+RT\left(\ln\frac{\gamma_i c}{c_*}-1\right)\right],
\quad c=m/\theta,
\]
mit (\partial_m f_i=\mu_i=\mu_i^0+RT\ln(\gamma_i c/c_*)) und
(\partial_\theta f_i=-RTc). Die Standardpotentiale und konstanten Aktivitätskoeffizienten werden damit konsistent in Advektion, Diffusion und Reservoirtermen geführt.

## 2. Diskrete Bilanz

Die innere Upwind-Produktion ist die P14-Produktion multipliziert mit (RT):
\[
D^{up}_f=RT|q_f|\,\Phi(c_L,c_R)\geq0,
\]
wobei für (q_f>0), (\Phi=c_R-c_L-c_L\ln(c_R/c_L)), und für (q_f<0),
(\Phi=c_L-c_R-c_R\ln(c_L/c_R)).

Für jede innere Diffusionsfläche ist
\[
J_f^{diff}=-L_f\frac{\mu_R-\mu_L}{\Delta x},\qquad
L_f=\frac{\theta_fD_i\Lambda(c_L,c_R)}{RT},
\]
und daher (D_f^{diff}=L_f(\nabla_h\mu)^2\Delta x\geq0). An den beiden Reservoir-Halbzellen wird dieselbe Onsager-Konstruktion verwendet; deren nichtnegative Beiträge werden als (D_{L/R}^{res}) separat ausgewiesen.

Die advektive Randpotentialleistung verwendet die tatsächlichen Upwind-Donoren:
\[
P_{\partial\Omega}^{adv}=q_Lg_i(c_L^{up})-q_Rg_i(c_R^{up}),\quad
g_i(c)=c\left[\mu_i^0+RT\left(\ln\frac{\gamma_i c}{c_*}-1\right)\right].
\]
Die diffusive Reservoir-Chemieleistung ist
\[
P_{res}^{diff}=\mu_{i,L}^{res}J_{L}^{diff}
-\mu_{i,R}^{res}J_{R}^{diff}.
\]

Damit folgt die gemeinsame semidiskrete Identität
\[
\boxed{
\dot F_i=P_{\partial\Omega}^{adv}+P_{res}^{diff}
-D^{up}-D_{int}^{diff}-D_{res}^{diff}.
}
\]
Alle drei Dissipationsbeiträge sind nichtnegativ. Der Rand-Diffusionsanteil entsteht aus der Differenz zwischen Zell- und Reservoirpotential an der jeweiligen Halbzelle. Die Vorzeichen gelten für die Konvention positiver Flüsse nach rechts.

## 3. Implementierung

- `ccfsm_p15_mobile_boundary_balance.py` ruft den P13-Operator auf und auditiert dessen tatsächliche Advektions- und Diffusionsflächenflüsse.
- Pro mobiler Spezies werden freie Energierate, advektive Randpotentialleistung, diffusive Reservoir-Chemieleistung, Upwind-Produktion, innere Onsager-Dissipation, Halbzellen-Dissipation und Bilanzresiduum separat ausgegeben.
- Der Audit berechnet die Transport-RHS direkt aus den gemeinsamen Flüssen; lokale Reaktionsraten werden bewusst nicht in diese Teilbilanz eingemischt.

## 4. Verifikation

`test_ccfsm_p15_mobile_boundary_balance.py` prüft die gemeinsame Identität, den Grenzfall ohne Diffusion, den reinen Diffusionsfall, unterschiedliche Reservoirzustände sowie ungültige Randkonzentrationen. Der Testlauf ist Software-/Algebraieverifikation, keine physikalische Validierung oder Parameterkalibrierung.

## 5. Grenzen und nächste offene Kopplungen

P15 umfasst nur die mobile ideale Mischungsenergie von M/O bei konstanten (\gamma_i), P13-Onsager-Diffusion und P14-Upwind-Advektion. Nicht enthalten sind:

- Reaktionsenergie und die chemische Kopplung an immobilisierte N/B-Pools,
- hydraulische Reservoir-/Druckarbeit und Darcy-Dissipation,
- mechanische Arbeit, Traktion und räumliche Mechanik,
- nichtideale, konzentrations- oder temperaturabhängige Aktivitätskoeffizienten,
- Struktur-, Oberflächen-, Kapillar- oder Grenzflächenenergien,
- ein globaler Existenz-/Energiebeweis für das nichtlineare gekoppelte PDE-System.

Die Identität ist eine semidiskrete Transport-Teilbilanz. Sie beweist weder die physikalische Richtigkeit der konstitutiven Gesetze noch die Kalibrierung an natürliche Synärese. Erzwungene Konsolidierungs- und Oedometerdaten bleiben von der natürlichen Synärese getrennt.
