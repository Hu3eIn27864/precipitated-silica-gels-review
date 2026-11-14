# CCFSM v0.5 — Kalibrierungs- und Modellvergleichspipeline

## Ziel und Geltungsbereich

v0.5 wertet die vorhandene Datei DATA/Raw/kurvendigitalisierung.csv aus. Berücksichtigt werden ausschließlich die sieben sauren und sieben basischen natürlichen, mechanisch unbelasteten Synäresekurven. Die sieben Reihen des Panels enforced_syneresis_20C werden vollständig ausgeschlossen.

Die digitalisierten Kurven sind sichtbare Figurenspuren; Mess- und Modelllinien können teilweise untrennbar überlagert sein. Sie sind weder Autor-Rohdaten noch unabhängige experimentelle Replikate. Die Zahl der Kurvenpunkte darf nicht als Stichprobengröße unabhängiger Experimente interpretiert werden.

## Modellfamilien

1. Exponentiell: S(t)=A[1-exp(-t/tau)] (zwei Parameter).
2. Gestreckt exponentiell: S(t)=A[1-exp(-(t/tau)^n)] (drei Parameter).
3. Zweistufige CCFSM-Antwort:

S(t)=A_eff[1-(k_f exp(-k_s t)-k_s exp(-k_f t))/(k_f-k_s)].

Für k_s=k_f=k gilt der stetige Grenzfall S(t)=A_eff[1-(1+kt)exp(-kt)].

Im zweistufigen Output ist A_eff=eta_a*q_inf. Aus einer einzelnen Schrumpfungskurve lassen sich eta_a und q_inf nicht separat bestimmen. Auch die beiden Raten sind nur als ungeordnetes Paar identifizierbar; die Sortierung in langsam/schnell weist ihnen keine chemische oder hydraulische Bedeutung zu.

## Schätz- und Vergleichsverfahren

- Die Amplitude wird für jedes Parameterset analytisch durch beschränkte kleinste Quadrate auf [0,1] profiliert.
- Positive Zeitparameter werden logarithmisch gesucht; zweidimensionale Fits verwenden ein deterministisches Gitter mit anschließender Koordinatensuche.
- Berichtet werden RMSE und AICc als deskriptive Anpassungsmaße.
- Chronologische Prüfung: erste 80 % der Zeitpunkte zum Fit, letzte 20 % als Holdout. Das prüft zeitliche Extrapolation innerhalb derselben Kurve, ist aber keine unabhängige Validierung an neuen Rezepturen oder Chargen.
- Parameter an Suchgrenzen werden mit boundary_hit markiert und sind nicht als belastbare Schätzungen zu verwenden.

## Unsicherheit und Identifizierbarkeit

Es werden bewusst keine gewöhnlichen punktweisen Konfidenzintervalle und kein i.i.d.-Bootstrap aus den Kurvenpunkten berechnet. Das wäre angesichts korrelierter Digitalisierungspunkte und der Mess-/Modellüberlagerung nicht gerechtfertigt. AICc und Holdout-RMSE sind Vergleichsdiagnostik, aber ihre üblichen probabilistischen Interpretationen sind eingeschränkt.

Die Seriennamen und Bedingungstexte werden unverändert übernommen. Aus diesen Kurven allein wird weder eine Arrhenius-Aktivierungsenergie noch ein kausales pH-/Konzentrationsgesetz abgeleitet. Dafür sind standardisierte Versuchsmetadaten und unabhängige Messgrößen nötig.

## Ausführung

Vom Repository-Root:

    python MODELLING/ccfsm/ccfsm_v05_calibration.py --input DATA/Raw/kurvendigitalisierung.csv --output-dir MODELLING/ccfsm/results_v0.5
    python -m unittest discover -s MODELLING/ccfsm -p 'test_*.py' -v

Erzeugte Dateien:
- ccfsm_v05_curve_fits.csv — Parameterschätzungen pro Kurve und Modell.
- ccfsm_v05_model_comparison.csv — AICc-, RMSE- und zeitliche Holdout-Vergleiche.
- ccfsm_v05_predictions_residuals.csv — Kurvenvorhersagen und Residuen.
- ccfsm_v05_curve_winners.csv — AICc-bester Modelltyp je Kurve.
- CCFSM_v0.5_CALIBRATION_REPORT_DE.md — automatisch erzeugter Kurzbericht.

GitHub Actions führt die Auswertung auf der Repository-Datendatei aus und stellt die Ergebnisdateien als CI-Artefakt bereit. Generierte Resultate bleiben damit von den Quelldaten getrennt.

## Aussagegrenze

v0.5 ist eine reproduzierbare Kurvenvergleichs- und Identifizierbarkeitspipeline. Ein guter Fit belegt weder die vollständige chemische Kinetik noch die hydraulische Konstitutivgleichung des CCFSM. Die physikalische Zuordnung der Raten verlangt unabhängige Struktur-, Permeabilitäts-, Temperatur- und/oder Flüssigkeitsabflussmessungen.
