# Leave-one-out-Sensitivitätsanalyse der KI-gestützten Kurvenablesungen

## Ziel und Datenstatus

Für jede der 12 Reihen wurde jeder Punkt genau einmal entfernt und das Einzelexponentialmodell erneut angepasst. Insgesamt entstanden 164 Leave-one-out-(LOO)-Fits. Die Eingabepunkte bleiben KI-gestützte, ungeprüfte Diagrammablesungen; diese Analyse quantifiziert nur, wie stark die Fitparameter auf einzelne übermittelte Punkte reagieren.

## Verfahren

- Baseline: Fit aller Punkte einer Reihe mit \(S(t)=A[1-\exp(-t/\tau)]\).
- LOO: jeweils genau einen Punkt entfernen, übrige Punkte unverändert fitten.
- Sensitivitätsbereich: Minimum und Maximum der 12/13/… LOO-Schätzungen je Parameter.
- Einflussreichster Punkt für \(\tau\): Punkt, dessen Entfernung die größte absolute relative Änderung von \(\tau\) gegenüber dem Baseline-Fit verursacht.
- Keine Gewichtung, keine Punktebereinigung und keine Unsicherheitsintervalle.

Ein LOO-Bereich ist **kein Konfidenzintervall**. Er misst weder die systematische Ableseunsicherheit noch die Streuung unabhängiger Proben. Der Nullpunkt (t=0, S=0) trägt bei dieser Modellform definitionsgemäß keinen Residualbeitrag; seine Entfernung verändert die Fits nicht.

## Ergebnisse

| Reihe | Baseline \(\tau\) (h) | LOO-Bereich \(\tau\) (h) | Spannweite relativ zur Baseline | Einflussreichster Punkt (t; S) |
|---|---:|---:|---:|---:|
| 8a sauer 20 °C | 11.12 | 8.69–16.65 | 71.6 % | (6 h; 0.10) |
| 8a sauer 40 °C | 8.93 | 8.02–9.55 | 17.2 % | (22 h; 0.18) |
| 8a sauer 60 °C | 8.24 | 7.95–8.69 | 9.1 % | (22 h; 0.19) |
| 8b basisch 20 °C | 41.28 | 34.66–56.78 | 53.6 % | (25 h; 0.18) |
| 8b basisch 40 °C | 24.83 | 22.33–25.78 | 13.9 % | (25 h; 0.22) |
| 8b basisch 60 °C | 24.90 | 22.32–28.53 | 24.9 % | (25 h; 0.33) |
| 10a sauer 20 °C | 0.524 | 0.495–0.541 | 8.7 % | (0.30 h; 0.13) |
| 10a sauer 40 °C | 0.696 | 0.656–0.736 | 11.5 % | (6.8 h; 0.49) |
| 10a sauer 60 °C | 0.620 | 0.609–0.647 | 6.1 % | (1.0 h; 0.42) |
| 10b basisch 20 °C | 0.726 | 0.644–0.774 | 18.0 % | (5.3 h; 0.51) |
| 10b basisch 40 °C | 0.683 | 0.654–0.709 | 8.1 % | (0.30 h; 0.18) |
| 10b basisch 60 °C | 1.118 | 1.022–1.210 | 16.8 % | (4.4 h; 0.86) |

Die prozentuale Spannweite ist \(100(\tau_\max-\tau_\min)/\tau_\mathrm{baseline}\), also kein symmetrischer Fehlerbalken.

## Befunde

### 1. Zeitkonstanten der Zylinderreihen sind teils punktdominiert

Figure 8a bei 20 °C ist besonders empfindlich: Entfernen des Punktes bei 6 h und \(S=0.10\) verschiebt \(\tau\) um rund +49.8 %. Bei Figure 8b/20 °C führt das Entfernen des ersten Nichtnullpunkts bei 25 h und \(S=0.18\) zu rund +37.6 %. Für Figure 8b/60 °C liegt die maximale Einzelpunktwirkung bei rund 14.6 %.

Diese Ergebnisse unterstreichen, dass frühe Kurvenpunkte die Zeitskala stark beeinflussen. Sie machen zugleich deutlich, dass die aus einer KI-Ablesung stammenden frühen Punkte vor einer quantitativen Interpretation geprüft werden müssen.

### 2. Tröpfchenreihen sind gegenüber einzelnen Punkten robuster

Für Figure 10a liegen die LOO-Spannweiten der Zeitkonstante bei etwa 6–12 %. Figure 10b zeigt etwa 8–18 %. Das bedeutet nur, dass kein einzelner Punkt allein den Fit dominiert. Ein systematischer Ablesefehler einer ganzen Kurve oder eine falsche Symbolzuordnung wird durch LOO nicht erkannt.

### 3. Figure 10b-Amplitudenwiderspruch bleibt bestehen

Auch nach Weglassen jeweils eines Punktes bleiben die minimalen LOO-Amplituden oberhalb der publizierten Werte:
- 20 °C: mindestens ca. 0.399 gegenüber publiziert 0.30;
- 40 °C: mindestens ca. 0.638 gegenüber publiziert 0.39;
- 60 °C: mindestens ca. 0.788 gegenüber publiziert 0.51.

Der systematische Widerspruch ist somit nicht durch einen einzelnen späten Ausreißer erklärbar. Plausible Ursachen bleiben eine systematische Kurven-/Symbolverwechslung, eine fehlerhafte Datenübertragung oder ein Missverständnis zwischen publiziertem Fitparameter und den abgelesenen Punkten. LOO kann diese Möglichkeiten nicht unterscheiden.

## Grenzen

- Punkte sind keine unabhängigen Replikate; LOO ersetzt keine Replikatstatistik.
- Es gibt keine Punkt-für-Punkt-Ableseunsicherheit und keine Fehlerbalkeninformation.
- Systematische Verzerrungen und falsche Kurvenzuordnungen bleiben bei LOO erhalten.
- \(A\) und \(\tau\) sind empirische Kurvenparameter, keine direkte Messung von Permeabilität, Diffusivität oder Reaktionskinetik.
- Die LOO-Bereiche dürfen nicht als Parameter-Konfidenzintervalle publiziert werden.

## Dateien und Reproduzierbarkeit

- Skript: `MODELLING/transport_model/leave_one_out_wilhelm_kind.py`
- Übersicht: `LITERATURE/wilhelm_kind_leave_one_out_summary.csv`
- Alle 164 Einzel-Fits: `LITERATURE/wilhelm_kind_leave_one_out_detail.csv`
- Eingabedaten: `LITERATURE/wilhelm_kind_approximate_measurement_points.csv`

Ausführung aus dem Verzeichnis `MODELLING/transport_model`:

```bash
python leave_one_out_wilhelm_kind.py \
  --input ../../LITERATURE/wilhelm_kind_approximate_measurement_points.csv \
  --summary-output ../../LITERATURE/wilhelm_kind_leave_one_out_summary.csv \
  --detail-output ../../LITERATURE/wilhelm_kind_leave_one_out_detail.csv
```

**Fazit:** LOO identifiziert einzelne punktdominierte Zeitkonstanten (insbesondere Figure 8a/20 °C und Figure 8b/20 °C), zeigt aber zugleich, dass der Figure-10b-Amplitudenwiderspruch über einzelne Punktentfernungen hinaus bestehen bleibt. Die Originalgrafikprüfung bleibt daher die nächste Validierungsstufe.
