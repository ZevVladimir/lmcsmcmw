#!/bin/bash
#SBATCH --job-name=b12_orbits
#SBATCH --account=gbesla
#SBATCH --partition=standard
#SBATCH --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=16G
#SBATCH --time=03:00:00
source ~/amms-core/env/activate.sh   # or the venv that has pygadgetreader (the one sfr_maps_b12.py ran in)
R=/rental/gbesla/mig2020/rsgrps/gbeslastudents/LegacySims/Besla2012/LS_MW
for m in 2 1; do   # Model 2 first: it's the hash-verified one
    python ~/lmcsmcmw/scripts/b12_orbits.py "$R/Fid$m" --model "$m"
done
