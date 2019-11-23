#!/bin/tcsh
#SBATCH -J U
#SBATCH -n 4
#SBATCH -t 12:00:00
#SBATCH -A ##YOUR PROJECT NUMBER (i.e. UHAR____)
#SBATCH -p dav
#SBATCH --ntasks-per-node=4
#SBATCH -o output.out
#SBATCH -e error.err


## Load required modules 
## https://www.rc.fas.harvard.edu/resources/documentation/software-on-the-cluster/python/
module load Anaconda3/5.0.1-fasrc02

## execute with sbatch submit.sh
foreach i (`seq 1 1 28`)
    python3 main_cluster.py $i
end

