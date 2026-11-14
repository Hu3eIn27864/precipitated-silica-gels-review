# CCFSM v1.0 – dreidimensionales Mehrfeldmodell der natürlichen Synärese

**Version:** 1.0.0 (Formulierungsentwurf)  
**Geltungsbereich:** gesättigte, natürliche und mechanisch unbelastete Synärese gefällter Silica-Gele; keine Trocknung, keine Oedometer- oder Druckzellkalibrierung.  
**Status:** mathematisch strukturierte Modellhypothese. Noch keine vollständige thermodynamische Herleitung, keine Identifikation aller Schließungsgesetze und kein Existenz-/Regularitätsbeweis für das volle System.

## 1. Ziel und Modellgrenze

CCFSM v1.0 beschreibt räumlich veränderliche Felder für Feststoffbewegung, Porenfluid, Netzwerkzustand, Morphologie und gelöste Spezies. Die Feldgleichungen sind gekoppelt. Die Geometrie darf dreidimensional und zeitabhängig sein. „Mechanisch unbelastet“ bedeutet verschwindende äußere mechanische Traktion auf der freien Geloberfläche, nicht verschwindenden Porendruck, nicht verschwindende Kapillarkräfte und nicht automatisch undurchlässige Ränder.

Die erste mathematische Referenzfassung nimmt ein zunächst vollständig gesättigtes Gel und kleine bis mäßige Deformationen auf einer festen Referenzdomäne an. Eine bewegte freie Oberfläche wird in einer späteren ALE-/Moving-boundary-Erweiterung behandelt. Die Randbedingungen zur Flüssigkeitsabgabe bleiben jedoch bereits in der Referenzfassung explizit.

## 2. Unbekannte und Zustandsfelder

Auf einem Gebiet \(\Omega\subset\mathbb R^3\), \(t\in(0,T)\):

| Feld | Bedeutung | Einheit / Schranke |
|---|---|---|
| \(\mathbf u(\mathbf x,t)\) | Feststoff-/Skelettverschiebung | m |
| \(\mathbf v_s=\partial_t\mathbf u\) | Skelettgeschwindigkeit | m s\(^{-1}\) |
| \(p(\mathbf x,t)\) | Porenfluiddruck relativ zum gewählten Referenzdruck | Pa |
| \(\mathbf q\) | Darcy-Volumenfluss relativ zum Skelett | m s\(^{-1}\) |
| \(\phi\) | Porosität | \(0<\phi<1\) |
| \(B\) | effektive tragende Siloxanbrückendichte | mol m\(^{-3}\); Bezugsvolumen festzulegen |
| \(D_f\) | effektive Fraktaldimension | dimensionslos; zulässiger Bereich quellenabhängig |
| \(z\) | mittlere Kontaktzahl | dimensionslos, \(z\ge0\) |
| \(\xi_u,\xi_r\) | nicht relaxiertes / relaxiertes Kontraktionsinventar | dimensionslos |
| \(c_i\) | Konzentration gelöster Spezies \(i\) in der Flüssigkeit | mol m\(^{-3}\) Flüssigkeit |
| \(T\) | lokale Geltemperatur | K |

\(\xi\) ist ausdrücklich keine mechanische Spannung. Mechanische Spannung wird ausschließlich mit \(\boldsymbol\sigma\) bezeichnet.

## 3. Kinematik und Phasenbilanz

Kleine Deformationen als erste Referenz:
\[
\boldsymbol\varepsilon(\mathbf u)=\tfrac12(\nabla\mathbf u+\nabla\mathbf u^\mathsf T),
\qquad J_s\simeq1+\nabla\cdot\mathbf u.
\]
Für größere Schrumpfung ist diese Linearisierung durch finite Kinematik (\(\mathbf F\), \(J=\det\mathbf F\)) zu ersetzen; beide Varianten dürfen nicht vermischt werden.

Für inkompressible Feststoff- und Flüssigphasen ohne Feststoffverlust gilt in der aktuellen Konfiguration:
\[
\partial_t(1-\phi)+\nabla\cdot[(1-\phi)\mathbf v_s]=0,
\]
\[
\partial_t(\phi\rho_f)+
\nabla\cdot[\phi\rho_f\mathbf v_s+\rho_f\mathbf q]=0.
\]
Bei konstanter Flüssigkeitsdichte folgt:
\[
\partial_t\phi+\nabla\cdot(\phi\mathbf v_s+\mathbf q)=0.
\]
Die Kurzform ohne Skelettadvektion ist nur zulässig, wenn diese bereits in der Koordinatenabbildung/Zeitableitung enthalten ist. Sie wird in v1.0 nicht stillschweigend verwendet.

## 4. Flüssigkeitstransport

Relativer Darcy-Fluss:
\[
\mathbf q=-\frac{\mathbf K(\phi,\mathcal M)}{\mu(\mathbf c,T)}
[\nabla p-\rho_f\mathbf g].
\]
\(\mathbf K\) ist ein symmetrischer, positiv definiter Permeabilitätstensor; im isotropen Grenzfall \(\mathbf K=\kappa\mathbf I\). \(\mathcal M\) bezeichnet messbar zu definierende Poren-/Netzwerkmorphologie.

Die Abhängigkeit \(\mathbf K(\phi,\mathcal M)\) ist eine Schließungsfunktion, kein bewiesenes Silica-Gesetz. \(D_f\) und \(z\) allein bestimmen Porenhalsradien, Konnektivität und Tortuosität nicht. Bis geeignete Daten vorliegen, bleibt \(\mathbf K\) ein unabhängiges Feld bzw. eine unabhängig gemessene Eingabe.

## 5. Mechanisches Gleichgewicht

Quasistatisches Gleichgewicht:
\[
\nabla\cdot\boldsymbol\sigma_{\rm tot}+\rho_{\rm bulk}\mathbf g=0,
\qquad
\boldsymbol\sigma_{\rm tot}=\boldsymbol\sigma_{\rm eff}-\alpha_Bp\mathbf I.
\]
\(\alpha_B\) ist ein Biot-artiger Kopplungskoeffizient und nicht ungeprüft gleich eins zu setzen.

Eine erste visko-poroelastische Schließung:
\[
\boldsymbol\sigma_{\rm eff}
=\mathbb C(B,D_f,z,\phi,T):
[\boldsymbol\varepsilon(\mathbf u)-\boldsymbol\varepsilon_{\rm sh}]
+\mathbb V:\partial_t[\boldsymbol\varepsilon(\mathbf u)-\boldsymbol\varepsilon_{\rm sh}].
\]
\(\mathbb C\) muss koerziv/positiv sein; \(\mathbb V\) dissipativ/positiv semidefinit. Beide Tensoren dürfen anisotrop und ortsabhängig sein. Die rein elastische Fassung setzt \(\mathbb V=0\).

Eine erste isotrope Eigenstrain:
\[
\boldsymbol\varepsilon_{\rm sh}(\xi_u,\xi_r)
=\epsilon_{\rm sh}(\xi_u,\xi_r)\mathbf I.
\]
Die Funktion \(\epsilon_{\rm sh}\) ist separat zu identifizieren. Für endliche Deformationen ist eine multiplikative oder logarithmische Eigenstrain-Kinematik erforderlich.

## 6. Netzwerkbildung und Morphologie

Mit \(D_t=\partial_t+\mathbf v_s\cdot\nabla\):
\[
D_tB=k_b(\mathbf c,T,\mathcal I)(B_\infty-B)-k_{-b}B.
\]
\(k_{-b}=0\) darf nur bei begründeter Irreversibilität gesetzt werden. Anfangs-/Randdaten und Kinetik müssen \(0\le B\le B_\infty\) erhalten.

Morphologische Nachführung:
\[
D_tD_f=k_m(D_{f,\rm eq}(B,\mathbf c,T)-D_f)+\nabla\cdot(\mathsf D_f\nabla D_f),
\]
\[
D_tz=k_z(z_{\rm eq}(B,D_f,\mathbf c,T)-z)+\nabla\cdot(\mathsf D_z\nabla z).
\]
Gradiententerme sind optionale Reorganisationsflüsse und ohne mikroskopische Begründung null zu setzen. Gleichgewichtsfunktionen sind konstitutive Hypothesen mit festzulegenden Wertebereichen.

## 7. Innere Kontraktion und Relaxation

Eine bilanzierbare lokale Dynamik:
\[
D_t\xi_u=\Omega_bD_tB-k_r\xi_u,\qquad
D_t\xi_r=k_r\xi_u,
\]
\[
D_t(\xi_u+\xi_r)=\Omega_bD_tB.
\]
Die Eigenstrain darf nur an eine explizit begründete Kombination aus \(\xi_u,\xi_r\) gekoppelt werden. Ob relaxierte Kontraktion geometrisch vollständig wirksam bleibt, ist eine Materialfrage und kein algebraischer Automatismus.

## 8. Chemischer Speziestransport

Für Spezies \(i\), Diffusions-/Dispersionstensor \(\mathsf D_i\):
\[
\partial_t(\phi c_i)+
\nabla\cdot(c_i\mathbf q+\phi c_i\mathbf v_s)
=\nabla\cdot(\phi\mathsf D_i\nabla c_i)+R_i(\mathbf c,B,D_f,z,T).
\]
Mit stöchiometrischer Matrix \(\boldsymbol\nu\) und Reaktionsraten \(\mathbf r\):
\[
\mathbf R=\boldsymbol\nu\mathbf r,\qquad
\mathbf a^\mathsf T\boldsymbol\nu=0
\]
für jedes konservierte Element/jede Komponente. Silicium-, Natrium-, Schwefel- und Ladungsbilanz sind getrennt zu prüfen. Säure-/Base-Speziation ist algebraisch oder kinetisch zu schließen, nicht unvereinbar doppelt. Elektroneutralität bzw. ein vollständiges Elektrotransportmodell ist erforderlich. Die v0.4a-Speziation ist noch kein räumlicher Reaktions-Diffusionssolver.

## 9. Thermodynamische Struktur – Zielbedingung

Eine freie Energiedichte ist als Funktion unabhängiger Zustände zu definieren:
\[
\psi=\psi(\boldsymbol\varepsilon-\boldsymbol\varepsilon_{\rm sh},
\phi,B,D_f,z,\xi_u,\xi_r,\mathbf c,T,\nabla D_f,\nabla z).
\]
Eine konsistente Herleitung verlangt mechanische Spannung aus der Energiederivative nach Dehnung, chemische Potentiale \(\mu_i=\partial\psi/\partial c_i\), Reaktionsaffinitäten aus chemischen Potentialen und Flüsse/Kinetiken mit positiv semidefiniter Mobilität.

Ziel ist:
\[
\frac{d}{dt}\mathcal F(t)+\mathcal D(t)
\le \mathcal P_{\rm boundary}(t)+\mathcal P_{\rm gravity}(t),
\qquad \mathcal D(t)\ge0.
\]
Für geschlossene, isotherme und schwerkraftfreie Randbedingungen reduziert sich dies auf \(d\mathcal F/dt\le0\). Die konkrete \(\psi\), Mobilitätsoperatoren und Reaktionsgesetze sind noch nicht vollständig konstruiert. Die Ungleichung ist Designkriterium, kein bereits bewiesenes Theorem.

## 10. Rand- und Anfangsbedingungen

Die Randfläche wird in undurchlässige, drainierende und freie Bereiche zerlegt.

**Mechanik:** freie Oberfläche \(\boldsymbol\sigma_{\rm tot}\mathbf n=\mathbf t_{\rm cap}\); nur ohne Oberflächenspannung/Krümmung darf \(\mathbf t_{\rm cap}=0\) gesetzt werden. Substratkontakt (Haftung, Reibung, Ablösung) ist explizit zu spezifizieren. Keine äußere Drucklast und keine Oedometerzwängung im natürlichen Kernmodell.

**Fluid:** undurchlässig \(\mathbf q\cdot\mathbf n=0\); drainierend \(p=p_{\rm ext}\) oder Robin:
\[
\mathbf q\cdot\mathbf n=L_p(p-p_{\rm ext}-p_c),\quad L_p\ge0.
\]
\(p_c\) beschreibt einen definierten kapillaren/Benetzungsbeitrag. \(L_p,p_c\) sind nicht aus dem Wort „natürlich“ ableitbar.

**Spezies:** Gesamtfluss relativ zum Rand an undurchlässigen Rändern null; offener Austritt mit konvektivem Austrag und spezifiziertem diffusivem Fluss.

**Netzwerk/Morphologie:** keine künstlichen Dirichlet-Werte; bei Gradiententerme Nullfluss oder physikalische Oberflächenkinetik.

Anfangsdaten \(\mathbf u_0,p_0,\phi_0,B_0,D_{f,0},z_0,\xi_{u,0},\xi_{r,0},c_{i,0},T_0\) müssen Stoffbilanzen, \(0<\phi<1\), positive Permeabilität und mechanische Zwangsbedingungen erfüllen.

## 11. Rückkopplung und Hierarchie

Die kausale Schleife:
\[
(\mathbf c,T)\to B\to(D_f,z,\phi,\xi)
\to(\mathbb C,\mathbb V,\mathbf K)
\to(p,\mathbf q,\mathbf u)\to(\phi,\mathbf c,B).
\]
Jeder Pfeil benötigt eine konstitutive Funktion oder einen Bilanzterm. Nicht belegte Pfeile bleiben unabhängige Eingaben.

Vereinfachung: P0 gesättigte isotherme Biot-Darcy-Poroelastizität; P1 plus beschränkte B-Kinetik; P2 plus konservativer Speziestransport; P3 Morphologie und gemessene Transport-/Modulschließungen; P4 viskoelastische Relaxation und nichtlineare Eigenstrain; P5 vollständige 3D-Kopplung mit realer freier Oberfläche. Ein Satz für P0 ist kein Beweis für P5.

## 12. Datenregeln und Nicht-Ansprüche

Primärziel bleiben natürliche, mechanisch unbelastete Synäresekurven gefällter Silica. Wilhelm-&-Kind-Ablesungen bleiben Näherungsdaten und prüfen zunächst globale Volumenantworten, nicht lokale Felder. Die 21 Druckzellreihen aus DATA/Raw/kurvendigitalisierung.csv bleiben ausgeschlossen. Scherer-TEOS-Daten sind nur externer Mechanismenvergleich. Fehlende Felder B, K, C, Df und z werden nicht aus S(t) erfunden.

Diese v1.0 beansprucht ausdrücklich **keine** vollständig abgeleitete freie Energie, keinen Existenz-/Eindeutigkeitsbeweis für das volle nichtlineare 3D-System, keinen globalen Regularitätsbeweis, keine universellen Struktur-Permeabilitäts- oder Struktur-Modul-Gesetze, keine Identifikation aller Parameter aus den vorhandenen globalen Kurven und noch keine durchgeführte 3D-Simulation. Sie ist eine vollständige Gleichungsarchitektur als Grundlage der nächsten mathematischen Arbeiten.
