import numpy as np
from pathlib import Path
import os
from pygadgetreader import readheader, readsnap

from amms.core.analysis.frames import Frame
from amms.core.analysis.sfr import sfr_map_from_young_stars, sfh, sfr_sky_map_from_young_stars
from amms.core.analysis.sky import radec_from_galactocentric, sky_bins
from amms.core.analysis.maps import project_lonlat
from amms.core.datasets import b12
from amms.core.config.paths import products_root

#TODO move to config.paths
SNAP = "/xdisk/gbesla/group/b12/lmc_smc_mw/model2/snaps/snapshot_069"
PRODUCTS = products_root() / "b12_model2"

# ---------------------------------------------------------------------------------------------------
# 1. Frame from the initial disk stars
# Don't use the young stars as they are sparse and disturbed
d_pid = readsnap(SNAP, "pid", "disk")
sel = b12.galaxy_mask(d_pid, "lmc")
frame = Frame.from_tracers(b12.to_kpc(readsnap(SNAP, "pos", "disk"))[sel], readsnap(SNAP, "vel", "disk")[sel], 
                           b12.to_msun(readsnap(SNAP, "mass", "disk"))[sel], r_axis=10.0, tracers="b12_lmc_disk_stars", 
                           reference=b12.PA_REFERENCE_CLOUDS_DEMO)

print("center", frame.center, "vs precomputed", b12.LMC_CENTER_069)

# ---------------------------------------------------------------------------------------------------
# 2. New stars shifted to the frame defined by initial disk stars
s_pid = readsnap(SNAP, "pid", "star")
sel = b12.galaxy_mask(s_pid, "lmc")

star_pos = readsnap(SNAP, "pos", "star")
pos = frame.positions(b12.to_kpc(star_pos)[sel])
mass = b12.to_msun(readsnap(SNAP, "mass", "star"))[sel]

# pygadgetreader labels it "stellar Age" but returns formation TIME
t_now = float(b12.to_gyr(readheader(SNAP, "time")))
age = t_now - b12.to_gyr(readsnap(SNAP, "age", "star"))[sel]

# 3. Maps
base = {"dataset": "b12_model2", "snapshot": 69, "galaxy": "lmc", "frame": frame.to_dict(), "t_now_gyr": t_now, "pa_convention": "line_of_nodes_clouds_demo"}

dt = 0.1
for axes in ("xy", "xz"):
    m = sfr_map_from_young_stars(pos, mass, age, dt=dt, axes=axes, extent=10.0, bins=40, meta=base)
    print(axes, dt, "n_young", m.meta["n_young"], "filled px", int((m.counts > 0).sum()))
    m.save(f"{PRODUCTS}/lmc_069_sfr_{axes}_dt{int(dt * 1000)}myr.npz")

edges, rates = sfh(age, mass, bins=40, range=(0.0, t_now))
print(edges)
print(rates)

# ---------------------------------------------------------------------------------------------------
# 4. RA/Dec sky map
pos_galcen = b12.to_kpc(star_pos)[sel] - b12.MW_CENTER
ra, dec = radec_from_galactocentric(pos_galcen)

lon_range=(30, 80)
lat_range=(-80, -60)

pix_deg = 0.5

nx, ny = sky_bins(lon_range, lat_range, pix_deg)

m_sky = sfr_sky_map_from_young_stars(ra, dec, mass, age, dt=dt, lon_range=lon_range, lat_range=lat_range, bins=(nx, ny), 
                                     axis_labels=(r"RA [$^\circ$]", r"DEC [$^\circ$]"), meta=base)

print("radec", dt, "n_young", m_sky.meta["n_young"], "filled px", int((m_sky.counts > 0).sum()))
m_sky.save(f"{PRODUCTS}/lmc_069_sfr_radec_dt{int(dt * 1000)}myr.npz")

# ---------------------------------------------------------------------------------------------------
# 5. Ra/Dec density of all LMC stars

m_all = project_lonlat(ra, dec, lon_range=lon_range, lat_range=lat_range, bins=(nx,ny), quantity="n_stars", unit="count",
                       axis_labels=(r"RA [$^\circ$]", r"DEC [$^\circ$]"), meta=base)

m_all.save(f"{PRODUCTS}/lmc_069_radec_allstars.npz")

# ---------------------------------------------------------------------------------------------------
# 6. RA/Dec SFR in 5Myr age slices. From 0 to t_now
SLICE_OUT = PRODUCTS / "sfr_radec_slices"
dt_slice = 0.01 # in Gyr
edges = np.arange(0.0, t_now, dt_slice)

# Time slices based off Mazzi+2024 panels
custom_edges = [(0.0, 3.98), (3.98, 7.94), (7.94, 15.8), (15.8, 31.6), (31.6, 63.1), (63.1, 126), (126, 251), (251, 398), (398, 631), (631, 1000)]

for edge in custom_edges:
    dt_slice = (edge[1] - edge[0])/1e3
    lo = edge[0] / 1e3
    m_slice = sfr_sky_map_from_young_stars(ra, dec, mass, age, dt=dt_slice, age_min=lo, lon_range=lon_range, lat_range=lat_range,
                                           bins=(nx, ny), axis_labels=(r"RA [$^\circ$]", r"DEC [$^\circ$]"), meta=base)

    # hi = lo + dt_slice
    hi = edge[1] / 1e3
    m_slice.save(SLICE_OUT / f"lmc_069_age{int(lo * 1000):03d}-{int(hi*1000):03d}myr.npz")
