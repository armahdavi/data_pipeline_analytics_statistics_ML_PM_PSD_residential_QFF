# -*- coding: utf-8 -*-
"""
Program to query and obtain additional calculations used in Table S2 of the SI

@author: alima
"""

import pandas as pd
df = pd.read_excel(r'C:/PhD Research/Paper 2 - PSD_QFF/PhD - PSD TSP/Processed/sn_summary.xlsx')

# column 2:
len(df[df['round'] == 1])
len(df[df['round'] == 2])
len(df[df['round'] == 3])
len(df[df['round'] == 4])

# column 3:
len(df[df['round'] == 1]['site'].unique())
len(df[df['round'] == 2]['site'].unique())
len(df[df['round'] == 3]['site'].unique())
len(df[df['round'] == 4]['site'].unique())

# columns 4-7:
len(df[(df['round'] == 1) & (df['ft'] == 1)])
len(df[(df['round'] == 1) & (df['ft'] == 2)])
len(df[(df['round'] == 1) & (df['ft'] == 3)])
len(df[(df['round'] == 1) & (df['ft'] == 4)])
    
len(df[(df['round'] == 2) & (df['ft'] == 1)])
len(df[(df['round'] == 2) & (df['ft'] == 2)])
len(df[(df['round'] == 2) & (df['ft'] == 3)])
len(df[(df['round'] == 2) & (df['ft'] == 4)])

len(df[(df['round'] == 3) & (df['ft'] == 1)])
len(df[(df['round'] == 3) & (df['ft'] == 2)])
len(df[(df['round'] == 3) & (df['ft'] == 3)])
len(df[(df['round'] == 3) & (df['ft'] == 4)])

len(df[(df['round'] == 4) & (df['ft'] == 1)])
len(df[(df['round'] == 4) & (df['ft'] == 2)])
len(df[(df['round'] == 4) & (df['ft'] == 3)])
len(df[(df['round'] == 4) & (df['ft'] == 4)])

