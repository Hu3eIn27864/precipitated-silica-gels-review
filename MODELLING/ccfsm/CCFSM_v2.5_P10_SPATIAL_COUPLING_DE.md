# CCFSM P10 — räumliche chemo-poroelastische Kopplung

**Status:** semidiskreter 1D-Finite-Volumen-Operator, aufgebaut auf der lokalen P9-Schließung. Keine Zeitintegration, keine vollständige PDE-Existenztheorie und keine empirische Kalibrierung.

## 1. Zustandswahl

Primärzustände sind die Fluidkapazität (\theta_j\in(0,1]) und die vier Siliciuminventare (m_{M,j},m_{O,j},s_{N,j},s_{B,j}>0), jeweils pro Referenzvolumen. Der lokale P9-Operator liefert daraus
[
(p_j,e_j,b_j,K_j)=\mathcal C_{P9}(\theta_j,m_{M,j},m_{O,j},s_{N,j},s_{B,j}).
]
Der Porendruck ist damit eine algebraische Zustandsgröße, nicht ein unabhängig integrierter Druckfeldwert. Das vermeidet eine doppelte Druck-/Speicherzustandsführung innerhalb dieser Reduktion.

## 2. Ein Darcy-Fluss für beide Bilanzen

An inneren Flächen wird die harmonische Permeabilität verwendet:
[
K_{j+1/2}=\frac{2K_jK_{j+1}}{K_j+K_{j+1}},\qquad
Q_{j+1/2}=-K_{j+1/2}\frac{p_{j+1}-p_j}{\Delta x}.
]
An den äußeren Halbzellenflächen gilt die entsprechende Reservoir-Druckbedingung:
[
Q_{1/2}=-K_1\frac{p_1-p_L}{\Delta x/2},\qquad
Q_{N+1/2}=-K_N\frac{p_R-p_N}{\Delta x/2}.
]
Positive Flüsse zeigen nach rechts. Der identische gespeicherte Flussvektor (Q) wird verwendet in
[
\dot\theta_j=-\frac{Q_{j+1/2}-Q_{j-1/2}}{\Delta x}
]
und im advectiven Anteil der mobilen M/O-Bilanzen. Dies ist die zentrale diskrete Konsistenzbedingung von P10.

## 3. Mobile Spezies und lokale Reaktion

Für (i\in\{M,O\}) wird der Fluss
[
J_{i,j+1/2}=c_{i,up}Q_{j+1/2}
-\theta_{j+1/2}D_i\frac{c_{i,j+1}-c_{i,j}}{\Delta x},
\qquad c_{i,j}=m_{i,j}/\theta_j
]
mit Upwind-Advektion und zentraler Konzentrationsdiffusion verwendet. Reservoirkonzentrationen setzen die äußeren Diffusionsrandwerte und die einströmende Upwind-Konzentration.

Die lokalen Reaktionen bleiben (M\rightleftharpoons O\rightleftharpoons N\rightleftharpoons B). Die Affinitäten werden aus den **totalen P9-Potentialen** gebildet. Mit logarithmischem Mittel als positiver Mobilität:
[
r_i=k_ic_*\,L(a_i,a_{i+1}/K_i^{eq})\,
\frac{\mu_i^{tot}-\mu_{i+1}^{tot}}{RT}.
]
Somit ist (r_i(\mu_i^{tot}-\mu_{i+1}^{tot})\ge0) für positive Aktivitäten. Die Reaktionsquellen verteilen sich als ((-r_1,r_1-r_2,r_2-r_3,r_3)) und erhalten lokal das gesamte Si-Inventar.

N/B bleiben immobil. M/O diffundieren und advectieren. Alle Inventare sind Si-Äquivalente; eine explizite Speziesstöchiometrie jenseits der vier Pool-Übergänge ist nicht ergänzt.

## 4. Diskrete Erhaltung

Summation über Zellen teleskopiert alle inneren Flüsse:
[
\frac{d}{dt}\left(\Delta x\sum_j\theta_j\right)
=-(Q_{N+1/2}-Q_{1/2}),
]
[
\frac{d}{dt}\left(\Delta x\sum_j(m_{M,j}+m_{O,j}+s_{N,j}+s_{B,j})\right)
=-\sum_{i=M,O}(J_{i,N+1/2}-J_{i,1/2}).
]
Bei hydraulisch geschlossenen und stofflich undurchlässigen Rändern bleiben Fluidkapazität und Gesamt-Si erhalten. Reaktionen ändern die lokale Summe nicht.

## 5. Dissipationsdiagnostik — keine vollständige Energietheorie

Der Code berichtet nichtnegative interne Darcy- und ideale mobile Diffusionsbeiträge:
[
\mathcal D_D=\sum_{f\ interior}\frac{Q_f^2}{K_f}\Delta x\ge0,
\qquad
\mathcal D_{diff,i}\sim\sum_f
\theta_fD_i\frac{(c_{i,R}-c_{i,L})^2}{\bar c_{i,f}\Delta x}\ge0.
]
Außerdem wird (r_iA_i\ge0) zellweise ausgegeben. Reservoirarbeit und offene Stoffflüsse sind Randterme. Diese getrennten nichtnegativen Diagnostiken sind **noch kein Beweis**, dass die Summe der P9/P8c-Energie über die vollständige gekoppelte Dynamik monoton fällt. Insbesondere muss eine künftige globale Energiebilanz die Abhängigkeit der mechanischen Energie von (	heta,m_i,s_i), die mechanischen Randbedingungen und alle Reservoirterme gemeinsam behandeln.

## 6. Implementierung und Tests

- `ccfsm_p10_spatial_coupling.py`: P9-Zellschließung, harmonische Flächenpermeabilität, Darcy-Flüsse, Fluidbilanz, M/O-Flüsse, P9-korrigierte Reaktionen und Dissipationsdiagnostiken.
- `test_ccfsm_p10_spatial_coupling.py`: einheitlicher Darcy-Fluss, geschlossene Fluidbilanz, geschlossene/offene Si-Bilanz, lokale Reaktionskonservierung, nichtnegative Reaktions-/Diffusions-/Darcy-Diagnostiken und Eingabevalidierung.

## 7. Grenzen und nächste Schritte

P10 ist 1D und semidiskret. Es gibt noch keinen Zeitschrittintegrator, keine Positivitätserhaltung für beliebig große explizite Zeitschritte, keine bewegte Gel/Flüssig-Grenzfläche, keine Kapillarspannung und keinen allgemeinen 3D-Festkörperlöser. Die (K(b,e))-Abhängigkeit und sämtliche mechanischen Parameter bleiben unkalibriert. Die natürliche Synärese wird nicht mit erzwungenen Druckzell-/Oedometerdaten kalibriert.

P11 sollte eine energiekompatible Zeitintegration mit Positivitätskontrolle und einem vollständigen diskreten Energiehaushalt entwickeln. Erst danach ist ein sinnvoller Schritt zu Konvergenz-/Stabilitätsanalysen und zur räumlichen Erweiterung.
