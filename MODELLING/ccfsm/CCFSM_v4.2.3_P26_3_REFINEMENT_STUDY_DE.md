# CCFSM v4.2.3 — P26.3 Verfeinerungs-, Positivitäts- und Sensitivitätsstudie

**Status:** Implementiert; quantitative Referenzläufe im CI geprüft.  
**Ziel:** P26.2 unter nichtpassenden Netzen für glatte Felder, steile Fronten, lokale Extrema und nahezu verschwindende Inventare systematisch untersuchen.

## 1. Versuchsaufbau

Für N in {16, 32, 64, 128} gleichmäßige Quellzellen werden Zielnetze mit N_T=N+3 Zellen und nichtuniformer Abbildung x_i=(i/N_T)^1.12 verwendet. Alle Netze decken dasselbe Intervall [0,1] ab. Auf jeder Quellzelle wird das Profil durch lokale L2-Projektion auf die Basis 1, xi, xi^2-1/12 abgebildet. P26.2 überträgt anschließend diese stückweise quadratische Rekonstruktion mit und ohne Positivitätsbegrenzer.

Profile:
- glatte Gaußverteilung mit positivem Hintergrund;
- steile logistische Front;
- oszillierendes Profil mit mehreren lokalen Extrema;
- sehr kleines Inventar mit schmalem Gaußbuckel.

## 2. Kennzahlen

Je Profil, Netz und Limiterstatus werden relative L1- und L2-Feldfehler, ein abgetasteter L-infinity-Fehler, das Minimum der Zielrekonstruktion und relative Residuen der drei globalen Momente ausgegeben. Bei aktivem Limiter werden die Transferresiduen mit dem tatsächlich begrenzten Quellfeld verglichen. Zusätzlich werden die durch den Limiter verursachten Änderungen des ersten und zweiten globalen Moments separat ausgewiesen; die Zellmittelwerte und damit die Masse bleiben erhalten. Quell- und Zielmomente beziehen sich auf das rekonstruierte Feld und sind nicht mit Fehlern gegenüber dem unbekannten Kontinuumsfeld zu verwechseln.

Zusätzlich wird eine empirische Störungsverstärkung berechnet: Eine kleine deterministische Störung der Quellkoeffizienten wird durch den linearen Transfer abgebildet und die maximale Koeffizientenänderung normiert. Diese Größe ist ein Sensitivitätsindikator, keine Matrix-Konditionszahl.

L1/L2 werden mit Fünf-Punkt-Gaußquadratur integriert. L-infinity wird durch dichte Abtastung innerhalb jeder Zielzelle angenähert, nicht analytisch maximiert.

## 3. Positivitätsinterpretation

Der P26.2-Limiter begrenzt die Quellmoden unter Erhaltung des Zellmittelwerts. Das garantiert jedoch nicht, dass die aus drei Zielmomenten rekonstruierte quadratische Zielzelle überall nichtnegativ bleibt. Genau diese mögliche Verletzung wird als Minimum der Zielrekonstruktion protokolliert. Der Limiter kann außerdem lokale Forminformation und Konvergenzordnung reduzieren.

## 4. Ausgaben und Grenzen

Der CI-Lauf erzeugt p26_3_refinement_metrics.csv und summary.json. Die Studie quantifiziert numerische Eigenschaften des 1-D-Transferoperators; sie validiert weder Silica-Materialparameter noch natürliche Synärese. Keine 2-D/3-D-Intersection-Geometrie, keine mechanische Druck-/Energieerhaltung und keine vollständige Fehleranalyse für beliebige FE-Felder.

Interpretation muss zwischen (a) Erhaltung der Momente des rekonstruierten Quellfelds und (b) Approximation des zugrunde liegenden kontinuierlichen Profils unterscheiden.
