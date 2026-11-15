# CCFSM P27.23 — gekoppeltes thermodynamisches Energie- und Dissipationsledger

**Datum:** 15.11.2026  
**Status:** implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel

P27.22 hat den mechanisch-poroelastischen Energieanteil von P9 und P19 im abgeglichenen Spezialfall vergleichbar gemacht. P27.23 führt diesen Befund mit P10/P13 zusammen: chemische, elastische und Biot-Speicherenergie werden als gespeicherte Energie getrennt geführt; Reaktions-, Darcy- und Onsager-Dissipation werden in konsistenten Einheiten bilanziert.

## Bilanz und Einheiten

Für Zellvolumina \(V_j\) und P9-Energiedichten gilt
\[
E_{P9}=\sum_j V_j(\psi_{el,j}+\psi_{B,j}+\psi_{chem,j}).
\]
Bei Wahl von P19 als mechanischem Eigentümer ersetzt dessen geprüfte FE-Energie den P9-Anteil \(\sum_j V_j(\psi_{el,j}+\psi_{B,j})\); sie wird **nicht zusätzlich** addiert. P9-Chemie bleibt ein separater Beitrag.

Dissipationsleistungen:
- P10-Reaktionen: \(D_{chem}=\sum_j V_j\,d_j\), mit \(d_j\) in W/m³.
- P10-Darcy-Innendissipation: \(D_{Darcy}=A\,d_{Darcy}\), wobei \(d_{Darcy}\) in W/m² angegeben ist.
- P13-Onsager-Diffusion: \(D_{diff}=A\sum_s d_{diff,s}\), ebenfalls aus W/m².

Damit sind Energiebeiträge in J und Leistungsbeiträge in W. Die Bilanzprüfung lautet
\[
\mathcal R_E=\dot E-\left(P_{ext}-D_{chem}-D_{Darcy}-D_{diff}\right).
\]
Externe Leistungen werden ausdrücklich als benannte Eingaben übergeben; das Modul erfindet keine Randarbeits- oder Reservoirleistung. Optional wird das kraftgesteuerte Dead-load-Gesamtpotential \(E-\int \sigma_{ext}\,\varepsilon\,dV\) getrennt vom gespeicherten Energieinhalt ausgewiesen.

## Implementierung

- `ccfsm_p27_23_thermodynamic_ledger.py`: volumen- und flächenrichtige Integration, P9/P19-Ownership, optionales Dead-load-Potential, Prüfung der Dissipationsvorzeichen und Energieratenresiduum.
- `test_ccfsm_p27_23_thermodynamic_ledger.py`: sieben Regressionen für Einheiten/Integration, Bilanzresiduum, P19-Ersatz statt Addition, Volumenabgleich, negative Dissipation, Dead-load-Potential und uneinheitliche Traktion.

## Aussagegrenzen

P13s Onsager-Diffusionsdissipation wird gezählt; der von P13 geerbte P10-Fick-Diffusionsdiagnostikterm wird nicht ein zweites Mal addiert. P10/P13 weisen selbst darauf hin, dass die Entropie-/Energiebilanz der Upwind-Advektion noch nicht geschlossen ist. Reservoir-Chemie- und Hydraulikleistungen müssen vom Aufrufer korrekt und mit Vorzeichenkonvention in `external_power_terms_w` eingetragen werden. Gradientenergien, vollständige Randarbeitsbilanz und eine geschlossene P21/P24-Zeitdiskretisierungs-Energieabschätzung sind nicht bewiesen.

P27.23 ist daher ein unit-konsistentes, nicht-doppelzählendes Buchungs- und Auditwerkzeug – kein Beweis eines globalen thermodynamischen Stabilitätssatzes und keine experimentelle Validierung.
