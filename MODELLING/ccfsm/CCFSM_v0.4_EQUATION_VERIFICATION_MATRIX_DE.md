# CCFSM v0.4 — Gleichungs- und Einflussparameter-Prüfmatrix

**Geltungsbereich:** natürliche, mechanisch unbelastete Synärese gefällter Silica-Gele. Statusangaben beziehen sich auf die derzeitige Modell- und Datenlage im Repository (14.11.2026).

Legende:
- **M-GRÜN**: mathematisch konsistent innerhalb der angegebenen Annahmen geprüft.
- **P-GELB**: physikalische Konstitutivannahme plausibel, aber für den konkreten Silica-/Protokollbereich nicht unabhängig bestätigt.
- **E-GELB/ROT**: empirische Parameterschätzung bzw. unabhängige Validierung fehlt.
- **NICHT AKTIV**: Parameter/Mechanismus ist im v0.3-Gleichungssystem noch keine dynamische Kopplung.

| ID | Beziehung | Einflussparameter | M | P | E | Nächster erforderlicher Nachweis |
|---|---|---|---|---|---|---|
| EQ-01 | (B)-Kinetik: (dot B=k_b(B_infty-B)) | (k_b,B_infty,B_0,pH,T_g,I,c_{Si},t_{age}) | M-GRÜN für konstante positive Parameter | P-GELB: Sättigungskinetik ist Hypothese | E-ROT | zeitaufgelöster Brücken-/Si-Proxy, getrennte Säure-/Basenroute |
| EQ-02 | Temperaturgesetz (k_j(T_g)) | (E_{a,j},T_g(t)) | M-GRÜN als Arrhenius-Ansatz | P-GELB | E-ROT | Gelkerntemperatur und Rate bei mehreren Temperaturen |
| EQ-03 | Speziation (pH,I,{c_i}	o) Aktivitäten | Säure/Base, Gegenionen, Silikatmodul, Wasser | NICHT AKTIV | P-GELB | E-ROT | vollständige Stoff-/Ladungsbilanz und validiertes Aktivitätsmodell |
| EQ-04 | reversible Brückenbilanz (dot B=k_f(cdot)(B_{max}-B)-k_{b hyd}(cdot)B) | pH, Temperatur, Ionen, gelöstes Si, (k_f,k_{b hyd}) | M-GRÜN nach Positivitätsprüfung | P-GELB | E-ROT | Si-Massenbilanz plus Zeitreihen; noch nicht in v0.3 implementiert |
| EQ-05 | Morphologie-Nachführung (dot D_f=k_m(D_{f,eq}-D_f)), (dot z=k_m(z_{eq}-z)) | (k_m,D_{f,0},Delta D_f,z_0,Delta z,B) | M-GRÜN bei zulässigen Zielwerten | P-GELB | E-ROT | synchronisierte zeitaufgelöste Df-/Kontaktmessung |
| EQ-06 | Porenstruktur-Schließung ((D_f,z,phi,r_{throat},C_{conn},	au_p)	okappa_{eff}) | Porenhalsverteilung, Konnektivität, Tortuosität, Sättigung | NICHT AKTIV | P-GELB | E-ROT | 3D-Porenanalyse plus unabhängige Permeabilitätsmessung |
| EQ-07 | Mechanik-Schließung Netzwerk (	o K_{eff}) | Kontaktverteilung, Bindungsstärke, Dichte, Rheologie | NICHT AKTIV | P-GELB | E-ROT | Modul/Rheologie am gleichen Gelzustand; freie-Synärese-relevanter Modul |
| EQ-08 | Kontraktionsbilanz (dot X=Omega_bdot B) | (Omega_b,B,B_0,X_0) | M-GRÜN, exakt aus v0.3-ODEs | P-GELB | E-ROT | unabhängige B- und X-Messung |
| EQ-09 | Relaxationspartition (dotsigma=Omega_bdot B-k_rsigma,dotepsilon_r=k_rsigma) | (k_r,sigma_0,epsilon_{r,0}) | M-GRÜN, Summe konserviert | P-GELB | E-ROT | unabhängige Relaxations-/Rheologiezeitreihe |
| EQ-10 | (q=1-e^{-X}) | (X) | M-GRÜN als Abbildung | P-GELB: Form der Abbildung unbewiesen | E-ROT | Vergleich mit unabhängiger Messung des intrinsischen Potenzials |
| EQ-11 | (k_h=3600C_gkappa K/(mu L_d^2)) | (C_g,kappa,K,mu,L_d,R_c) | M-GRÜN dimensionsanalytisch für reduzierte erste Mode | P-GELB: Rand-/Interfaceannahmen prüfen | E-GELB/ROT | Geometrie-spezifische Lösung und unabhängige Messung aller Faktoren |
| EQ-12 | (dot S=k_h(eta_aq-S)) | (k_h,eta_a,q,S_0) | M-GRÜN: lineare ODE, bedingte Schranken bewiesen | P-GELB | E-GELB/ROT | gemeinsame q-/S-Messung und hold-out Vorhersage |
| EQ-13 | Beobachtungsbilanz (V_{obs}=V_{syneresis}+V_{evap}+ldots) | Verdunstung, freie Oberfläche, Probengeometrie | NICHT AKTIV | P-GELB | E-ROT | Leer-/Verdunstungskontrollen, Flüssigkeits- und Volumenbilanz |

## Harte Freigaberegeln

1. Eine Gleichung darf nicht als vollständig grün markiert werden, wenn ein physikalischer Wirkpfad nur vermutet wird.
2. Ein guter Fit von (S(t)) beweist nicht die Identität der inneren Zustände (B,D_f,z,sigma,kappa,K).
3. Rezeptur und pH werden nicht als unabhängige Prädiktoren doppelt gezählt, wenn pH bereits aus der Chemie folgt.
4. Säure- und Basenroute sowie Tropfen- und Zylindergeometrie bleiben getrennte Protokolle, bis eine gemeinsame Gesetzmäßigkeit validiert ist.
5. Temperatur ist die gemessene Geltemperatur (T_g(t)), nicht ungeprüft die Badtemperatur.
6. Nur mechanisch unbelastete natürliche Synärese darf die CCFSM-Naturparameter kalibrieren.
7. Daten aus einer Kurvendigitalisierung erhalten zusätzliche Messunsicherheit und gelten nicht als Rohdaten der Autoren.

## Priorisierte Freigabe-Reihenfolge

**Gate 1 — Mess- und Definitionsqualität:** eindeutiger (t_0), Definition von (S), Temperaturverlauf, Geometrie, Masse-/Volumenbilanz und Replikate.

**Gate 2 — Chemie:** Rezeptur, pH, Gegenionen/Ionenstärke, gelöstes Si und Netzwerk-Si bilanzieren; (B(t)) oder validierten Proxy identifizieren.

**Gate 3 — Struktur:** (D_f,z,phi,r_{throat},C_{conn},	au_p) am selben Probenalter messen.

**Gate 4 — Mechanik und Transport:** (K_{eff},kappa_{eff},mu,R_c) unter passenden Zuständen separat bestimmen.

**Gate 5 — gekoppelte Vorhersage:** Parameter auf Trainingsprotokollen bestimmen, danach unberührte Temperatur-/Geometrieprotokolle vorhersagen; Unsicherheitsintervalle und Modellvergleich angeben.

Erst nach Gate 5 ist eine vollständig grüne empirische Modellgleichung vertretbar. Die mathematische Grünmarkierung kann unabhängig davon bereits früher erreicht werden.


## Ergänzung v0.4 — chemisches Teilmodell

| ID | Beziehung | Parameter | M | P | E | Freigabebedingung |
|---|---|---|---|---|---|---|
| EQ-14 | \(\dot c_m=-r_o+r_d;\ \dot c_o=r_o-r_n;\ \dot c_n=r_n-r_d\) | \(k_o,k_n,k_d,c_m,c_o,c_n\) | M-GRÜN: exakte Si-Erhaltung | P-GELB: geschlossene Bilanz, Spezieszuordnung vereinfacht | E-ROT | zeitaufgelöste Si-Spezies plus Si-Ausflussbilanz |
| EQ-15 | \(r_o=k_oc_{ref}(c_m/c_{ref})^{n_o}\Omega^{m_o}F_{pH}F_I\) | pH-Kanalgewichte/-ordnungen, \(I,m_I,c_{eq}\) | M-GRÜN als definierte Rate | P-GELB: Modellsysteme nicht gleich Industriefällung | E-ROT | pH-/I-/Konzentrationsmatrix im Zielsystem |
| EQ-16 | \(r_n=k_nc_oF_{pH}F_I;\ r_d=k_dc_nF_d\) | Netzwerk- und Auflösungsraten | M-GRÜN | P-GELB | E-ROT | gelöste/oligomere/netzwerkgebundene Si-Zeitreihen |
| EQ-17 | \(\dot\beta=k_{form}F_{pH}F_I(1-\beta)-k_{b hyd}F_{hyd}\beta\) | \(k_{form},k_{b hyd},f_{load}\) | M-GRÜN: Intervall \([0,1]\) invariant | P-GELB: mesoskopische Brückendefinition | E-ROT | unabhängiger Tragfähigkeits-/Konnektivitätsproxy |
| EQ-18 | \(B=f_{load}c_n\beta\) | \(f_{load},c_n,\beta\) | M-GRÜN: \(0\le B\le f_{load}c_n\) | P-GELB | E-ROT | gleichzeitige Netzwerk-Si- und Kontaktmessung |

Die drei Si-Pools sind eine konservative Transferbilanz. Bei relevantem Siliciumaustrag im Syneresat muss ein gemessener Randfluss ergänzt werden. Die pH-/Ionenstärke-/Arrheniusfaktoren sind flexible Hypothesen und keine universellen Naturgesetze.
