# CCFSM P27.17 — prozessgetrennte P21-Konservativitätsprüfung

**Stand:** 15.11.2026  
**Status:** implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel

P27.17 erweitert den P27.16-Fluss-Audit um eine unabhängige Zerlegung der P21-Rechten-Seite in Darcy-Fluidbilanz, mobile Advektion, Onsager-Diffusion und lokale Reaktionen. Geprüft werden sowohl die lokale Rekonstruktion der vier Inventar-RHS als auch getrennte globale Randflussidentitäten.

## Prozesszerlegung

Für Fluidkapazität gilt \(\dot\theta=-\mathrm{div}(q)\). Für mobile Spezies M/O werden die gelieferten Gesamtflüsse und Advektionsflüsse getrennt geprüft; der Onsager-Diffusionsfluss wird als Differenz \(J_{diff}=J_{total}-J_{adv}\) rekonstruiert. Die lokalen Reaktionsquellen werden unabhängig aus den drei P10-Raten gebildet:
\[
S_M=-r_1,\quad S_O=r_1-r_2,\quad
S_N=r_2-r_3,\quad S_B=r_3.
\]
Die Summe der vier Reaktionsquellen muss punktweise null sein. N/B besitzen in P21 keinen eigenen Transportfluss und werden deshalb als reaktionsgetriebene Inventare bilanziert.

## Prüfgates

1. Lokale FV-Gleichung pro Darcy-, Advektions- und Diffusionsbeitrag.
2. Globale Teleskopbilanz gegen linken und rechten Randfluss.
3. Gesamt-RHS-Rekonstruktion für M/O/N/B aus Prozessbeiträgen.
4. Separater N/B-Reaktionsquellenabschluss und globale Silicium-Stöchiometrie.

## Regressionen

Acht Tests decken geschlossene Prozessbilanz, Reaktionsstöchiometrie, RHS-/Flussfehler, nichtuniforme Zellbreiten, fehlende Prozessdaten und Aussagegrenzen ab.

## Aussagegrenzen

Der Audit verwendet ausschließlich die gelieferten diskreten P21-Felder. Die Diffusion wird aus Gesamt- minus Advektionsfluss rekonstruiert, nicht unabhängig aus chemischen Potentialen neu berechnet. Es wird weder die Vollständigkeit der Quellen noch die physikalische Richtigkeit der Flüsse bewiesen. Keine 3-D-Erhaltung, keine globale Energieidentität, keine Stabilitäts- oder Existenzgarantie und keine experimentelle Validierung.
