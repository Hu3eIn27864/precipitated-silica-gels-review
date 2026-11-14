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
| EQ-04 | reversible Brückenbilanz (dot B=k_f(cdot)(B_{max}-B)-k_{hyd}(cdot)B) | pH, Temperatur, Ionen, gelöstes Si, (k_f,k_{hyd}) | M-GRÜN nach Positivitätsprüfung | P-GELB | E-ROT | Si-Massenbilanz plus Zeitreihen; noch nicht in v0.3 implementiert |
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
