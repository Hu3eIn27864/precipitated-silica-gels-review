# CCFSM v4.2.49 — P27.29: Upwind-Zweigwechsel und Zeitstützstellenverfeinerung

**Datum:** 15.11.2026  
**Status:** Implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel

P27.29 untersucht eine in P27.28 noch nicht abgedeckte Schwierigkeit: Wenn ein advektiver Randfluss sein Vorzeichen wechselt, wechselt auch das vom P27.25-Adapter verwendete Upwind-Chemiepotential. Die Randleistungsfunktion besitzt dann im Allgemeinen einen Knick. Eine Trapezregel über ein Intervall, das den Wechsel überquert, interpoliert über zwei verschiedene Upwind-Zweige.

## Synthetischer Referenzfall

Für (T=2,s) werden lineare Flüsse (j_L(t)=t-1) und (j_R(t)=t-1.5) verwendet. Der linke Fluss wechselt bei (t=1,s), der rechte bei (t=1.5,s) das Vorzeichen. Die Upwind-Potentiale sind absichtlich verschieden:

- Links: negatives Fluxvorzeichen verwendet Zellpotential 5 J/mol; nichtnegatives Vorzeichen Reservoirpotential 2 J/mol.
- Rechts: negatives Fluxvorzeichen verwendet Reservoirpotential 3 J/mol; nichtnegatives Vorzeichen Zellpotential 7 J/mol.

Die exakten Integrale werden stückweise an den Nullstellen der Flüsse ausgewertet. Für (A=1.5,m^2) lauten die Referenzen:
- linker chemischer Randarbeitsbeitrag: −2.25 J
- rechter chemischer Randarbeitsbeitrag: +3.75 J
- Summe chemische Randarbeit: +1.50 J
- Netto-M-Materialtransfer: +1.50 mol

## Verfeinerungsprüfung

Die P27.25-Rekonstruktion wird auf jedem Teilintervall separat aufgerufen und anschließend summiert. Damit werden Zeitstützstellenfolgen mit und ohne explizite Stützstelle am jeweiligen Zweigwechsel verglichen. Material- und Energiefehler werden separat ausgewiesen. Eine Stützstelle am Vorzeichenwechsel trennt die beiden glatten Upwind-Zweige; weitere Verfeinerung kontrolliert die verbleibenden Quadraturfehler.

Vier Regressionen prüfen die analytischen stückweisen Referenzen, Zweigwechselzeiten, Verfeinerungsdiagnostik und Eingabevalidierung.

## Aussagegrenzen

Dies ist ein synthetischer Adapter-/Quadraturtest. Er beweist weder die vollständige diskrete Upwind-Entropie-Kettenregel noch die Integration des tatsächlichen P24-Newton-Pfads. Feststoff-/Brückenreservoirarbeit, mechanische Randarbeit, physikalische Reservoirgesetze und physikalische Validierung bleiben offen.
