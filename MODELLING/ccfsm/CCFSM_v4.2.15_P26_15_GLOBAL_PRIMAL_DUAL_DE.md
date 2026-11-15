# CCFSM v4.2.15 — P26.15: globaler rationaler Primär-/Dualentscheid

**Status:** implementierter exakter Zertifikatsrahmen mit endlicher Dualrichtungs-Suche. Kein vollständiger endlicher Entscheidungsalgorithmus.

## Ziel

P26.14 sucht einen global zulässigen nichtnegativen quadratischen Zellprofilvektor und akzeptiert ihn nur nach exakter rationaler Momenten- und Markov-Lukács-Prüfung. P26.15 ergänzt die duale Gegenseite: Ein strikt positiver rationaler Abstand zwischen Zielmomenten und einer rigorosen rationalen oberen Schranke der Supportfunktion beweist Unzulässigkeit.

## Duale Trennung

Für eine Richtung \(y=(y_1,y_2)\ne0\) wertet P26.8 zellweise die Supportfunktion der Menge nichtnegativer quadratischer Profile aus. Die lokalen Richtungskoeffizienten lauten
\[
p_j=y_1h_j^2/12+y_2c_jh_j^2/6,\qquad
q_j=y_2h_j^3/180.
\]
Die Summe der lokalen Support-Obergrenzen ist eine rigorose rationale obere Schranke. Der Abstand
\[
\gamma_{\rm lower}=y\cdot t-\sum_j h_{K(m_j)}^{\rm upper}(p_j,q_j)
\]
wird vollständig rational geprüft; nur \(\gamma_{\rm lower}>0\) ergibt certified_infeasible.

P26.15 enumeriert primitive ganzzahlige Richtungen in wachsenden L-infinity-Schalen. Dies ist eine systematische Suche über rationale Richtungen. Bei existierender strikter Trennung existieren wegen Dichte rationaler Richtungen auch rationale Separatoren; ein endliches Suchlimit kann sie dennoch verpassen.

## Gekoppelter Primär-/Dualablauf

1. Exakte Dualsuche zuerst. Ein bestätigter strikter Separator beendet den Ablauf mit certified_infeasible.
2. Ohne Dualzertifikat wird P26.14 aufgerufen.
3. Nur ein vollständig rational rekonstruierter Primärzeuge mit exakten drei globalen Momenten und exakter kontinuierlicher Zellpositivität ergibt feasible_exact_primal_witness.
4. Andernfalls lautet das Ergebnis unresolved.

Kein dualer Treffer in einer endlichen Suche ist kein Zulässigkeitsbeweis. Numerische Nichtkonvergenz ist ebenfalls kein Unzulässigkeitsbeweis.

## Regressionen

- Nullinventar mit nichtverschwindenden Moden: strikt positives rationales Dualzertifikat.
- Positives zweizelliges Konstantprofil: exakter Primärzeuge.
- Positive Nullmoden-Kontrolle: kein falscher Unzulässigkeitsnachweis.
- Begrenzte Dualsuche: keine automatische Feasibility-Schlussfolgerung.

## Geltungsbereich und Grenzen

Nur 1-D-Intervalle, feste nichtnegative Zellmittelwerte und stückweise quadratische Profile mit globalen ersten/zweiten Momenten. Die Dualsuche bleibt endlich und kann einen Separator übersehen. Die Primärsuche nutzt eine numerische Dykstra-Projektion nur als Kandidatengenerator und eine endliche rationale Nachsuche. Keine 2-D/3-D-Erweiterung, keine vollständige allgemeine SOCP-Entscheidungsroutine, keine experimentelle oder physikalische Validierung.
