# Result Classification

## Strict Confirmatory

These results use fully separated train, validation, and test regions or the
formal grouped-guide protocol:

- Strict spatial split: 1,342/837/928 graphs.
- Context/full pooled Ring: 0.3626/0.4111.
- Graph-paired Ring lift: +0.0532 [0.0474, 0.0586].
- Predictive context/full R2: 0.3712/0.4669; partial R2: 0.1521
  [0.1476, 0.1559].
- PPP matching-decoupling and patch-scale analyses.
- Five-fold guide OOD with assay-matched and external scRNA seeds.
- Formal selector: TQR 0.6944, mean spillover reduction 0.1200, and absolute
  burden decrease 0.1244 [0.0559, 0.1926].
- Pairwise burden-order agreement: 0.6250 [0.6108, 0.6393].

## Original Exact Task

These model-comparison and frozen-input diagnostics use the original
full-development block-held-out benchmark:

- Fourteen-method exact-task Table 1.
- SPINE-Core and SPINE-Refine comparison.
- Direct-effect profile/location factorial and randomized-CCC controls.
- Historical development ablations and aggregate gene-space results.

They support method comparison and mechanism diagnosis, but are not used as
strict confirmatory effect estimates.

## Exploratory Post Hoc

These results illustrate mechanisms or external plausibility:

- Legacy discovery-selector reductions of 0.354, 0.418, and oracle 0.672.
- TGF-beta/stroma, vascular-stress, and myeloid-activation selector cases.
- Perturb-FISH module-level prioritization support.
- De novo IFN-gamma mouse-brain deployment.
- Historical reference-ST mining and development blend sweeps.

The manuscript does not use these analyses as confirmatory or prospective
effect estimates.
