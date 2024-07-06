# -*- coding: utf-8 -*-
"""
Program to collect all mastersizer laser obscuration values from the PSD raw data

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd

exec(open(r'Generic Codes\notion_corrections.py').read())

df_obs = pd.DataFrame([])
for file in ['mastersizer_ida.csv', 'mastersizer_bht.csv', '033nf.csv', '041nf.csv', '046nf.csv', '049nf.csv']:
    df = pd.read_csv(backslash_correct(r'C:\Career\Learning\Python Practice\Stata_Python_Booster\PhD - PSD TSP\Raw\\' + file))
    df['SN'] = df['Sample Name'].str[5:8].astype(int)
    df['Fr'] = df['Sample Name'].str[9:10]
    df = df[['SN', 'Fr', 'Laser Obscuration']]
    
    df = df.groupby(['SN', 'Fr'], as_index = False)['Laser Obscuration'].agg('median')
    # df = df.groupby(['SN', 'Fr'], as_index = False)['Laser Obscuration'].agg('max')
    # df = df.groupby(['SN', 'Fr'], as_index = False)['Laser Obscuration'].agg('mean')
    
    df_obs = df_obs.append(df)
    
df_obs.sort_values(['SN', 'Fr'], inplace = True)
df_obs.to_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\laser_obs_master.xlsx'), index = False)
    