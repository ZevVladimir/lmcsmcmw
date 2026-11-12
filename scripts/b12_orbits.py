"""
The center track of each cloud over one B12 run output into ext_b12-model<N>/orbit_<galaxy>.h5

Center = b12.galaxy_frame (which uses a shrinking sphere on only the disk stars)
Reads each snapshot once from /rental with one pass
Since B12's MW is analytic at the origin no orbit_mw
distance to MW = |pos_kpc|
"""
import argparse
from pathlib import Path

import numpy as np

from amms.core import products
from amms.core.datasets import b12

ap = argparse.ArgumentParser()
ap.add_argument("snapdir", type=Path)
ap.add_argument("--model", type=int, choices=(1, 2), required=True)
ap.add_argument("--galaxies", nargs="+", choices=("lmc", "smc"), default=["lmc", "smc"])
ap.add_argument("--overwrite", action="store_true")
a = ap.parse_args()

# Using exactly 3 digit glob skips extra files like snapshot_069.bin and doesn't descend into subdirs
snaps = sorted(a.snapdir.glob("snapshot_[0-9][0-9][0-9]"))
if not snaps:
    raise SystemExit(f"no snapshots in {a.snapdir}")

num = np.array([int(s.name[-3:]) for s in snaps])
t = np.array([b12.snapshot_time_gyr(s) for s in snaps])
pos = {g: np.empty((len(snaps), 3)) for g in a.galaxies}
vel = {g: np.empty((len(snaps), 3)) for g in a.galaxies}

for i, s in enumerate(snaps):
    disk = b12.load(s, "disk") # read in both clouds
    for g in a.galaxies:
        f = b12.galaxy_frame(disk, g)
        pos[g][i], vel[g][i] = f.center, f.v_center
    print(s.name, f"t={t[i]:.3f}", *(f"{g}={np.round(pos[g][i], 2)}" for g in a.galaxies), flush=True)

for g in a.galaxies:
    path = products.write_product(
        f"ext_b12-model{a.model}", "orbit", g,
        {"snapshot": num, "t_gyr": t, "pos_kpc": pos[g], "vel_kms": vel[g]},
        source=str(a.snapdir.resolve()),
        meta={**b12.conventions(), "galaxy": g,
              "frame": "box (galactocentric; MW potential set at origin)",
              "center": "b12.galaxy_frame: shrinking sphere on disk stars, r_center=10",
              "n_snapshots": len(snaps)},
        overwrite=a.overwrite, 
    )
    print(path)
