# CCFSM v4.2.40 — P27.20 Zwei-Zustands-Energie-Snapshot-Adapter

**Stand:** 15.11.2026  
**Status:** implementierter Adapter; noch kein vollständiger Energieabschluss.

## Zweck und Bilanzierung

P27.20 verbindet zwei zeitlich geordnete Zustände über eine dimensionskonsistente Energiedifferenz. Die FV-Energie wird aus einer explizit vom Aufrufer gelieferten freien Energiedichte (f_h) integriert:

\[
E_{FV}^{k}=A\sum_j \Delta x_j f_{h,j}^{k},
\qquad
\overline{\dot E}_{FV}=\frac{E_{FV}^{k+1}-E_{FV}^{k}}{A\Delta t}.
\]

Die P19-mechanisch-poroelastische gespeicherte Energie wird aus `stored_energy_j` übernommen und separat als mittlere Rate pro Referenzfläche ausgewiesen. Beide Raten haben damit die Einheit W/m².

## Schnittstelle

- `build_two_state_energy_snapshot` verlangt zwei Zeitpunkte, identische 1-D-FV-Zellbreiten, FV-Energiedichten in J/m³, Querschnittsfläche in m² und zwei P19-Lösergebnisse.
- Nichtuniforme, aber zwischen den Zuständen identische Zellbreiten sind zulässig.
- Bei geändertem FV-Netz wird bewusst abgebrochen; vor dem Vergleich ist eine konservative Remap-/Restriktionsoperation erforderlich.
- P19-Energien werden als bereits integrierte Joule-Werte behandelt und nicht nochmals mit der Fläche multipliziert.
- Die Differenz der P19-Randtraktionsarbeits-Diagnostik wird nur auf ausdrückliche Option ausgegeben. Sie ist nur für einen kompatiblen Lastpfad (insbesondere unveränderte Traktion) als Pfadarbeit interpretierbar. Dirichlet-Reaktionsarbeit wird nicht automatisch ergänzt.

## Kopplung mit P27.19

Das Ergebnis liefert `energy_rate_components_w_m2` für den P27.19-Ledger. Die externen Traktionsleistungen werden nur dann als Ledger-Eingabe angeboten, wenn die optionale Endpunktdifferenz aktiviert wurde. Dissipationen (P10-Reaktion, P13/Onsager, Darcy) müssen weiterhin separat und mit korrekter Flächen-/Volumenintegration bereitgestellt werden.

## Aussagegrenzen

- Die FV-Energiedichte ist eine Eingabe, keine aus P10/P13 automatisch hergeleitete freie Energie. Es gibt noch keinen Beweis, dass sie mit der P19-Energie aus einer gemeinsamen freien Energie stammt oder Doppelzählungen ausschließt.
- Die P19-Energiedifferenz ist eine endliche Differenz zweier quasistatischer Gleichgewichtszustände, keine kontinuierliche Ableitung und keine vollständige mechanische Leistungsbilanz.
- Endpoint-Differenzen der Traktionsarbeit sind ohne Lastpfadannahme keine allgemeine Pfadarbeit; Dirichlet-Arbeit, Randenergie, Advektion und weitere äußere Beiträge können fehlen.
- Zwei Zustände allein zertifizieren weder Energieabnahme noch thermodynamische Stabilität, Zeitintegrator-Konvergenz, PDE-Existenz, 3-D-Positivität oder experimentelle Validität.

## Regressionen

Sieben Tests decken Energiedifferenzen/Einheiten, nichtuniforme Gitter, optionale Traktionsarbeit, Gitter-/Zellzahlfehler sowie Zeit-, Flächen- und P19-Energievalidierung ab.
