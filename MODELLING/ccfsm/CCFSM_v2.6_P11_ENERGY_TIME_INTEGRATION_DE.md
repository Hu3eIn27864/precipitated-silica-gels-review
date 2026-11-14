# CCFSM P11 — energieüberwachte Zeitintegration mit Positivitätskontrolle

**Version:** CCFSM v2.6  
**Datum:** 14. November 2026  
**Ausgangspunkt:** P10 räumliche 1D-Finite-Volumen-Kopplung

## 1. Ziel und Abgrenzung

P10 liefert ein semidiskretes ODE-System für die Fluidkapazität \(\theta_j\) und die vier Silicium-Inventare \((m_M,m_O,s_N,s_B)_j\). P11 ergänzt einen Zeitschritt, der (i) die Positivität der Zustände erhält, (ii) \(0<\theta\leq1\) erzwingt und (iii) jeden Schritt anhand der P9-Zellenergien überprüft.

Verwendet wird adaptive explizite Euler-Integration mit einer analytischen Positivitäts-Schranke und anschließender Energierückwärtssuche (Backtracking). Ein Schritt wird nur akzeptiert, wenn die diskrete Gesamtenergie innerhalb einer angegebenen Rundungstoleranz nicht steigt.

Das ist bewusst ein **akzeptanzkontrollierter Algorithmus**, kein unbedingtes Energie-stabiles Integrationsverfahren.

## 2. Semidiskretes System

Mit P10 gilt

\[
\dot\theta_j=-\frac{Q_{j+1/2}-Q_{j-1/2}}{\Delta x},\qquad
\dot{\mathbf u}_j=-\frac{\mathbf J_{j+1/2}-\mathbf J_{j-1/2}}{\Delta x}
+\mathbf R_j,
\]

wobei \(\mathbf u=(m_M,m_O,s_N,s_B)^T\). Der Darcy-Fluss \(Q\) ist derselbe in Fluid- und mobilem Stofftransport. Die lokalen Reaktionen erhalten die Summe der vier Pools exakt.

## 3. Diskrete Energie

Die implementierte diskrete gespeicherte Energie ist

\[
\mathcal E_h(\theta,\mathbf u)
=\Delta x\sum_{j=1}^{N}
\Psi_{P9}(\theta_j,\mathbf u_j),
\]

wobei \(\Psi_{P9}\) die in P9 implementierte Summe aus elastischer Energie, Biot-Speicherenergie und idealer Mischungsenergie bezeichnet. Die mechanischen Korrekturen der N/B-Potentiale stammen aus derselben lokalen P9-Schließung.

Für einen Vorschlag \(z^{n+1}=z^n+\Delta t\,F_{P10}(z^n)\) wird die Schrittweite zunächst so begrenzt, dass jede Komponente positiv bleibt und \(\theta\leq1\). Danach wird \(\Delta t\) nötigenfalls halbiert, bis

\[
\mathcal E_h(z^{n+1})\leq
\mathcal E_h(z^n)+\varepsilon_E\max(1,|\mathcal E_h(z^n)|)
\]

erfüllt ist. Die Toleranz \(\varepsilon_E\) ist eine numerische Rundungstoleranz, keine physikalische Energiequelle.

## 4. Randbedingungen und Geltungsbereich

Die Energiekontrolle wird in P11 nur für geschlossene Randbedingungen freigegeben: beide hydraulischen Randflüsse und beide mobilen Silicium-Randflüsse müssen numerisch null sein. Bei Reservoir-Ein-/Ausströmung ist die gespeicherte Energie des Gels allein nicht die vollständige Bilanz; Reservoir-Chemiepotentiale, hydraulische Leistung und gegebenenfalls mechanische Randarbeit müssen ergänzt werden. Solche offenen Schritte werden daher zurückgewiesen und nicht fälschlich als dissipativ klassifiziert.

Die Zeitintegration ist erster Ordnung und explizit. Die Positivitäts-Schranke verhindert, dass ein akzeptierter Euler-Schritt die Inventare oder Fluidkapazität aus dem zulässigen Bereich bewegt. Die Energierückwärtssuche stellt zusätzlich die diskrete Nichtzunahme für jeden tatsächlich akzeptierten Schritt sicher, sofern ein solcher Schritt innerhalb der Backtracking-Grenze gefunden wird.

## 5. Was damit gezeigt ist — und was nicht

**Algorithmisch abgesichert und getestet:**
- strikte Positivität der vier Inventare und \(0<\theta\leq1\) nach jedem akzeptierten Schritt;
- Nichtzunahme der implementierten P9-Gesamtenergie bis zur expliziten Toleranz;
- Erhaltung des globalen Silicium-Inventars und der Gesamtfluidkapazität bei geschlossenen Rändern bis auf Gleitkomma-Rundung;
- Zurückweisung offener Randflüsse, solange Reservoir-Energie-/Arbeitsbeiträge nicht Bestandteil der Energiefunktion sind.

**Nicht bewiesen:**
- dass für jeden Zustand und jede gewünschte Schrittweite ein Schritt innerhalb endlich vieler Backtracking-Schritte gefunden wird;
- uniforme Zeitschrittweiten, Konvergenzordnung im gekoppelten Grenzfall oder Langzeitfehlerabschätzungen;
- unbedingte Energie-Stabilität ohne Akzeptanzprüfung;
- vollständige thermodynamische Bilanz bei nichtverschwindender äußerer Traktion oder offenen Reservoiren;
- Existenz/Regularität der kontinuierlichen nichtlinearen 1D- oder 3D-PDE;
- empirische Richtigkeit bzw. Kalibrierung der P9-Permeabilitäts- und Eigenverzerrungsgesetze.

Insbesondere ist P11 kein mathematischer Existenzbeweis für die vollständige CCFSM. Die Positivitäts- und Energieeigenschaften beziehen sich auf die hier definierte diskrete Schrittregel und den geschlossenen Randfall.

## 6. Reproduktion

Im Verzeichnis `MODELLING/ccfsm`:

```bash
python -m unittest test_ccfsm_p11_energy_time_integration -v
python -m unittest discover -s . -p "test_*.py" -v
```

Die Tests prüfen Reaktions-Energieabnahme, geschlossene globale Bilanzen, Positivität, stationären Nullreaktionsfall, Zurückweisung offener Grenzen und ungültiger Eingaben. Softwaretests sind keine physikalische Validierung.
