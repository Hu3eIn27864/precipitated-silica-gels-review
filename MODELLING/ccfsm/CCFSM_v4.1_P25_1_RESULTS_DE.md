# CCFSM P25.1 — Ergebnisse der Cross-Mesh-Verfeinerung

**Workflow:** [Run #308](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43670669824)  
**Commit:** `b1f629f2cf2d5c9c23bd055b1de8f4981dd753e9`  
**Status:** CI erfolgreich; 278 Unit-Tests bestanden; P25- und P25.1-Studien sowie beide Ergebnisartefakte erfolgreich hochgeladen. P25.1-Artefakt: [CSV/JSON-Ergebnisse](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43670669824/artifacts/14143648589).  
**Fall:** synthetisch, (T=10^{-2},s), Reservoirdruck (10^5,Pa); keine experimentelle Kalibrierung oder physikalische Validierung.

## 1. Zeitverfeinerung

Gleiches Endzeitintervall auf (N=4) Zellen; Fehler relativ zur 16-Schritt-Lösung.

| Solver | Schritte | relativer Fehler (L^infty) | Iterationen gesamt | maximales Residuum |
|---|---:|---:|---:|---:|
| P22 | 1 | (1.880\times10^{-8}) | 25 | (6.10\times10^{-12}) |
| P22 | 2 | (8.745\times10^{-9}) | 48 | (6.13\times10^{-12}) |
| P22 | 4 | (3.725\times10^{-9}) | 92 | (6.14\times10^{-12}) |
| P22 | 8 | (1.226\times10^{-9}) | 176 | (6.15\times10^{-12}) |
| P22 | 16 | 0 (Referenz) | 336 | (6.15\times10^{-12}) |
| P24 | 1 | (1.885\times10^{-8}) | 2 | (3.85\times10^{-14}) |
| P24 | 2 | (8.800\times10^{-9}) | 4 | (3.19\times10^{-14}) |
| P24 | 4 | (3.772\times10^{-9}) | 8 | (1.18\times10^{-14}) |
| P24 | 8 | (1.257\times10^{-9}) | 16 | (9.70\times10^{-15}) |
| P24 | 16 | 0 (Referenz) | 32 | (4.17\times10^{-15}) |

Die paarweisen Diagnose-Raten liegen je nach Intervall ungefähr zwischen 1.10 und 1.60. Die Fehler sinken monoton, aber die Rate ist noch nicht stabil genug, um eine formale Ordnung zu beanspruchen. Die 16-Schritt-Lösung ist eine numerische Referenz, keine exakte Lösung.

## 2. Räumliche Cross-Mesh-Fehler

Die Lösungen der Netze (N=1,2,4) werden volumen-erhaltend auf (N=8) restringiert. Angegeben ist die relative (L^2)-Norm gegen diese Referenz.

| Solver | Zellen | Zustandsfehler (L^2) | Druckfehler (L^2) | Rate Zustand / Druck |
|---|---:|---:|---:|---:|
| P22 | 1 | (1.560\times10^{-7}) | (1.352\times10^{-4}) | 2.13 / 2.22 |
| P22 | 2 | (3.562\times10^{-8}) | (2.905\times10^{-5}) | 1.88 / 2.30 |
| P22 | 4 | (9.697\times10^{-9}) | (5.916\times10^{-6}) | nicht auswertbar* |
| P22 | 8 | 0 (Referenz) | 0 (Referenz) | — |
| P24 | 1 | (1.560\times10^{-7}) | (1.352\times10^{-4}) | 2.13 / 2.22 |
| P24 | 2 | (3.562\times10^{-8}) | (2.905\times10^{-5}) | 1.88 / 2.30 |
| P24 | 4 | (9.697\times10^{-9}) | (5.916\times10^{-6}) | nicht auswertbar* |
| P24 | 8 | 0 (Referenz) | 0 (Referenz) | — |

*Die Rate zwischen (N=4) und (N=8) wird nicht berechnet, da der Fehler der Referenzlösung definitionsgemäß null ist.

Die ersten beiden Raumverfeinerungsintervalle zeigen ungefähr quadratische Abnahme der Fehler. Das ist ein vielversprechender numerischer Befund für diesen Testfall, aber noch kein Konvergenzbeweis: Die Referenz ist selbst diskret, und nur zwei unabhängige Rateintervalle sind vorhanden.

## 3. Druck-/Darcy-Gradient und Stoffbilanz

| Zellen | Druckspanne [Pa] | maximaler Darcy-Fluss [m/s] | relative P23-Si-Bilanz |
|---:|---:|---:|---:|
| 1 | 0 | (5.34\times10^{-8}) | P22 (3.21\times10^{-42}), P24 (5.13\times10^{-15}) |
| 2 | (7.64\times10^4) | (2.60\times10^{-7}) | P22 (4.39\times10^{-17}), P24 (5.34\times10^{-15}) |
| 4 | (1.15\times10^5) | (6.72\times10^{-7}) | P22 (1.83\times10^{-16}), P24 (3.41\times10^{-15}) |
| 8 | (1.34\times10^5) | (1.50\times10^{-6}) | P22 (3.27\times10^{-16}), P24 (9.39\times10^{-15}) |

Der (N=1)-Fall hat naturgemäß keine interne Zell-zu-Zell-Druckspanne; dort bleibt nur die Reservoir-/Randflusswirkung. Ab (N=2) ist der interne Druckgradient deutlich ungleich null und wächst in der Verfeinerungsfolge. Der maximale Darcy-Fluss ist in allen Fällen ungleich null. Alle geprüften P23-Siliciumbilanzen sind innerhalb der Audit-Toleranz verifiziert; Fluidkapazität und Inventare bleiben admissibel.

## 4. P22/P24 auf identischen Netzen

Über (N=1,2,4,8) liegt die relative Zustandsabweichung der Solver zwischen (6.08\times10^{-12}) und (6.15\times10^{-12}); die relative Druckabweichung zwischen (1.83\times10^{-12}) und (2.59\times10^{-12}). P22 benötigt 25 Iterationen, P24 2 Newton-Iterationen pro Einzelschritt in diesen Referenzfällen.

## 5. Freigabeurteil

- **Softwareverifikation:** CI #306 erfolgreich; 278/278 Tests.
- **Konservative Restriktion:** Integral-Erhaltung auf verschachtelten gleichmäßigen FV-Netzen durch Blockmittelung; Regressionstests bestanden.
- **Zeitfolge:** monotone Fehlerabnahme für P22/P24; beobachtete Rate noch nicht stabil genug für eine formale Ordnungsaussage.
- **Raumfolge:** Fehler sinken deutlich; die ersten beiden paarweisen Raten liegen nahe 2.0. Aussage bleibt diagnostisch, weil die (N=8)-Lösung keine exakte Referenz ist.
- **Druckkopplung:** interner Druckgradient und Darcy-Fluss sind für (N\geq2) tatsächlich aktiviert.
- **Stoffbilanz:** P23-Siliciumbilanz für alle erfolgreichen Fälle verifiziert.
- **Physikalische Validierung:** nicht erfolgt; synthetischer Belastungsfall, keine Materialparameter werden daraus abgeleitet.

**P25.1-Status:** Teilfreigabe für Cross-Mesh-Softwareverifikation und den getesteten Druck-/Darcy-Gradientfall. Für eine stärkere Konvergenzaussage benötigen wir eine unabhängige/manufactured solution, weitere Netzstufen und idealerweise höherwertige FE-Approximationen. P26 bleibt zuständig für allgemeine konservative FE/FV-Projektion auf nicht deckungsgleichen Netzen.
