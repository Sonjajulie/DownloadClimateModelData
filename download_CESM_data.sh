#!/bin/tcsh
#SBATCH -J HIST_TS
#SBATCH -n 4
#SBATCH -t 24:00:00
#SBATCH -A UHAR0013
#SBATCH -p dav
#SBATCH --ntasks-per-node=4
#SBATCH -o output_$var.out
#SBATCH -e error_$var.err

module load cdo
module load nco

# execute with:
# sbatch download_data.sh psl 'cam.ho' atm
set var_out = $argv[1]
set stream = $argv[2]
set component = $argv[3]

set var = ` echo $var_out | tr "[a-z]" "[A-Z]" `
set file_path_in=/gpfs/fs1/collections/cdg/data/cesmLE/CESM-CAM5-BGC-LE/$component/proc/tseries/monthly/$var/
set file_path_out=/glade/scratch/totz/$var_out/

mkdir -p $file_path_out

foreach i (`seq 1 1 35`)
    echo "Download data for model $i\n"
    # first model starts earlier
    # model 34 & 35 have only 2 files
    if ($i == 1) then
        set year_start = 185001
        set year_mid = 208012
    else if ($i >33) then
        set year_start = 192001
        set year_mid = 210012
    else
        set year_start = 192001
        set year_mid = 208012
    endif
    # add padding
    set pad_i = `echo $i | sed -e :a -e 's/^.\{1,2\}$/0&/;ta'`
    # set file paths for output, which will be used to select variable
    set file1_t = $file_path_out/$var_out.$pad_i.1.nc
    set file2_t = $file_path_out/$var_out.$pad_i.2.nc
    # set file paths for output which will be used to select season
    set file1 = $file_path_out/$var_out.$pad_i.$year_start-200512.nc
    set file2 = $file_path_out/$var_out.$pad_i.200601-$year_mid.nc
    # select only variable psl ~ Sea level pressure
    cdo selvar,$var $file_path_in/b.e11.B20TRC5CNBDRD.f09_g16.$pad_i.$stream.$var.$year_start-200512.nc $file1_t
    cdo selvar,$var $file_path_in/b.e11.BRCP85C5CNBDRD.f09_g16.$pad_i.$stream.$var.200601-$year_mid.nc $file2_t
    #Download only Sept-Nov data
    cdo seasmean -selmon,9,10,11 $file1_t $file1
    cdo seasmean -selmon,9,10,11 $file2_t $file2

    if ($i < 34) then
        # set third file for the last time range 208101-210012
        set file3 = $file_path_out/icefrac.$pad_i.208101-210012.nc
        set file3_t = $file_path_out/fsno.$pad_i.3.nc
        cdo selvar,$var $file_path_in/b.e11.BRCP85C5CNBDRD.f09_g16.$pad_i.$stream.$var.208101-210012.nc $file3_t
        cdo seasmean -selmon,9,10,11 $file3_t $file3
        # merge to one file 
        cdo mergetime $file1 $file2 $file3 $file_path_out/$var_out.$pad_i.$year_start-210012.nc
        # remove other files
        rm $file1 $file2 $file3 $file1_t $file2_t $file3_t
    else
        # merge to one file 
        cdo mergetime $file1 $file2  $file_path_out/$var_out.$pad_i.192001-210012.nc
        # remove other files
        rm $file1 $file2 $file1_t $file2_t
    endif
end
