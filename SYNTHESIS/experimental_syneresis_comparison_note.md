# Quantitative comparison of the extracted syneresis fit parameters

## Scope

This note analyses the 18 records in
`LITERATURE/experimental_syneresis_comparison.csv`. The natural-syneresis
records are empirical `S_max, tau` fit parameters from Wilhelm & Kind (2015),
not digitised raw curves. The forced-syneresis records are additional
centrifugation results from Wilhelm (2017); their reported equivalent
pressure is a height-averaged centrifugal body-force approximation, not a
uniform applied pressure. The two protocols are not pooled.

## Descriptive contrasts

For the natural-syneresis cylinder series (reported diameter 12 mm), the
base/acid ratio of fitted time constants is 2.35, 2.74 and 5.50 at 20, 40
and 60 °C, respectively. The base-minus-acid difference in fitted ultimate
shrinkage is +0.10, +0.19 and +0.31. Thus, within this cylinder protocol,
the base gel has a longer fitted time scale and larger fitted shrinkage at
each reported temperature.

For the approximately 3 mm droplet series, the corresponding base/acid
time-constant ratios are 1.68, 0.89 and 1.23, while base-minus-acid
differences in fitted ultimate shrinkage are -0.07, -0.02 and +0.03.
The ordering is therefore not the same as in the cylinder series. Droplet
shape, contact/drainage boundaries and thermal preparation history are
insufficiently constrained to attribute this contrast to an intrinsic
geometry-independent material coefficient.

For the 20 °C centrifugation series, base/acid fitted time-constant ratios
at equivalent pressures 0.10, 0.26 and 0.39 bar are 1.28, 1.39 and 0.90;
base-minus-acid ultimate-shrinkage differences are +0.37, +0.34 and +0.33.
The non-monotonic time-constant response at the highest pressure is retained
as reported, not smoothed or forced into a monotonic law.

## Interpretation

1. The acid/base ordering depends on specimen/protocol class. A universal
   statement such as "base gels always synerese faster" is not supported by
   these fitted parameters.
2. The much shorter droplet time constants cannot be interpreted as a
   direct permeability increase without a validated droplet geometry,
   boundary conditions, and a mechanical constitutive response.
3. A fitted single-exponential `tau` is not by itself a measured
   diffusivity. Converting it to an apparent first-mode diffusivity is
   conditional on a diffusion eigenmode being the correct physical model.
4. The cylinder's reported diameter alone does not establish its height or
   end drainage. The finite-cylinder first-mode expression is therefore a
   sensitivity/limiting-case tool, not a calibration route for these data.
5. The centrifugation pressure is not a spatially uniform external load and
   should not be merged with natural-syneresis records.

## Modelling consequence

The current evidence justifies geometry- and protocol-specific forward
models and separate hydraulic/mechanical state variables. It does not yet
justify fitting a common material diffusivity, extracting intrinsic
permeability, or assigning pH-specific constitutive laws. The next
experimental-data gate is recovery of specimen dimensions, boundary
conditions, raw time series and independent mechanical/hydraulic data.
