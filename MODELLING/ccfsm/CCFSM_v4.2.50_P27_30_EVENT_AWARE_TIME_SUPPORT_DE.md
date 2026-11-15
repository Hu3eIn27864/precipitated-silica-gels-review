# CCFSM v4.2.50 — P27.30: ereignisbewusste Zeitstützstellen für Upwind-Zweigwechsel

**Datum:** 15.11.2026  
**Status:** Implementiert; Hosted-CI-Prüfung ausstehend.

## Ziel

P27.30 erweitert P27.29 von vorgegebenen bekannten Nullstellen zu einer einfachen ereignisbewussten Regel: Vorzeichenwechsel der Randflüsse werden aus zeitlich abgetasteten Flusshistorien erkannt, ihre Nullstellen durch lineare Interpolation bestimmt und als zusätzliche Zeitstützstellen in ein uniformes Basisgitter eingefügt.

## Verfahren

1. Für jeden Randfluss werden Werte an streng monotonen Detektionszeiten bereitgestellt.
2. Bei einem Vorzeichenwechsel zwischen zwei benachbarten Abtastpunkten wird die Nullstelle linear interpoliert.
3. Die Ereigniszeiten werden mit dem uniformen Basisgitter vereinigt und sortiert.
4. Der P27.25-Schrittadapter wird auf jedem Teilintervall ausgewertet; chemische Randarbeit und Netto-Materialtransfer erhalten getrennte Fehlermaße gegenüber stückweise analytischen Referenzen.

Die Detektion ist bewusst explizit und reproduzierbar. Sie erkennt keine mehrfachen, zwischen zwei Detektionspunkten liegenden Nullstellen, wenn die abgetasteten Endwerte dasselbe Vorzeichen besitzen. Für reale Solvertrajektorien wäre deshalb eine engere Abtastung, eine ereignisgesteuerte Nullstellensuche oder eine Schranke für die Flusskrümmung erforderlich.

## Synthetischer Referenzfall

Der P27.29-Fall bleibt erhalten: (j_L(t)=t-1), (j_R(t)=t-1.5), mit Wechselzeiten 1.0 s und 1.5 s. Die Upwind-Potentiale betragen links 5/2 J mol⁻¹ und rechts 3/7 J mol⁻¹ (negative/nichtnegative Flusszweige). Für (T=2) s und (A=1.5) m² lauten die exakten Referenzen −2.25 J links, +3.75 J rechts, +1.50 J insgesamt sowie +1.50 mol Netto-M-Transfer.

Das Standardexperiment verwendet drei uniforme Teilintervalle und vier Detektionsintervalle. Die beiden erkannten Ereignisse werden in das uniforme Gitter eingefügt. Dadurch wird ein Intervall, das einen Upwind-Knick überquert, in branch-einheitliche Teilintervalle aufgeteilt. Uniforme und ereignisbewusste Ergebnisse berichten Teilintervallzahl, Zeitstützstellen, chemischen Arbeitsfehler und Materialtransferfehler.

## Tests

Sechs Regressionen prüfen interpolierte Nullstellen, Fälle ohne Vorzeichenwechsel, Einfügen beider Ereignisse, Fehlerreduktion gegenüber dem uniformen Basisgitter, getrennte Material-/Energiefehler und mehrere Nullstellen/Eingabevalidierung.

## Aussagegrenzen

P27.30 ist ein synthetischer Ereigniserkennungs- und Quadraturtest auf Basis stückweise linearer Flussinterpolation. Die Erkennung kann nicht beobachtete Mehrfachnullstellen zwischen Detektionspunkten übersehen. Sie beweist keine vollständige diskrete Upwind-Entropie-Kettenregel, integriert nicht die tatsächliche P24-Newton-Trajektorie und validiert weder Reservoirgesetze noch die physikalischen CCFSM-Gleichungen. Feststoff-/Brücken- und mechanische Randarbeit bleiben offen.
Hosted workflow [#726](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43741957699) führte alle sechs P27.30-Regressionen erfolgreich aus. Der Gesamtworkflow ist dennoch **nicht grün**: 615 Tests liefen; sieben Fehler/Exceptions liegen in anderen bzw. älteren Testbereichen (P27.10, P27.13, P27.17, P27.18, P27.23 und P27.28). P27.30 wird daher als gezielt bestanden, die Gesamtintegration aber als offen geführt.
