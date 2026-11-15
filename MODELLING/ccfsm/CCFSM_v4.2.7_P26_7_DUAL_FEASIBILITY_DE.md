# P26.7 — Dualer Trennungsnachweis für globale Machbarkeit

## Problemgeometrie
Bei festen Zellmittelwerten m_j >= 0 ist die Menge K_j der zellweise zulässigen Modenpaare konvex und kompakt. Die erreichbaren globalen Modenmomente bilden die Minkowski-Summe der linearen Bilder dieser Mengen:
C = Sum_j A_j K_j.
Mit h_j=x_(j+1)-x_j und c_j=(x_j+x_(j+1))/2 gilt
Delta M1 = Sum_j a_j h_j^2/12,
Delta M2 = Sum_j (a_j c_j h_j^2/6 + b_j h_j^3/180).

## Duale Separationsidee
Für ein Ziel t=(Delta M1,Delta M2) gilt t nicht in C, falls eine Richtung y existiert mit
y dot t > h_C(y) = Sum_j h_Kj(A_j^T y).
Die Zell-Supportfunktion wird auf dem analytischen Rand der zulässigen Koeffizientenmenge ausgewertet: zwei gerade Randsegmente und der elliptische Bogen mit a=sqrt(12)m sin(phi), b=6m(1+cos(phi)), phi in [-2pi/3,2pi/3].

## Implementierung und epistemische Grenze
dual_feasibility_diagnostic durchsucht Richtungen auf dem Einheitskreis und verfeinert lokale Maxima; Zell-Supportwerte werden numerisch auf dem Rand berechnet. Ein positiver Abstand liefert einen numerischen trennenden Zeugen. Die aktuelle Implementierung verwendet Gleitkommaarithmetik und endliche Abtastung; sie ist noch kein formal verifiziertes Unzulässigkeitszertifikat mit Intervall- oder exakten Schranken. no_separator_found bedeutet ausdrücklich nicht feasible.

## Geltungsbereich
1-D-Intervalle, feste Zellmittelwerte, quadratische Rekonstruktionen. Keine 2-D/3-D-Geometrie und keine physikalische Validierung.
