# Experimental geometry audit — Wilhelm & Kind (2015) and Wilhelm (2017)

**Purpose:** distinguish directly reported geometry from calculated estimates and unresolved drainage boundaries before choosing a transport geometry.

## 1. Natural syneresis: cylindrical samples

Wilhelm & Kind (2015), Section 3.2 and Table 1, report cylindrical samples with diameter \(d_{Cyl}=12\,\mathrm{mm}\) and gel volume \(V_{Gel}\approx3\,\mathrm{mL}\). The paper reports the diameter and approximate volume; it does not state a directly measured sample height in that passage.

If—and only if—the sample is treated as a right circular cylinder with uniform 12 mm diameter, the implied initial height is

\[
H_{\mathrm{calc}}=\frac{V}{\pi(d/2)^2}
=\frac{3000\;\mathrm{mm^3}}{\pi(6\;\mathrm{mm})^2}
\approx26.5\;\mathrm{mm}.
\]

This is a **derived geometric estimate**, not a directly reported height. It is useful for a sensitivity analysis, but it must not be silently promoted to a measured dimension. The pycnometer method measures volume by displacement/gravimetry; the complete external drainage boundary and the local geometry of the gel in the vessel still need confirmation from the apparatus description/figure and the cited earlier method.

The 2015 article later explicitly assumes radial flow for its comparison of natural and enforced syneresis and uses (r_{cyl}=d_{cyl}/2=6\,\mathrm{mm}) as the characteristic drainage length. That is a **published modelling assumption** and should be reproduced when reproducing the authors’ comparison. It is not the same as independent experimental verification that axial drainage is negligible. Therefore, use the radial model as the primary reproduction of the paper’s assumption and treat finite-cylinder end drainage as a separate sensitivity case, not as a replacement assumption.

## 2. Natural syneresis: approximately 3 mm droplets

The paper reports \(d_{Drop}\approx3\,\mathrm{mm}\), optical observation from top and side views, and a PMMA measurement cell whose sample areas are sealed with cover glasses. It also notes that droplets are first held at 20 °C for the first 20 minutes, then transferred to the cell and brought to the target temperature.

Thus, the reported nominal droplet size alone does **not** establish a freely suspended sphere with a uniformly drained spherical boundary. Confinement/contact against the cell and cover glasses may affect shape and drainage. A sphere first-mode conversion is therefore a sensitivity comparator only, not a validated geometric interpretation of these data.

The temperature history is a further confounder: the paper explicitly attributes part of the similar early curves at 40 and 60 °C to the initial period at 20 °C and subsequent heating of the droplets.

## 3. Forced syneresis: pressure cell versus centrifugation

The 2015 pressure-cell experiments use an initial sample height of 16 mm for the main table and a membrane/filter-plate assembly. The 2017 dissertation's centrifugal data use \(h_0=20\,\mathrm{mm}\) and define equivalent pressure by averaging the centrifugal body force over the initial sample height. These are distinct loading geometries and should remain separate datasets.

The dissertation explicitly discusses a membrane-related additional hydraulic resistance in pressure-cell experiments. Hence a fitted \(\tau\) can include sample drainage, boundary/membrane resistance and evolving gel mechanics; it should not be interpreted as an intrinsic permeability measurement.

## 4. Data status and next extraction action

- **Directly reported:** 12 mm cylinder diameter; approximate 3 mL gel volume; approximate 3 mm droplet size; sample cell uses cover glasses; target temperature follows an initial 20 °C droplet period; 16 mm pressure-cell height; 20 mm centrifugal sample height.
- **Calculated, assumption-dependent:** approximately 26.5 mm cylinder height from \(V=3\,\mathrm{mL}\) and \(d=12\,\mathrm{mm}\), assuming a right circular cylinder.
- **Unresolved:** actual gel shape in the pycnometer; whether the side and both ends are effectively drained; droplet contact geometry; effective drainage length; any contact or external flow resistance.
- **Required before calibration:** source-figure digitisation with uncertainty estimates; apparatus-boundary verification; separate model calibration and held-out comparison.

## Primary sources

- Wilhelm, S.; Kind, M. *Influence of pH, Temperature and Sample Size on Natural and Enforced Syneresis of Precipitated Silica*. Polymers 2015, 7, 2504–2521. DOI: 10.3390/polym7121528. Open full text: https://www.mdpi.com/2073-4360/7/12/2504
- Wilhelm, S. *Über die Synärese kolloidaler Strukturen am Beispiel von Siliciumdioxid*. KIT dissertation, 2017. DOI: 10.5445/KSP/1000073100. Open full text: https://publikationen.bibliothek.kit.edu/1000073100/4718247
