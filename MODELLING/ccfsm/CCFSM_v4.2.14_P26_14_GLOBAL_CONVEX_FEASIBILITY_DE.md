# CCFSM v4.2.14 — P26.14: globaler konvexer Machbarkeitslöser

**Status:** numerischer Kandidatengenerator mit exakter rationaler Primärzertifizierung; kein vollständiger Machbarkeitsentscheider.

## Ziel und Formulierung

Für feste nichtnegative Zellmittelwerte \(m_j\) werden stückweise quadratische Profile
\[
u_j(x)=m_j+a_jx+b_j(x^2-1/12),\quad x\in[-1/2,1/2],
\]
gesucht, welche globale Masse sowie erstes und zweites Moment erhalten und in jeder Zelle kontinuierlich nichtnegativ sind.

P26.12 beschreibt den vollständigen affinen Raum der globalen Momentengleichungen. P26.13 liefert die exakte lokale Darstellung
\[
u_j(x)=[1,x]Q_j[1,x]^T+\lambda_j(1/4-x^2),\quad Q_j\succeq0,\quad\lambda_j\ge0.
\]
Damit ist die Gesamtzulässigkeitsmenge konvex; die 2x2-PSD-Bedingung ist äquivalent zu einer Rotated-SOC-Bedingung.

## Implementierter Ablauf

1. Eingaben werden als rationale Dezimalwerte interpretiert; daraus werden die drei Zielmomente exakt festgelegt.
2. Dykstra-Projektion (P26.6) auf globale Momentengleichungen und das Produkt zellweiser Positivitätsmengen erzeugt einen numerischen Kandidaten.
3. P26.12 rationalisiert freie Koordinaten und rekonstruiert zwei Pivotkoordinaten exakt.
4. P26.13 prüft je Zelle ein rationales Markov-Lukács-Zertifikat.

Nur bei erfolgreicher Prüfung wird feasible_exact_primal_witness ausgegeben. Der Zeuge erfüllt alle drei Momentengleichungen exakt und ist auf jedem vollständigen Zellintervall nichtnegativ.

## Statussemantik

- feasible_exact_primal_witness: exakt rationaler, unabhängig nachprüfbarer Primärzeuge.
- unresolved: Dykstra oder endliche rationale Nachsuche scheitert. Dies ist kein Unzulässigkeitsbeweis.
- P26.14 erzeugt selbst kein duales Unzulässigkeitszertifikat; dafür bleiben P26.8/P26.9 zuständig.

## Tests und Grenzen

CI prüft einen positiven zweizelligen Konstantfall, einen negativen Einzellfall (bewusst unresolved statt certified_infeasible) und die Dimensionsvalidierung.

Nur 1-D-Intervalle, feste nichtnegative Zellmittelwerte und quadratische Profile. Die endliche rationale Suche ist unvollständig; ein nichtleerer reeller Zulässigkeitsbereich muss nicht getroffen werden. Die numerische Projektion ist Kandidatengenerierung, kein Beweis. Keine 2-D/3-D-Erweiterung und keine physikalische Validierung der Synäresekinetik.
