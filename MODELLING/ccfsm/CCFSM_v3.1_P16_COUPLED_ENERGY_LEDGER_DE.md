# CCFSM P16 — gekoppelte Energiebilanz und mechanischer Variationsaudit

**Status:** semidiskreter Kettenregel-/Bilanz-Audit entlang des P13-Operators. Chemische Reaktionsleistung, hydraulische Reservoirleistung und Darcy-Dissipation werden explizit zerlegt. Zusätzlich wird die Variationskonsistenz der P9-Mechanik geprüft. P16 behauptet ausdrücklich keinen vollständigen thermodynamischen Satz.

## 1. Zusammenführung

P16 kombiniert:
- P15: mobile M/O-Advektion und Onsager-Diffusion mit Reservoir-Chemieleistung;
- P10: lokale detaillierte M/O/N/B-Reaktionen mit den P9-Gesamtpotentialen;
- P9: Fluidenergie-Konjugierte (p-Pi_{osm}), chemische Gesamtpotentiale und die lokale Biot-/Eigenstrain-Schließung;
- P13: gemeinsame semidiskrete Zustandsentwicklung.

Die gespeicherte Energierate wird direkt aus der diskreten Kettenregel berechnet:
\[
\dot E_h=\Delta x\sum_j\left[
(p_j-\Pi_{osm,j})\dot\theta_j+
\sum_{i=M,O,N,B}\mu_{i,j}^{tot}\dot n_{i,j}
\right].
\]

## 2. Reaktionsbeitrag

Für die drei Reaktionsraten (r_1,r_2,r_3) ist
\[
(\dot n_M,\dot n_O,\dot n_N,\dot n_B)
=(-r_1,r_1-r_2,r_2-r_3,r_3).
\]
Mit den in P10 verwendeten Affinitäten (A_k=\mu_k^{tot}-\mu_{k+1}^{tot}) folgt exakt
\[
P_{chem}^{rxn}=\Delta x\sum_j\sum_i\mu_{i,j}^{tot}\dot n_{i,j}
=-\Delta x\sum_j\sum_{k=1}^3r_{k,j}A_{k,j}
=-D_{rxn}\leq0.
\]
Die mechanischen Korrekturen an N/B werden dabei nicht doppelt als separate Energie addiert: Sie stecken in den P9-Gesamtpotentialen.

## 3. Hydraulischer Beitrag

Aus (dot\theta_j=-(q_{j+1/2}-q_{j-1/2})/\Delta x) und (q=-K\nabla_hp) ergibt Summation durch Teile:
\[
\Delta x\sum_jp_j\dot\theta_j
=p_{ext}(q_L-q_R)-D_{Darcy},
\]
mit
\[
D_{Darcy}=\sum_{f=1}^{N-1}\frac{q_f^2}{K_f}\Delta x
+\frac{q_L^2}{K_L}\frac{\Delta x}{2}
+\frac{q_R^2}{K_R}\frac{\Delta x}{2}\geq0.
\]
Die beiden Halbzellen-Dissipationen sind wichtig; nur innere Flächen zu summieren wäre bei offenen Druckreservoiren unvollständig. Die Vorzeichenkonvention ist (q>0) von links nach rechts; positive Reservoirleistung an das Gel ist (p_{ext}(q_L-q_R)).

## 4. Zusammengesetzte Bilanz und Audit

Die vom Code geprüfte Zerlegung lautet
\[
\dot E_h=
\dot F_{mobile}^{transport}
+P_{chem}^{rxn}
+p_{ext}(q_L-q_R)-D_{Darcy}
+R_{ledger}.
\]
(R_{ledger}) ist das numerisch ausgewiesene Kettenregel-/Zerlegungsresiduum. Die mobile Transportrate stammt aus P15, die Reaktionsleistung aus den tatsächlichen P10-Raten und P9-Gesamtpotentialen, und die hydraulische Leistung/Dissipation aus denselben P13-Darcy-Flüssen.

Das ist zunächst eine Identität relativ zu den im bestehenden Code deklarierten Konjugierten. Sie ist kein unabhängiger Beweis, dass die P9-Energie und P9-Spannung aus demselben Variationsprinzip stammen.

## 5. Kritischer mechanischer Variationsaudit

Bei festgehaltenen (	heta,n_i) ist die Ableitung der in P9 gespeicherten elastischen plus Biot-Speicherenergie nach der axialen Dehnung
\[
\frac{\partial(\psi_{el}+\psi_{Biot})}{\partial\varepsilon_{xx}}
=\lambda(\varepsilon_{xx}-3\varepsilon_{ch})
+2G(\varepsilon_{xx}-\varepsilon_{ch})-\alpha p.
\]
P9 setzt die ausgewiesene Gesamtspannung dagegen als
\[
t_{P9}=(\lambda+2G)(\varepsilon_{xx}-\varepsilon_{ch})-\alpha p.
\]
Die Differenz ist
\[
R_{mech}=-2\lambda\varepsilon_{ch}.
\]
Sie verschwindet nur in Sonderfällen (z. B. (lambda=0) oder (arepsilon_{ch}=0)). Der Audit gibt dieses Residuum zellweise aus und setzt `p9_mechanical_variational_closure_verified` nur bei erfüllter Toleranz auf wahr. Das ist ein konkreter Hinweis auf eine noch zu korrigierende bzw. zu begründende mechanische Schließung, nicht etwas, das durch die chemische Energiebilanz verdeckt werden darf.

## 6. Grenzen

- Die mechanische äußere Traktionsarbeit ist nicht in die Energiefunktion integriert; bei nichtverschwindender Traktion wird keine vollständige Bilanz behauptet.
- Der P9-Variationsaudit prüft die lokale Energie-/Spannungskonsistenz, nicht räumliche mechanische Gleichgewichtsarbeit oder Randverschiebungsleistung.
- Keine globale Energie-/Entropieabschätzung für das nichtlineare 3D-PDE-System, kein Existenz-/Eindeutigkeitsbeweis und keine empirische Kalibrierung.
- Aktivitätskoeffizienten sind konstant; Struktur-, Oberflächen-, Kapillar- und nichtideale Energien fehlen.
- Natürliche Synärese bleibt der Zielprozess. Erzwungene Konsolidierungs-/Oedometerdaten werden nicht zur Kalibrierung dieser Bilanz herangezogen.

## 7. Nächster notwendiger Schritt

Vor einem globalen Energiesatz muss P9 mechanisch variational konsistent gemacht werden: gespeicherte elastische Energie, Biot-Energie, Eigenstrain und Spannungsdefinition müssen aus derselben 3D-/1D-Reduktion folgen. Danach sind Traktions-/Verschiebungsrandarbeit und räumliche mechanische Kopplung erneut herzuleiten.
