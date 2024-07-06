# -*- coding: utf-8 -*-
"""
Program to make a master database of PSDs (volume fraction vs. size) for all RP1649 and HUD dust samples and save them in different processed files.
This code uses a function "mastersizer_"

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
exec(open(r'C:\PhD Research\Generic Codes\notion_corrections.py').read())
# exec(open(r'C:\Career\Learning\Python Practice\Generic Codes\labels_all.py').read())
exec(open(r'C:\PhD Research\Generic Codes\mastersizer_all.py').read())

################################################
### Step 1: RP-1649 Samples - PSD Processing ###
################################################

path_import = backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Raw')
path_export = backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd')

## Getting 6-cycle samples prepared for ultimate info (mean, error (by max, min), and count) for 6_cycle samples.  
for file in ('033', '041', '046', '049'):
    df = pd.read_csv(path_import + '//' + file + '.csv')
    df['Sample Name'] = df['Sample Name'].str[0:23]
    df['Sample Name'] = df['Sample Name'].str[0:11] + 'yymmdd_' + df['Sample Name'].str[18:]
    df.to_csv(path_import + '//' + file + 'nf.csv', index = False) # nf (no fractionation) is a sign that you have removed the fractionation with sampling name


## Making a master list:
# This masterlist has: 1) Size, 2) mean of each psd, 3) error of each psd, 4) count of each psd, and avoids any replicate (r2, r3 etc.,)
# requires a mother df called df to extract the info from the above.
# 6-cycle samples that have multiple psds from various extraction of filter various areas have been already fixed (see a few lines above)

i = 1
for file in ['mastersizer_ida.csv', 'mastersizer_bht.csv', '033nf.csv', '041nf.csv', '046nf.csv', '049nf.csv']:
    export_file = file[:-4] + '_ordered'
    temp_rp = mastersizer_input_v2(path_import, path_export, file, export_file)        
    
    if i == 1:
        df_rp = temp_rp
        i += 1
    else:
        df_rp = pd.merge(df_rp, temp_rp, on = "Size", how = 'outer')

## Getting rid of r2 replicates
no_r2_list = [col for col in df_rp.columns if col[24:26] != 'r2']
df_rp = df_rp[no_r2_list]
df_rp.to_excel(path_export + '/natl_psd_master.xlsx', index = False)

########################################################
### Step 2: HUD Central Texas samples PSD Processing ###
########################################################

import glob
import os
os.chdir(path_import)

i = 1
for file in glob.glob('S*.csv') + glob.glob('HUD*.csv'):
    export_file = file[:-4] + '_ordered'
    temp_hud = mastersizer_input_v2(path_import, path_export, file, export_file)        
    
    if i == 1:
        df_hud = temp_hud
        i += 1
    else:
        df_hud = pd.merge(df_hud, temp_hud, on = "Size", how = 'outer')

df_hud.to_excel(path_export + '/hud_psd_master.xlsx', index = False)
