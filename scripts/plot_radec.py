# plot_radec.py
from amms.core.analysis.maps import Map2D
from amms.core.plotting.maps import show_map
from amms.core.analysis.sky import sky_aspect
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

FIGS = Path(__file__).resolve().parent.parent / "figures"
FIGS.mkdir(exist_ok=True)
out = FIGS / "radec.png"

m = Map2D.load("/xdisk/gbesla/zvladimir/products/b12_model2/lmc_069_sfr_radec_dt100myr.npz")

lon0, lon1, lat0, lat1 = m.extent
aspect = sky_aspect((lat0 + lat1) / 2.0)

show_map(m, log=True, min_counts=1, aspect=aspect)

plt.savefig(out , dpi=150, bbox_inches="tight")
