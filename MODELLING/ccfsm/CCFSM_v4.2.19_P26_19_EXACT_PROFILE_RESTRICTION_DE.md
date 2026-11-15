# P26.19 — Exakte lokale Profilrestriktion und Rückkoarsenierung

**Stand: 15. November 2026**

## Ziel

P26.19 erweitert P26.18 von globaler Momentenäquivalenz auf lokale Gleichheit stückweise-quadratischer Profile. Auf einer Elternzelle mit normierter Koordinate \(\xi\in[-1/2,1/2]\) sei
\[
u(\xi)=m+a\xi+b(\xi^2-1/12).
\]
Die Verfeinerung muss eine echte geschachtelte Partition desselben Gebiets sein.

## Exakte Restriktion

Für eine Kindzelle mit Mittelpunktversatz \(d=(c_{child}-c_{parent})/H\) und Breitenverhältnis \(r=h/H\) ergibt die affine Koordinatentransformation:
\[
m_c=m+ad+b(d^2+r^2/12-1/12),\qquad
a_c=r(a+2bd),\qquad
b_c=br^2.
\]
Alle Größen werden als rationale Zahlen berechnet. Die Formel erhält das dargestellte physikalische Polynom punktweise, nicht nur seine drei globalen Momente.

## Rückkoarsenierung

Aus den exakten Kindmomenten werden die Elternkoeffizienten zurückgewonnen:
\[
m=M_0/H,\quad
a=12(M_1-cM_0)/H^2,\quad
b=180(M_2-2cM_1+c^2M_0-M_0H^2/12)/H^3.
\]
Anschließend wird das rekonstruierte Elternprofil erneut auf das Feinmesh restringiert. Die Kennzeichnung exact_local_restriction wird nur bei exakter Übereinstimmung sämtlicher Kindmittelwerte sowie linearer und quadratischer Koeffizienten gesetzt.

## Dateien und Reproduktion

- ccfsm_p26_19_exact_profile_restriction.py: Restriktions-, Koarsenierungs- und Round-trip-Funktionen.
- test_ccfsm_p26_19_exact_profile_restriction.py: exakte Regressionstests.
- ccfsm_p26_19_profile_restriction_study.py: reproduzierbare Referenzstudie.

Ausführung:
    python MODELLING/ccfsm/ccfsm_p26_19_profile_restriction_study.py --output-dir ccfsm-p26-19-results
    python -m unittest discover -s MODELLING/ccfsm -p 'test_ccfsm_p26_19_exact_profile_restriction.py' -v

Grenzen: Nur 1-D und stückweise quadratische Profile auf exakt geschachtelten Partitionen. Eine beliebige Feinlösung muss nicht aus einer Elternquadratik stammen; in diesem Fall schlägt die lokale Gleichheitsprüfung erwartungsgemäß fehl. Keine allgemeine Projektion auf nicht geschachtelten Netzen, keine 2-D/3-D-Erweiterung, keine physikalische oder experimentelle Validierung.
