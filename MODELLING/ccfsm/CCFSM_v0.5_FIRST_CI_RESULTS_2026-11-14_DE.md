# CCFSM v0.5 — erster CI-Lauf (14.11.2026)

## Verifikation

- GitHub Actions Run: 43595413689
- Commit der ausgeführten Pipeline: 6f0a5d8f25424c1c91f8358fc6ea727c75d22045
- Ergebnis: erfolgreich
- CCFSM-Tests: 72/72 bestanden
- Natürliche Kurven eingelesen: 14 (7 sauer, 7 basisch)
- Modellanpassungen: 42 (drei Modellfamilien je Kurve)
- Ergebnisartefakt: ccfsm-v0.5-natural-syneresis-results (30 Tage Aufbewahrung)

## Erste aggregierte Ergebnisse

| Modell | AICc-Sieger von 14 Kurven | Median Holdout-RMSE |
|---|---:|---:|
| Exponentiell | 4 | 0,02107 |
| Gestreckt exponentiell | 10 | 0,02983 |
| Zweistufiges CCFSM | 0 | 0,01984 |

Der AICc-Sieger ist je Kurve das Modell mit dem kleinsten AICc auf dem vollständigen Kurvenverlauf. Der Holdout-RMSE wird dagegen auf den letzten 20 % der Zeitpunkte berechnet, nachdem auf den ersten 80 % angepasst wurde. Deshalb messen beide Spalten unterschiedliche Dinge und dürfen nicht zu einer einzigen Rangfolge vermischt werden.

## Vorläufige Interpretation

1. Auf dem vollständigen Verlauf gewinnt das gestreckte Exponentialmodell nach AICc bei 10 von 14 Kurven. Das spricht dafür, dass die einfache Ein-Zeitkonstanten-Form die Kurvenform häufig nicht vollständig beschreibt.
2. Das zweistufige CCFSM gewinnt in diesem AICc-Vergleich keine Kurve. Es hat jedoch den kleinsten aggregierten Median des zeitlichen Holdout-RMSE. Das ist ein interessanter Hinweis auf mögliche Extrapolationsstabilität, aber noch kein Nachweis einer physikalisch korrekten Zweistufenmechanik.
3. Die Differenz der Holdout-RMSE-Werte ist klein und sollte kurvenweise sowie mit Blick auf Randparameter und Residuen geprüft werden.
4. Da die Eingaben digitalisierte, korrelierte und teils überlagerte Figurenspuren sind, sind die üblichen AICc-Stichprobenannahmen und statistischen Signifikanzdeutungen nicht erfüllt. Die Kennzahlen sind zunächst deskriptiv.

## Konsequenz für die nächste Modelliteration

Nicht sofort zusätzliche Parameter in CCFSM aufnehmen. Zuerst sind die kurvenweisen Fit-/Holdout-Tabellen und Residuen zu untersuchen, insbesondere:
- welche Reihen die CCFSM-Zweistufenform systematisch verfehlt;
- ob deren Raten an Suchgrenzen liegen oder praktisch zusammenfallen;
- ob die Holdout-Vorteile des CCFSM von einzelnen Reihen getragen werden;
- ob die Abweichungen durch die sichtbare Mess-/Modellüberlagerung erklärbar sein könnten.

Eine unabhängige Validierung an neuen Gelchargen, Rezepturen oder gemessenen Struktur-/Permeabilitätsdaten liegt mit diesem Lauf nicht vor. Erzwungene Synärese wurde nicht verwendet.
