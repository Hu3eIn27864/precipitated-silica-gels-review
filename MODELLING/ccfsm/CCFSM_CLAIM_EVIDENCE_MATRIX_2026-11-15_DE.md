# CCFSM — Claim–Evidence-Matrix (15.11.2026)

| Claim | Exakte Grundlage | Aktueller Belegtyp | Zulässige Formulierung | Nicht zulässig |
|---|---|---|---|---|
| v0.1 Einzelexponentialantwort | ODE \(\dot S=(A-S)/\tau\) | geschlossene Lösung, Unit-Tests | „empirische effektive Beschreibung unter festen Bedingungen“ | „universelles Naturgesetz“ |
| v0.2 eindeutige Lösung | affine, global Lipschitz ODE in \((q,S)\) | explizite Lösung / Picard–Lindelöf | „eindeutige globale Lösung für konstante zulässige Parameter“ | „Existenz des realen 3D-CCFSM bewiesen“ |
| v0.2 zulässiger Zustandsbereich | \(0\le S_0\le\eta_aq_0\le\eta_aq_\infty<1\) | Variation-of-constants Beweis | „Invarianz und Monotonie unter den genannten Anfangsdaten“ | „Positivität für beliebige Anfangsdaten“ |
| v0.2 Rate-label symmetry | Transferfunktion ist symmetrisch in \(k_n,k_h\) | analytischer Beweis | „die Labels sind aus einer idealen Nullstart-S(t)-Kurve allein nicht unterscheidbar“ | „beide Raten können nie identifiziert werden“ |
| v0.2 Endpoint product | Grenzwert \(\eta_aq_\infty\) | expliziter Grenzwert | „nur das Produkt ist aus der Kurve bestimmbar“ | getrennte Bestimmung von \(\eta_a\), \(q_\infty\) aus nur S(t) |
| v0.2 hydraulic scaling | First-mode poroelastische Reduktion | bedingte Skalierung/Dimensionsanalyse | „unter homogener linearer gesättigter Referenzannahme gilt näherungsweise …“ | „beweist gemessene Permeabilität oder L_d^-2 Gesetz“ |
| P0 Biot-Darcy | linearer Referenzkern, geschlossene No-flow Grenze | schwacher Existenz-/Eindeutigkeitssatz unter Koerzivität | „P0-Referenzsystem besitzt …“ | „vollständiges CCFSM besitzt …“ |
| P1 Brückenvariable | explizite Relaxation, affine gleichmäßig elliptische Mobilität | bedingter schwacher Satz | „für diese mathematische Platzhalterschließung“ | „Silica-Permeabilität hängt linear von Brückendichte ab“ |
| P26 Zertifikate | rationale Zeugen und SOS/Supportbedingungen | exakte rationale Verifikation im 1-D-quadratischen Spezialfall | „exakte Zertifikate für die definierten Projektionsprobleme“ | „das gesamte numerische CCFSM ist formal verifiziert“ |
| P27 Wurzelisolation | Intervall-Einschließung und Polynomspezialfall | bedingte Zertifizierung | „unter gültigem Intervall-Einschließungsvertrag“ | „vollständige Ereigniserkennung beliebiger Flüsse“ |
| Empirische Kurven | Wilhelm & Kind (2015), berichtete Fits; figure-digitisierte Punkte | Literaturdaten plus approximative Digitalisate | Datenart und Unsicherheit ausdrücklich benennen | Digitalisate als Original-Rohdaten oder unabhängige Validierung darstellen |

## Freigabeprinzip

Jeder Satz im Manuskript erhält intern eine Kategorie:

- **T — Theorem/proof:** mathematisch bewiesen mit expliziten Annahmen;
- **C — Certificate:** unabhängig prüfbares exaktes Zertifikat;
- **N — Numerical verification:** Unit-/Regression-/CI-/Referenztest;
- **E — Empirical evidence:** publizierte Messung oder transparent digitalisierte Literaturdaten;
- **H — Hypothesis:** vorgeschlagene, noch nicht identifizierte Modellschließung.

Ein Manuskript darf Kategorien nicht rhetorisch aufwerten (z. B. N zu T oder H zu E).
