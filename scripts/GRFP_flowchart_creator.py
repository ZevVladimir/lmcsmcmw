"""
Creates the flowchart used in my GRFP research proposal

Illustrates the current B12 state of the art then the two new major improvements, Himansh's Nbody ICs and Ethan's SMUGGLE run, and then the goal which is my work

This is a one off piece of code that isn't intended for future use which would require implementation in amms-core plotting and version stamping

This is also written to be run locally and is missing the more generic codes. This is purely just stitching together premade plots
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

FIG_DIR = Path("/home/zvladimir/lmcsmcmw/figures")

PANELS = {
    "baseline": dict(
        path=FIG_DIR / "sfr_slices.png", #TODO choose just one slice
        title="Current state of the art",
        caption="Besla et al. 2012 Model 2",
    ),
    "nbody": dict(
        path=FIG_DIR / "clouds_ra_dec_simulated.jpg",
        title="Demonstrated: higher-res N-body ICs",
        caption="Rathore+In prep?"
    ),
    "ism": dict(
        path="/home/zvladimir/lmcsmcmw/figures/jahn2023_smuggle-1.png",
        title="Demonstrated: SMUGGLE ISM model",
        caption="Jahn+2023, SMC analog",
    ),
    "goal": dict(
        path="/home/zvladimir/lmcsmcmw/figures/mazzi2021_sfr.png", #TODO choose just one slice
        title="Goal: match these observations",
        caption="With high-res N-body + SMUGGLE",
    ),
}

def draw_panel(ax, spec):
    if spec["path"] is not None and Path(spec["path"]).exists():
        ax.imshow(plt.imread(spec["path"]), cmap="gray")
    else:
        ax.add_patch(Rectangle((0.03, 0.03), 0.94, 0.94, fill=False, linestyle="--", linewidth=1.5, transform=ax.transAxes))
        ax.text(0.5, 0.5, "placeholder", ha="center", va="center", transform=ax.transAxes)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(spec["title"], fontsize=10)
    ax.set_xlabel(spec["caption"], fontsize=8, style="italic")


fig = plt.figure(figsize=(11, 4.5))

ax_a = fig.add_axes([0.03, 0.12, 0.22, 0.72])
ax_b = fig.add_axes([0.38, 0.57, 0.20, 0.38])
ax_c = fig.add_axes([0.38, 0.04, 0.20, 0.38])
ax_goal = fig.add_axes([0.75, 0.12, 0.22, 0.72])

for ax , key in [(ax_a, "baseline"), (ax_b, "nbody"), (ax_c, "ism"), (ax_goal, "goal")]:
    draw_panel(ax, PANELS[key])

fig.text(0.48, 0.5, "+", fontsize=26, ha="center", va="center")

arrow_kw = dict(arrowstyle="-|>", mutation_scale=20, linewidth=1.5, color="black", transform=fig.transFigure)

fig.patches.append(FancyArrowPatch((0.26, 0.48), (0.36, 0.48), **arrow_kw))
fig.patches.append(FancyArrowPatch((0.60, 0.48), (0.74, 0.48), **arrow_kw))

fig.savefig(FIG_DIR / "grfp_flowchart_draft.png", dpi=300)
