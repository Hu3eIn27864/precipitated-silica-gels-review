# CCFSM v4.2.4 — P26.4 positivitätserhaltende Zielrekonstruktion

**Ziel:** P26.2 nach dem Netztransfer so ergänzen, dass jede quadratische Zielzelle nichtnegativ ist und ihre Zellmasse exakt behält.

## 1. Zielzellpolynom

Auf einer Zielzelle J_j=[x_j,x_(j+1)] mit Mittelwert m_j wird die normierte Darstellung verwendet:

u_j(xi)=m_j+a_j xi+b_j(xi²-1/12),  -1/2 <= xi <= 1/2.

Die beiden höheren Moden haben Mittelwert null. Daher ändert jede Skalierung dieser Moden die Zellmasse nicht.

## 2. Positivitätsbedingte radiale Kontraktion

Sei d_j das Minimum von a_j xi+b_j(xi²-1/12) auf [-1/2,1/2]. Falls m_j+d_j >= 0, bleibt die Zelle unverändert. Andernfalls wird

theta_j=(1-epsilon) min(1,m_j/(-d_j)),
a_j_plus=theta_j a_j, b_j_plus=theta_j b_j,

mit kleinem Rundungssicherheitsfaktor epsilon verwendet. Für m_j=0 werden beide Moden auf null gesetzt. Damit bleibt der Mittelwert exakt gleich und das resultierende quadratische Polynom ist nichtnegativ auf dem gesamten Intervall (bis auf Gleitkomma-Rundung).

Das Minimum wird analytisch über die Endpunkte und – bei konvexer Krümmung – den inneren Scheitelpunkt bestimmt.

## 3. Was wird erhalten und was nicht?

- Exakt erhalten: jede Zielzellmasse und damit die globale Masse.
- Nicht generell erhalten: erstes und zweites räumliches Moment. Die Kontraktion ändert die linearen und quadratischen Moden; deren Verluste werden zellweise und global ausgegeben.
- Nicht behauptet: globale optimale Projektion in Koeffizientenraum. Das Verfahren ist die größtmögliche zulässige gemeinsame Skalierung entlang des ursprünglichen Modenvektors, kein allgemeiner konvexer Optimierer.
- Negative Zielzellmittelwerte werden abgewiesen: bei negativer Masse kann kein überall nichtnegatives Feld existieren.

## 4. Schnittstelle und Tests

project_positive_quadratic ruft zunächst P26.2 ohne Quelllimiter auf und begrenzt anschließend die Zielzellpolynome. limit_target_reconstruction kann auch auf bereits projizierte Zielkoeffizienten angewandt werden. Diagnostik umfasst Limiterfaktoren, Minima vor/nach Begrenzung und Änderungen der Momente 0/1/2.

Regressionen decken Rand- und innere Scheitelpunkt-Unterschwinger, unveränderte positive Felder, Nullmittelwert, ungültige Mittelwerte, endliche Eingaben, Massenerhaltung und Momentenänderungen ab.

## 5. Geltungsgrenzen

1-D-Intervalle und quadratische Rekonstruktionen; keine 2-D/3-D-Geometrie, keine automatische FE-Rekonstruktion, keine Druck- oder Energieerhaltung und keine physikalische Validierung. Positivität des übertragenen Konzentrations-/Inventarfelds ist nicht mit mechanischer Druckkonsistenz gleichzusetzen; P19 muss für das Zielnetz erneut gelöst werden.


## 6. CI-Referenzlauf und quantitative Ergebnisse

GitHub Actions Lauf #357 erfolgreich; **315/315 Unit-Tests** bestanden. Der P26.4-Studienlauf und der Upload des Artefakts waren erfolgreich.

Fünf synthetische Zielzellfälle wurden geprüft; zwei benötigten eine Modenkontraktion. Das Minimum der Zielpolynome nach Begrenzung war 0. Die maximale absolute Massenänderung betrug 0. Die maximalen absoluten Änderungen der ersten und zweiten globalen Momente betrugen in diesen bewusst belastenden Fällen jeweils rund 1/6. Diese Werte illustrieren den möglichen Form-/Momentenverlust, nicht einen allgemeinen Fehlermaßstab.

Ergebnisdatei: p26_4_positive_target_cases.csv; Zusammenfassung: summary.json. CI-Lauf: https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43673207806 ; Artefakt: https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43673207806/artifacts/14145520449.
