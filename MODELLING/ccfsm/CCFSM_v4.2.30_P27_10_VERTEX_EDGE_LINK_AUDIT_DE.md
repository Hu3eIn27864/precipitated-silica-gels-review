# CCFSM v4.2.30 — P27.10 Knoten- und Kanten-Link-Audit

## Ziel

P27.10 erweitert P27.9 um lokale topologische Link-Prüfungen für ein positiv orientiertes Tetraedernetz. Der Prüfer ruft zunächst P27.9 auf und wertet nur ein dort inzidenzkonsistentes Netz weiter aus.

## Kanten-Link

Der Link einer Kante besteht aus den gegenüberliegenden Knotenpaaren aller inzidenten Tetraeder. Als Graph muss er
- für eine innere Kante ein zusammenhängender Kreis sein (jeder Link-Knoten Grad 2),
- für eine Randkante ein zusammenhängender Weg sein (genau zwei Knoten Grad 1, alle übrigen Grad 2).

Die Randklassifikation folgt daraus, ob die Kante in einer P27.9-Randfläche liegt.

## Knoten-Link

Der Link eines Knotens besteht aus den gegenüberliegenden Dreiecken aller inzidenten Tetraeder. Erwartet wird
- für einen inneren Knoten eine zusammenhängende triangulierte 2-Sphäre: keine Rand-Link-Kanten und Euler-Charakteristik 2,
- für einen Randknoten eine zusammenhängende triangulierte 2-Scheibe: ein einziger geschlossener Randzyklus und Euler-Charakteristik 1.

Zusätzlich darf keine Link-Kante mehr als zwei Link-Dreiecke besitzen; die Link-Dreiecke müssen über gemeinsame Kanten zusammenhängen. Die Kanten-Link-Prüfungen kontrollieren die lokalen Link-Knoten zusätzlich auf Weg-/Kreisstruktur.

## Status und Tests

- `locally_manifold_audited`: alle untersuchten Knoten- und Kanten-Links erfüllen die jeweiligen Kriterien.
- `link_inconsistent`: mindestens ein Link verletzt diese Kriterien.
- `base_audit_failed`: P27.9 konnte das Netz nicht als inzidenzkonsistent einstufen.

Die Tests umfassen ein einzelnes Tetraeder (Randfall), zwei Tetraeder mit gemeinsamer Fläche, eine geschlossene zyklische Kantenumgebung, einen getrennten Kanten-Link und die Weitergabe eines P27.9-Fehlers.

## Präzise Aussagegrenze

P27.10 prüft lokale PL-Mannigfaltigkeitsbedingungen für die durch die Tetraeder gegebene simpliciale Struktur, unter den geprüften Orientierungs- und Inzidenzannahmen. Das Ergebnis ist kein geometrischer Einbettungsbeweis (Selbstüberschneidungen sind nicht ausgeschlossen), kein Beweis einer globalen Kugel-/Gebiets-Topologie, kein FE-Konditionierungsnachweis und keine CCFSM-Positivitäts-, Energie- oder physikalische Validierung.
