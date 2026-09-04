import numpy as np
from pathlib import Path
import os
from pygadgetreader import readheader, readsnap

from amms.core.analysis.frames import Frame
from amms.core.analysis.sfr import sfr_map_from_young_stars
from amms.core.datasets import b12

#TODO move to config.paths
SNAP = "/xdisk/gbesla/group/b12/lmc_smc_mw/model2/snaps/snapshot_069"
OUT = Path(os.environ.get("AMMS_PRODUCTS", "/xdisk/gbesla/zvladimir/products")) / "b12_model2"

# 1. Frame from the initial disk stars
# Don't use the young stars as they are sparse and disturbed
d_pid = readsnap(SNAP, "pid", "disk")
sel = b12.galaxy_mask(d_pid, "lmc")
frame = Frame.from_tracers(b12.to_kpc(readsnap(SNAP, "pos", "disk"))[sel], readsnap(SNAP, "vel", "disk")[sel], b12.to_msun(readsnap(SNAP, "mass", "disk"))[sel], r_axis=10.0, tracers="b12_lmc_disk_stars")

print("center", frame.center, "vs precomputed", b12.LMC_CENTER_069)

# 2. New stars shifted to the frame defined by initial disk stars
s_pid = readsnap(SNAP, "pid", "star")
sel = b12.galaxy_mask(s_pid, "lmc")
pos = frame.positions(b12.to_kpc(readsnap(SNAP, "pos", "star"))[sel])
mass = b12.to_msun(readsnap(SNAP, "mass", "star"))[sel]

# pygadgetreader labels it "stellar Age" but returns formation TIME
t_now = float(b12.to_gyr(readheader(SNAP, "time")))
age = t_now - b12.to_gyr(readsnap(SNAP, "age", "star"))[sel]

# 3. Maps
base = {"dataset": "b12_model2", "snapshot": 69, "galaxy": "lmc", "frame": frame.to_dict(), "t_now_gyr": t_now}

dt = 0.1
for axes in ("xy", "xz"):
    m = sfr_map_from_young_stars(pos, mass, age, dt=dt, axes=axes, extent=15.0, bins=60, meta=base)
    print(axes, dt, "n_young", m.meta["n_young"], "filled px", int((m.counts > 0).sum()))
    m.save(f"{OUT}/lmc_069_sfr_{axes}_dt{int(dt * 1000)}myr.npz")
