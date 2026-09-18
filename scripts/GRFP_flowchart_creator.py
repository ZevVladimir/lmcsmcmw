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
        title="Demosntrated: higher-res N-body ICs",
        caption="Rathore+In prep?"
    ),
    "ism": dict(
        path=None,
        title="Demosntrated: SMUGGLE ISM model",
        caption="Jahn+2023, SMC analog",
    ),
    "goal": dict(
        path=None,
        title="Goal: this proposal",
        caption="High-res N-body + SMUGGLE",
    ),
}

def draw_panel(ax, spec):
    if spec["path"] is not None and Path(spec["path"]).exists():
        ax.imshow(plt.imread(spec["path"]))
    else:
        ax.add_path(Rectangle((0.03, 0.03), 0.94, 0.94, fill=False, linestyle="--", linewidth=1.5, transform=ax.transAxes))
