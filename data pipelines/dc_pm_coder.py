# -*- coding: utf-8 -*-
"""
Program to link DC-1700 particle counter data (from sensors) into gravimetric PM measurements

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
import numpy as np
import glob
import os
exec(open(r'C:\PhD Research\Generic Codes\notion_corrections.py').read())

####################################################
### Step 1: Taking start and end time of each DC ###
####################################################

df_sch = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\DES\3_month_schedule_all.xlsx'))
df_sch.sort_values(['site', 'round'], inplace = True)
for s in df_sch['site'].unique():
    for r in df_sch[df_sch['site'] == s]['round'].unique():
        locals()['start_%s_%s' %(s,r)] = df_sch[(df_sch['site'] == s) & (df_sch['round'] == r)]['start']
        locals()['end_%s_%s' %(s,r)] = df_sch[(df_sch['site'] == s) & (df_sch['round'] == r)]['end']

        
###############################################################################
### Step 2: Reading all site DCs one by one, append, and merge into PM data ###
###############################################################################

path = backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Stata_Python_Booster\PhD - PSD TSP\Raw')
os.chdir(path)

list_dir = [fol for fol in os.listdir() if os.path.isdir(fol) == True]
list_file = [path + '/' + dire  for dire in list_dir]

df_dc_append = pd.DataFrame([])

for fold in list_file:
    df = pd.read_stata(fold + '/dc1700_append.dta')
    
    df['DC 0.5-2.5'] = df['small_CountPerFoot3'] - df['large_CountPerFoot3']
    df.rename(columns = {'large_CountPerFoot3' : 'DC > 2.5' }, inplace = True)
    
    df['str_time'] = df['time'].astype(str) # existing version
    df = df[df['str_time'].str[-5:] == '01:00'] 
    
    '''
    for s in df_sch['site'].unique():
        for r in df_sch[df_sch['site'] == s]['round'].unique():
            df.loc[(df['time'] >= locals()['start_%s_%s' %(s,r)].iloc[0]) 
                   & (df['time'] < locals()['end_%s_%s' %(s,r)].iloc[0]), 'round'] = r
    '''         
    
    for s in df_sch['site'].unique():
        for r in df_sch[df_sch['site'] == s]['round'].unique():
            df.loc[(df['time'] >= locals()['start_%s_%s' %(s,r)].iloc[0]), 'round'] = r
    
    s = int(fold[-2:])
    df.dropna(subset = ['round'], inplace = True)    
    df['site'] = s
    
    df = df[['site', 'round', 'time', 'DC 0.5-2.5', 'DC > 2.5']]
    df_dc_append = df_dc_append.append(df)
    
    
df_dc_append[['DC 0.5-2.5', 'DC > 2.5']] = df_dc_append[['DC 0.5-2.5', 'DC > 2.5']] * 35.3147

df_dc_append.to_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\dc_1700.xlsx'), index = False)

df_dc_collapse = df_dc_append.groupby(['site', 'round'], as_index = False)['DC 0.5-2.5', 'DC > 2.5'].quantile([0.1, 0.5, 0.9])
df_dc_collapse['stat'] = df_dc_collapse.index.get_level_values(1).astype(str)
df_dc_collapse.to_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\dc_1700_agg.xlsx'), index = False)

