# plot_radec.py
from amms.core.analysis.maps import Map2D
from amms.core.plotting.maps import show_map
import matplotlib.pyplot as plt

m = Map2D.load("/xdisk/gbesla/zvladimir/products/b12_model2/lmc_069_sfr_radec_dt100myr.npz")
show_map(m, log=True, min_counts=1)
plt.savefig("radec.png", dpi=150, bbox_inches="tight")
