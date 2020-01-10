#!/bin/tcsh

module load cdo


set dir_precc=/glade/scratch/totz/precc/
set dir_precl=/glade/scratch/totz/precc/
set dir_total_prec=/glade/scratch/totz/total_prec/

foreach i (`seq 1 1 35`)
    echo "sum data for model $i\n"
    # first model starts earlier
    # model 34 & 35 have only 2 files
    if ($i == 1) then
        set year_start_final = 185001
    else
        set year_start_final = 192001
    endif

    # add padding
    set pad_i = `echo $i | sed -e :a -e 's/^.\{1,2\}$/0&/;ta'`
    # sum prec = precc + precl, set name to prec
    cdo enssum ${dir_precc}/precc.$pad_i.$year_start_final-210012.nc ${dir_precl}/precl.$pad_i.$year_start_final-210012.nc  ${dir_total_prec}/prec.$pad_i.$year_start_final-210012.nc
     cdo chname,PRECC,prec_t ${dir_total_prec}/prec.$pad_i.$year_start_final-210012.nc ${dir_total_prec}/prec_t.$pad_i.$year_start_final-210012.nc
    rm ${dir_total_prec}/prec.$pad_i.$year_start_final-210012.nc
