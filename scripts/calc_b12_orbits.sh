#!/bin/bash
#SBATCH --job-name=b12_orbits
#SBATCH --account=gbesla
#SBATCH --partition=standard
#SBATCH --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=16G
#SBATCH --time=03:00:00
#SBATCH --output=%x-%j.out
# legacy-gadget, not env/activate.sh: amms venv has no pygadgetreader; activate.sh loads 3.11 and breaks this 3.14 venv
module purge && module load python/3.14/3.14.2
source ~/.venvs/legacy-gadget/bin/activate
R=/rental/gbesla/mig2020/rsgrps/gbeslastudents/LegacySims/Besla2012/LS_MW
for m in 2 1; do
    python ~/lmcsmcmw/scripts/b12_orbits.py "$R/Fid$m" --model "$m"
done
