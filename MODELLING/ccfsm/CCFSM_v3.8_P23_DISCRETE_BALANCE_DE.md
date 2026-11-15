# CCFSM P23 — diskrete Stoff- und Energiebilanz des akzeptierten P22-Schritts

**Stand:** 15.11.2026  
**Ziel:** Den tatsächlich akzeptierten impliziten-Euler-Schritt aus P22 bilanzieren. P23 ist ein Audit, kein neuer Zeitschrittintegrator.

## 1. Diskrete Siliciumbilanz

Die vier Inventare (n_M,n_O,n_N,n_B) sind Si-Äquivalente pro Referenzvolumen. Für die FV-Zellweite (Delta x) gilt

[
N_{m Si}^n=Delta xsum_j(n_{M,j}^n+n_{O,j}^n+n_{N,j}^n+n_{B,j}^n).
]

Die Reaktionsstöchiometrie ((-r_1,r_1-r_2,r_2-r_3,r_3)) hebt sich in der Summe exakt auf. Interne FV-Flüsse teleskopieren. Bei positivem Fluss von links nach rechts ist daher für den akzeptierten Schritt

[
Delta N_{m Si}^{m Rand}
=Delta tleft[(J_M+J_O)_L-(J_M+J_O)_Right],
]
[
R_{m Si}=(N_{m Si}^{n+1}-N_{m Si}^{n})-
Delta N_{m Si}^{m Rand}.
]

P23 berechnet beide Seiten unabhängig aus den Zuständen und den P21-Grenzflächenflüssen des finalen, zum akzeptierten Zustand gehörenden Snapshots. Das Residuum wird nicht algebraisch auf null gesetzt. N/B sind immobil und tragen keinen Randfluss.

## 2. Energiebilanz: bewusst getrennte Ebenen

P23 berechnet die tatsächliche Differenz der P9-lokalen FV-Energie
(E_{m P9}^{n+1}-E_{m P9}^{n}) aus Anfangs- und akzeptiertem Zustand.

Zusätzlich werden aus dem finalen P19-Snapshot die mechanische FE-Energie, die Neumann-Traktionsarbeit und das Dirichlet-Reaktionsresiduum ausgegeben. **Eine mechanische Energiedifferenz ist noch nicht verfügbar**, weil P22 bislang keinen P19-Snapshot des Anfangszustands mitführt. Ebenso ist die FE-Energie (J über die gelieferten FE-Quadraturgewichte) nicht ohne Geometrie-/Querschnittsabbildung mit der FV-Energie pro Querschnittsfläche (J/m²) addierbar. P23 addiert diese Größen daher nicht.

Die P16-Kettenregelrate ist eine semidiskrete Rate und wird nicht als diskrete Energieänderung ausgegeben. Darcy-, Onsager- und Reaktionsdissipation sind damit noch nicht zu einer vollständigen globalen diskreten Energiebilanz des P21/P22-Schritts geschlossen. Es wird weder ein globales Energieresiduum noch Energie-Monotonie behauptet.

## 3. Implementierung und Verifikation

- `ccfsm_p23_discrete_balance.py`: Auditfunktion `p23_audit_accepted_step`.
- `test_ccfsm_p23_discrete_balance.py`: geschlossene und offene Siliciumbilanz, Zurückweisung nicht akzeptierter Schritte und explizite Nichtbehauptung globaler Energiebilanz.
- Voraussetzung ist ein konvergierter P22-Result-Datensatz mit akzeptiertem Zustand und finalem P21/P19-Snapshot.
- Toleranzprüfung der Stoffbilanz ist skalenbezogen; die Rohwerte und das relative Residuum werden stets zurückgegeben.

## 4. Grenzen und nächste Arbeit

P23 schließt die globale FV-Siliciumbilanz für den vom P22-Snapshot repräsentierten Schritt, sofern die akzeptierte Zustandsänderung numerisch konsistent mit den ausgegebenen Randflüssen ist. Es ist kein Nachweis der physikalischen Richtigkeit der Reaktionskinetik oder der Materialschließungen.

Für eine vollständige diskrete Energiebilanz sind als nächste technische Voraussetzungen nötig:
1. P22 muss Anfangs- und End-P19-Energie-/Arbeitsdaten mit derselben FE-Geometrie und Quadratur führen.
2. FE- und FV-Energien benötigen eine dimensionsrichtige gemeinsame Referenzmaß-Abbildung.
3. Die P21-Onsager-, Darcy-, Reaktions- und offenen Reservoirleistungen müssen entlang derselben akzeptierten diskreten Gleichung ausgewertet werden.
4. Dirichlet-Reaktionen und ihre inkrementelle Randarbeit sowie Neumann-Traktionsarbeit müssen mit konsistenter Zeitdiskretisierung eingehen.

**Status:** P23 ist ein erster diskreter Stoffbilanz-Audit und ein partieller Energiedifferenz-Audit. Kein vollständiger Energieabschluss, keine Netz-/Zeitkonvergenz und keine physikalische Validierung.
