# CCFSM v0.5 — Zweiggetrennte Sensitivitätsanalyse natürlicher Synäresekurven

**Stand:** 14.11.2026  
**Status:** explorative Reanalyse vorhandener, KI-gestützter Diagramm-Näherungsablesungen. Keine neuen Messdaten, keine unabhängige Pixel-Digitalisierung und keine physikalische Validierung.

## 1. Datenbestand und Evidenztrennung

Die vorhandene kuratierte Datei enthält 164 Punkte in 12 Reihen:

| Evidenzzweig | Punkte | Reihen |
|---|---:|---:|
| primary_exploratory | 58 | 4 |
| primary_with_local_reversals | 40 | 3 |
| sensitivity_only | 22 | 2 |
| figure_table_conflict_branch | 44 | 3 |
| **Gesamt** | **164** | **12** |

Die ersten beiden Klassen bilden die sieben primären Reihen (98 Punkte), die bereits in v0.5 verwendet wurden. Die zwei Sensitivitätsreihen (22 Punkte; Figure 8a sauer, 40/60 °C) und drei Figure-10b-Konfliktreihen (44 Punkte) wurden separat ausgewertet. Es wurden keine Druckzell-/Δp-Daten eingelesen oder mit natürlichen Reihen vermischt.

Alle 164 Werte sind als `ai_assisted_approximation` markiert. Sie sind weder Autor-Rohdaten noch pixelkalibrierte Markerpositionen. Deshalb sind AICc, RMSE und Fits nur deskriptive Diagnosewerte; es werden keine Konfidenzintervalle oder Signifikanztests abgeleitet.

## 2. Fitvergleich je Reihe

Für jede Reihe wurden unabhängig angepasst:

- Einzelexponential: (S=A[1-\exp(-t/\tau)]), zwei Parameter.
- Gestreckt exponentiell: (S=A[1-\exp(-(t/\tau)^\beta)]), drei Parameter, Suchbereich (0.3\le\beta\le3.0).

Die Amplitude wird bei gegebener Zeitkonstante analytisch minimiert; die Zeitkonstante wird eindimensional minimiert. Beim gestreckten Exponential wird zusätzlich β in einem festen Raster gesucht. Die vollständigen Kennzahlen und Randtreffer stehen in `wilhelm_kind_branch_sensitivity_2026-11-14.csv`. Reproduzierbarer Code: `ccfsm_v05_branch_sensitivity.py`.

**Primäre sieben Reihen:** Das gestreckte Exponential hat nach AICc in 4/7 Reihen den kleineren Wert, das einfache Exponential in 3/7. Das entspricht qualitativ dem früheren v0.5-Modellvergleich. Daraus folgt keine physikalische Überlegenheit einer gestreckten Kinetik: Die Reihen sind wenige, ungeprüfte Diagrammablesungen, und die residualen Fehler sind nicht unabhängig.

**Warnsignale für Überanpassung:** In der basischen Figure-8-Reihe bei 20 °C erreicht der gestreckte Fit sowohl β=0.3 als auch (A=1) als Suchgrenzen und liefert eine unplausibel große Zeitkonstante. In der sauren Figure-8a-Sensitivitätsreihe bei 40 °C liegt β=3.0 an der oberen Suchgrenze. Diese Fits sind nicht als physikalische Parameter zu verwenden. Der große AICc-Vorteil an einer Suchgrenze ist ein Diagnosehinweis auf unzureichende Form-/Zeitinformation, kein Beleg für eine reale gestreckte Kinetik.

## 3. Was die vorhandenen Kurven über die CCFSM-Aussagen sagen

### 3.1 Empirisch gestützt — aber nur deskriptiv

1. **Endschrumpfung hängt von Gelchemie und Probenkonfiguration ab.** In den Zylinderreihen steigen die primär gefitteten Amplituden der basischen Kurven mit der Temperatur ungefähr von 0.285 (20 °C) über 0.359 (40 °C) auf 0.492 (60 °C). Die sauren Zylinderwerte liegen nahe 0.19–0.20. Für Tröpfchen liegen die sauren Amplituden ungefähr bei 0.369, 0.426 und 0.471. Diese Unterschiede sind mit einer chemie- und strukturabhängigen Schrumpfkapazität vereinbar, identifizieren aber keinen bestimmten mikroskopischen Mechanismus.
2. **Eine einzige universelle Zeitkonstante passt nicht über alle Geometrien und Bedingungen.** Die Zylinder-Zeitmaßstäbe liegen in der Größenordnung von Stunden bis mehreren zehn Stunden, die Tröpfchen-Fits unter einer Stunde. Probengeometrie, Drainageweg, Randbedingungen und thermische Vorgeschichte müssen daher explizit behandelt werden.
3. **Die Temperaturantwort ist nicht universell Arrhenius-artig aus diesen Tabellen/Fits abzuleiten.** Die sauren Tröpfchen-Fits ergeben etwa 0.524, 0.696 und 0.620 h bei 20/40/60 °C; dies ist nicht monoton. Die basischen Zylinder-Fits liegen bei 41.28, 24.83 und 24.90 h; zwischen 40 und 60 °C kaum Änderung. Die sauren Zylinderwerte bei 40/60 °C sind Sensitivitätsdaten und dürfen nicht in eine definitive Temperaturregression eingehen.
4. **Figure 10b bleibt ein eigenständiger Quellenkonflikt.** Die getrennten Kurven-Fits ergeben (A\approx0.419,0.643,0.825) bei 20/40/60 °C, während die gedruckte Table 2 (A=0.30,0.39,0.51) angibt. Die Kurvenablesungen bleiben approximativ; weder Tabelle noch Abbildung wird überschrieben.

### 3.2 Nicht durch diese Daten identifiziert

- (B), (D_f), (z), Brückendichte, Relaxationsrate (k_r), Permeabilität, effektiver Modul und Kontaktwiderstand sind aus (S(t)) allein nicht separat bestimmbar.
- Die CCFSM-Zustandsgrößen (B,D_f,z,\sigma,\epsilon_r) werden in diesen Reihen nicht direkt gemessen. Eine gute Kurvenanpassung wäre daher kein Nachweis dieser Zustände.
- Die beobachtete Amplitude identifiziert im v0.3/v0.5-Ansatz nur das Produkt (A_{eff}=\eta_a q_\infty), nicht η und (q_\infty) einzeln.
- Der zweistufige CCFSM-Fit traf im korrigierten v0.5-Lauf bei allen sieben Primärkurven mindestens eine Suchgrenze. Die vorhandenen Daten trennen die zwei Raten daher nicht stabil. Das widerlegt die Modellstruktur nicht, zeigt aber fehlende Identifizierbarkeit in diesem Datensatz.

## 4. Konsequenzen für die Modellarchitektur

Die Kurven sind konsistent mit einem phänomenologischen Bild aus (i) einer chemie-/strukturabhängigen Schrumpfkapazität und (ii) einem geometrie-/transportabhängigen Zeitmaßstab. Sie beweisen jedoch nicht die postulierte Kausalkette.

Für eine belastbare CCFSM-Prüfung müssen die latenten Zustände mit unabhängigen Messungen verknüpft werden:

- (B): quantitative Siloxan-Brücken-/Kondensationsinformation, z. B. geeignete spektroskopische oder chemische Messgrößen;
- (D_f,z): zeitaufgelöste Strukturmessung (SAXS/SANS oder geeignete Bildgebung), wobei (z) nicht automatisch aus (D_f) folgt;
- κ_eff: Permeabilität bzw. Poren-/Porenhals-Konnektivität als Funktion der Alterung;
- (K_eff): unabhängige mechanische Messung;
- Temperatur: tatsächliche Gelinnentemperatur und dokumentierte thermische Vorgeschichte;
- Geometrie/Rand: definierte Drainageflächen und Kontakt-/Grenzflächenbedingungen.

Erst dann ist die Kette (B,D_f,z\rightarrow\text{Porenstruktur/}\kappa_{eff}\rightarrow k_h\rightarrow S(t)) quantitativ prüfbar. Bis dahin dürfen keine Potenzgesetze (\kappa(D_f)) oder (K(D_f)) als empirisch bestätigt ausgegeben werden.

## 5. Entscheidung und nächster Schritt

**Entscheidung:** CCFSM bleibt als mechanistisch motivierte, aber nur teilweise identifizierte Modellhypothese bestehen. Die vorhandenen natürlichen Kurven stützen die Notwendigkeit chemie-, temperatur-, geometrie- und transportabhängiger Beiträge. Sie validieren weder die inneren Zustandsvariablen noch die gekoppelten Stoffgesetze.

Der nächste wissenschaftlich sinnvolle Schritt ist nicht ein weiterer freier Mehrparameterfit. Vorrang haben (1) manuelle, pixelkalibrierte Prüfung der Originalmarker, insbesondere Figure 8a 40/60 °C und Figure 10b 20/40/60 °C, und (2) ein experimenteller Minimaldatensatz mit zeitaufgelöster Schrumpfung plus mindestens einer unabhängigen Struktur- und einer Transport-/Mechanikmessung.
