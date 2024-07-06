# -*- coding: utf-8 -*-
"""
Ptogram to merge:
    1) all PSD and d-value parameters; and
    2) PM database
    
    into walkthrough survey parameters to include them in the database

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
exec(open(r'C:\PhD Research\Generic Codes\notion_corrections.py').read())


###########################################################################
### Merging main columns of d-value, PM, and walkthrough survey columns ###
############### to add the site properties to the database ################
###########################################################################

### natl_d_master

df = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\natl_d_master.xlsx'))
df = df[(df['stat'] == 'median') & (df['Sample Name'].str[9:10] == 'D')]
df.sort_values(['site', 'round'], inplace = True)
df.drop_duplicates(['site', 'round'], keep = 'first', inplace = True)
df.drop(['Sample Name', 'stat', 'Ext_loc', 'ft'], axis = 1, inplace = True)


### pm_master
df_pm = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\pm_master.xlsx'))
df_pm.columns

df_pm = df_pm[['site', 'round', 'ft', 'TSP Concentration', 'PM10', 'PM2.5', 'filtration volume', 'eff_2.5', 'eff_10']]

df = df.merge(df_pm, on = ['site', 'round'], how = 'outer')

### walk_through_survey
df_wt = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\DES\walkthourgh_survey.xlsx'))
df_wt.columns
df_wt.drop(['nature_attached_building', 'neighb_desc', 'other_comments'], axis = 1, inplace = True)
df = df.merge(df_wt, on = ['site'], how = 'outer')

df.to_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\pm_d_prop.xlsx'), index = False)
