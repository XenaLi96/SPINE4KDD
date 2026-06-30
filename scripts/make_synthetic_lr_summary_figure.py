#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib as mpl  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib"))


NEIGHBOR = "#3F7FB5"
RING = "#D07A2D"
BASELINE = "#8F969E"
ACCENT = "#4B3F72"
GRID = "#D7DCE2"
TEXT = "#1F2933"


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "font.size": 7,
            "axes.titlesize": 8,
            "axes.labelsize": 7,
            "xtick.labelsize": 6,
            "ytick.labelsize": 6,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.7,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "legend.frameon": False,
        }
    )


def main_model_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("Context-only", 0.0033, 0.0062),
            ("Pre alpha=0", 0.0663, 0.1281),
            ("Pre alpha=.75", 0.0692, 0.1320),
            ("Pre alpha=1", 0.0699, 0.1327),
            ("Fine-tuned", 0.6193, 0.8148),
        ],
        columns=["model", "neighbor", "ring"],
    )


def cross_split_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("Main", 0.0033, 0.0062, 0.6193, 0.8148),
            ("Perturbation", 0.0037, 0.0095, 0.2743, 0.5503),
            ("Interface", 0.0038, 0.0076, 0.6070, 0.8056),
            ("Strength", 0.0040, 0.0089, 0.5201, 0.8068),
            ("Host patch", 0.0030, 0.0056, 0.5970, 0.8063),
        ],
        columns=["split", "niche_neighbor", "niche_ring", "trained_neighbor", "trained_ring"],
    )


def mismatch_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("LIANA LR proxy", 0.0739, 0.1022),
            ("Direct distance", 0.0727, 0.0994),
            ("Random ligand-target", 0.2135, 0.3144),
            ("Shuffled direct effect", 0.0357, 0.0359),
        ],
        columns=["simulator", "neighbor", "ring"],
    )


def factor_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("Geometry", "Cluster", 0.4608, 0.8159),
            ("Geometry", "Interface", 0.4491, 0.8011),
            ("Geometry", "Random", 0.3975, 0.7069),
            ("Strength", "0.75", 0.4323, 0.7538),
            ("Strength", "1.25", 0.4391, 0.7931),
            ("Strength", "2.00", 0.4359, 0.7769),
            ("Direct frac.", "0.05", 0.4309, 0.7638),
            ("Direct frac.", "0.10", 0.4407, 0.7854),
            ("Radius", "0.50", 0.4470, 0.7687),
            ("Radius", "1.00", 0.4246, 0.7806),
        ],
        columns=["factor", "setting", "neighbor", "ring"],
    )


def write_source_data(out_dir: Path) -> None:
    source_dir = out_dir / "source_data"
    source_dir.mkdir(parents=True, exist_ok=True)
    main_model_df().to_csv(source_dir / "synthetic_lr_main_models.csv", index=False)
    cross_split_df().to_csv(source_dir / "synthetic_lr_cross_split.csv", index=False)
    factor_df().to_csv(source_dir / "synthetic_lr_factor_breakdown.csv", index=False)
    mismatch_df().to_csv(source_dir / "synthetic_lr_mismatch_null.csv", index=False)


def panel_letter(ax: plt.Axes, letter: str, title: str) -> None:
    ax.set_title(f"{letter}. {title}", loc="left", pad=4, color=TEXT)


def plot_main_models(ax: plt.Axes) -> None:
    df = main_model_df()
    x = np.arange(len(df))
    ax.plot(x, df["neighbor"], color=NEIGHBOR, lw=1.8, marker="o", ms=4, zorder=3)
    ax.plot(x, df["ring"], color=RING, lw=1.8, marker="o", ms=4, zorder=3)
    ax.fill_between(x, 0, 0.15, color="#F4F6F8", zorder=0)
    ax.axhline(0, color="#9AA2AA", lw=0.7)
    ax.set_ylim(-0.02, 0.9)
    ax.set_xlim(-0.25, len(df) - 0.45)
    ax.set_ylabel("Pearson r")
    ax.set_xticks(x)
    ax.set_xticklabels(df["model"], rotation=22, ha="right")
    ax.grid(axis="y", color=GRID, lw=0.45, alpha=0.65)
    ax.text(4.05, df.loc[4, "ring"] + 0.01, "Ring", color=RING, ha="left", va="center", fontsize=7)
    ax.text(4.05, df.loc[4, "neighbor"] - 0.01, "Neighbor", color=NEIGHBOR, ha="left", va="center", fontsize=7)
    ax.annotate(
        "synthetic\nfine-tune",
        xy=(4, 0.8148),
        xytext=(3.1, 0.74),
        arrowprops={"arrowstyle": "-", "lw": 0.7, "color": ACCENT},
        color=ACCENT,
        ha="right",
        va="center",
        fontsize=6,
    )
    panel_letter(ax, "A", "Fine-tuning is the recovery step")


def plot_cross_split(ax: plt.Axes) -> None:
    df = cross_split_df().iloc[::-1].reset_index(drop=True)
    y = np.arange(len(df))
    for i, row in df.iterrows():
        ax.hlines(i - 0.11, row["niche_neighbor"], row["trained_neighbor"], color="#CBD2D9", lw=1.2, zorder=1)
        ax.hlines(i + 0.11, row["niche_ring"], row["trained_ring"], color="#CBD2D9", lw=1.2, zorder=1)
    ax.scatter(df["niche_neighbor"], y - 0.11, color=BASELINE, s=12, marker="o", zorder=2)
    ax.scatter(df["niche_ring"], y + 0.11, color=BASELINE, s=14, marker="x", zorder=2)
    ax.scatter(df["trained_neighbor"], y - 0.11, color=NEIGHBOR, s=28, zorder=3)
    ax.scatter(df["trained_ring"], y + 0.11, color=RING, s=28, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(df["split"])
    ax.set_xlim(-0.02, 0.88)
    ax.set_xlabel("Pearson r")
    ax.grid(axis="x", color=GRID, lw=0.45, alpha=0.65)
    ax.text(0.86, len(df) - 0.65, "Ring", color=RING, ha="right", va="center", fontsize=7)
    ax.text(0.68, len(df) - 0.95, "Neighbor", color=NEIGHBOR, ha="right", va="center", fontsize=7)
    ax.annotate(
        "unseen perturbation\nis the hard split",
        xy=(0.29, 3.0),
        xytext=(0.58, 2.35),
        arrowprops={"arrowstyle": "-", "lw": 0.7, "color": ACCENT},
        color=ACCENT,
        ha="right",
        va="center",
        fontsize=6,
    )
    panel_letter(ax, "B", "Generalization across held-out axes")


def plot_factor_heatmap(ax: plt.Axes, fig: plt.Figure) -> None:
    df = factor_df()
    data = df[["neighbor", "ring"]].to_numpy()
    cmap = LinearSegmentedColormap.from_list("synthetic_blue_orange", ["#F7F9FB", "#A7C7E7", "#E7B37A", "#B95F2D"])
    im = ax.imshow(data, aspect="auto", cmap=cmap, vmin=0.35, vmax=0.83)
    labels = [f"{row.factor}: {row.setting}" for row in df.itertuples(index=False)]
    ax.set_yticks(np.arange(len(df)))
    ax.set_yticklabels(labels)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Neighbor", "Ring"])
    ax.tick_params(axis="both", length=0)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            color = "white" if val > 0.68 else TEXT
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=6, color=color)
    for cut in [2.5, 5.5, 7.5]:
        ax.axhline(cut, color="white", lw=1.2)
    for spine in ax.spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.025)
    cbar.set_label("Pearson r", fontsize=6)
    cbar.ax.tick_params(labelsize=5, length=2)
    panel_letter(ax, "C", "Recovery is stable across construction factors")


def plot_mismatch(ax: plt.Axes) -> None:
    df = mismatch_df().iloc[::-1].reset_index(drop=True)
    y = np.arange(len(df))
    ax.axvspan(0, 0.15, color="#F4F6F8", zorder=0)
    ax.axvline(0.6193, color=NEIGHBOR, lw=0.9, ls="--", alpha=0.65)
    ax.axvline(0.8148, color=RING, lw=0.9, ls="--", alpha=0.65)
    for i, row in df.iterrows():
        ax.hlines(i - 0.10, 0, row["neighbor"], color=NEIGHBOR, lw=1.4, alpha=0.75)
        ax.hlines(i + 0.10, 0, row["ring"], color=RING, lw=1.4, alpha=0.75)
    ax.scatter(df["neighbor"], y - 0.10, color=NEIGHBOR, s=28, zorder=3)
    ax.scatter(df["ring"], y + 0.10, color=RING, s=28, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(df["simulator"])
    ax.set_xlim(0, 0.86)
    ax.set_xlabel("Pearson r")
    ax.grid(axis="x", color=GRID, lw=0.45, alpha=0.65)
    ax.text(0.64, len(df) - 0.55, "main neighbor", color=NEIGHBOR, fontsize=6, rotation=90, va="top")
    ax.text(0.835, len(df) - 0.55, "main ring", color=RING, fontsize=6, rotation=90, va="top")
    panel_letter(ax, "D", "Mismatch and null controls do not explain recovery")


def make_figure(out_png: Path, out_pdf: Path | None, source_out_dir: Path) -> None:
    configure_matplotlib()
    write_source_data(source_out_dir)
    fig = plt.figure(figsize=(7.25, 4.35), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.02, 1.0], height_ratios=[0.93, 1.07])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])
    plot_main_models(ax_a)
    plot_cross_split(ax_b)
    plot_factor_heatmap(ax_c, fig)
    plot_mismatch(ax_d)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=600, bbox_inches="tight")
    if out_pdf is not None:
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Make the compact synthetic LR summary figure for SPINE4KDD.")
    parser.add_argument("--out-png", type=Path, default=ROOT / "synthetic_lr_summary.png")
    parser.add_argument("--out-pdf", type=Path, default=ROOT / "synthetic_lr_summary.pdf")
    parser.add_argument("--source-out-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    make_figure(args.out_png, args.out_pdf, args.source_out_dir)
    print(f"wrote {args.out_png}")
    if args.out_pdf is not None:
        print(f"wrote {args.out_pdf}")
    print(f"wrote source data under {args.source_out_dir / 'source_data'}")


if __name__ == "__main__":
    main()
