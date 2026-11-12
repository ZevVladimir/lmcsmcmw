"""
Cache one B12 cloud's new stars at one snapshot:
    pos in that cloud's disk frame
    t_form_gyr
    mass
Drop ft==0
Radius cuts and binning are done in notebooks not here
Snapshot path is argument with directory mapping verified by sha256 not hardcoded
"""
import argparse
from pathlib import Path

from amms.core import products
from amms.core.datasets import b12

ap = argparse.ArgumentParser()
ap.add_argument("snap", type=Path)
ap.add_argument("--model", type=int, choices=(1,2), required=True)
ap.add_argument("--galaxy", choices=("lmc", "smc"), required=True)
ap.add_argument("--overwrite", action="store_true")
a = ap.parse_args()

snapnum = int(a.snap.name.rsplit("_", 1)[1])
frame = b12.galaxy_frame(b12.load(a.snap, "disk"), a.galaxy)
print(a.galaxy, "center", frame.center)

s = b12.load(a.snap, "star", a.galaxy, fields=("pos", "mass", "age"))
keep = b12.formed_in_run(s["t_form_gyr"])

path = products.write_product(
    f"ext_b12-model{a.model}", "newstars", f"{a.galaxy}-{snapnum:03d}",
    {"pos_kpc": frame.positions(s["pos_kpc"][keep]),
     "t_form_gyr": s["t_form_gyr"][keep],
     "mass_msun": s["mass_msun"][keep]},
     source=str(a.snap.resolve()),
     meta={**b12.conventions(), "galaxy": a.galaxy, "snapshot": snapnum,
           "t_now_gyr": b12.snapshot_time_gyr(a.snap), "frame": frame.to_dict(),
           "n_dropped_ft0": int((~keep).sum())},
    overwrite=a.overwrite,
)
print(path, int(keep.sum()), "kept,", int((~keep).sum()), "ft==0 dropped")
