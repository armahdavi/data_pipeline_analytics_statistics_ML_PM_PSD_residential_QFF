# -*- coding: utf-8 -*-
"""
Program to make a master database of d-values for all RP-1649 and HUD dust samples and save them in different processed files.
d-values are size cut-offs that report cumulative dust under the specified particle size.

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
exec(open(r'C:\PhD Research\Generic Codes\notion_corrections.py').read())
# exec(open(r'C:\Career\Learning\Python Practice\Generic Codes\labels_all.py').read())
exec(open(r'C:\PhD Research\Generic Codes\mastersizer_all.py').read())

####################################################
### Step 1: RP-1649 Samples - d-value Processing ###
####################################################

path_import = backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Raw')
path_export = backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd')
i = 1
for file in ['mastersizer_ida.csv', 'mastersizer_bht.csv', '033nf.csv', '041nf.csv', '046nf.csv', '049nf.csv']:
    export_file = file[:-4] + '_d_ordered'
    temp_rp = mastersizer_d_input(path_import, path_export, file, export_file)        
    
    if i == 1:
        df_d_rp = temp_rp
        i += 1
    else:
        df_d_rp = df_d_rp.append(temp_rp)

list_sample_all = list(df_d_rp['Sample Name'].unique())

## Getting rid of r2 replicates
df_d_rp = df_d_rp[~(df_d_rp['Sample Name'].str[-2:] == 'r2')]

# sorting based on the importance of stat and sample name
custom_dict = {'median' : 0, 
               'gmean' : 1, 
               'gstd' : 2,
               'min' : 3,
               'max': 4,
               'count': 5}  

df_d_rp['SN'] = df_d_rp['Sample Name'].str[5:8].astype(int)
# df_d_rp.rename(columns={'Sample Name': 'SN'}, inplace = True)
df_d_rp.sort_values(by = ['stat', 'Sample Name'], key=lambda x: x.map(custom_dict), inplace = True)

sn_summary = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\\Processed\sn_summary.xlsx'))
df_d_rp = df_d_rp.merge(sn_summary, on = 'SN', how = 'outer')

df_d_rp = df_d_rp[['Sample Name', 'site', 'round', 'ft', 
                   'Dx (0)', 'Dx (10)', 'Dx (25)', 'Dx (50)', 'Dx (75)', 'Dx (90)', 'Dx (100)', 
                   'stat',  'Ext_loc']]

df_d_rp.to_excel(path_export + '/natl_d_master.xlsx', index = False)

### Brief summary with collapsed for median only
df_d_rp_brief = df_d_rp[(df_d_rp['stat'] == 'median') & (df_d_rp['Sample Name'].str[9:10] == 'D')]
df_d_rp_brief['Sample Name'] = df_d_rp_brief['Sample Name'].str[5:8].astype(int)
df_d_rp_brief.rename(columns = {'Sample Name': 'SN'}, inplace = True)
del df_d_rp_brief['stat']


no_peak = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\no_peak_v2.xlsx'))
df = df_d_rp_brief.merge(no_peak, on = 'SN', how = 'outer')
del df['Ext_loc']
df = df[['SN', 'site', 'round', 'ft', 'Dx (0)', 'Dx (10)', 'Dx (25)', 'Dx (50)', 'Dx (75)', 'Dx (90)', 'Dx (100)', 'No. Peaks']]
df.sort_values('SN', inplace = True)

df.to_excel(path_export + '/natl_d_summary.xlsx', index = False)


################################################
### Step 2: HUD Samples - d-value Processing ###
################################################

import glob
import os
os.chdir(path_import)

i = 1
for file in glob.glob('S*.csv') + glob.glob('HUD*.csv'):
    export_file = file[:-4] + '_d_ordered'
    temp_d_hud = mastersizer_d_input(path_import, path_export, file, export_file)        
    
    if i == 1:
        df_d_hud = temp_d_hud
        i += 1
    else:
        df_d_hud = df_d_hud.append(temp_d_hud)

df_d_hud.to_excel(path_export + '/hud_d_master.xlsx', index = False)

