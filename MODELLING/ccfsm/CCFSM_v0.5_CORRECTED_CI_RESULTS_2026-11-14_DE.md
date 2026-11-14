# CCFSM v0.5 — korrigierter CI-Lauf (14.11.2026)

## Verifikation und Datenabgrenzung

- GitHub Actions Run: 43595635203
- Pipeline-Commit: 8ce6c202e725bf4e4bc80285530551fa3799d44d
- Ergebnis: erfolgreich; **73/73 CCFSM-Tests bestanden**.
- Natürliche Reihen im explorativen Fit: 7 kuratierte Näherungskurven aus Wilhelm & Kind (2015), Figures 8 und 10.
- Fits: 21 (drei Modellfamilien je Kurve).
- Separater Audit: 21 Reihen in DATA/Raw/kurvendigitalisierung.csv haben Δp-Druckbedingungen; 0 davon wurden als natürliche Kalibrierkurven verwendet.
- Ergebnisartefakt: ccfsm-v0.5-natural-syneresis-results, GitHub Actions Artifact ID 14113634977.

Die sieben natürlichen Reihen sind KI-gestützte ungeprüfte Näherungsablesungen. Sie sind nicht pixelkalibriert und keine Autor-Rohdaten. Diese Ergebnisse sind daher ausdrücklich explorativ.

## Modellvergleich

| Modell | AICc-Sieger von 7 | Randtreffer von 7 Fits | Median Holdout-RMSE |
|---|---:|---:|---:|
| Exponentiell | 3 | 0 | 0,04207 |
| Gestreckt exponentiell | 4 | 0 | 0,01755 |
| Zweistufiges CCFSM | 0 | 7 | 0,04207 |

Der Holdout besteht aus den letzten 20 % der Zeitpunkte jeder Kurve; die ersten 80 % werden zum Fit verwendet. Dies ist keine unabhängige Validierung an neuen Gelchargen oder Rezepturen. Bei 9–21 Punkten je Kurve ist die Holdout-Stichprobe klein.

## Identifizierbarkeit

Der zweistufige CCFSM-Fit erreicht bei **allen sieben Kurven mindestens eine Suchgrenze**. Die geschätzten Ratenpaare sind deshalb nicht als physikalische Koeffizienten zu interpretieren. Die Kurven enthalten offenbar nicht genügend verlässliche Information, um die beiden Zeitskalen stabil zu trennen. Außerdem identifiziert die Schrumpfungskurve nur A_eff = eta_a*q_inf, nicht die beiden Faktoren separat.

Das ist kein Gegenbeweis gegen die zweistufige Modellstruktur. Es ist ein negatives Identifizierbarkeitsergebnis für diese kleine, ungeprüfte Näherungsdatenbasis.

## Konsequenz

1. Keine weiteren freien CCFSM-Parameter an diese sieben Kurven anpassen.
2. Die Originalmarker von Figures 8 und 10 pixelkalibriert und unabhängig prüfen; insbesondere Fehlerbalken, Mittelwerte und Modelllinien trennen.
3. Die publizierten Tabellenparameter aus Tables 1 und 2 als eigene Evidenzklasse behalten.
4. Die 21 Δp-Reihen aus DATA/Raw/kurvendigitalisierung.csv separat als erzwungene Synärese behandeln. Sie dürfen höchstens in einer späteren, separaten Druckzell-/Mechanikprüfung verwendet werden.
5. Eine echte natürliche CCFSM-Validierung benötigt zusätzliche unabhängige Struktur-, Permeabilitäts- oder Porenflüssigkeitsmessungen.

Die korrigierte Pipeline und der frühere Provenienzfehler sind im Repository versioniert. Die erste, falsch klassifizierte CI-Zusammenfassung bleibt als zurückgezogenes Auditprotokoll erhalten.
