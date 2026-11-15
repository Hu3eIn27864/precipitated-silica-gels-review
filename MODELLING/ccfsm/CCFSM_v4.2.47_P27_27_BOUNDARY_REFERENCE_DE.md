# CCFSM v4.2.47 — P27.27: analytische Randfluss-Referenzfälle

**Datum:** 15.11.2026  
**Status:** Implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel

P27.27 prüft den P27.25-Adapter mit analytisch vorgegebenen geschlossenen und offenen Randfällen. Alle Randflüsse und Potentiale sind innerhalb des synthetischen Zeitschritts konstant. Die Referenzintegrale sind deshalb exakt und unabhängig von einer numerischen Zeitquadratur bestimmbar.

## Implementierung

- \`ccfsm_p27_27_boundary_reference.py\` erzeugt geschlossene und offene synthetische P21-Snapshots, ruft den bestehenden P27.25-Adapter auf und vergleicht dessen Ergebnisse mit separat notierten analytischen Referenzwerten.
- \`test_ccfsm_p27_27_boundary_reference.py\` enthält sechs Regressionen.
- Geprüft werden Stofftransfer von M/O, chemische mobile Randarbeit und hydraulische Reservoirarbeit.
- Fehler werden für jede Größe separat ausgewiesen; die Toleranz wird nicht zur Korrektur oder Normierung der Ergebnisse verwendet.

## Analytischer offener Referenzfall

Für M werden links ein positiver advektiver Fluss \(a_L=2\), rechts \(a_R=1\), sowie diffusive Flüsse \(d_L=0.5\), \(d_R=-0.25\) mol m\(^{-2}\) s\(^{-1}\) vorgegeben. Die Potentiale sind \(\mu_L=5\), \(\mu_R=11\), \(\mu_{\mathrm{cell,right}}=7\) J mol\(^{-1}\).

Damit ergibt sich gemäß der im P27.25-Adapter verwendeten Vorzeichenkonvention:
\[
P_{\mathrm{chem}}=\mu_Ld_L-\mu_Rd_R+\mu_La_L-\mu_{\mathrm{cell,right}}a_R
=8.25\ \mathrm{W\,m^{-2}}.
\]
Für \(A=2\ \mathrm{m^2}\) und \(\Delta t=3\ \mathrm{s}\) folgt \(W_{\mathrm{chem}}=49.5\ \mathrm{J}\).

Der hydraulische Referenzleistungsfluss beträgt \(4\ \mathrm{W\,m^{-2}}\), somit \(W_{\mathrm{hyd}}=24\ \mathrm{J}\). Der Netto-M-Eintrag ist \(2.5-0.75=1.75\ \mathrm{mol\,m^{-2}\,s^{-1}}\), entsprechend \(10.5\ \mathrm{mol}\) über den Schritt. Für O sind alle Randflüsse null.

Im geschlossenen Fall sind sämtliche Randflüsse und die hydraulische Reservoirleistung null; daher müssen chemische Randarbeit, hydraulische Arbeit und M/O-Nettoübertrag ebenfalls null sein.

## Aussagegrenzen

Die Fälle verifizieren Vorzeichen, Einheiten und die Auswertung des P27.25-Adapters für konstante synthetische Randdaten. Sie sind keine physikalische Reservoirmodellierung. Zeitvariable P24-Verläufe, vollständige Upwind-Entropie-/Kettenregel, chemische Arbeit der Feststoff-/Brückenreservoirs und mechanische Randarbeit bleiben ungeprüft. P27.27 begründet daher keinen vollständigen Energieabschluss und keine physikalische Validierung.
