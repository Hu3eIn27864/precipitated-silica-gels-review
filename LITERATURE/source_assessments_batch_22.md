# Source assessment batch 22 — MD model of precipitated-silica consolidation

## PSG-004 — Sahabi & Kind (2011)

**Reference:** Sahabi, H. & Kind, M. (2011). “Experimentally Justified Model-Like Description of Consolidation of Precipitated Silica.” *Polymers* 3(4), 2156–2171. DOI: [10.3390/polym3042156](https://doi.org/10.3390/polym3042156). Open KIT full text: https://publikationen.bibliothek.kit.edu/1000033909/3014841

### Scope and modelling architecture
The article develops an MD description of precipitated-silica gel-fragment consolidation and compares it with an earlier MC model and published experimental observations. The industrial process context is sodium silicate plus sulfuric acid, followed by gelation, stirrer fragmentation and consolidation of fragments.

- The simulated fragment is a fractal aggregate of 1,000 primary particles generated using a cluster–cluster aggregation procedure.
- Colloid–colloid and colloid–solvent interactions are represented with integrated Lennard-Jones-type potentials derived from Hamaker interactions; the solvent is represented by a dense lattice of solvent particles.
- A constant-stress ensemble is used for a gel fragment; an isothermal-isobaric ensemble is used for a particle network.
- The paper distinguishes MC ensemble sampling from MD trajectories and motivates MD when time dependence is needed.
- The model network is assembled from repeated clusters to form a macroscopic particulate network representation.

### Comparison with experiments and limitations reported by the authors
1. **Single-fragment structural evolution:** simulated fractal-dimension evolution is compared with Schlomach & Kind (2004). The MD curve agrees less well than the earlier MC result in the intermediate regime. Agreement is obtained only after multiplying the MD time step by a factor of 100 (1 min = 100 simulation steps).
2. **Network consolidation:** an MD network-compression curve is compared with Sahabi & Kind (2011) oedometer data. Agreement is reported after a time-step factor of 10 (1 min = 10 simulation steps).
3. **Interaction potential:** an additional electrostatic repulsion was introduced to create a DLVO interaction variant; the authors report that this variant was not appropriate for the observed consolidation comparison.
4. **Missing fluid transport:** the authors explicitly state that fluid flow through the particle network was neglected and must be included to describe the temporal course more thoroughly; they identify this coupling as future work.

### Relevance to the present review and modelling project
This is a direct historical precedent for modelling consolidation of precipitated-silica fragments with particle-scale interactions. It supports the review narrative that network reorganisation and particle interactions can be modelled at the fragment scale, but it also exposes the key limitation that motivates a coupled multiscale framework: particle rearrangement under stress is not sufficient to describe the kinetics if pore-liquid transport is omitted.

The explicit author acknowledgement of missing fluid flow is especially important. The current project should therefore keep structural relaxation and hydraulic transport as distinct model components, and should not interpret particle-scale MD/MC time as macroscopic syneresis time without a physically justified mapping.

### Evidence lineage and transferability
- This is the same KIT/Kind research lineage as Sahabi & Kind (2011) oedometer study (PSG-003), and it reuses published experimental comparators from Sahabi & Kind (2011) and Schlomach & Kind (2004). The model paper is not an independent experimental replication.
- Its interaction parameters and dimensionless simulation time are not a transferable calibration for the present project unless the original values, solvent representation, boundary conditions and structural initialization are independently reconstructed.
- The apparent agreement after time-step rescaling is not a predictive validation of physical time. The authors themselves identify incomplete interaction assumptions and missing fluid flow.
- The paper's rejection of the tested DLVO variant is specific to that model and comparison; it does not prove that electrostatics are irrelevant to all precipitated-silica chemistries or ionic strengths.

**Evidence class:** A for direct target-material modelling precedent; experimental observations are inherited from the cited KIT research family. Use as a critical modelling precedent, not as a validated parameter source.
