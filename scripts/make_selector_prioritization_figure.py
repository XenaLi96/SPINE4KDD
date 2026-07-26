#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib as mpl  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib"))


TARGET = "#7A8796"
SELECTOR = "#1B9E8A"
ACCENT = "#D07A2D"
STRICT = "#7A4EAB"
TEXT = "#1F2933"
GRID = "#D7DCE2"
LIGHT = "#F2F5F7"
SELECTOR_LIGHT = "#DDF2EC"
CASE_ORDER = ["TGF$\\beta$/stroma", "Vascular stress", "Myeloid activation"]
BURDEN_COMPONENTS = ["weighted", "far-field", "off-program", "undesirable"]
PDF_METADATA = {
    "Creator": "SPINE4KDD/scripts/make_selector_prioritization_figure.py",
    "Producer": "Matplotlib",
    "CreationDate": datetime(2026, 6, 30, tzinfo=timezone.utc),
    "ModDate": datetime(2026, 6, 30, tzinfo=timezone.utc),
}


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "font.size": 6.3,
            "axes.titlesize": 7,
            "axes.labelsize": 6.3,
            "xtick.labelsize": 5.7,
            "ytick.labelsize": 5.7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.7,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "legend.frameon": False,
        }
    )


def case_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("TGF$\\beta$/stroma", "near down", "rraga", "oligo2", 97.9076, 49.7128),
            ("Vascular stress", "near down", "rraga", "clu", 99.8073, 24.4440),
            ("Myeloid activation", "far up", "Cfap410", "stk39", 89.2837, 24.3860),
        ],
        columns=[
            "target",
            "ring_direction",
            "target_only_guide",
            "selector_guide",
            "target_retention_pct",
            "burden_reduction_pct",
        ],
    )


def burden_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("weighted", 1.187680, 0.597251),
            ("far-field", 1.212523, 0.604024),
            ("off-program", 1.228201, 0.614737),
            ("undesirable", 1.456936, 0.777966),
        ],
        columns=["component", "target_only", "selector"],
    )


def burden_full_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("TGF$\\beta$/stroma", "target-only", 5.074, 1.188, 1.213, 1.228, 1.457),
            ("TGF$\\beta$/stroma", "selector", 4.968, 0.597, 0.604, 0.615, 0.778),
            ("Vascular stress", "target-only", 2.734, 1.278, 1.213, 1.347, 1.655),
            ("Vascular stress", "selector", 2.729, 0.965, 0.892, 1.024, 1.380),
            ("Myeloid activation", "target-only", 1.578, 0.717, 0.918, 0.742, 0.811),
            ("Myeloid activation", "selector", 1.409, 0.542, 0.651, 0.550, 0.657),
        ],
        columns=["target", "role", "target_score", "weighted", "far-field", "off-program", "undesirable"],
    )


def operating_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("clean weighted", 5286, 36, 0.639, 0.354),
            ("off-program", 5286, 36, 0.667, 0.362),
            ("rank-consensus", 5286, 36, 0.620, 0.418),
            ("observed oracle", 5286, 36, 1.000, 0.672),
        ],
        columns=["setting", "actions", "specs", "tqr", "burden_reduction"],
    )


def perturb_fish_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("reliable", 39, 0.718, 0.151, 0.207, 0.874),
            ("all", 64, 0.641, 0.137, 0.218, 0.851),
        ],
        columns=["subset", "specs", "tqr", "burden_reduction", "obs_u_pred_s_reduction", "lower_burden_agreement"],
    )


def calibration_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("main block", 1, 0.042802),
            ("main block", 2, 0.074828),
            ("main block", 3, 0.105657),
            ("main block", 4, 0.131138),
            ("main block", 5, 0.163424),
            ("main block", 6, 0.204430),
            ("main block", 7, 0.262575),
            ("main block", 8, 0.313679),
            ("main block", 9, 0.404669),
            ("main block", 10, 0.574978),
            ("strict guide", 1, 0.053471),
            ("strict guide", 2, 0.079250),
            ("strict guide", 3, 0.119854),
            ("strict guide", 4, 0.174181),
            ("strict guide", 5, 0.170260),
            ("strict guide", 6, 0.236068),
            ("strict guide", 7, 0.243349),
            ("strict guide", 8, 0.318398),
            ("strict guide", 9, 0.381406),
            ("strict guide", 10, 0.461366),
        ],
        columns=["split", "pred_decile", "observed_tqr"],
    )


def formal_selector_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("target-only", 0.6944, 0.0000, np.nan, np.nan),
            ("selector", 0.6944, 0.1244, 0.0559, 0.1926),
        ],
        columns=["method", "tqr", "burden_decrease", "ci_low", "ci_high"],
    )


def write_source_data(out_dir: Path) -> None:
    source_dir = out_dir / "source_data"
    source_dir.mkdir(parents=True, exist_ok=True)
    case_df().to_csv(source_dir / "selector_case_summary.csv", index=False)
    burden_df().to_csv(source_dir / "selector_tgfb_burden_decomposition.csv", index=False)
    burden_full_df().to_csv(source_dir / "selector_burden_decomposition.csv", index=False)
    operating_df().to_csv(source_dir / "selector_operating_points.csv", index=False)
    perturb_fish_df().to_csv(source_dir / "selector_perturb_fish_support.csv", index=False)
    calibration_df().to_csv(source_dir / "selector_calibration_deciles.csv", index=False)
    formal_selector_df().to_csv(source_dir / "selector_formal_three_way.csv", index=False)


def panel_title(ax: plt.Axes, letter: str, title: str, fontsize: float | None = None) -> None:
    kwargs = {"fontsize": fontsize} if fontsize is not None else {}
    ax.set_title(f"{letter}. {title}", loc="left", pad=4, color=TEXT, **kwargs)


def draw_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    text: str,
    fc: str,
    w: float = 0.36,
    h: float = 0.16,
    fontsize: float = 5.4,
) -> None:
    x, y = xy
    rect = mpl.patches.FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle="round,pad=0.025,rounding_size=0.025",
        fc=fc,
        ec="#9AA5AD",
        lw=0.75,
        transform=ax.transAxes,
    )
    ax.add_patch(rect)
    ax.text(x, y, text, transform=ax.transAxes, ha="center", va="center", fontsize=fontsize, color=TEXT)


def plot_selector_workflow(ax: plt.Axes) -> None:
    ax.axis("off")
    ax.set_box_aspect(1)
    panel_title(ax, "A", "Intervention prioritization")
    box_w = 0.72
    box_h = 0.18
    centers = [0.78, 0.50, 0.22]
    draw_box(ax, (0.50, centers[0]), "SPINE\nfields", LIGHT, w=box_w, h=box_h, fontsize=5.4)
    draw_box(ax, (0.50, centers[1]), "score\nU and S", LIGHT, w=box_w, h=box_h, fontsize=5.4)
    draw_box(ax, (0.50, centers[2]), "select\nlow burden\ntarget kept", SELECTOR_LIGHT, w=box_w, h=box_h, fontsize=4.9)
    arrows = [((0.50, centers[0] - box_h / 2 - 0.01), (0.50, centers[1] + box_h / 2 + 0.01)),
              ((0.50, centers[1] - box_h / 2 - 0.01), (0.50, centers[2] + box_h / 2 + 0.01))]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, xycoords=ax.transAxes, arrowprops={"arrowstyle": "->", "lw": 0.8, "color": TEXT})

def plot_case_arrows(ax: plt.Axes) -> None:
    ax.set_box_aspect(1)
    df = case_df()
    offsets = [-0.6, 0.0, 0.6]
    ax.axhline(90, color="#B9C1C8", lw=0.8, ls="--")
    ax.scatter([0], [100], s=34, color=TARGET, zorder=3)
    label_offsets = {
        "TGF$\\beta$/stroma": (-1.2, -1.0, "right"),
        "Vascular stress": (1.4, 0.75, "left"),
        "Myeloid activation": (2.3, -0.75, "left"),
    }
    for offset, (_, row) in zip(offsets, df.iterrows()):
        y0 = 100.0 + offset
        y1 = row["target_retention_pct"]
        x1 = row["burden_reduction_pct"]
        ax.annotate("", xy=(x1, y1), xytext=(0, y0), arrowprops={"arrowstyle": "->", "lw": 1.0, "color": SELECTOR, "alpha": 0.8})
        ax.scatter([x1], [y1], s=40, color=SELECTOR, edgecolor="white", linewidth=0.5, zorder=4)
        dx, dy, ha = label_offsets[row["target"]]
        label = row["target"]
        ax.text(x1 + dx, y1 + dy, label, ha=ha, va="center", fontsize=5.2, color=TEXT)
    ax.text(1.2, 90.25, "90% retention", fontsize=5.0, color="#59636E", va="bottom")
    ax.set_xlim(-3, 58)
    ax.set_ylim(86.8, 102.0)
    ax.set_xlabel("Burden reduction (%)")
    ax.set_ylabel("Target retention (%)")
    ax.grid(axis="both", color=GRID, lw=0.45, alpha=0.7)
    panel_title(ax, "B", "Exploratory post-hoc cases")


def plot_burden_dumbbell(ax: plt.Axes) -> None:
    ax.set_box_aspect(1)
    df = burden_df().iloc[::-1].reset_index(drop=True)
    y = np.arange(len(df))
    for i, row in df.iterrows():
        ax.hlines(i, row["selector"], row["target_only"], color="#C7CED6", lw=1.6, zorder=1)
        ax.annotate("", xy=(row["selector"], i), xytext=(row["target_only"], i), arrowprops={"arrowstyle": "->", "lw": 1.0, "color": SELECTOR, "alpha": 0.9})
    ax.scatter(df["target_only"], y, color=TARGET, s=28, zorder=3, label="target-only")
    ax.scatter(df["selector"], y, color=SELECTOR, s=34, zorder=4, label="SPINE selector")
    ax.set_yticks(y)
    ax.set_yticklabels(df["component"])
    ax.set_xlabel("Burden score")
    ax.set_xlim(0.42, 1.58)
    ax.set_ylim(-0.35, 3.45)
    ax.grid(axis="x", color=GRID, lw=0.45, alpha=0.7)
    ax.text(1.15, 3.34, "target-only", color=TARGET, fontsize=5.2, ha="left", va="center")
    ax.text(0.46, 3.34, "selector", color=SELECTOR, fontsize=5.2, ha="left", va="center")
    panel_title(ax, "C", "Exploratory case decomposition", fontsize=6.0)


def plot_formal_selector(ax: plt.Axes) -> None:
    ax.set_box_aspect(1)
    ax.axis("off")
    panel_title(ax, "D", "Formal held-out result", fontsize=6.0)

    ax.text(0.03, 0.83, "Target-qualified rate", transform=ax.transAxes, fontsize=5.2, color=TEXT)
    x0, x1 = 0.08, 0.44
    bar_w = 0.23
    scale = 0.25
    for x, label, color in [(x0, "target-only", TARGET), (x1, "selector", SELECTOR)]:
        rect = mpl.patches.Rectangle(
            (x, 0.55),
            bar_w,
            scale * 0.6944,
            transform=ax.transAxes,
            facecolor=color,
            edgecolor="none",
        )
        ax.add_patch(rect)
        ax.text(x + bar_w / 2, 0.525, label, transform=ax.transAxes, ha="center", va="top", fontsize=4.8)
        ax.text(x + bar_w / 2, 0.55 + scale * 0.6944 + 0.012, "0.6944", transform=ax.transAxes, ha="center", va="bottom", fontsize=5.2, fontweight="bold")

    ax.text(0.82, 0.75, "Mean spillover\nreduction", transform=ax.transAxes, ha="center", va="top", fontsize=4.8, color=TEXT)
    ax.text(0.82, 0.59, "12.0%", transform=ax.transAxes, ha="center", va="center", fontsize=7.5, fontweight="bold", color=SELECTOR)

    ax.text(0.03, 0.42, "Absolute burden decrease", transform=ax.transAxes, fontsize=5.2, color=TEXT)
    bx0, bx1 = 0.03, 0.97
    bmin, bmax = 0.0, 0.22
    y = 0.30
    map_x = lambda value: bx0 + (value - bmin) / (bmax - bmin) * (bx1 - bx0)
    ax.plot([map_x(0.0559), map_x(0.1926)], [y, y], transform=ax.transAxes, color=SELECTOR, lw=1.7)
    ax.plot([map_x(0.0559), map_x(0.0559)], [y - 0.025, y + 0.025], transform=ax.transAxes, color=SELECTOR, lw=0.9)
    ax.plot([map_x(0.1926), map_x(0.1926)], [y - 0.025, y + 0.025], transform=ax.transAxes, color=SELECTOR, lw=0.9)
    ax.scatter([map_x(0.1244)], [y], transform=ax.transAxes, s=27, color=SELECTOR, edgecolor="white", linewidth=0.4, zorder=3)
    ax.text(map_x(0.1244), y + 0.045, "0.1244", transform=ax.transAxes, ha="center", va="bottom", fontsize=5.2, fontweight="bold")
    ax.text(0.50, 0.19, "95% CI [0.0559, 0.1926]", transform=ax.transAxes, ha="center", va="center", fontsize=4.8, color="#59636E")
    ax.text(0.50, 0.075, "burden-order agreement\n0.6250 [0.6108, 0.6393]", transform=ax.transAxes, ha="center", va="center", fontsize=4.55, color=TEXT)


def plot_appendix_overview(ax: plt.Axes) -> None:
    ax.axis("off")
    panel_title(ax, "A", "Selector interface and audit scale")
    draw_box(ax, (0.50, 0.74), "SPINE\nresponse fields", LIGHT, w=0.60, h=0.17, fontsize=6.0)
    draw_box(ax, (0.50, 0.51), "target utility U\nin requested ring", LIGHT, w=0.72, h=0.16, fontsize=5.7)
    draw_box(ax, (0.50, 0.30), "collateral burden S\nfar-field / off-program / undesirable", LIGHT, w=0.82, h=0.15, fontsize=5.1)
    draw_box(ax, (0.50, 0.10), "rank target-retaining\nlow-burden actions", SELECTOR_LIGHT, w=0.76, h=0.15, fontsize=5.6)
    for start, end in [((0.50, 0.65), (0.50, 0.60)), ((0.50, 0.43), (0.50, 0.38)), ((0.50, 0.22), (0.50, 0.18))]:
        ax.annotate("", xy=end, xytext=start, xycoords=ax.transAxes, arrowprops={"arrowstyle": "->", "lw": 0.8, "color": TEXT})
    ax.text(
        0.50,
        0.93,
        "5,286 actions / 36 target specs\nobserved fields used only for evaluation",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=5.4,
        color="#59636E",
    )


def plot_appendix_cases(ax: plt.Axes) -> None:
    df = case_df().iloc[::-1].reset_index(drop=True)
    y = np.arange(len(df))
    ax.axvline(90, color="#B9C1C8", lw=0.8, ls="--")
    ax.axvline(0, color="#B9C1C8", lw=0.8)
    ax.scatter(df["target_retention_pct"], y + 0.13, color=TARGET, s=38)
    ax.scatter(df["burden_reduction_pct"], y - 0.13, color=SELECTOR, s=38)
    for i, row in df.iterrows():
        ax.text(row["target_retention_pct"] - 1.0, i + 0.13, f"{row['target_retention_pct']:.1f}%", ha="right", va="center", fontsize=5.5, color=TARGET)
        ax.text(row["burden_reduction_pct"] + 1.0, i - 0.13, f"{row['burden_reduction_pct']:.1f}%", ha="left", va="center", fontsize=5.5, color=SELECTOR)
    ax.set_yticks(y)
    ax.set_yticklabels(df["target"], fontsize=5.6)
    ax.set_xlim(0, 104)
    ax.set_xlabel("Percent")
    ax.grid(axis="x", color=GRID, lw=0.45, alpha=0.7)
    ax.text(0.03, 0.94, "target retention", transform=ax.transAxes, ha="left", va="center", fontsize=5.2, color=TARGET)
    ax.text(0.03, 0.86, "burden reduction", transform=ax.transAxes, ha="left", va="center", fontsize=5.2, color=SELECTOR)
    panel_title(ax, "B", "Exploratory post-hoc cases")


def plot_appendix_burden_heatmap(ax: plt.Axes) -> None:
    full = burden_full_df()
    reductions = []
    for target in CASE_ORDER:
        target_row = full[(full["target"] == target) & (full["role"] == "target-only")].iloc[0]
        selector_row = full[(full["target"] == target) & (full["role"] == "selector")].iloc[0]
        reductions.append([100.0 * (target_row[c] - selector_row[c]) / target_row[c] for c in BURDEN_COMPONENTS])
    data = np.asarray(reductions)
    im = ax.imshow(data, cmap=mpl.colors.LinearSegmentedColormap.from_list("burden_drop", ["#F7F9FB", "#A7D9D0", SELECTOR]), vmin=0, vmax=55)
    ax.set_xticks(np.arange(len(BURDEN_COMPONENTS)))
    ax.set_xticklabels(BURDEN_COMPONENTS, rotation=30, ha="right")
    ax.set_yticks(np.arange(len(CASE_ORDER)))
    ax.set_yticklabels(CASE_ORDER, fontsize=5.6)
    ax.tick_params(length=0)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j, i, f"{data[i, j]:.0f}%", ha="center", va="center", fontsize=5.4, color=TEXT)
    for spine in ax.spines.values():
        spine.set_visible(False)
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.045, pad=0.025)
    cbar.set_label("Burden reduction", fontsize=5.5)
    cbar.ax.tick_params(labelsize=5, length=2)
    panel_title(ax, "C", "Burden decomposition across cases")


def plot_appendix_operating(ax: plt.Axes) -> None:
    df = operating_df()
    colors = [SELECTOR, "#4BA3C7", "#C77C2B", "#7A8796"]
    ax.scatter(df["tqr"], df["burden_reduction"], s=[54, 54, 54, 62], color=colors, zorder=3)
    offsets = {
        "clean weighted": (0.010, -0.020, "left"),
        "off-program": (0.010, 0.012, "left"),
        "rank-consensus": (0.012, 0.018, "left"),
        "observed oracle": (-0.012, -0.022, "right"),
    }
    for _, row in df.iterrows():
        dx, dy, ha = offsets[row["setting"]]
        ax.text(row["tqr"] + dx, row["burden_reduction"] + dy, row["setting"], fontsize=5.4, ha=ha, va="center")
    ax.set_xlim(0.58, 1.03)
    ax.set_ylim(0.30, 0.72)
    ax.set_xlabel("Target-qualified rate")
    ax.set_ylabel("Burden reduction")
    ax.grid(color=GRID, lw=0.45, alpha=0.7)
    panel_title(ax, "D", "Operating points and oracle gap")


def plot_appendix_perturb_fish(ax: plt.Axes) -> None:
    df = perturb_fish_df()
    metrics = [
        ("tqr", "TQR"),
        ("burden_reduction", "burden\nred."),
        ("obs_u_pred_s_reduction", "obs-U /\npred-S"),
        ("lower_burden_agreement", "pairwise\nagreement"),
    ]
    x = np.arange(len(metrics))
    width = 0.34
    reliable = df[df["subset"] == "reliable"].iloc[0]
    all_specs = df[df["subset"] == "all"].iloc[0]
    ax.bar(x - width / 2, [reliable[k] for k, _ in metrics], width, color=SELECTOR, label="39 reliable specs")
    ax.bar(x + width / 2, [all_specs[k] for k, _ in metrics], width, color="#9AA5AD", label="64 all specs")
    ax.set_xticks(x)
    ax.set_xticklabels([label for _, label in metrics])
    ax.set_ylim(0, 0.95)
    ax.set_ylabel("Score")
    ax.grid(axis="y", color=GRID, lw=0.45, alpha=0.7)
    ax.legend(loc="upper left", fontsize=5.3)
    panel_title(ax, "E", "Perturb-FISH module-level support")


def plot_appendix_calibration(ax: plt.Axes) -> None:
    cal = calibration_df()
    for split, color in [("main block", SELECTOR), ("strict guide", STRICT)]:
        subset = cal[cal["split"] == split]
        ax.plot(subset["pred_decile"], subset["observed_tqr"], marker="o", lw=1.4, ms=3.0, color=color, label=split)
    ax.set_xlim(1, 10)
    ax.set_ylim(0, 0.63)
    ax.set_xticks([1, 5, 10])
    ax.set_xlabel("Predicted utility decile")
    ax.set_ylabel("Observed TQR")
    ax.grid(axis="y", color=GRID, lw=0.45, alpha=0.7)
    ax.legend(loc="upper left", fontsize=5.3)
    ax.text(9.7, 0.575, "0.575", color=SELECTOR, ha="right", va="bottom", fontsize=5.4)
    ax.text(9.7, 0.461, "0.461", color=STRICT, ha="right", va="top", fontsize=5.4)
    panel_title(ax, "F", "Target calibration remains bounded")


def make_compact_figure(out_png: Path, out_pdf: Path | None, source_out_dir: Path) -> None:
    configure_matplotlib()
    write_source_data(source_out_dir)
    fig = plt.figure(figsize=(3.55, 3.65), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0])
    plot_selector_workflow(fig.add_subplot(gs[0, 0]))
    plot_case_arrows(fig.add_subplot(gs[0, 1]))
    plot_burden_dumbbell(fig.add_subplot(gs[1, 0]))
    plot_formal_selector(fig.add_subplot(gs[1, 1]))
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=450, bbox_inches="tight")
    if out_pdf is not None:
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_pdf, bbox_inches="tight", metadata=PDF_METADATA)
    plt.close(fig)


def make_appendix_figure(out_png: Path, out_pdf: Path | None, source_out_dir: Path) -> None:
    configure_matplotlib()
    write_source_data(source_out_dir)
    fig = plt.figure(figsize=(7.15, 5.35), constrained_layout=True)
    gs = fig.add_gridspec(2, 3, width_ratios=[1.0, 1.08, 1.12], height_ratios=[1.0, 1.0])
    plot_appendix_overview(fig.add_subplot(gs[0, 0]))
    plot_appendix_cases(fig.add_subplot(gs[0, 1]))
    plot_appendix_burden_heatmap(fig.add_subplot(gs[0, 2]))
    plot_appendix_operating(fig.add_subplot(gs[1, 0]))
    plot_appendix_perturb_fish(fig.add_subplot(gs[1, 1]))
    plot_appendix_calibration(fig.add_subplot(gs[1, 2]))
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=450, bbox_inches="tight")
    if out_pdf is not None:
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_pdf, bbox_inches="tight", metadata=PDF_METADATA)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the SPINE intervention-prioritization main and appendix figures.")
    parser.add_argument(
        "--main-png",
        type=Path,
        default=ROOT / "selector_application_main.png",
        help="Compact main-text PNG output path.",
    )
    parser.add_argument(
        "--main-pdf",
        type=Path,
        default=ROOT / "selector_application_main.pdf",
        help="Compact main-text PDF output path. Use an empty string to skip PDF output.",
    )
    parser.add_argument(
        "--appendix-png",
        type=Path,
        default=ROOT / "appendix_image" / "selector_prioritization_appendix.png",
        help="Detailed appendix PNG output path.",
    )
    parser.add_argument(
        "--appendix-pdf",
        type=Path,
        default=ROOT / "appendix_image" / "selector_prioritization_appendix.pdf",
        help="Detailed appendix PDF output path. Use an empty string to skip PDF output.",
    )
    parser.add_argument(
        "--source-out",
        type=Path,
        default=ROOT,
        help="Directory that receives source_data/ selector CSV files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    main_pdf = None if str(args.main_pdf) == "" else args.main_pdf
    appendix_pdf = None if str(args.appendix_pdf) == "" else args.appendix_pdf
    make_compact_figure(args.main_png, main_pdf, args.source_out)
    make_appendix_figure(args.appendix_png, appendix_pdf, args.source_out)


if __name__ == "__main__":
    main()
