# CCFSM v0.4 — vollständige Einflussparameter-Architektur

**Geltungsbereich:** natürliche, mechanisch unbelastete Synärese gefällter Silica-Gele aus Silikat- und Säure-/Basenroute. Keine Kalibrierung mit Oedometer-, Press- oder erzwungenen Synäreseversuchen.

**Zweck:** systematische Erfassung der Einflussgrößen, ihrer Wirkpfade, Einheiten, erforderlichen Messungen und Identifizierbarkeit. Diese Version ist eine Parameter- und Kausalarchitektur, keine Behauptung, dass alle aufgeführten Parameter bereits quantitativ in einer geschlossenen Zustandsgleichung stehen.

## 1. Modellierungsregel

Wir unterscheiden strikt:

1. **Rezeptur-/Prozessparameter**: werden bei der Herstellung vorgegeben (z. B. Silikatkonzentration, Säurezugabe, Mischintensität).
2. **Chemische Zustände**: entstehen aus Rezeptur und Reaktion und müssen zeitaufgelöst gemessen oder chemisch bilanziert werden (pH, Silicium-Spezies, Ionenstärke, Übersättigung).
3. **Netzwerkzustände**: Brückendichte, Konnektivität, Kontaktzahl, Fraktalstruktur und Kontraktionsinventar.
4. **Transport-/Mechanikparameter**: Porosität, Porenhalsverteilung, Permeabilität, effektiver Modul, Viskosität und Grenzflächenwiderstand.
5. **Beobachtungs-/Randbedingungen**: Geometrie, Entwässerungslänge, Gefäßoberfläche, freie Oberfläche, Verdunstung und Messdefinition.

**Keine Doppelzählung:** pH ist chemisch durch Rezeptur, Neutralisation, Speziation, Pufferung und Reaktionsfortschritt bestimmt. In einem Regressions-/Kinetikansatz dürfen Rezepturvariablen und pH nicht unkritisch als unabhängige additive Ursachen behandelt werden. pH kann als gemessener Zustand oder als Ausgabe eines chemischen Teilmodells auftreten.

## 2. Kausale Architektur

```
Rezeptur + Zugabereihenfolge + Mischung + Alterung
                    |
                    v
       chemische Zustände: pH(t), T_g(t), I(t),
       Silikat-Spezies, gelöstes Si, Übersättigung
                    |
                    v
       Kondensation / Brückenbildung B(t)
                    |
          +---------+----------+
          |                    |
          v                    v
  Morphologie / Kontakte   Kontraktionsinventar
  D_f, z, Porenraum        X, Relaxation
          |                    |
          v                    v
  Porenhalsnetz /          intrinsisches Potenzial q
  Konnektivität                  |
          |                     |
          v                     |
  Permeabilität kappa            |
          +-----------+---------+
                      v
          natürliche Entwässerung + Gelmechanik
          mu, K_eff, Grenzfläche, Geometrie
                      |
                      v
              beobachtete S(t)
```

Verdunstung, Temperaturgradienten und Gefäß-/Luft-Grenzflächen können zusätzliche Beiträge zur beobachteten Volumen- und Massenbilanz erzeugen. Sie müssen experimentell kontrolliert oder separat modelliert werden.

## 3. Vollständige Parametergruppen

Die maschinenlesbare Liste liegt in `CCFSM_v0.4_INFLUENCE_PARAMETER_REGISTER.csv`. Die folgenden Gruppen definieren die Modellgrenzen.

### A. Rezeptur und Fällchemie

- Silikat-Massen-/Stoffmengenkonzentration und Silikatmodul (SiO2/Alkalioxid, sofern vorhanden).
- Säure-/Basenidentität, Konzentration, Aktivität, Zugabemenge, Zugaberate und stöchiometrisches Verhältnis.
- Natrium-, Sulfat- und sonstige Gegenionenkonzentrationen; Ionenstärke und Aktivitätskoeffizienten.
- Wasseranteil, Feststoff-/SiO2-Gehalt, Anfangsvolumen und Dichte.
- pH(t), gelöstes Silicium, Silikat-Spezies, Übersättigung und chemischer Reaktionsfortschritt.

Die Rezepturgrößen sind Eingaben; pH, Speziation und Übersättigung sind daraus resultierende Zustände. Säure- und Basenroute werden getrennt parametrisiert und validiert.

### B. Temperatur, Mischung und Alterung

- Gelinnentemperatur T_g(t), nicht nur Bad-/Ofentemperatur; gegebenenfalls Temperaturgradienten.
- Mischerdrehzahl, Leistungs-/Energieeintrag, Scherhistorie, Zugabereihenfolge und Zugabezeit.
- Zeitnullpunkt t0 (Mischbeginn, Gelpunkt oder Beginn der freien Synärese) explizit definieren.
- Alterungszeit vor Entlastung/Start der Synärese und thermische Vorgeschichte.

Temperaturabhängige Raten dürfen beispielsweise Arrhenius-Formen besitzen,
[
k_j(T_g)=k_{j,ref}exp[-E_{a,j}/R(1/T_g-1/T_{ref})],
]
aber Aktivierungsenergien sind je Mechanismus zu bestimmen. Badtemperatur ist kein Ersatz für gemessene Geltemperatur.

### C. Chemische Netzwerkbildung

- effektive tragende Siloxanbrückendichte B(t), B_infinity und Anfangswert B0;
- Bildungs-/Kondensationsrate k_b und gegebenenfalls reversible Hydrolyse-/Auflösungsrate;
- Anteil gelöstes, kolloidales und netzwerkgebundenes Silicium;
- effektive Kontraktionskopplung Omega_b.

B ist ein mesoskopischer Zustand, nicht unmittelbar gleich der gesamten Si-O-Si-Bindungszahl. Die Bilanz gelöstes + Netzwerk-Si + ausgetretenes Si ist als unabhängige Massenbilanz zu prüfen.

### D. Netzwerkstruktur und Porenraum

- Fraktaldimension D_f samt Auswertungsskala und Messmethode;
- mittlere Kontakt-/Koordinationszahl z und Kontaktverteilung;
- Porosität phi, spezifische Oberfläche, Porengrößen- und insbesondere Porenhalsverteilung;
- Konnektivität, Tortuosität, Perkolationsanteil und Anisotropie;
- Aggregat-/Primärpartikelgrößen und räumliche Heterogenität.

D_f oder z allein bestimmen die Permeabilität nicht eindeutig. Die Verbindung zur Permeabilität muss über Porenraum-/Porenhalsinformation und eine validierte Struktur-Transport-Beziehung laufen.

### E. Kontraktion, Relaxation und Gelmechanik

- nicht relaxierter Kontraktionsanteil sigma und relaxierter Anteil epsilon_r;
- Relaxationsrate k_r und gegebenenfalls Spektrum statt Ein-Rate-Näherung;
- intrinsisches Potenzial q und zugänglicher Anteil eta_a;
- effektiver, für freie natürliche Synärese relevanter Modul K_eff(t);
- viskoelastische Zeit-/Relaxationsspektren, falls eine einzelne Relaxationsrate nicht genügt.

sigma ist in v0.3 eine dimensionslose Kontraktionsvariable, keine Spannung in Pa. Ein echter Spannungszustand benötigt eine zusätzliche konstitutive Beziehung.

### F. Transport und Flüssigkeit

- intrinsische/effective Permeabilität kappa_eff(t), abhängig von Porennetz und Sättigung;
- Viskosität mu(T, Zusammensetzung), Dichte rho und gegebenenfalls Oberflächenspannung gamma;
- Flüssigkeitssättigung, relative Permeabilität und Kapillardruck, sofern Mehrphasen-/Kapillareffekte relevant sind;
- hydraulische Grenzflächen-/Kontaktresistenz R_c und Randbedingungsfaktor C_g;
- Entwässerungslänge L_d und tatsächliche Entwässerungsflächen.

Die reduzierte hydraulische Rate
[
k_h=3600 C_grac{kappa_{eff}K_{eff}}{mu L_d^2}
]
ist eine erste-Moden-Näherung. Bei relevanten Grenzflächenwiderständen, nichtuniformer Geometrie oder zeitabhängiger Permeabilität ist ein räumlich aufgelöstes Transportmodell erforderlich.

### G. Geometrie, Grenzfläche und Umgebung

- Probenform, Volumen, Höhe, Radius und Oberfläche-zu-Volumen-Verhältnis;
- Entwässerungsrand (ein-/zweiseitig, offen/geschlossen), Gefäßmaterial und Rauheit;
- Benetzbarkeit/Kontaktwinkel, Haftung/Slip und Flüssigkeitsfilm an Gefäßwand;
- Luft-/Flüssigkeits-Grenzfläche, Verdunstungsrate, relative Feuchte und Gasfluss;
- äußere mechanische Last: für dieses CCFSM-Naturmodell ist sie null; Versuche mit aufgeprägter Last sind außerhalb des Geltungsbereichs.

### H. Mess- und Beobachtungsparameter

- Definition von S: Volumenschrumpfung, lineare Schrumpfung oder Masse-/Volumenproxy nicht vermischen;
- Proben- und Geltemperatur, Zeitauflösung, Messauflösung und Kalibrierung;
- Unsicherheiten/Kovarianzen der Bilddigitalisierung und der aus Abbildungen abgelesenen Kurven;
- Verdunstungs- und Flüssigkeitsaustrittskorrektur;
- t0, Probenpräparation und Abbruch-/Endpunktkriterien.

## 4. Gleichungsstatus und Freigaberegel

Jede Gleichung erhält einen von vier Statuswerten:

- **GREEN-MATHEMATICAL:** mathematisch hergeleitet/geprüft (Einheiten, Grenzfälle, Invarianten, numerische Konvergenz).
- **GREEN-PHYSICAL:** konstitutive Beziehung durch unabhängige Messungen oder belastbare Literatur für den konkreten Material-/Protokollbereich gestützt.
- **GREEN-EMPIRICAL:** Parameter aus geeigneten Daten geschätzt, Unsicherheit quantifiziert und unabhängige Validierung bestanden.
- **AMBER-HYPOTHESIS / RED-REJECTED:** plausible, aber unvalidierte Hypothese bzw. falsifizierte/inkonsistente Beziehung.

Eine Gleichung ist erst **vollständig GRÜN**, wenn alle drei GREEN-Ebenen (mathematisch, physikalisch, empirisch) erfüllt sind. Ein mathematischer Beweis kann eine falsche Physik nicht grün machen.

## 5. Parameterstatus v0.4

| Block | Im v0.3-Code | v0.4 Register | Wissenschaftlicher Status |
|---|---|---|---|
| Brückenkinetik | ja | erweitert | mathematisch formulierbar; kinetisch unkalibriert |
| pH-/Spezies-/Ionenchemie | nein | vollständig katalogisiert | chemisches Teilmodell und Messungen fehlen |
| Temperaturgeschichte | separates v0.2a | integriert als Eingabegruppe | Geltemperatur und Aktivierungsenergien fehlen |
| Mischung/Alterung | nein | katalogisiert | Prozesshistorie muss gemessen werden |
| D_f / z | ja | erweitert um Porenraum | nur Teilstruktur; keine hydraulische Rückkopplung |
| Relaxation | ja | erweitert | sigma kein echter Spannungszustand; Relaxationsmessung fehlt |
| Permeabilität/Modul | nur gemessene Eingaben | erweitert | Struktur-Transport-Kopplung fehlt |
| Grenzflächen / Verdunstung | nein | katalogisiert | kontrollieren oder separat modellieren |
| Geometrie | nur L_d, C_g | erweitert | reale Entwässerungsrandbedingungen fehlen |
| Messfehler | nein | katalogisiert | Unsicherheitsmodell fehlt |

## 6. Priorisierung: was zuerst in die Gleichungen gehört

**Stufe 1 — zwingend für belastbare Kalibrierung:** Geltemperaturverlauf, pH-Verlauf, Silikat-/Säure-/Basenrezeptur, Ionenstärke bzw. Gegenionen, SiO2-Gehalt, Misch-/Zugabehistorie, Alterung, Probengeometrie/Entwässerung, Viskosität, Permeabilität, effektiver Modul, natürliche Schrumpfung und Flüssigkeitsaustritt.

**Stufe 2 — für mechanistische Kopplung:** zeitabhängige Brücken-/Si-Bilanz, D_f, z, Porosität, Porenhalsverteilung, Konnektivität, Tortuosität, Relaxation/Rheologie, Grenzflächenwiderstand.

**Stufe 3 — nur wenn Messdaten ihre Relevanz zeigen:** Kapillardruck-/Mehrphasenparameter, Benetzung/Kontaktwinkel, anisotrope Permeabilität, breite Relaxationsspektren, detaillierte Aktivitätskoeffizienten und lokale Temperatur-/Konzentrationsfelder.

Die Stufen bedeuten keine physikalische Irrelevanz der späteren Parameter. Sie ordnen die Mess- und Modellierungspriorität nach Einfluss auf die erste quantitativ überprüfbare CCFSM-Fassung.

## 7. Konkrete nächste Modellversion

CCFSM v0.4 sollte zunächst ein **modulares Eingabe- und Zustandsmodell** sein:
- Rezeptur-/Prozesshistorie als protokollierte Eingabe;
- chemische Zustände als Messdaten oder separates chemisches Submodell;
- Netzwerk-/Porenzustände als eigenständige Zustandsgrößen;
- Transportparameter als gemessene Felder oder validierte Struktur-Funktionen;
- natürliche Randbedingungen explizit.

Nicht alle Parameter sollten in eine einzelne empirische Funktion wie (k_b=f(pH,T,c,ldots)) gezwungen werden. Zunächst ist die kausale Trennung nötig, damit Parameter nicht doppelt gezählt und nicht identifizierbare Größen nicht verborgen werden.

**Erfolgskriterium:** Für jeden Einflussparameter ist dokumentiert, ob er Eingabe, Zustand, abgeleitete Größe oder Mess-/Randbedingung ist; über welchen Wirkpfad er S beeinflusst; welche Einheit er hat; welche Messung ihn bestimmt; und ob die Gleichung mathematisch, physikalisch und empirisch grün ist.


## Chemisches Teilmodell (v0.4)

Die chemische ODE-Implementierung und ihre Grenzen sind in [CCFSM_v0.4_CHEMICAL_SUBMODEL_DE.md](CCFSM_v0.4_CHEMICAL_SUBMODEL_DE.md) beschrieben. Monomer-Si, lösliche Oligomere, kondensiertes Netzwerk-Si und tragende Brückenfraktion sind getrennt. Das breite Einflussparameterregister enthält jetzt auch die chemischen Zustände und Koeffizienten. Alle chemischen Raten bleiben unkalibriert.
