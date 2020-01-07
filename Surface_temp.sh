#!/bin/tcsh
#SBATCH -J HIST_TS
#SBATCH -n 4
#SBATCH -t 24:00:00
#SBATCH -A UHAR0013
#SBATCH -p dav
#SBATCH --ntasks-per-node=4
#SBATCH -o output.out
#SBATCH -e error.err

module load cdo
module load nco

#Download surface temperature data from the first 35 ensemble members in the CESM Large Ensemble
foreach i (`seq 1 1 35`)
    if ($i == 1) then
	#Download only Oct-Feb data
        ncks -d time,0,,12 -d time,1,,12 -d time,8,,12 -d time,9,,12 -d time,10,,12 -d time,11,,12 /gpfs/fs1/collections/cdg/data/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TS/b.e11.B20TRC5CNBDRD.f09_g16.001.cam.h0.TS.185001-200512.nc /glade/scratch/totz/TS_$i.nc

    else if ($i < 10) then
        ncks -d time,0,,12 -d time,1,,12 -d time,8,,12 -d time,9,,12 -d time,10,,12 -d time,11,,12 /gpfs/fs1/collections/cdg/data/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TS/b.e11.B20TRC5CNBDRD.f09_g16.00$i.cam.h0.TS.192001-200512.nc /glade/scratch/totz/TS_$i.nc

    else
        ncks -d time,0,,12 -d time,1,,12 -d time,8,,12 -d time,9,,12 -d time,10,,12 -d time,11,,12 /gpfs/fs1/collections/cdg/data/cesmLE/CESM-CAM5-BGC-LE/atm/proc/tseries/monthly/TS/b.e11.B20TRC5CNBDRD.f09_g16.0$i.cam.h0.TS.192001-200512.nc /glade/scratch/totz/TS_$i.nc
    endif
end

