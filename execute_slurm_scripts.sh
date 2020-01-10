#!/bin/tcsh

# documentation: http://www.cesm.ucar.edu/projects/community-projects/LENS/data-sets.html


# variables in array:
#   Large-scale (stable) precipitation rate (liq + ice) (precl)
#   Convective precipitation rate (liq + ice) (precc) 
#   Surface temperature (radiative) (TS)
#   Fraction of sfc area covered by sea-ice (icefrac) 
#   Sea level pressure (psl)
#set arr=(precl precc TS icefrac psl)
set arr=(precc precl TS)
foreach var ($arr) 
    sbatch --output=output_$var.out --error=error_$var.err --job-name=cesm_$var download_CESM_data.sh $var "cam.h0" atm 12 1 2
end

#set arr=(icefrac psl)
#foreach var ($arr) 
#    sbatch --output=output_$var.out --error=error_$var.err --job-name=cesm_$var download_CESM_data.sh $var "cam.h0" atm 9 10 11
#end


# fraction of ground covered by snow 
# not in for loop included because stream and component are different
#set var = fsno
#sbatch --output=output_$var.out --error=error_$var.err --job-name=cesm_$var download_CESM_data.sh $var "clm2.h0" lnd 9 10 11

# Geopotential Z at 500 mbar pressure surface (Z500)
# not in for loop included because stream and shell script are different
#set var = Z500
#sbatch --output=output_$var.out --error=error_$var.err --job-name=cesm_$var download_CESM_data_daily.sh $var "cam.h1" atm 9 10 11



