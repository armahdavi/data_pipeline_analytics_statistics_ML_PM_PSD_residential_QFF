# -*- coding: utf-8 -*-
"""
Program to find the number of peaks in a PSD curve using scipy.signal module.

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
from scipy.signal import find_peaks
exec(open(r'C:\PhD Research\Generic Codes\notion_corrections.py').read())


df = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\natl_psd_master.xlsx'))
list_all = list(df.columns)

list_select = [col for col in list_all if (col[9:10] == 'D') & (col[-4:] == 'mean')]
size = df['Size']
df = df[list_select].round(decimals = 2)

subject = df['1649_037_D_190417_az_am_mean'] # for test only
subject2 = df['1649_050_D_190418_az_am_mean'] # for test only

####################################################################
### Finding peaks for each processed PSD in natl_psd_master.xlsx ###
####################################################################

peak_dict = {}

for col in df.columns:
    peaks = find_peaks(df[col], height = 0.1, threshold = 0.01, distance = 3)[0]
    peak_dict[int(col[5:8])] = len(peaks)

no_peak_v2 = pd.DataFrame(peak_dict.items(), columns=['SN', 'No. Peaks'])
no_peak_v2.sort_values('SN', inplace = True)

no_peak_v2.to_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd') + '/no_peak_v2.xlsx', index = False)
