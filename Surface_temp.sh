#!/bin/tcsh
#SBATCH -J HIST_TS
#SBATCH -n 4
#SBATCH -t 24:00:00
#SBATCH -A UHAR0012
#SBATCH -p dav
#SBATCH --ntasks-per-node=4
#SBATCH -o output.out
#SBATCH -e error.err

module load cdo
module load nco

PATH_DOWNLOAD="/gpfs/fs1/collections/cdg/data/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TS/"
PATH_TO_STORE_FILES=""

echo "Download data from ${PATH_DOWNLOAD} to ${PATH_TO_STORE_FILES}"
for i in {01..35}; do 
    #Download only Oct-Feb data
    ncks -d time,0,,12 -d time,1,,12 -d time,8,,12 -d time,9,,12 -d time,10,,12 -d time,11,,12 "${PATH_DOWNLOAD}/b.e11.B20TRC5CNBDRD.f09_g16.0${i}.cam.h.TS.185001-200512.nc" "${PATH_TO_STORE_FILES}/TS_${i}.nc"
done
echo "Finished!"
