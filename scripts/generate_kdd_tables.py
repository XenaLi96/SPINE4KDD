#!/usr/bin/env python3

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source_data"
GENERATED = ROOT / "generated"


def read_csv(name: str) -> list[dict[str, str]]:
    with (SOURCE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write(name: str, content: str) -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    (GENERATED / name).write_text(content.rstrip() + "\n", encoding="utf-8")


def esc(text: str) -> str:
    return (
        text.replace("&", r"\&")
        .replace("%", r"\%")
        .replace("_", r"\_")
        .replace(" x ", r" $\times$ ")
        .replace("SPINE-", r"\methodname{}-")
        .replace("CCC-GNN", r"CCC--GNN")
        .replace("R2", r"$R^2$")
        .replace(" um", r"\,$\mu$m")
    )


def table1() -> None:
    rows = read_csv("table1_exact_task.csv")
    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\scriptsize",
        r"\caption{\textbf{Exact-task comparison on the original full-development block-held-out benchmark.} This comparison uses the original full-development benchmark. All confirmatory effect estimates use the strict 1,342/837/928 split in \Cref{tab:confirmatory_analysis}.}",
        r"\label{tab:exact_task_main}",
        r"\setlength{\tabcolsep}{5.2pt}",
        r"\begin{tabular}{llrrrr}",
        r"\toprule",
        r"Group & Method & Neighbor $\uparrow$ & Centered $\uparrow$ & Ring $\uparrow$ & MAE $\downarrow$ \\",
        r"\midrule",
    ]
    previous = None
    for row in rows:
        group = esc(row["group"]) if row["group"] != previous else ""
        method = esc(row["method"])
        if row["group"] == "SPINE":
            method = r"\textbf{" + method + "}"
        lines.append(
            f"{group} & {method} & {float(row['neighbor']):.5f} & "
            f"{float(row['centered']):.5f} & {float(row['ring']):.5f} & "
            f"{float(row['mae']):.5f} \\\\"
        )
        previous = row["group"]
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table*}"])
    write("table1_exact_task.tex", "\n".join(lines))


def rows_for(panel: str) -> list[dict[str, str]]:
    return [row for row in read_csv("table2_confirmatory.csv") if row["panel"] == panel]


def table2() -> None:
    a, b, c, d, e = (rows_for(panel) for panel in "ABCDE")
    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\scriptsize",
        r"\caption{\textbf{Confirmatory signal decomposition, benchmark decoupling, and transfer diagnostics.} Panels A, C, and E use the strict three-way spatial split. Pooled Ring correlation and graph-paired lift are different estimands. Partial $R^2=1-\mathrm{SSE}_{\mathrm{full}}/\mathrm{SSE}_{\mathrm{context}}$.}",
        r"\label{tab:confirmatory_analysis}",
        r"\setlength{\tabcolsep}{3.0pt}",
        r"\begin{minipage}[t]{0.49\textwidth}",
        r"\centering",
        r"\textbf{A. Independent spatial split and predictive variance}\\[-0.2em]",
        r"\resizebox{\linewidth}{!}{%",
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Metric & Context & Full & Effect & 95\% CI \\",
        r"\midrule",
    ]
    for row in a:
        lines.append(
            f"{esc(row['item'])} & {row['context'] or '--'} & {row['full'] or '--'} & "
            f"{esc(row['effect']) if row['effect'] else '--'} & {row['ci'] or '--'} \\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"}",
            r"\medskip",
            r"\textbf{B. Direct-effect profile/location factorial}\\[-0.2em]",
            r"\begin{tabular}{lr}",
            r"\toprule",
            r"Input control & Ring Pearson \\",
            r"\midrule",
        ]
    )
    for row in b:
        lines.append(f"{esc(row['item'])} & {row['full']} \\\\")
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\medskip",
            r"\textbf{C. PPP decoupling}\\[-0.2em]",
            r"\begin{tabular}{lrr}",
            r"\toprule",
            r"PPP construction & Paired lift & 95\% CI \\",
            r"\midrule",
        ]
    )
    for row in c:
        lines.append(f"{esc(row['item'])} & {row['effect']} & {row['ci']} \\\\")
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{minipage}",
            r"\hfill",
            r"\begin{minipage}[t]{0.49\textwidth}",
            r"\centering",
            r"\textbf{D. Five-fold guide-OOD seed transfer}\\[-0.2em]",
            r"\resizebox{\linewidth}{!}{%",
            r"\begin{tabular}{lrrrr}",
            r"\toprule",
            r"Seed source & Zero & Seed & Difference & Direction \\",
            r"\midrule",
        ]
    )
    for row in d:
        lines.append(
            f"{esc(row['item'])} & {row['context']} & {row['full']} & "
            f"{row['effect']} & {row['ci']} \\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"}",
            r"\medskip",
            r"\textbf{E. Patch-scale sensitivity}\\[-0.2em]",
            r"\resizebox{\linewidth}{!}{%",
            r"\begin{tabular}{lrrr}",
            r"\toprule",
            r"Patch and median radius & Context & Full & Paired lift \\",
            r"\midrule",
        ]
    )
    for row in e:
        lines.append(
            f"{esc(row['item'])} & {row['context']} & {row['full']} & {row['effect']} \\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"}",
            r"\medskip",
            r"\parbox{0.96\linewidth}{\raggedright \textit{Reading.} Expression-decoupled variants retain positive lift, whereas no-spatial matching does not. Assay-matched spatial seeds improve all five guide-OOD folds; external scRNA seeds underperform zero seed in all five.}",
            r"\end{minipage}",
            r"\end{table*}",
        ]
    )
    write("table2_confirmatory.tex", "\n".join(lines))


def table3() -> None:
    rows = read_csv("table3_formal_selector.csv")
    a = [row for row in rows if row["panel"] == "A"]
    b = [row for row in rows if row["panel"] == "B"][0]
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\scriptsize",
        r"\caption{\textbf{Formal three-way-split perturbation prioritization.} Train, validation, and test partitions are fully separated; target qualification is unchanged relative to target-only. Larger discovery-set reductions and biological examples are exploratory post-hoc analyses in the appendix.}",
        r"\label{tab:selector_main}",
        r"\setlength{\tabcolsep}{2.5pt}",
        r"\resizebox{\columnwidth}{!}{%",
        r"\begin{tabular}{lrrr}",
        r"\toprule",
        r"Method & TQR $\uparrow$ & Spill. red. $\uparrow$ & Abs. burden decrease $\uparrow$ \\",
        r"\midrule",
    ]
    for row in a:
        decrease = row["absolute_burden_decrease"]
        if row["ci"]:
            decrease += " " + row["ci"]
        lines.append(
            f"{esc(row['method'])} & {row['tqr']} & "
            f"{row['mean_spillover_reduction']} & {decrease} \\\\"
        )
    lines.extend(
        [
            r"\midrule",
            r"\multicolumn{4}{l}{\textit{Burden-ranking diagnostic}} \\",
            rf"{esc(b['method'])} & \multicolumn{{3}}{{r}}{{{b['pairwise_burden_order']}}} \\",
            r"\bottomrule",
            r"\end{tabular}",
            r"}",
            r"\end{table}",
        ]
    )
    write("table3_formal_selector.tex", "\n".join(lines))


def appendix_confirmatory() -> None:
    direct = read_csv("direct_effect_factorial.csv")
    guide = read_csv("guide_ood_fivefold.csv")
    external = {row["fold"]: row for row in read_csv("external_seed_propagation.csv")}
    concert = read_csv("concert_pseudodelta.csv")
    reference = read_csv("reference_st_low_data.csv")
    matching = rows_for("C")
    scale = rows_for("E")
    selector = read_csv("table3_formal_selector.csv")

    control_names = {
        "oracle_sender_seed": "Correct profile + correct region",
        "predicted_sender_seed": "Train-guide mean profile + correct region",
        "shuffle_perturbation_gene": "Wrong-guide profile + correct region",
        "shuffle_sender_mask": "Correct profile + relocated near region",
        "shuffle_sender_seed": "Shuffled profile + correct region",
        "noise_sender_seed": "Norm-matched noise profile + correct region",
        "randomize_coordinates": "Correct profile + randomized coordinates",
        "randomize_ccc_edge_scores": "Correct profile + randomized CCC",
        "cell_type_mean_sender_seed": "Global-mean profile + correct region",
        "random_profile_random_region": "Random profile + random region",
    }

    lines = [
        r"\subsection{Strict Three-Way Spatial Split and Confirmatory Estimands}",
        r"\label{app:strict_three_way}",
        r"The confirmatory cache contains 1,342 \texttt{top\_right} training graphs, 837 \texttt{bottom\_left} validation graphs, and 928 \texttt{bottom\_right} test graphs. Spatial partitioning precedes matching, and checkpoint selection uses only validation. Pooled Ring Pearson concatenates test summaries, whereas graph-paired lift averages within-graph full-minus-context changes. Confidence intervals for paired lift resample guides. Predictive partial $R^2$ is $1-\mathrm{SSE}_{\mathrm{full}}/\mathrm{SSE}_{\mathrm{context}}$ and its interval resamples spatial clusters.",
        r"",
        r"\subsection{PPP Matching-Decoupling Audits}",
        r"\label{app:ppp_decoupling_generated}",
        r"\begin{table}[h]",
        r"\centering\scriptsize",
        r"\caption{Within-variant full-minus-context Ring lift. Each residual model is paired with its own context checkpoint on identical graphs and targets; CIs resample guides.}",
        r"\label{tab:app_ppp_decoupling}",
        r"\begin{tabular}{lrr}",
        r"\toprule",
        r"PPP construction & Paired lift & 95\% CI \\",
        r"\midrule",
    ]
    for row in matching:
        lines.append(f"{esc(row['item'])} & {row['effect']} & {row['ci']} \\\\")
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
            r"",
            r"\subsection{Profile--Location Factorial Controls}",
            r"\label{app:profile_location_factorial}",
            r"\begin{table}[h]",
            r"\centering\scriptsize",
            r"\caption{Frozen exact-task direct-effect controls. The sender profile or region is changed without retraining.}",
            r"\label{tab:app_profile_location}",
            r"\begin{tabular}{lrrr}",
            r"\toprule",
            r"Control & Neighbor & Centered & Ring \\",
            r"\midrule",
        ]
    )
    for row in direct:
        lines.append(
            f"{esc(control_names[row['control']])} & "
            f"{float(row['neighbor_pearson']):.4f} & "
            f"{float(row['neighbor_centered_pearson']):.4f} & "
            f"{float(row['prop_ring_pearson']):.4f} \\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
            r"",
            r"\subsection{Patch-Scale Sensitivity}",
            r"\label{app:patch_scale}",
            r"\begin{table}[h]",
            r"\centering\scriptsize",
            r"\caption{Patch scale on the strict spatial split. Radius is the all-split median; lift is graph-paired full minus context.}",
            r"\label{tab:app_patch_scale}",
            r"\begin{tabular}{lrrr}",
            r"\toprule",
            r"Patch and median radius & Context Ring & Full Ring & Paired lift \\",
            r"\midrule",
        ]
    )
    for row in scale:
        lines.append(
            f"{esc(row['item'])} & {row['context']} & {row['full']} & {row['effect']} \\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
            r"",
            r"\subsection{Five-Fold Guide OOD and External scRNA Transfer}",
            r"\label{app:fivefold_seed_transfer}",
            r"\begin{table*}[h]",
            r"\centering\scriptsize",
            r"\caption{Per-fold conditional propagation and cross-assay seed transfer. Observed seeds are measured in the spatial assay; external seeds are estimated from companion dissociated scRNA-seq.}",
            r"\label{tab:app_fivefold_seed_transfer}",
            r"\begin{tabular}{clrrrrrr}",
            r"\toprule",
            r"Fold & Held-out guides & Graphs & Zero Ring & Spatial Ring & $\Delta$ spatial & External Ring & $\Delta$ external \\",
            r"\midrule",
        ]
    )
    for row in guide:
        ext = external[row["fold"]]
        guides = row["heldout_guides"].replace("sgrna_", "").replace(",", ", ")
        lines.append(
            f"{row['fold']} & {esc(guides)} & {row['n_test']} & "
            f"{float(row['zero_ring']):.4f} & {float(row['observed_ring']):.4f} & "
            f"{float(row['observed_minus_zero_ring']):+.4f} & "
            f"{float(ext['external_ring']):.4f} & {float(ext['external_minus_zero_ring']):+.4f} \\\\"
        )
    lines.extend(
        [
            r"\midrule",
            r"Macro & all held-out guides & -- & 0.4400 & 0.4619 & +0.0220 & 0.4130 & -0.0270 \\",
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table*}",
            r"",
            r"\subsection{Official CONCERT Diagnostic}",
            r"\label{app:concert_diagnostic}",
            r"The public CONCERT implementation is evaluated on native spatial-tile holdouts. It predicts expression or counterfactual cell state at new coordinates, not the same sender-conditioned cell-resolved field as \methodname{}; the comparison therefore diagnoses objective alignment rather than defining a common leaderboard.",
            r"\begin{table}[h]",
            r"\centering\scriptsize",
            r"\caption{Guide-versus-control pseudo-delta recovery. CONCERT is below the training-guide mean in all four evaluated contrasts despite strong native reconstruction.}",
            r"\label{tab:app_concert_diagnostic}",
            r"\begin{tabular}{llrr}",
            r"\toprule",
            r"Slide & Perturbation & CONCERT & Guide mean \\",
            r"\midrule",
        ]
    )
    for row in concert:
        lines.append(
            f"{esc(row['sample'])} & {esc(row['perturbation'])} & "
            f"{float(row['aggregate_gene_pearson_concert']):.4f} & "
            f"{float(row['aggregate_gene_pearson_guide_mean']):.4f} \\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
            r"",
            r"\subsection{Reference-ST Low-Data Negative Result}",
            r"\label{app:reference_st_lowdata}",
            r"\begin{table}[h]",
            r"\centering\scriptsize",
            r"\caption{Paired Ring gain from the optional unperturbed reference-ST adapter. The anomalous full-data absolute training run is excluded; only paired gains are interpreted.}",
            r"\label{tab:app_reference_st_lowdata}",
            r"\begin{tabular}{lrr}",
            r"\toprule",
            r"Paired-data fraction & Training graphs & Paired Ring gain \\",
            r"\midrule",
        ]
    )
    for row in reference:
        gain = float(row["reference_minus_no_prior_ring"])
        lines.append(
            f"{float(row['fraction']):.0%}".replace("%", r"\%")
            + f" & {row['n_train']} & {gain:+.4f} \\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
            r"No positive architectural claim is made from these near-zero paired changes.",
            r"",
            r"\subsection{Formal Selector Evaluation}",
            r"\label{app:formal_selector}",
            r"The formal selector freezes the utility model, burden model family, rank-consensus weight, target-retention rule, and top-$k$ operating point using validation. Observed test fields are used only to compute TQR and burden. Target-only and the constrained selector both reach TQR 0.6944; mean relative reduction is 0.1200 and absolute burden decrease is 0.1244 [0.0559, 0.1926] across 36 target specifications. The standalone \methodname{} context spillover head reaches pairwise burden-order agreement 0.6250 [0.6108, 0.6393].",
        ]
    )
    assert len(selector) == 3
    write("appendix_confirmatory.tex", "\n".join(lines))


def main() -> None:
    table1()
    table2()
    table3()
    appendix_confirmatory()


if __name__ == "__main__":
    main()
