"""
Plot the cached Sigma_SFR maps. Only reads saved processed data not the snapshots
Run sfr_maps_b12.py first
"""
import os
from pathlib import Path

import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt

from amms.core.analysis.maps import Map2D
from amms.core.plotting.maps import shared_norm, show_map

PRODUCTS = Path(os.environ["AMMS_PRODUCTS"]) / "b12_model2"
FIGS = Path(__file__).resolve().parent.parent / "figures"
FIGS.mkdir(exist_ok=True)

m_xy = Map2D.load(PRODUCTS / "lmc_069_sfr_xy_dt100myr.npz")
m_xz = Map2D.load(PRODUCTS / "lmc_069_sfr_xz_dt100myr.npz")

norm = shared_norm([m_xy, m_xz], percentiles=(1, 99.5), min_counts=3)

fig, axd = plt.subplot_mosaic("AB", figsize=(9.5, 4.2), constrained_layout=True)
im = show_map(m_xy, axd["A"], norm=norm, min_counts=3, cmap="inferno", cbar=False)
show_map(m_xz, axd["B"], norm=norm, min_counts=3, cmap="inferno", cbar=False)

axd["A"].set_title(f"face-on  ($\\Delta t$ = {m_xy.meta['dt_gyr']*1000:.0f} Myr)")
axd["B"].set_title("edge-on")

fig.colorbar(im, ax=[axd["A"], axd["B"]], label=r"$\Sigma_{\rm SFR}$ [M$_\odot$ yr$^{-1}$ kpc$^{-2}$]")

out = FIGS / "b12_lmc_069_sfr_dt100myr.png"
fig.savefig(out, dpi=300)
print("wrote", out)

