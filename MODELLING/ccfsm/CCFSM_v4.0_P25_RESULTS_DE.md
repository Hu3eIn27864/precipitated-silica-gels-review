# CCFSM P25 — Auswertung des numerischen Referenzlaufs

**Workflow:** [Run #295](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43670098385)  
**Commit:** `73a4292a7ebad21b92b07a8e1b7595c224990b15`  
**Status:** <badge>CI erfolgreich</badge> 273 Unit-Tests; P25-Studie und Artefakt-Upload erfolgreich.  
**Referenzzeit:** (T=10^{-2},mathrm{s}); synthetischer kleiner FV/FE-Fall, keine experimentelle Kalibrierung.

## 1. Zeitverfeinerung

Gleiches Endzeitintervall (T), jeweils 1, 2 oder 4 implizite Schritte. Fehler ist die relative (L^infty)-Abweichung zur feinsten berechneten Zeitfolge (4 Schritte), nicht zu einer exakten Lösung.

| Solver | Schritte | (Delta t) [s] | Fehler gegen 4 Schritte | Iterationen gesamt | maximales Residuum |
|---|---:|---:|---:|---:|---:|
| P22 | 1 | 0.0100 | (1.547\times10^{-8}) | 25 | (6.675\times10^{-12}) |
| P22 | 2 | 0.0050 | (5.150\times10^{-9}) | 48 | (6.705\times10^{-12}) |
| P22 | 4 | 0.0025 | 0 (Referenz) | 92 | (6.719\times10^{-12}) |
| P24 | 1 | 0.0100 | (1.549\times10^{-8}) | 2 | (4.566\times10^{-14}) |
| P24 | 2 | 0.0050 | (5.164\times10^{-9}) | 4 | (2.089\times10^{-14}) |
| P24 | 4 | 0.0025 | 0 (Referenz) | 8 | (1.421\times10^{-14}) |

Die beiden nichttrivialen Fehlerstufen fallen jeweils ungefähr um den Faktor 3. Das ist mit dem erwarteten Verhalten erster Ordnung des impliziten Eulerverfahrens vereinbar. Eine belastbare beobachtete Konvergenzordnung wird daraus noch nicht abgeleitet: Es gibt nur zwei Fehlerwerte relativ zu einer selbst berechneten Referenz; ein unabhängiger Zeitreferenzwert und zusätzliche asymptotische Stufen fehlen.

## 2. Raumverfeinerung und Solververgleich

Bei (N=1,2,4) FV-Zellen, jeweils zugeordneten axialen P19-FE-Elementen, sind beide Solver konvergiert.

| FV-Zellen | P22/P24 Zustandsabweichung | Druckabweichung | P23 relative Si-Bilanzabweichung |
|---:|---:|---:|---:|
| 1 | (6.744\times10^{-12}) | (6.664\times10^{-12}) | (8.853\times10^{-17}) |
| 2 | (6.718\times10^{-12}) | (5.612\times10^{-12}) | (1.181\times10^{-16}) |
| 4 | (6.718\times10^{-12}) | (6.346\times10^{-12}) | (3.284\times10^{-16}) |

Alle drei Raumfälle erfüllen die P23-Siliciumbilanzprüfung. Die kleinsten Inventare bleiben positiv; (	heta) bleibt im zulässigen Intervall (0<\theta\leq1). Der Solververgleich belegt die Übereinstimmung von P22 und P24 auf denselben diskreten Netzen. Er ist **kein** räumlicher Diskretisierungsfehler gegen eine exakte Lösung: Ein solcher Referenzwert bzw. eine Netzübertragungsnorm für die Lösungen verschiedener Netze ist noch nicht implementiert.

## 3. Nichtlinearer Robustheitstest

**P24, FD-Schrittweite:**

| FD-Schritt | Status | Newton-Iterationen | skaliertes Residuum |
|---:|---|---:|---:|
| (10^{-4}) | konvergiert | 2 | (2.842\times10^{-15}) |
| (10^{-6}) | konvergiert | 2 | (4.566\times10^{-14}) |
| (10^{-8}) | konvergiert | 2 | (4.718\times10^{-12}) |

Alle drei Einstellungen konvergieren. Das Residuum steigt bei sehr kleiner FD-Schrittweite an, konsistent mit zunehmender Rundungs-/Auslöschungsempfindlichkeit. Daraus folgt keine allgemeine optimale FD-Schrittweite.

**P22, Picard-Relaxation:**

| Relaxation (omega) | Status | Iterationen | Zustandsresiduum | Druckresiduum |
|---:|---|---:|---:|---:|
| 0.2 | konvergiert | 74 | (9.454\times10^{-12}) | (1.397\times10^{-12}) |
| 0.5 | konvergiert | 25 | (6.675\times10^{-12}) | (3.955\times10^{-12}) |
| 1.0 | konvergiert | 4 | (1.233\times10^{-14}) | (7.516\times10^{-12}) |

In diesem Referenzfall ist ungedämpftes Picard am schnellsten. Das ist fallbezogen und kein Beweis, dass (omega=1) für andere Zustände oder größere Zeitschritte stabil ist.

## 4. Freigabeurteil

- **Softwareverifikation:** bestanden; 273/273 Unit-Tests im CI-Lauf #295.
- **Zeitfolge:** beide Solver konvergieren; Fehlerabnahme ist mit erster Ordnung vereinbar, aber die formale Ordnungsfreigabe bleibt offen.
- **Raumfolge:** P22/P24 stimmen auf allen drei Netzen sehr eng überein; die räumliche Konvergenzordnung ist mangels netzübergreifender Referenz noch nicht bestimmt.
- **Stoffbilanz:** P23 schließt in den drei Raumfällen relativ auf (10^{-16})-Niveau.
- **Solverrobustheit:** alle getesteten FD- und Relaxationsvarianten konvergieren; kleine FD-Schritte erhöhen das Residuum, kleinere Relaxation erhöht deutlich die Iterationszahl.
- **Physikalische Validierung:** nicht erfolgt. Der Fall ist synthetisch und liefert keine neuen Materialparameter.

**P25-Status:** numerischer Harness und erster erfolgreicher Verfeinerungs-/Robustheitslauf abgeschlossen. Die vollständige Konvergenzfreigabe bleibt teilweise offen (insbesondere echte räumliche Fehlernorm, zusätzliche asymptotische Zeitstufen und anspruchsvollere gekoppelte Belastungsfälle).
