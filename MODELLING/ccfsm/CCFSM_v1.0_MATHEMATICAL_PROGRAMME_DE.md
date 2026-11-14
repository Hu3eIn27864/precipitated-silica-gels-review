# CCFSM v1.0 – thermodynamische Herleitung und mathematisches Forschungsprogramm

**Status:** Forschungsprogramm und partielle Strukturresultate; keine vorweggenommenen Existenz-/Regularitätsbeweise für das volle Modell.

## 1. Ziel

Das vollständige CCFSM koppelt quasistatische Mechanik, Druck-/Flüssigkeitstransport, konvektive Reaktionsgleichungen und zustandsabhängige Materialkoeffizienten. Es ist nicht identisch mit Navier–Stokes. Der Vergleich bezeichnet den Anspruch an die 3D-Nichtlinearität und mathematische Tiefe.

## 2. P0-Referenzsystem: lineare gesättigte Poroelastizität

Auf beschränktem Lipschitz-Gebiet \(\Omega\subset\mathbb R^3\), konstante Koeffizienten, isotherm, keine Reaktion:
\[
-\nabla\cdot(2G\varepsilon(\mathbf u)+\lambda(\nabla\cdot\mathbf u)\mathbf I-\alpha p\mathbf I)=\mathbf f,
\]
\[
S_0\partial_t p+\alpha\partial_t(\nabla\cdot\mathbf u)
-\nabla\cdot\left(\frac{\mathbf K}{\mu}\nabla p\right)=g.
\]
\(G>0\), \(3\lambda+2G>0\), \(S_0>0\), \(\mathbf K\) symmetrisch und gleichmäßig positiv definit. Mechanische Dirichlet-Daten schließen starre Bewegungen aus; für Druck sind ein nichtleerer Dirichlet-Rand oder geeignete Mittelwert-/Kompatibilitätsbedingungen nötig.

Für jedes \(p(t)\) ist die Mechanik ein koerzives elliptisches Problem (Korn-Ungleichung nach Fixierung starrer Modi). Elimination der Mechanik führt unter üblichen Biot-Bedingungen zu einer parabolischen Druckstruktur. Dies ist der geeignete Startpunkt für Standardtheorie schwacher Lösungen, aber hier noch kein vollständig ausgeführter Beweis mit allen Funktionsraumdetails.

## 3. Schwache Formulierung

Finde \(\mathbf u(t)\in V\subset H^1(\Omega)^3\), \(p(t)\in H^1(\Omega)\):
\[
\int_\Omega \mathbb C\varepsilon(\mathbf u):\varepsilon(\mathbf w)\,dx
-\alpha\int_\Omega p\,\nabla\cdot\mathbf w\,dx
=\langle\mathbf f,\mathbf w\rangle
\quad\forall\mathbf w\in V,
\]
\[
\int_\Omega S_0\partial_t p\,r\,dx
+\alpha\int_\Omega\partial_t(\nabla\cdot\mathbf u)r\,dx
+\int_\Omega\frac{\mathbf K}{\mu}\nabla p\cdot\nabla r\,dx
=\langle g,r\rangle+\text{Randfluss}.
\]
Die Randterme folgen aus der Drainagebedingung. Für Energieabschätzungen testet man die Mechanik mit \(\partial_t\mathbf u\), die Fluidgleichung mit \(p\) und addiert. Bei konsistenter symmetrischer Biot-Kopplung entsteht eine Energieabschätzung mit dissipativem Term
\[
\int_\Omega\frac{\mathbf K}{\mu}\nabla p\cdot\nabla p\,dx\ge0.
\]
Die exakte Speicherenergie hängt von der Biot-Konvention und Randbedingungen ab und muss vor einem formalen Theorem vollständig ausgeschrieben werden.

## 4. Thermodynamische Konstruktion

Ein möglicher Ansatz:
\[
\mathcal F=\int_\Omega[
\psi_{\rm el}(\varepsilon-\varepsilon_{\rm sh},B,D_f,z,\phi)
+\psi_{\rm mix}(\mathbf c,\phi,T)
+\psi_{\rm net}(B,D_f,z,\xi_u,\xi_r)
+\tfrac12\nabla D_f\cdot\mathsf A_f\nabla D_f
+\tfrac12\nabla z\cdot\mathsf A_z\nabla z]\,dx.
\]
Gradiententerme sind optional und benötigen physikalische Begründung. Thermodynamische Kräfte folgen aus Variationsableitungen: Spannung aus \(\partial_\varepsilon\psi\), chemische Potentiale aus \(\partial_{c_i}\psi\), interne Affinitäten aus \(-\partial_a\psi\) (Vorzeichenkonvention explizit festlegen).

Eine zulässige Onsager-Struktur verwendet symmetrisch positiv semidefinite Mobilitäten, z. B. Darcyfluss proportional zum Gradienten des Fluidpotentials, Speziesflüsse proportional zu chemischen Potentialgradienten und interne Kinetiken proportional zu ihren Affinitäten. Reaktionsraten müssen die Affinitäten dissipativ abbauen. Ziel:
\[
\dot{\mathcal F}+\mathcal D\le\mathcal P_{\rm ext},\qquad \mathcal D\ge0.
\]
Die konkrete freie Energie und Onsager-Matrizen müssen noch konstruiert werden. Dies ist eine Designvorgabe, keine behauptete Ableitung.

## 5. Invarianz- und Positivitätsziele

Zu zeigen oder als Annahme zu kennzeichnen sind \(0<\phi<1\), \(B\ge0\) (ggf. \(B\le B_\infty\)), \(c_i\ge0\), positive Definitheit von \(\mathbf K\), \(\mathcal D\ge0\), elementare Stoffbilanzen und positive mechanische Tangentensteifigkeit. Quasi-positive Reaktionskinetik und geeignete Diffusionsrandbedingungen können Konzentrationspositivität erhalten. Porositätsschranken müssen aus Volumenbilanz und Materialgesetz folgen, nicht durch numerisches Clipping.

## 6. Existenz-/Eindeutigkeits-Roadmap

| Stufe | System | Ziel | Hindernisse |
|---|---|---|---|
| P0 | lineare Biot-Darcy-Poroelastizität | schwache Existenz, Eindeutigkeit, Energie | Korn, Koerzivität, Speicherterm |
| P1 | P0 + beschränkte B-Kinetik | Existenz und B-Schranken | Koeffizientenabhängigkeit |
| P2 | konservativer Reaktions-Diffusionsblock | Positivität, Stoffbilanz, schwache Existenz | Quasi-Positivität, Reaktionswachstum |
| P3 | variable K, C und Morphologie | bedingte Existenz; ggf. Eindeutigkeit | Degeneration, Nichtlinearität |
| P4 | Viskoelastizität und Eigenstrain | Energieungleichung, schwache Lösungen | Gedächtnis, nichtkonvexe Energie |
| P5 | bewegte freie Oberfläche, volle 3D-Kopplung | lokale/globale Theorie je nach Annahmen | freie Randfläche, Kapillarität, Regularität |

Ein Resultat für P1–P5 darf erst nach Angabe exakter Koeffizientenannahmen, Funktionsräume und Randbedingungen behauptet werden. Globale klassische Regularität des vollen nichtlinearen 3D-Systems bleibt Forschungsziel und folgt nicht aus der P0-Energieabschätzung.

## 7. Numerische Verifikation

Eine spätere FEM- oder konservative FVM-Implementierung muss getrennte Fluid-/Feststoffmassenbilanzen und Elementbilanzen schließen, Konzentrations-/Porositätspositivität ohne willkürliches Clipping kontrollieren, bei geschlossenen isothermen Rändern diskrete Energie kontrollieren, Darcy-Flüsse konservativ über Zellflächen behandeln, Netz-/Zeitschrittverfeinerung dokumentieren und P0/1D/ODE-Grenzfälle reproduzieren. Softwaretests sind keine physikalische Validierung.

## 8. Analytische Grenzfälle

Homogenes Material mit \(\nabla p=0\); impermeable Oberfläche mit erhaltener Gesamtfluidmasse; Drainageleitfähigkeit gegen unendlich; \(\mathbf K\to0\); \(\mathbb V\to0\); \(k_b\to0\); \(k_r\to0\); räumlich homogene Felder als ODE-Grenzfall.

## 9. Was für ein formales Theorem fehlt

Exakte Energie und Koerzivität; Parameterbereiche und Koeffizientenregularität; Randzerlegung; Funktionsräume; approximierendes Galerkin-/Zeitdiskretisierungsschema; uniforme a-priori-Abschätzungen; Kompaktheit und Passage zum nichtlinearen Grenzwert; Eindeutigkeitsargument (monotone Operatoren oder Gronwall unter Lipschitz-Annahmen).

**Ergebnis:** v1.0 definiert einen Beweisfahrplan. Es wäre unzulässig, dies bereits als Beweis des vollständigen CCFSM oder als Lösung des 3D-Navier–Stokes-Problems zu bezeichnen.
