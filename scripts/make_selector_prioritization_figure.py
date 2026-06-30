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
            ("harmful", 1.456936, 0.777966),
        ],
        columns=["component", "target_only", "selector"],
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
            ("reliable", 39, 0.718, 0.151, 0.207, 0.851),
            ("all", 64, 0.641, 0.137, 0.218, 0.851),
        ],
        columns=["subset", "specs", "tqr", "burden_reduction", "obs_u_pred_s_reduction", "pairwise_safety"],
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


def write_source_data(out_dir: Path) -> None:
    source_dir = out_dir / "source_data"
    source_dir.mkdir(parents=True, exist_ok=True)
    case_df().to_csv(source_dir / "selector_case_summary.csv", index=False)
    burden_df().to_csv(source_dir / "selector_tgfb_burden_decomposition.csv", index=False)
    operating_df().to_csv(source_dir / "selector_operating_points.csv", index=False)
    perturb_fish_df().to_csv(source_dir / "selector_perturb_fish_support.csv", index=False)
    calibration_df().to_csv(source_dir / "selector_calibration_deciles.csv", index=False)


def panel_title(ax: plt.Axes, letter: str, title: str) -> None:
    ax.set_title(f"{letter}. {title}", loc="left", pad=4, color=TEXT)


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
    panel_title(ax, "A", "SPINE drug selector")
    draw_box(ax, (0.50, 0.76), "SPINE\nfields", LIGHT, w=0.58, h=0.20, fontsize=5.5)
    draw_box(ax, (0.50, 0.49), "score U\nand S", LIGHT, w=0.68, h=0.20, fontsize=5.5)
    draw_box(ax, (0.50, 0.21), "select action:\nlow burden,\ntarget kept", SELECTOR_LIGHT, w=0.74, h=0.24, fontsize=5.1)
    arrows = [((0.50, 0.66), (0.50, 0.59)), ((0.50, 0.38), (0.50, 0.33))]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, xycoords=ax.transAxes, arrowprops={"arrowstyle": "->", "lw": 0.8, "color": TEXT})

def plot_case_arrows(ax: plt.Axes) -> None:
    ax.set_box_aspect(1)
    df = case_df()
    offsets = [-0.6, 0.0, 0.6]
    ax.axhline(90, color="#B9C1C8", lw=0.8, ls="--")
    ax.scatter([0], [100], s=34, color=TARGET, zorder=3)
    label_offsets = {
        "TGF$\\beta$/stroma": (1.1, -0.55),
        "Vascular stress": (1.1, 0.55),
        "Myeloid activation": (1.1, -0.65),
    }
    for offset, (_, row) in zip(offsets, df.iterrows()):
        y0 = 100.0 + offset
        y1 = row["target_retention_pct"]
        x1 = row["burden_reduction_pct"]
        ax.annotate("", xy=(x1, y1), xytext=(0, y0), arrowprops={"arrowstyle": "->", "lw": 1.0, "color": SELECTOR, "alpha": 0.8})
        ax.scatter([x1], [y1], s=40, color=SELECTOR, edgecolor="white", linewidth=0.5, zorder=4)
        dx, dy = label_offsets[row["target"]]
        label = row["target"]
        ax.text(x1 + dx, y1 + dy, label, ha="left", va="center", fontsize=5.2, color=TEXT)
    ax.text(2.2, 89.7, "90% retention", fontsize=5.0, color="#59636E", va="top")
    ax.set_xlim(-3, 58)
    ax.set_ylim(86.8, 102.0)
    ax.set_xlabel("Burden reduction (%)")
    ax.set_ylabel("Target retention (%)")
    ax.grid(axis="both", color=GRID, lw=0.45, alpha=0.7)
    panel_title(ax, "B", "Target kept, burden reduced")


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
    ax.text(0.53, 3.12, "selector", color=SELECTOR, fontsize=5.2, ha="left", va="center")
    panel_title(ax, "C", "TGF$\\beta$/stroma burden split")


def plot_checks(ax: plt.Axes) -> None:
    ax.set_box_aspect(1)
    cal = calibration_df()
    for split, color in [("main block", SELECTOR), ("strict guide", STRICT)]:
        subset = cal[cal["split"] == split]
        ax.plot(subset["pred_decile"], subset["observed_tqr"], marker="o", lw=1.4, ms=2.8, color=color, label=split)
    ax.set_xlim(1, 10.8)
    ax.set_ylim(0, 0.63)
    ax.set_xticks([1, 5, 10])
    ax.set_xlabel("Predicted utility decile")
    ax.set_ylabel("Observed TQR")
    ax.grid(axis="y", color=GRID, lw=0.45, alpha=0.7)
    ax.legend(loc="lower right", fontsize=4.9, handlelength=1.2, borderpad=0.1)
    ax.text(
        0.04,
        0.95,
        "Spatial selector:\nTQR 0.64 / burden -35%\nPerturb-FISH:\nTQR 0.72 / safety 0.85",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=4.8,
        color="#59636E",
    )
    panel_title(ax, "D", "Support and calibration boundary")


def make_figure(out_png: Path, out_pdf: Path | None, source_out_dir: Path) -> None:
    configure_matplotlib()
    write_source_data(source_out_dir)
    fig = plt.figure(figsize=(3.55, 3.65), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0])
    plot_selector_workflow(fig.add_subplot(gs[0, 0]))
    plot_case_arrows(fig.add_subplot(gs[0, 1]))
    plot_burden_dumbbell(fig.add_subplot(gs[1, 0]))
    plot_checks(fig.add_subplot(gs[1, 1]))
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=450, bbox_inches="tight")
    if out_pdf is not None:
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_pdf, bbox_inches="tight", metadata=PDF_METADATA)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the compact SPINE drug-selector appendix figure.")
    parser.add_argument(
        "--png",
        type=Path,
        default=ROOT / "appendix_image" / "selector_prioritization_appendix.png",
        help="PNG output path.",
    )
    parser.add_argument(
        "--pdf",
        type=Path,
        default=ROOT / "appendix_image" / "selector_prioritization_appendix.pdf",
        help="PDF output path. Use an empty string to skip PDF output.",
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
    out_pdf = None if str(args.pdf) == "" else args.pdf
    make_figure(args.png, out_pdf, args.source_out)


if __name__ == "__main__":
    main()
