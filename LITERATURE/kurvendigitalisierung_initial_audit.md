# Audit der hochgeladenen Kurvendigitalisierung

**Auditdatum:** 13. November 2026  
**Status:** strukturelle Erstprüfung; keine kinetischen Fits und keine physikalische Validierung.

## Eingangsdatei und Provenienz

Die vom Nutzer bereitgestellte Datei `kurvendigitalisierung.csv` wurde in der aktuellen Analyseumgebung eingelesen. SHA-256 der hochgeladenen Originaldatei: `948d5040060cf024f20a23f23d4aa720a113075202cc75b4bbd5702a224e79e9`. Die Datei ist UTF-8-kodiert (mit BOM), verwendet Semikolon als Feldtrenner und Dezimalkommas.

Die Spalte `trace_type` kennzeichnet sämtliche Punkte als
`combined visible trace (measurement/model overlap where inseparable)`.
Damit ist die Punktfolge ausdrücklich keine sauber separierte Messkurve.
Messpunkte und überlagerte Modellkurve lassen sich aus dieser Datei allein nicht
zuverlässig auseinanderhalten. Die Daten werden daher als **digitisierte
kombinierte Sichtkurven** geführt, nicht als Rohmessdaten oder unabhängig
verifizierte Messdaten.

## Strukturprüfung

- 4.780 Datenzeilen, 6 Spalten, keine fehlenden Felder.
- 21 Kurven in drei Panels:
  - `enforced_syneresis_20C`: 7 Druckbedingungen, je 241 Punkte, 0–60 h.
  - `acidic_pH_below_pH_iso`: 7 Druckbedingungen, je 221 Punkte, 0–55 h.
  - `basic_pH_above_pH_iso`: 7 Druckbedingungen, je 221 Punkte, 0–55 h.
- Zeitwerte liegen in 0,25-h-Schritten; innerhalb jeder Kurve sind die Zeitstempel eindeutig.
- Relative Volumenabnahme / Schrumpfung liegt insgesamt zwischen 0 und 0,9992.
  Die genaue Achsendefinition und Normalisierung müssen vor einer physikalischen
  Interpretation nochmals gegen die jeweilige Originalabbildung geprüft werden.

## Qualitätsbefund: Nichtmonotone Verläufe

Bei Sortierung jeder Kurve nach Zeit zeigen 20 von 21 Kurven mindestens einen
negativen Schritt der digitalisierten Schrumpfungsgröße. Insgesamt wurden 554
negative aufeinanderfolgende Schritte gezählt. Besonders große Sprünge treten
beispielsweise in `top_15.5`, `acid_7.41` und `basic_7.76` auf.

Solche Sprünge können durch die Überlagerung von Mess- und Modellspur,
Kurvenkreuzungen, Linien-/Marker-Verwechslung, Digitalisierung oder
Ablese-/Kalibrierungsfehler entstehen. Die vorliegende Datei erlaubt keine
eindeutige Zuordnung. Die Werte werden deshalb **nicht** automatisch geglättet,
monotonisiert, interpoliert oder gelöscht.

## Konsequenz für die Modellierung

Ein unkritischer Fit einer monotonen Kinetik, etwa
\[
S(t)=S_\infty\left[1-\exp\left(-\left(t/\tau\right)^n\right)\right],
\]
würde die Kurvenstruktur teilweise übergehen und könnte Parameter systematisch
verzerren. Daher werden aus dieser Datei in diesem Commit noch keine
kinetischen Parameter, Unsicherheiten oder Materialkonstanten abgeleitet.

Vor einem belastbaren Fit sind erforderlich:

1. Originalabbildungen mit Achsenkalibrierung und Legenden je Panel sichern.
2. Messmarker und Modelllinien getrennt digitalisieren; untrennbare Bereiche
   explizit maskieren oder als kombiniert kennzeichnen.
3. Zeit- und y-Achsen-Skalierung, Startzeitpunkt sowie Definition der relativen
   Volumenabnahme verifizieren.
4. Reproduzierbare Zweitdigitalisierung oder unabhängige Stichprobenprüfung
   durchführen und Digitalisierungsunsicherheit dokumentieren.
5. Erst danach die vorregistrierten Modellfälle (z. B. n=1 und n=1,23) mit
   Fitfenster-, Residuen- und Sensitivitätsanalyse vergleichen.

## Reproduzierbarkeit und Ablage

`LITERATURE/audit_kurvendigitalisierung.py` liest die archivierte Originaldatei,
prüft das Schema und erzeugt eine numerisch konvertierte Kopie sowie eine
Kennzahlentabelle je Kurve. Das Skript korrigiert, glättet oder filtert keine
Punkte.

**Ablagehinweis:** In diesem Commit werden Auditbericht, Skript und
Kurven-Audit-Tabelle versioniert. Die vollständige 600-kB-Eingangsdatei konnte
über den verfügbaren GitHub-Dateischreibkanal nicht aus dem lokalen Upload in
das Repository übertragen werden; ihr SHA-256 ist oben dokumentiert. Sie ist
daher noch nicht im Repository archiviert und muss separat nachgereicht bzw.
über einen Datei-Upload in GitHub abgelegt werden. Der Auditbericht behauptet
nicht, dass die Rohdatei bereits committed wurde.
