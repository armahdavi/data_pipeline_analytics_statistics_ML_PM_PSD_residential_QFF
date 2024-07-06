# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 17:03:32 2022

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()

import pandas as pd
import numpy as np

exec(open(r'Generic Codes\notion_corrections.py').read())

df = pd.read_excel(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\natl_d_summary.xlsx')
df_scipy = pd.read_excel(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\natl_d_summary.xlsx')

df_stata = pd.read_stata(r'C:\PhD Research\PhD - PSD TSP\peak_no_stata.dta')
df_stata = df_stata[['SN', 'no_peak']].astype(int)

df = df_scipy.merge(df_stata, on ='SN', how = 'outer')
del df['No. Peaks']

##### No of peaks
df[df['ft'] == 1]['no_peak'].value_counts()
df[df['ft'] == 2]['no_peak'].value_counts()
df[df['ft'] == 3]['no_peak'].value_counts()
df[df['ft'] == 4]['no_peak'].value_counts()


#### d summary
df = pd.read_excel(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\natl_d_master.xlsx')
df = df[((df['stat'] == 'median')|(df['stat'] == 'min')|(df['stat'] == 'max')) & (df['Sample Name'].str[9:10] == 'D')]

df['Sample Name'] = df['Sample Name'].str[5:8].astype(int)
df.rename(columns = {'Sample Name': 'SN'}, inplace = True)

## Version 1 (better) : min of mins, median of medians, max of maxes

df_d_sum = pd.DataFrame(np.zeros((12, 7)))
df_d_sum.columns =['Dx (0)', 'Dx (10)', 'Dx (25)', 'Dx (50)', 'Dx (75)', 'Dx (90)', 'Dx (100)']


for var in [col for col in df.columns if 'Dx' in col]:
    i = 0
    if i <= 11:
        for f in [1,2,3,4]:
            for st in ['min', 'median', 'max']:
                df_d_sum.loc[i,'stat'] = st
                df_d_sum.loc[i, var] = df[(df['stat'] == st) & (df['ft'] == f)][var].agg(st)
                df_d_sum.loc[i, 'ft'] = f
                i += 1

df_d_sum.to_excel(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\d_summary.xlsx', index = False)

## Version 2: acceptable (in the paper): min, median, and maxes of all medians

df_d_sum2 = pd.DataFrame(np.zeros((12, 7)))
df_d_sum2.columns =['Dx (0)', 'Dx (10)', 'Dx (25)', 'Dx (50)', 'Dx (75)', 'Dx (90)', 'Dx (100)']

for var in [col for col in df.columns if 'Dx' in col]:
    i = 0
    if i <= 11:
        for f in [1,2,3,4]:
            for st in ['min', 'median', 'max']:
                df_d_sum2.loc[i,'stat'] = st
                df_d_sum2.loc[i, var] = round(df[(df['stat'] == 'median') & (df['ft'] == f)][var].agg(st),1)
                df_d_sum2.loc[i, 'ft'] = f
                i += 1

df_d_sum2.to_excel(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\d_summary_v2.xlsx', index = False)
