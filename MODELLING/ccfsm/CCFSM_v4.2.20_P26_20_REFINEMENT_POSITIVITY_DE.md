# P26.20 — Positivitätserhalt bei exakter Gitterverfeinerung

**Stand: 15. November 2026**

## Ziel

P26.20 schließt an P26.13 (Markov-Lukács-Zertifikate) und P26.19 (exakte Profilrestriktion) an. Geprüft wird, ob ein nichtnegatives quadratisches Zellprofil unter exakter Restriktion auf ein geschachteltes Feinmesh nichtnegativ bleibt und ob die Kindzellen-Zertifikate unabhängig geprüft werden können.

## Mathematische Aussage

Auf einer Elternzelle sei
\[
u(\xi)=m+a\xi+b(\xi^2-1/12),\qquad \xi\in[-1/2,1/2].
\]
Die Restriktion auf eine Kindzelle ist eine affine Koordinatentransformation desselben Polynoms. Daher gilt punktweise: Ist u nichtnegativ auf der Elternzelle, dann ist die eingeschränkte Funktion auf jeder Kindzelle ebenfalls nichtnegativ. Dies setzt eine exakte geschachtelte Partition desselben Gebiets voraus.

## Zertifikat und unabhängige Prüfung

Für jede Kindzelle wird die Darstellung
\[
u(x)=[1,x]Q[1,x]^T+\lambda(1/4-x^2),\qquad Q\succeq0,\quad\lambda\geq0
\]
mit rationalen Einträgen geprüft. Der P26.20-Verifikator berechnet unabhängig die Koeffizientenidentitäten, den nichtnegativen Multiplikator und die PSD-Bedingungen der symmetrischen 2×2-Gram-Matrix (beide Diagonaleinträge und Determinante). Er importiert nicht den P26.13-Zertifikatskonstruktor. Die Referenzstudie verwendet P26.13 zur Zertifikatserzeugung und P26.20 zur unabhängigen Prüfung.

## Reproduktion

Dateien:
- ccfsm_p26_20_refinement_positivity.py — unabhängige exakte Zertifikatsprüfung.
- test_ccfsm_p26_20_refinement_positivity.py — Regressionen für strikt positive, randberührende und Nullprofile sowie manipulierte Zertifikate.
- ccfsm_p26_20_refinement_positivity_study.py — reproduzierbare Referenzfälle.

Ausführung:
python MODELLING/ccfsm/ccfsm_p26_20_refinement_positivity_study.py --output-dir ccfsm-p26-20-results
python -m unittest discover -s MODELLING/ccfsm -p 'test_ccfsm_p26_20_refinement_positivity.py' -v

## Aussagegrenzen

- Nur 1-D, rationale geschachtelte Netze und stückweise quadratische Profile.
- Exakte Restriktion erhält das bestehende Polynom; sie garantiert keine Positivität einer beliebigen nichtkonformen Zielprojektion.
- Die Studie nutzt synthetische rationale Profile, keine gemessenen Silica-Daten.
- Keine 2-D/3-D-Verallgemeinerung, keine physikalische oder experimentelle Validierung.
- Der Schritt ist ein Zertifikats-/Verifikationsbaustein, kein globaler SOCP-Optimierer.
