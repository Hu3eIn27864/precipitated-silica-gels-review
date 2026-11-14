# CCFSM P20 — gestaffelte Kopplung von Chemie/Transport und räumlicher Mechanik

**Status:** implementierter Zustands-Snapshot-Adapter zwischen P9/P13 (lokale konstitutive Felder und 1D-Finite-Volumen-Transport) und P19 (räumliches quasistatisches FE-Gleichgewicht). P20 ist ausdrücklich noch kein monolithisch oder vollständig bidirektional gekoppelter 3D-Zeitintegrator.

## 1. Kopplungskette

Aus dem aktuellen FV-Zustand theta_j,(m_M,m_O,s_N,s_B)_j berechnet P9 lokal die Brückenfraktion
\[
b_j=\frac{s_{B,j}}{s_{N,j}+s_{B,j}+\delta_B}
\]
und die chemische Eigenstrain
\[
c_j=\beta_B(b_j-b_0).
\]
Der Fluidinhaltszuwachs ist gemäß P9
\[
\zeta_j=\theta_j-\theta_{ref}.
\]
Diese beiden Zellfelder werden über cell_index auf die vom Aufrufer gelieferten P19-FE-Quadraturpunkte übertragen. P19 löst dann
\[
p=M(\zeta-\alpha\operatorname{tr}\varepsilon(u)),\quad
\sigma=\lambda\operatorname{tr}(\varepsilon-cI)I+
2G(\varepsilon-cI)-\alpha pI,
\quad \nabla\cdot\sigma=0.
\]

Parallel wird P13 auf demselben Zustand ausgewertet und liefert den vorhandenen 1D-FV-Transport-RHS einschließlich P9-lokaler Darcy-Flüsse, Onsager-Diffusion und Reaktionen.

## 2. Bewusst getrennte Druckfelder

P20 gibt sowohl den P9-lokalen Druck als auch den P19-räumlichen FE-Druck an den zugeordneten Quadraturpunkten aus:
\[
\Delta p_q=p_{P19,q}-p_{P9,j(q)}.
\]
Diese Differenz ist ein Modellvergleich, kein Fehlerresiduum: P9 verwendet eine lokale axiale Plane-Strain-Schließung mit vorgegebener axialer Traktion; P19 löst eine räumliche Randwertaufgabe mit den übergebenen FE-Randbedingungen. Beide Druckfelder müssen nicht identisch sein.

P13-Darcy- und Stoffflüsse verwenden in P20 weiterhin die P9-lokalen Felder. Der P19-Druck wird noch nicht in die Flussberechnung zurückgeführt. Das verhindert eine unzulässige Behauptung vollständiger Zweiwegkopplung.

## 3. Diskrete Schnittstelle

Das Modul ccfsm_p20_staggered_coupling.py erwartet pro FE-Quadraturpunkt:
- cell_index: zugehörige FV-Zelle,
- B: technische 3D-Dehnungs-Verschiebungs-Matrix (6 x ndof),
- weight: positives Volumengewicht.

Eigenstrain und Fluidinhalt werden aus dem verknüpften FV-Zustand und den P9-Parametern abgeleitet. FE-Randquadratur und Dirichlet-DOFs werden an P19 durchgereicht. Das Ergebnis enthält den P13-Transport-RHS, die P19-Verschiebung/Spannung/Druckfelder und den Druckvergleich.

## 4. Verifikation

Regressionstests prüfen:
- korrekte Übertragung von Brückenfraktion zu Eigenstrain und theta-theta_ref zu Fluidinhalt,
- erfolgreiche P19-Gleichgewichtslösung,
- Ausgabe beider Druckfelder ohne Gleichheitsannahme,
- Ablehnung ungültiger Zellindizes und inkonsistenter FE-Freiheitsgrade.

Diese Tests verifizieren die Software-Schnittstelle und algebraische Abbildung, nicht die physikalische Richtigkeit der Kopplung oder eine empirische Kalibrierung.

## 5. Was für echte Zweiwegkopplung noch fehlt

1. P19-Druck bzw. die mechanisch konsistente Fluidkomponente muss auf FV-Zellen projiziert werden.
2. Darcy-Flüsse müssen mit diesem räumlichen Druckfeld und einer konsistenten Permeabilität neu berechnet werden.
3. Die gleichen Flüsse müssen Fluidkontinuität und mobile M/O-Advektion konservativ antreiben.
4. Mechanische Beiträge zu chemischen Potentialen müssen aus derselben räumlichen Energie abgeleitet werden.
5. Ein gemeinsamer Zeitschritt mit Positivität, Energiebilanz und mechanischer Randarbeit ist zu verifizieren.

Bis dahin bleiben natürliche Synärese und erzwungene Druckkonsolidierung getrennte Daten- und Modellzweige. Es werden keine unkalibrierten Struktur-Permeabilitätsgesetze als validierte Silica-Eigenschaften ausgegeben.
