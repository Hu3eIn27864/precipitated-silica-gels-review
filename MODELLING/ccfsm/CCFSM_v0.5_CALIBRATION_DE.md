# CCFSM v0.5 — explorative Auswertung natürlicher Synäresekurven

## Korrigierte Datenprovenienz

Die erste v0.5-CI-Fassung verwendete fälschlich die 14 sauren/basischen Reihen aus DATA/Raw/kurvendigitalisierung.csv als natürliche Synärese. Diese Reihen tragen jedoch Bedingungen Δp=... bar und gehören zur Druckzellenmessung der erzwungenen Synärese (Wilhelm & Kind 2015, Figure 12/Table 3; KIT-Dissertation, Abschnitt 5.2). Die erste Ergebniszusammenfassung ist deshalb als natürliche Kalibrierung zurückgezogen. Sie darf nicht für CCFSM-Aussagen über natürliche Synärese zitiert werden.

Die korrigierte Pipeline verwendet ausschließlich die kuratierten primären Reihen aus LITERATURE/wilhelm_kind_approximate_measurement_points_curated.csv. Das sind sieben natürliche Reihen aus Figures 8 und 10:
- Figure 8a: sauer, 20 °C (Zylinder)
- Figure 8b: basisch, 20/40/60 °C (Zylinder)
- Figure 10a: sauer, 20/40/60 °C (Tröpfchen)

Die Daten sind KI-gestützte ungeprüfte Näherungsablesungen, nicht pixelkalibrierte Originalmarker und nicht Autor-Rohdaten. 22 sensitivity_only-Punkte und 44 figure_table_conflict_branch-Punkte bleiben ausgeschlossen. Lokale Reversals im freigegebenen primären Zweig werden nicht geglättet oder gelöscht.

Die Datei DATA/Raw/kurvendigitalisierung.csv wird nur als Provenienz-Audit eingelesen. Die 21 Reihen werden als Druckzell-/erzwungene Synärese klassifiziert und vollständig aus natürlichen Fits ausgeschlossen.

## Modellfamilien

1. Exponentiell: S(t)=A[1-exp(-t/tau)].
2. Gestreckt exponentiell: S(t)=A[1-exp(-(t/tau)^n)].
3. Zweistufige CCFSM-Antwort:

S(t)=A_eff[1-(k_f exp(-k_s t)-k_s exp(-k_f t))/(k_f-k_s)].

Für k_s=k_f=k gilt S(t)=A_eff[1-(1+kt)exp(-kt)].

A_eff=eta_a*q_inf. Aus einer einzelnen Schrumpfungskurve sind eta_a und q_inf nicht getrennt identifizierbar. Das Ratenpaar ist ungeordnet; die Sortierung langsam/schnell begründet keine chemische oder hydraulische Zuordnung.

## Schätzung und Vergleich

- Die Amplitude wird je Parameterset analytisch durch beschränkte kleinste Quadrate auf [0,1] profiliert.
- Positive Zeitparameter werden logarithmisch gesucht; zweidimensionale Fits verwenden ein deterministisches Gitter und anschließende Koordinatensuche.
- Berichtet werden RMSE, AICc und ein chronologischer Holdout (erste 80 % der Zeitpunkte Fit, letzte 20 % Test).
- Parameter an Suchgrenzen werden mit boundary_hit markiert.
- AICc und Holdout-RMSE sind wegen kleiner Kurvenzahl und ungeprüfter Näherungsablesungen rein deskriptiv. Es werden keine i.i.d.-Konfidenzintervalle oder statistischen Signifikanzbehauptungen abgeleitet.

## Ausführung

Vom Repository-Root:

    python MODELLING/ccfsm/ccfsm_v05_calibration.py --input LITERATURE/wilhelm_kind_approximate_measurement_points_curated.csv --pressure-audit DATA/Raw/kurvendigitalisierung.csv --output-dir MODELLING/ccfsm/results_v0.5
    python -m unittest discover -s MODELLING/ccfsm -p 'test_*.py' -v

Ausgaben:
- ccfsm_v05_curve_fits.csv
- ccfsm_v05_model_comparison.csv
- ccfsm_v05_predictions_residuals.csv
- ccfsm_v05_curve_winners.csv
- CCFSM_v0.5_CALIBRATION_REPORT_DE.md

## Aussagegrenze

Dies ist eine explorative Modellvergleichspipeline für sieben approximativ abgelesene natürliche Kurven. Sie ist keine belastbare empirische Kalibrierung, keine unabhängige Validierung und kein Nachweis der vollständigen chemisch-hydraulischen CCFSM-Gleichungen. Für belastbare Kalibrierung sind verifizierte markerbasierte Daten, Fehlerbalken/Replikatstreuung und unabhängige Struktur-/Transportmessungen erforderlich.
