# Figure QA

## Figure 3

- Conclusion: SPINE recovers signed local and whole-region response-field
  structure on held-out Spatial Perturb-seq graphs.
- Evidence: whole-region PPP target/SPINE comparison and two representative
  64-cell neighborhoods.
- Source: `main_exp.png`; quantitative claims use all 928 test graphs and 512
  genes.
- Modification: `scripts/relabel_main_experiment_figure.py` changes only text
  in black label strips from legacy labels to `PPP target` and `SPINE`.
  Response pixels, coordinates, stars, and color scales are unchanged.
- Review risk: examples are qualitative; the caption explicitly points to the
  full quantitative benchmark.

## Figure 4

- Conclusion: the formal selector preserves target qualification and achieves a
  modest held-out burden reduction; larger cases are exploratory.
- Evidence: panel D reports TQR 0.6944/0.6944, 12.0% mean spillover reduction,
  absolute decrease 0.1244 [0.0559, 0.1926], and burden-order agreement 0.6250
  [0.6108, 0.6393].
- Source: `source_data/table3_formal_selector.csv` and
  `source_data/selector_formal_three_way.csv`.
- Backend: Python/Matplotlib via
  `scripts/make_selector_prioritization_figure.py`.
- Exports: `selector_application_main.pdf`,
  `selector_application_main.png`, and appendix PDF/PNG.
- Statistical unit: 36 target specifications for formal selector intervals.
- Review risk: panels B-C are discovery-set illustrations and are explicitly
  labeled exploratory in the figure and caption.
