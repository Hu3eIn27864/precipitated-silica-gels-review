# CCFSM v4.2.44 — P27.24: diskrete Zweizustands-Energiebilanz für P24

## Ziel

P27.23 bilanziert Energieraten in Watt. P27.24 bilanziert dagegen die tatsächlich gespeicherte Energieänderung zwischen Anfangszustand (n) und akzeptiertem Endzustand (n+1) eines impliziten P24-Schritts:

\[
E^{n+1}-E^n = W_{\mathrm{ext},[n,n+1]}-D_{[n,n+1]}+R_E.
\]

Alle Größen auf der rechten Seite sind über den gesamten Zeitschritt integrierte Energien in Joule. (D\) wird aus den vom Aufrufer gelieferten, nichtnegativen Schrittintegralen für Reaktion, Darcy und Onsager-Diffusion zusammengesetzt. Äußere Arbeit wird als explizite, vorzeichenbehaftete Abbildung übergeben.

## Implementierung

- Anfangs- und Endzustand werden auf demselben festen Zellvolumenraster integriert; wechselnde Zellzahlen oder nicht passende Volumenlisten werden abgelehnt.
- Die P9-Mechanik- und Biot-Energie wird integriert. Bei P19-Energieeigentümerschaft ersetzt ein erfolgreicher P27.22-Audit **an beiden Zuständen** die P9-Mechanikenergie. Die P19-Energie wird nicht zusätzlich addiert.
- Chemische P9-Energie bleibt ein separat wählbarer Anteil.
- Optional kann die Totale-Potential-Konvention mit expliziter homogener Totlast verwendet werden.
- Der diskrete Rest wird unabhängig aus Zustandsenergiedifferenz, externer Arbeit und integrierter Dissipation berechnet. Er wird nicht auf null gesetzt.
- Eine optionale Advektionsdissipation wird nur gezählt, wenn sie ausdrücklich als Schrittintegral geliefert wird.

## Wichtige Grenze

Der aktuelle P21/P24-Vertrag liefert keinen vollständigen, bewiesenen Schrittintegral-Abschluss für die Entropieproduktion der upwind-advehierten Spezies. Deshalb bleibt dieser Term standardmäßig als offen markiert. Reservoir-, Dirichlet-Reaktions-, Traktions- und chemische Randarbeit müssen mit konsistenten Vorzeichen und über denselben Zeitschritt in `external_work_j` eingehen. Die Dissipationswerte sind explizite Eingaben; P27.24 behauptet nicht, sie bereits exakt aus dem P24-Newton-Lauf zu integrieren.

Ein kleiner Rest bedeutet daher zunächst nur: **Die übergebenen diskreten Energien, Arbeiten und Dissipationen schließen numerisch.** Er ist kein solver-interner Energie-Monotonienachweis, kein vollständiger thermodynamischer Satz für P21/P24 und keine physikalische Validierung.

## Regressionen

Acht Tests prüfen einen absichtlich nicht schließenden Fall, exakten Bilanzschluss, Nichtnegativität, Raster-/Geometrie-Konsistenz, positives dt, P19-Ersetzung an beiden Zuständen und explizite Behandlung der Advektionsschließung.

## Nächster Freigabeschritt

P27.25 sollte die Schrittintegrale direkt aus den akzeptierten P24-Anfangs-/End-Snapshots und den tatsächlichen FV-Flüssen rekonstruieren, einschließlich Randarbeit, Reaktionsenergie und Advektionsentropie. Erst nach unabhängiger Herleitung dieser Terme darf die Markierung „vollständiger Energieabschluss“ gesetzt werden.
