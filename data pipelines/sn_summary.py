# -*- coding: utf-8 -*-
"""
Program to make a spreadsheet that includes the filters serial numbers

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
exec(open(r'C:\PhD Research\Paper 2 - PSD_QFF\Learning\Generic Codes\notion_corrections.py').read())
exec(open(r'C:\PhD Research\Paper 2 - PSD_QFF\Learning\Generic Codes\labels_all.py').read())


######################################################################################################################
### Step 1: Reading Filters that were analyzed in Blue Heaven Technologies Inc., to include in Extraction Location ###
######################################################################################################################

df = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\DES\filter_selected.xls'))
df.replace({'filter_type': label_filter_type2}, inplace = True)
df.rename(columns = {'filter_type' : 'ft'}, inplace = True)

df = df[['site', 'ft']]

#################################################################################################
### Step 2: Reading filter weight gain master to refine and merge for SN and extract location ###
#################################################################################################

df2 = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\DES\Filters_weight_gain_master.xlsx'), sheet_name = 'Gravimetric_analysis_refined')
df2 = df2[['SN', 'site', 'round', 'filter_code', 'Ext_loc']]
df2.rename(columns={'filter_code':'ft'}, inplace = True)

sn_summary = df.merge(df2, on = ['site', 'ft'], how = 'outer')
sn_summary.sort_values('SN', inplace = True)
sn_summary.reset_index(inplace = True)
sn_summary = sn_summary[['SN', 'site', 'round', 'ft', 'Ext_loc']]

## Saving the processed file
sn_summary.to_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\\Processed') + '/sn_summary.xlsx', index = False)
