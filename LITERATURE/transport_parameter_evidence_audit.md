# Transport-parameter evidence audit: permeability and mechanics

**Audit date:** 2026-11-11  
**Question:** Are independent permeability and mechanical data available for the target precipitated-silica gel, rather than merely fitted shrinkage time constants?

## Findings

| Source | Material / protocol | What it contributes | Transferability to syneresis model | Current use |
|---|---|---|---|---|
| Ragueh et al. (2015), *Separation and Purification Technology* 156, 2–11, DOI [10.1016/j.seppur.2015.10.005](https://doi.org/10.1016/j.seppur.2015.10.005) | Industrial precipitated silica aggregates; pressure filtration and osmotic compression of filter cakes; structural length scales | Direct evidence that the hierarchical aggregate network has a pressure-dependent consolidation response; the paper describes a percolation threshold and a cake-scale porous-medium treatment | **High material relevance, limited state/geometry transfer.** A filter cake is not the same initial condition or boundary-value problem as a free-standing wet gel undergoing natural syneresis. Cake permeability/resistance cannot be silently relabelled intrinsic gel permeability | Structural/mechanical trend comparator; extract exact numerical curves only after figure/table and material-grade audit |
| Wilhelm & Kind (2015), *Polymers* 7, 2504–2521, DOI [10.3390/polym7121528](https://doi.org/10.3390/polym7121528) | Sodium-silicate/sulfuric-acid precipitated silica; natural and pressure-cell syneresis | Smax and empirical tau values for natural cylinders/droplets and pressure-cell conditions | **Direct target chemistry**, but tau is an empirical curve parameter, not independently measured permeability or modulus; membrane/filter-plate resistance is part of forced-cell setup | Target observable; do not identify k and M separately from tau |
| Scherer (1989), *J. Non-Cryst. Solids* 108, 28–36, DOI [10.1016/0022-3093(89)90329-3](https://doi.org/10.1016/0022-3093(89)90329-3) | Silica-gel syneresis; abstract reports comparison with independently measured permeability, modulus and viscosity | Demonstrates a viable poro-viscoelastic syneresis strategy and the need for independent material inputs | **Mechanistic comparator only** until gel chemistry and numerical data are checked; not established as industrial precipitated silica | Reproduce only after full numerical inputs and specimen chemistry are recovered |
| Scherer & Swiatek (1989), *J. Non-Cryst. Solids* 113, 119–129, DOI [10.1016/0022-3093(89)90002-1](https://doi.org/10.1016/0022-3093(89)90002-1) | Alkoxide-derived silica-gel sheets; pressure-driven pore-liquid flow | Permeability measurement methodology; acid/base contrast and strong change during partial drying reported in abstract | **Low-to-moderate transferability** because synthesis route differs; no numerical values or uncertainty extracted yet | Method comparator; never copy absolute permeability values into precipitated-silica model |
| Park et al. (2006), *Environmental Science & Technology* 40, 2699–2705, DOI [10.1021/es0515304](https://doi.org/10.1021/es0515304) | Fractal aggregates deposited as membrane filter cakes; batch-cell and confocal microscopy | Links aggregate size, fractal dimension, transmembrane pressure, cake porosity and specific cake resistance; experimental check of collapsed-cake model | **Adjacent filtration comparator**, not precipitated-silica syneresis and not a direct gel permeability dataset | Qualitative structural/transport comparator only |

## Interpretation

1. **No independent target-system pair (permeability plus modulus) has yet been identified** for the exact precipitated-silica gels used in the Wilhelm & Kind syneresis series.
2. The Ragueh study is the strongest bridge from precipitated-silica network structure to pressure-dependent cake consolidation. Its response is useful for constraining qualitative trends, but it does not by itself provide a transferable constitutive law for a syneresing, unconfined gel.
3. Scherer's work shows why independent hydraulic and mechanical measurements matter, but the target chemistry and numerical availability must be verified before quantitative transfer.
4. Consequently, the model should currently be used for (i) mathematical verification, (ii) bounded sensitivity studies, and (iii) predictions of qualitative geometry/pressure trends. It should not yet report fitted target-system intrinsic permeability or modulus.

## Identifiability gate

For a linear poroelastic approximation,

\[
c_v=\frac{K}{m_v\gamma_w}=\frac{K M}{\gamma_w}
\qquad\text{or}\qquad
c_v=\frac{\kappa M}{\mu}.
\]

A single shrinkage curve constrains a lumped transport/mechanical timescale, additionally confounded by geometry and drainage boundaries. At least one independent hydraulic measurement and one independent mechanical measurement are needed to separate permeability from stiffness/compressibility. If either is unavailable, retain a family of admissible parameter pairs rather than selecting one fitted pair.

## Immediate extraction tasks

- Ragueh et al.: map each reported silica grade/sample to structural length scales, pressure range, porosity/solid fraction and cake resistance; resolve the already flagged S3 fractal-dimension table/text discrepancy before using that value.
- Scherer & Swiatek: recover full methods and numerical permeability curves, then mark alkoxide-derived gel values as comparator-only.
- Wilhelm & Kind: digitise measured markers separately from empirical fit curves; retain pressure-cell membrane resistance as a separate apparatus term.
- Do not calibrate the model against a dataset and then call the same dataset an independent validation.


## Additional source-label inconsistencies identified in Ragueh et al. (2015)

A visual inspection of the open PDF tables revealed that the earlier S3 fractal-dimension conflict is not the only transcription hazard. Table 2 prints the material labels as S1, S3, S3 (primary particle diameters 17, 25, 10 nm), while Table 3 and the article's prose identify the three materials as S1, S2, S3. The 25 nm row is likely S2, but the CSV preserves the printed label and marks the likely interpretation as unconfirmed. Table 3 itself reports S3 (D_f=1.8), while the adjacent prose gives 2.2. Both values are retained without resolution.

Table 4 specific resistance is relative to an undisclosed reference (R). One S1 entry at 600 kPa is printed without the (R) symbol; it is flagged rather than silently repaired. This prevents reconstruction of absolute cake permeability from the table alone.


## 2026-11-11 — Derived Ragueh resistance ratios and source-access update

A derived Table 4 comparison is stored in `LITERATURE/ragueh_2015_relative_resistance_analysis.csv`. The reported relative cake resistance rises 45.2% (S1), 60.0% (S2) and 55.8% (S3) from 400 to 600 kPa. At fixed pressure, S1/S3 resistance ratios are 3.25, 2.56 and 3.03. These comparisons remain on the source's relative scale (undisclosed reference R); they are not absolute permeability values. The 600 kPa S1 entry lacks the R symbol in the printed table and is treated as provisional.

A second inspection of the Ragueh PDF confirms the S1/S3/S3 label pattern in Table 1 in addition to Table 2. The middle row is probably S2, but the source does not authorise silent correction. The S3 fractal dimension remains 1.8 in Table 3 versus 2.2 in adjacent prose.

For Wilhelm & Kind (2015), the original publisher image assets are now accessible at 1024-pixel width for Figures 8 and 10 (URLs recorded in `MODELLING/validation_data_roadmap.md`). This removes the previous image-access blocker, although digitisation and pixel/axis uncertainty annotation have not yet been completed. The KIT repository record confirms Open Access availability; its 13 MB PDF endpoint remains beyond the retrieval limit in this environment.


## Ergänzende Primärliteratur: direkte Kopplung von Synerese, Permeabilität und Netzwerkmechanik

### Scherer (1989), *Mechanics of syneresis I: Theory* und *II: Experimental study*

- **Theorie:** Die Syneresegeschwindigkeit hängt von Probengröße, Porenströmungswiderstand und viskoelastischen Netzwerkeigenschaften ab. Ein anfänglich langsamer Schrumpfungsabschnitt kann aus dem allmählichen Aufbau des Porenflüssigkeitsdrucks entstehen.
- **Experiment:** Die Schrumpfungskurven von Silicagelen stimmen laut Abstract vernünftig mit Modellkurven überein, wenn unabhängig bestimmte Permeabilität, Modul und Viskosität eingesetzt werden.
- **Bedeutung:** Ein direkter konzeptioneller Präzedenzfall für die Trennung von hydraulischem Transport und mechanischer Relaxation; unterstützt die Modellarchitektur, nicht die Übertragbarkeit numerischer Parameter auf gefällte Kieselsäure.
- **Systemgrenze:** Alkoxid-abgeleitete Silicagele, nicht industriell gefällte Kieselsäure aus Silikat-Säure-Fällung. Als Mechanismen- und Modellvergleich führen, nicht als Kalibrierdatensatz des Zielsystems.

Bibliographie:
- Scherer, G. W. (1989). Mechanics of syneresis I. Theory. *Journal of Non-Crystalline Solids*, 108(1), 18–27. https://doi.org/10.1016/0022-3093(89)90328-1
- Scherer, G. W. (1989). Mechanics of syneresis II. Experimental study. *Journal of Non-Crystalline Solids*, 108(1), 28–36. https://doi.org/10.1016/0022-3093(89)90329-3

### Scherer & Swiatek (1989), *Measurement of permeability II: Silica gel*

- Permeabilität wurde über einen Druckgradienten in der Porenflüssigkeit dünner (~2 mm) alkoxid-abgeleiteter Gelplatten bestimmt; die geringe Dicke sollte viskoelastische Effekte minimieren.
- Für ein homogenes säurekatalysiertes Gel lag die Permeabilitäts-Größenordnung im Einklang mit Carman–Kozeny. Für ein inhomogenes basenkatalysiertes Gel lag sie höher als vorhergesagt, plausibel aufgrund größerer Poren.
- Teilweises Trocknen verringerte die Permeabilität um ungefähr zwei Größenordnungen.
- **Bedeutung:** Netzwerkheterogenität und Verdichtung können die hydraulische Leitfähigkeit stark verändern; eine einzelne Porositätskennzahl genügt nicht zur zuverlässigen Permeabilitätsbestimmung.
- **Systemgrenze:** Alkoxid-basierte Gele; keine Werte für gefällte Kieselsäure und kein direkter Parametertransfer.

Bibliographie:
- Scherer, G. W. & Swiatek, R. M. (1989). Measurement of permeability II. Silica gel. *Journal of Non-Crystalline Solids*, 113(2–3), 119–129. https://doi.org/10.1016/0022-3093(89)90002-1

### Scherer (1996), *Influence of viscoelasticity and permeability on the stress response of silica gel*

Der Langmuir-Review fasst zusammen, dass die Reaktion von Silicagelen auf mechanische Lasten und Temperaturänderungen sowohl von Permeabilität als auch Modul abhängt; Synerese und Viskoelastizität treten in chemisch aggressiven Flüssigkeiten auf. Er ist ein thematisch passender Langmuir-Vorläufer, ersetzt aber keine unabhängigen Primärdaten für gefällte Kieselsäure.

Bibliographie:
- Scherer, G. W. (1996). Influence of viscoelasticity and permeability on the stress response of silica gel. *Langmuir*, 12(5), 1109–1116. https://doi.org/10.1021/la9503111

### Konsequenz für die Modellstrategie

1. Das 1-D/radiale Konsolidierungsmodell bleibt als Transport-Referenz nützlich, reicht aber allein nicht aus, wenn Gelmodul und Viskosität während der Synerese evolvieren.
2. Die nächste Modellstufe sollte einen zeitabhängigen hydraulischen Parameter \(\kappa(\phi,\mathcal{S})\) und eine zeitabhängige mechanische Antwort \(M(t)\) bzw. ein viskoelastisches Relaxationsmodell getrennt führen. \(\mathcal{S}\) bezeichnet Strukturmerkmale wie Porennetzwerk, Kontaktzahl und Aggregatstruktur; es ist noch keine kalibrierte Zustandsvariable.
3. Erst unabhängige Permeabilitäts- und Rheologie-/Modulmessungen erlauben, beide Beiträge zu identifizieren. Die Schrumpfungskurve allein bleibt eine gekoppelte Antwort.
4. Alkoxid-Silicagel-Daten werden zunächst für qualitative Modellprüfung und dimensionslose Skalierung verwendet; Parametertransfer auf gefällte Kieselsäure ist ohne belegte Vergleichbarkeit von Prozesschemie, Partikelstruktur und Flüssigkeitszusammensetzung nicht zulässig.
