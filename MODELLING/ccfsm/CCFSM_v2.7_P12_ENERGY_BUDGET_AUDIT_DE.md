# CCFSM P12 — offene Energiebilanz und Randarbeits-Audit

**Version:** CCFSM v2.7  
**Datum:** 14. November 2026  
**Ausgangspunkt:** P10 räumliche Kopplung und P11 Energieüberwachung

## 1. Ziel

P12 macht die zuvor nur teilweise ausgewiesenen Randbeiträge sichtbar. Für einen P11-Zustand wird die semidiskrete P10-Energierate über die Kettenregel berechnet und mit hydraulischer Reservoirleistung sowie einem explizit als Näherung gekennzeichneten chemischen Randarbeits-Term verglichen.

P12 ist ein **Energiebilanz-Audit**, noch kein vollständig thermodynamisch geschlossenes offenes Randwertproblem. Der Audit gibt deshalb einen nicht geschlossenen Residualterm zurück und behauptet keine Identität, die das aktuelle P10-Schema nicht herleitet.

## 2. Kettenregel der gespeicherten Energie

Für die P9-Zellenergiedichte und den P10-Vektor (F_{10}) wird die semidiskrete Änderungsrate

[
dot{mathcal E}_h
=Delta xsum_jleft[
rac{partialPsi_j}{partial	heta_j}dot	heta_j+
sum_{iin{M,O,N,B}}mu_{i,j}^{m tot}dot u_{i,j}
ight]
]

ausgewertet. Dabei werden die in P9 implementierten konjugierten Größen (p-Pi_{m osm}) und (mu_i^{m tot}) verwendet. Die mechanischen chemischen Korrekturen bleiben somit im Audit erhalten.

## 3. Hydraulische und chemische Randleistung

Mit positiver Darcy-Richtung von links nach rechts ist die im P10-Code verwendete hydraulische Reservoirleistung

[
P_{m hyd}^{m res}=p_{m ext}(Q_R-Q_L).
]

Für M/O werden die tatsächlichen P10-Randflüsse ausgegeben. Eine chemische Randleistungs-Schätzung wird mit den Donor-seitigen chemischen Potentialen gebildet. Sie ist derzeit ausdrücklich **keine exakte diskrete Entropieflussformel**: Die aktuelle Kombination aus Upwind-Advektion und konzentrationsbasierter Fick-Diffusion besitzt noch keine hergeleitete gemeinsame diskrete freie-Energie-Ungleichung mit Reservoirpotentialen.

Der Audit meldet daher

[
R_E=dot{mathcal E}_h-
left(P_{m hyd}^{m res}+P_{m chem}^{m res,est}ight)
]

als *unclosed residual*. Dieser Wert ist ein Diagnosewert und darf nicht als numerischer Fehler einer bereits bewiesenen Energiebilanz interpretiert werden.

## 4. Mechanische Randarbeit

P9 enthält die gespeicherte elastische und Biot-Energie, aber kein äußeres Traktionspotential in der gespeicherten Energie. Der P12-Audit kennzeichnet daher jede nichtverschwindende axiale Traktion als mechanisch unvollständig. Die Randarbeit (t,dot e) bzw. das korrespondierende Potential muss in einer zukünftigen variational konsistenten Formulierung ergänzt werden; eine bloße Addition eines beliebigen Terms wäre nicht ausreichend.

## 5. Verifizierte Eigenschaften

Die Tests prüfen:
- geschlossenen Nullfluss-Referenzfall und verschwindende Randleistung;
- Ausgabe der hydraulischen Reservoirleistung bei offenen Druckrändern;
- explizite Kennzeichnung der chemischen Randleistung als Näherung;
- Kennzeichnung äußerer Traktion als nicht bilanzierter mechanischer Beitrag;
- endliche Energie-, Dissipations- und Residualdiagnostik.

## 6. Grenzen und nächste mathematische Aufgaben

P12 beweist keine vollständige offene Energiebilanz. Insbesondere fehlen:
1. ein diskreter chemischer Entropiefluss, der exakt zur Upwind-/Diffusionsdiskretisierung passt;
2. eine konsistente Behandlung der Diffusion über Reservoir-Halbzellen mit chemischen Potentialen;
3. ein mechanisches äußeres Potential und dessen diskrete Arbeitsbilanz;
4. ein Satz, der Randarbeit, Dissipation und gespeicherte Energie für alle zulässigen Zustände verknüpft.

Der nächste tragfähige Schritt ist daher nicht, das Residuum wegzudefinieren, sondern P13 als thermodynamisch kompatible Flussdiskretisierung samt mechanischem Arbeitsfunktional aufzubauen. P12 verwendet keine erzwungenen Oedometerdaten zur Kalibrierung natürlicher Synärese und beansprucht keine empirische Validierung oder PDE-Existenz.

## 7. Reproduktion

```bash
python -m unittest test_ccfsm_p12_energy_budget_audit -v
python -m unittest discover -s . -p "test_*.py" -v
```
