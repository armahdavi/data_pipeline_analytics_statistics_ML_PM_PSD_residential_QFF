# -*- coding: utf-8 -*-
"""
Program to find the location of peaks in a PSD curve (in terms of size distribution).

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
from scipy.signal import find_peaks
exec(open(r'C:\PhD Research\Generic Codes\notion_corrections.py').read())


df = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\natl_psd_master.xlsx'))
list_all = list(df.columns)

list_select = [col for col in list_all if (col[-4:] == 'mean')]
size = df['Size']
df = df[['Size'] + list_select]

peak_loc = pd.DataFrame([], columns = ['SN', "Fr", 'Peak Size'])
i = 0
for item in list_select:
    df.sort_values(item, inplace = True)
    keep_list = ['Size', item]
    keep = df[keep_list]
    peak_loc.loc[i] = [item[5:8], item[9:10], keep['Size'].iloc[-1]]
    i += 1

peak_loc.to_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\peak_locator.xlsx'), index = False)
