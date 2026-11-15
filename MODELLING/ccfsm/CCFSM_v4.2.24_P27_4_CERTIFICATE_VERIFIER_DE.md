# P27.4 — unabhängiger exakter Verifizierer für P27.3

**Status:** implementiert; unabhängige Verifikation der P27.3-Zertifikatsstruktur, keine globale Positivitätsentscheidung für beliebige P2-Polynome.

## Ziel

P27.3 konstruiert adaptive Unterteilungszertifikate für quadratische Polynome auf einem Tetraeder. P27.4 prüft diese Zertifikate in einem getrennten Modul, das weder den P27.3-Konstruktor noch die P27.2-Bernstein-Umrechnung importiert.

## Prüfschritte

1. Prüft Tetraederdimension und exakt von null verschiedenes orientiertes Sechsfachvolumen.
2. Rekonstruiert die zehn Wurzel-Bernstein-Koeffizienten ausschließlich aus vier Eckwerten und sechs Kantenmittelpunktwerten.
3. Reproduziert die festgelegte Achtfach-Unterteilung (vier Eck-Tetraeder und vier zentrale Tetraeder; zentrale Oktaederdiagonale m01–m23).
4. Berechnet für jeden Pfad die lokalen Koeffizienten exakt mit rationaler Arithmetik neu.
5. Prüft, dass die Blattpfade einen vollständigen, präfixfreien Baum bilden: kein Blatt fehlt, ist doppelt oder unerreichbar.
6. Akzeptiert einen positiven Abschluss nur, wenn jedes Blatt den Status `nonnegative` trägt und alle zehn neu berechneten Koeffizienten nichtnegativ sind.
7. Prüft bei einem Negativbefund den baryzentrischen Punkt (Summe 1, alle Komponenten nichtnegativ) und wertet das ursprüngliche Wurzelpolynom exakt aus; der Wert muss mit dem Zertifikat übereinstimmen und strikt negativ sein.
8. Ein `unresolved`-Abschluss ist nur verifiziert, wenn mindestens ein tatsächlich nicht zertifiziertes Blatt bis zur angegebenen Tiefe vorliegt.

## Sicherheits- und Geltungsgrenzen

- Der Verifizierer ist unabhängig im Software-/Import-Sinn, aber verwendet dieselbe mathematische Unterteilungsdefinition. Eine unabhängige mathematische Beweisprüfung durch Dritte ist damit nicht ersetzt.
- Ein SHA-256-Hash wäre nur ein Integritäts-Fingerprint, keine Signatur oder Authentifizierung; er wird nicht als Beweis verwendet.
- Die positive Bernstein-Bedingung ist hinreichend, nicht notwendig. Endliche Unterteilung kann für ein nichtnegatives Polynom offen bleiben.
- Ein verifizierter Negativpunkt beweist Nicht-Nichtnegativität; ein negativer Bernstein-Koeffizient allein tut dies nicht.
- Keine Konformitätsgarantie für benachbarte Elemente, keine globale Mesh-Invarianz und keine Integration in den gekoppelten P19–P24-3D-Zeitschritt.
- Dies ist ein Zertifikatsverifizierer, kein 3D-Positivitätssatz für das vollständige CCFSM.

## Tests

Mutationstests verändern Blattkoeffizienten, entfernen oder duplizieren Blätter, verändern Wurzelwerte und manipulieren einen Negativzeugen. Zusätzlich werden positive und unresolved Abschlüsse sowie ein exakter Negativpunkt geprüft.
