# Manuskript 1 — synthetischer Benchmark zur praktischen Identifizierbarkeit

**Stand:** 15.11.2026  
**Status:** reproduzierbare synthetische Demonstration; keine experimentelle Auswertung

## 1. Ziel

Der Benchmark illustriert, dass strukturelle Identifizierbarkeit nicht automatisch gute Parameterschätzungen aus endlichen Daten bedeutet. Er variiert (i) den Abstand der beiden Raten und (ii) Beobachtungsfenster sowie Abtastdichte. Die Messfehler sind synthetisch und additiv gaußverteilt.

Das Skript liegt unter `MANUSCRIPT_01_PRACTICAL_IDENTIFIABILITY_BENCHMARK.py`. Es benötigt NumPy und SciPy. Die Zufallsfolge ist mit Seed `20261115` fixiert.

## 2. Versuchsaufbau

In allen Fällen gilt der Nullstart und der exakte Zweiraten-Ausgang

\[
S(t)=C\left[1-\frac{k_h e^{-k_nt}-k_n e^{-k_ht}}{k_h-k_n}\right],
\]

mit dem stetigen Gleichratenlimit. Der Endwert ist \(C=0.4\). Pro Fall werden 100 unabhängige synthetische Messreihen erzeugt. Jede Beobachtung erhält unabhängiges additives Rauschen mit Standardabweichung \(\sigma=0.002\) in den Einheiten von \(S\). Geschätzt werden \(C\) und die beiden positiven Raten durch Multi-Start-Nonlinear-Least-Squares in logarithmierten Parametern. Die ausgegebenen Raten werden sortiert; physikalische Labels werden nicht geschätzt.

| Fall | Wahre Raten | Messzeiten | Messpunkte |
|---|---:|---:|---:|
| Nahe Raten, dicht/lang | 0.100 und 0.105 | 0–100 | 100 |
| Nahe Raten, grob/kurz | 0.100 und 0.105 | 0–15 | 12 |
| Getrennte Raten, dicht/lang | 0.030 und 0.300 | 0–180 | 100 |
| Getrennte Raten, grob/kurz | 0.030 und 0.300 | 0–15 | 12 |

Die Raten haben die inverse Einheit der hier frei gewählten Zeiteinheit. Die Werte sind reine synthetische Testparameter und keine aus Silica-Experimenten abgeleiteten Größen.

## 3. Ergebnisse

Die folgende Tabelle zeigt den Median des absoluten relativen Schätzfehlers über 100 Wiederholungen sowie das 90%-Quantil dieses Fehlers für die beiden sortierten Raten.

| Fall | Medianfehler \(C\) | Medianfehler langsame Rate | Medianfehler schnelle Rate | 90%-Quantil langsame Rate | 90%-Quantil schnelle Rate |
|---|---:|---:|---:|---:|---:|
| Nahe Raten, dicht/lang | 0.065 % | 2.69 % | 2.80 % | 9.14 % | 11.80 % |
| Nahe Raten, grob/kurz | 9.46 % | 15.81 % | 16.74 % | 85.93 % | 155.41 % |
| Getrennte Raten, dicht/lang | 0.054 % | 0.34 % | 2.35 % | 0.98 % | 6.07 % |
| Getrennte Raten, grob/kurz | 44.50 % | 84.12 % | 39.36 % | 308.28 % | 61.33 % |

## 4. Interpretation

1. Bei dichtem und langem Beobachtungsplan werden die gut getrennten Raten in diesem synthetischen Beispiel vergleichsweise zuverlässig rekonstruiert.
2. Bei nur 12 Messpunkten in einem kurzen Zeitfenster werden Endwert und Raten deutlich unsicherer; insbesondere kann die langsame Dynamik unzureichend erfasst sein.
3. Nahe beieinanderliegende Raten sind auch bei dichtem/langem Messplan schwieriger zu trennen als deutlich verschiedene Raten. Das entspricht der kleinen Diskriminante \((k_n-k_h)^2\).
4. Das grobe/kurze Szenario ist in diesem Beispiel für eine belastbare Zweiraten-Schätzung ungeeignet. Die hohen 90%-Quantile zeigen, dass einzelne Wiederholungen sehr große Schätzfehler aufweisen.

Die konkreten Zahlen hängen von Rauschmodell, Rauschstärke, Zeitplan, Startwerten, Optimierer und Parameterschranken ab. Sie sind kein allgemeiner Fehlergrenzwert und keine Aussage über vorhandene Silica-Daten.

## 5. Grenzen und nächste Verbesserung

- Der Benchmark verwendet exakt simulierte Daten aus derselben Modellklasse, die anschließend angepasst wird („inverse crime“). Modellfehlanpassung wird nicht untersucht.
- Es gibt keine Messoffsets, korrelierten Fehler, Heteroskedastizität oder Unsicherheit des Zeitnullpunkts.
- Die Multi-Start-Suche ist eine praktische Optimierungsstrategie, kein Beweis globaler Optimalität.
- Die Auswertung verwendet keine Profil-Likelihood-Konfidenzintervalle und keine externe Validierung.
- Die synthetische Messgröße \(S\) ist dimensionslos skaliert; die Zahlen sind nicht als experimentelle Volumenmessung zu lesen.

Als nächster methodischer Schritt sind Profil-Likelihood bzw. Bootstrap-Intervalle, Messoffset- und Modellfehlanpassungs-Szenarien sowie ein Vergleich mit einer Einraten-Referenz sinnvoll. Erst danach sollte ein konkreter Messplan für reale Daten empfohlen werden.

**Claim–Evidence-Einstufung:** Die Tabelle ist eine reproduzierbare numerische Illustration unter expliziten synthetischen Annahmen. Sie ist weder empirische Evidenz noch eine Validierung des CCFSM.
