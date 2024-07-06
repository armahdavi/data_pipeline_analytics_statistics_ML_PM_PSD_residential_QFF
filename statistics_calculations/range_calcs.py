# -*- coding: utf-8 -*-

"""
Program to qiuery and calculate the descriptive statistics of various parameters studied including:
    1) TSP (concentration and mass)
    2) PM 2.5 and PM10 (concnetration and mass)
    2) Filtration volume
    3) Filter efficiency for PM2.5 and PM10
    4) Dx values
    
@author: alima
"""

import pandas as pd
from scipy.stats import spearmanr 
from scipy.stats import ranksums

exec(open(r'C:\PhD Research\Generic Codes\notion_corrections.py').read())


#########################################################
### PM Concentrations, PM Mass, and Fitration Volumns ###
#########################################################

df1 = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\pm_master.xlsx'))
df1['TSP Concentration'].describe()
df1['TSP mass'].describe()
df1['filtration volume'].describe()

## TSP mass vs. round
spearmanr(df1['TSP mass'], df1['filtration volume'])

ranksums(df1[df1['round'] == 1]['TSP mass'], df1[df1['round'] == 2]['TSP mass'])
ranksums(df1[df1['round'] == 1]['TSP mass'], df1[df1['round'] == 3]['TSP mass'])
ranksums(df1[df1['round'] == 1]['TSP mass'], df1[df1['round'] == 4]['TSP mass'])
ranksums(df1[df1['round'] == 2]['TSP mass'], df1[df1['round'] == 3]['TSP mass'])
ranksums(df1[df1['round'] == 2]['TSP mass'], df1[df1['round'] == 4]['TSP mass'])
ranksums(df1[df1['round'] == 3]['TSP mass'], df1[df1['round'] == 4]['TSP mass'])                                               

## FV vs. round
ranksums(df1[df1['round'] == 1]['filtration volume'], df1[df1['round'] == 2]['filtration volume']) # Significant
ranksums(df1[df1['round'] == 1]['filtration volume'], df1[df1['round'] == 3]['filtration volume']) # Significant
ranksums(df1[df1['round'] == 1]['filtration volume'], df1[df1['round'] == 4]['filtration volume']) # Significant

ranksums(df1[df1['round'] == 1]['filtration volume'], df1[df1['round'] != 1]['filtration volume']) # Significant

ranksums(df1[df1['round'] == 2]['filtration volume'], df1[df1['round'] == 3]['filtration volume'])
ranksums(df1[df1['round'] == 2]['filtration volume'], df1[df1['round'] == 4]['filtration volume'])
ranksums(df1[df1['round'] == 3]['filtration volume'], df1[df1['round'] == 4]['filtration volume'])                                               

## TSP mass vs. FT
ranksums(df1[df1['ft'] == 1]['TSP mass'], df1[df1['ft'] == 2]['TSP mass'])
ranksums(df1[df1['ft'] == 1]['TSP mass'], df1[df1['ft'] == 3]['TSP mass'])
ranksums(df1[df1['ft'] == 1]['TSP mass'], df1[df1['ft'] == 4]['TSP mass'])
ranksums(df1[df1['ft'] == 2]['TSP mass'], df1[df1['ft'] == 3]['TSP mass'])
ranksums(df1[df1['ft'] == 2]['TSP mass'], df1[df1['ft'] == 4]['TSP mass'])
ranksums(df1[df1['ft'] == 3]['TSP mass'], df1[df1['ft'] == 4]['TSP mass'])   

## TSP mass vs. FT                          
ranksums(df1[df1['ft'] == 1]['filtration volume'], df1[df1['ft'] == 2]['filtration volume'])
ranksums(df1[df1['ft'] == 1]['filtration volume'], df1[df1['ft'] == 3]['filtration volume'])
ranksums(df1[df1['ft'] == 1]['filtration volume'], df1[df1['ft'] == 4]['filtration volume'])
ranksums(df1[df1['ft'] == 2]['filtration volume'], df1[df1['ft'] == 3]['filtration volume'])
ranksums(df1[df1['ft'] == 2]['filtration volume'], df1[df1['ft'] == 4]['filtration volume'])
ranksums(df1[df1['ft'] == 3]['filtration volume'], df1[df1['ft'] == 4]['filtration volume'])  

## QFF vs FF and Inv FV
df1_ref = df1
spearmanr(df1['TSP Concentration'], df1['TSP mass'], nan_policy='omit')
spearmanr(df1['TSP Concentration'], df1['filtration volume'], nan_policy='omit')

a = df1['filtration volume'].describe().loc['75%']
spearmanr(df1[df1['filtration volume'] > a]['TSP Concentration'], df1[df1['filtration volume'] > a]['TSP mass'], nan_policy='omit')

## PM10: QFF vs FF and Inv FV
spearmanr(df1['PM10'], df1['TSP mass']*df1['PM10 Fr'], nan_policy='omit')
spearmanr(df1['PM10'], df1['filtration volume']*df1['eff_10'], nan_policy='omit') # Significant

spearmanr(df1['PM2.5'], df1['TSP mass']*df1['PM2.5 Fr'], nan_policy='omit')
spearmanr(df1['PM2.5'], df1['filtration volume']*df1['eff_2.5'], nan_policy='omit') # Significant

## TSP mass for 6_cyc filters
df1[(df1['SN'] == 33) | (df1['SN'] == 41) | (df1['SN'] == 46) | (df1['SN'] == 49)]['TSP mass'].describe()

## PM10/2.5 Eff vs. FT
ranksums(df1[df1['ft'] == 1]['eff_10'], df1[df1['ft'] == 2]['eff_10'])
ranksums(df1[df1['ft'] == 1]['eff_10'], df1[df1['ft'] == 3]['eff_10'])
ranksums(df1[df1['ft'] == 1]['eff_10'], df1[df1['ft'] == 4]['eff_10']) # Significant
ranksums(df1[df1['ft'] == 2]['eff_10'], df1[df1['ft'] == 3]['eff_10'])
ranksums(df1[df1['ft'] == 2]['eff_10'], df1[df1['ft'] == 4]['eff_10']) # Significant
ranksums(df1[df1['ft'] == 3]['eff_10'], df1[df1['ft'] == 4]['eff_10'])

ranksums(df1[df1['ft'] == 1]['eff_2.5'], df1[df1['ft'] == 2]['eff_2.5']) # Significant
ranksums(df1[df1['ft'] == 1]['eff_2.5'], df1[df1['ft'] == 3]['eff_2.5']) # Significant
ranksums(df1[df1['ft'] == 1]['eff_2.5'], df1[df1['ft'] == 4]['eff_2.5']) # Significant
ranksums(df1[df1['ft'] == 2]['eff_2.5'], df1[df1['ft'] == 3]['eff_2.5'])
ranksums(df1[df1['ft'] == 2]['eff_2.5'], df1[df1['ft'] == 4]['eff_2.5']) # Significant
ranksums(df1[df1['ft'] == 3]['eff_2.5'], df1[df1['ft'] == 4]['eff_2.5']) # Significant

## PM10/2.5 vs/ Eff_10/2.5
spearmanr(df1['PM10 Fr'], df1['eff_10'])
spearmanr(df1['PM2.5 Fr'], df1['eff_2.5'])

#####################################################
### DC vs. PM results made inside the figure code ###
#####################################################

## Dx 50
df2 = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\natl_d_summary.xlsx'))
df2['Dx (50)'].describe()

df3 = pd.read_excel(r'C:/PhD Research/Paper 2 - PSD_QFF/Processed/psd/hud_d_master.xlsx')
df3 = df3[df3['stat'] == 'median']
df3['Sample Type'] = df3['Sample Name'].str[-5:-3]

df3.loc[df3['Sample Type'] == 'D_', 'Sample Type'] = 'FD'
df3[df3['Sample Type'] == 'FD']['Dx (50)'].describe()


## Laser obscuration
df4 = pd.read_excel(r'C:/PhD Research/Paper 2 - PSD_QFF/Processed/psd/laser_obs_master.xlsx')
df4[(df4['Laser Obscuration'] < 10) & (df4['Fr'] == "D")]['Laser Obscuration'].describe()
df4[(df4['Laser Obscuration'] < 10) & (df4['Fr'] == "D")]['Laser Obscuration'].iloc[:-1].describe() # Why one is not included in STATA Data?
df4[(df4['Laser Obscuration'] < 10) & (df4['Fr'] == "D")]
df4['SN'].value_counts
len(df4['SN'].unique())
len(df4[(df4['Laser Obscuration'] < 10) & (df4['Fr'] == "D")])
len(df4[(df4['Laser Obscuration'] < 10) & (df4['Fr'] == "S")])


## Peak locator
df5 = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\peak_locator.xlsx'))
df5 = df5[df5['Fr'] == 'D']
df5['Peak Size'].describe()



#####################################
### D-Values vs. House Properties ###
#####################################

df6 = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\pm_d_prop.xlsx'))

## Filtration volume
spearmanr(df6['Dx (0)'], df6['filtration volume'])
spearmanr(df6['Dx (10)'], df6['filtration volume'])
spearmanr(df6['Dx (25)'], df6['filtration volume'])
spearmanr(df6['Dx (50)'], df6['filtration volume'])
spearmanr(df6['Dx (75)'], df6['filtration volume'])
spearmanr(df6['Dx (90)'], df6['filtration volume'])
spearmanr(df6['Dx (100)'], df6['filtration volume'])


## season (i.e. round)
ranksums(df6[df6['round'] == 1]['Dx (0)'], df6[df6['round'] == 2]['Dx (0)'])
ranksums(df6[df6['round'] == 1]['Dx (0)'], df6[df6['round'] == 3]['Dx (0)'])
ranksums(df6[df6['round'] == 1]['Dx (0)'], df6[df6['round'] == 4]['Dx (0)'])
ranksums(df6[df6['round'] == 2]['Dx (0)'], df6[df6['round'] == 3]['Dx (0)'])
ranksums(df6[df6['round'] == 2]['Dx (0)'], df6[df6['round'] == 4]['Dx (0)'])
ranksums(df6[df6['round'] == 3]['Dx (0)'], df6[df6['round'] == 4]['Dx (0)'])

ranksums(df6[df6['round'] == 1]['Dx (25)'], df6[df6['round'] == 2]['Dx (25)'])
ranksums(df6[df6['round'] == 1]['Dx (25)'], df6[df6['round'] == 3]['Dx (25)'])
ranksums(df6[df6['round'] == 1]['Dx (25)'], df6[df6['round'] == 4]['Dx (25)'])
ranksums(df6[df6['round'] == 2]['Dx (25)'], df6[df6['round'] == 3]['Dx (25)'])
ranksums(df6[df6['round'] == 2]['Dx (25)'], df6[df6['round'] == 4]['Dx (25)'])
ranksums(df6[df6['round'] == 3]['Dx (25)'], df6[df6['round'] == 4]['Dx (25)'])

ranksums(df6[df6['round'] == 1]['Dx (50)'], df6[df6['round'] == 2]['Dx (50)'])
ranksums(df6[df6['round'] == 1]['Dx (50)'], df6[df6['round'] == 3]['Dx (50)'])
ranksums(df6[df6['round'] == 1]['Dx (50)'], df6[df6['round'] == 4]['Dx (50)'])
ranksums(df6[df6['round'] == 2]['Dx (50)'], df6[df6['round'] == 3]['Dx (50)'])
ranksums(df6[df6['round'] == 2]['Dx (50)'], df6[df6['round'] == 4]['Dx (50)'])
ranksums(df6[df6['round'] == 3]['Dx (50)'], df6[df6['round'] == 4]['Dx (50)'])

ranksums(df6[df6['round'] == 1]['Dx (75)'], df6[df6['round'] == 2]['Dx (75)'])
ranksums(df6[df6['round'] == 1]['Dx (75)'], df6[df6['round'] == 3]['Dx (75)'])
ranksums(df6[df6['round'] == 1]['Dx (75)'], df6[df6['round'] == 4]['Dx (75)'])
ranksums(df6[df6['round'] == 2]['Dx (75)'], df6[df6['round'] == 3]['Dx (75)'])
ranksums(df6[df6['round'] == 2]['Dx (75)'], df6[df6['round'] == 4]['Dx (75)'])
ranksums(df6[df6['round'] == 3]['Dx (75)'], df6[df6['round'] == 4]['Dx (75)'])


## House volume
spearmanr(df6['Dx (0)'], df6['volume'])
spearmanr(df6['Dx (10)'], df6['volume'])
spearmanr(df6['Dx (25)'], df6['volume'])
spearmanr(df6['Dx (50)'], df6['volume'])
spearmanr(df6['Dx (75)'], df6['volume'])
spearmanr(df6['Dx (90)'], df6['volume'])
spearmanr(df6['Dx (100)'], df6['volume'])


## Floor Area
spearmanr(df6['Dx (0)'], df6['floor_area'])
spearmanr(df6['Dx (10)'], df6['floor_area'])
spearmanr(df6['Dx (25)'], df6['floor_area'])
spearmanr(df6['Dx (50)'], df6['floor_area'])
spearmanr(df6['Dx (75)'], df6['floor_area'])
spearmanr(df6['Dx (90)'], df6['floor_area'])
spearmanr(df6['Dx (100)'], df6['floor_area'])


## No. occup
spearmanr(df6['Dx (0)'], df6['no_occupants']) # This is significant but there is weak correlation
spearmanr(df6['Dx (10)'], df6['no_occupants']) # This is significant but there is weak correlation
spearmanr(df6['Dx (25)'], df6['no_occupants']) # This is significant but there is weak correlation
spearmanr(df6['Dx (50)'], df6['no_occupants']) # This is significant but there is weak correlation
spearmanr(df6['Dx (75)'], df6['no_occupants']) # This is significant but there is weak correlation
spearmanr(df6['Dx (90)'], df6['no_occupants']) # This is significant but there is weak correlation
spearmanr(df6['Dx (100)'], df6['no_occupants']) 


## Basement apartment
ranksums(df6[df6['basement_apartment'] == 'no']['Dx (0)'], df6[df6['basement_apartment'] == 'yes']['Dx (0)'])
ranksums(df6[df6['basement_apartment'] == 'no']['Dx (10)'], df6[df6['basement_apartment'] == 'yes']['Dx (10)'])
ranksums(df6[df6['basement_apartment'] == 'no']['Dx (25)'], df6[df6['basement_apartment'] == 'yes']['Dx (25)'])
ranksums(df6[df6['basement_apartment'] == 'no']['Dx (50)'], df6[df6['basement_apartment'] == 'yes']['Dx (50)'])
ranksums(df6[df6['basement_apartment'] == 'no']['Dx (75)'], df6[df6['basement_apartment'] == 'yes']['Dx (75)'])
ranksums(df6[df6['basement_apartment'] == 'no']['Dx (90)'], df6[df6['basement_apartment'] == 'yes']['Dx (90)'])
ranksums(df6[df6['basement_apartment'] == 'no']['Dx (100)'], df6[df6['basement_apartment'] == 'yes']['Dx (100)'])


## No. pets
ranksums(df6[df6['no_pets'] == 0]['Dx (0)'], df6[df6['no_pets'] != 0]['Dx (0)'])
ranksums(df6[df6['no_pets'] == 0]['Dx (10)'], df6[df6['no_pets'] != 0]['Dx (10)'])
ranksums(df6[df6['no_pets'] == 0]['Dx (25)'], df6[df6['no_pets'] != 0]['Dx (25)'])
ranksums(df6[df6['no_pets'] == 0]['Dx (50)'], df6[df6['no_pets'] != 0]['Dx (50)'])
ranksums(df6[df6['no_pets'] == 0]['Dx (75)'], df6[df6['no_pets'] != 0]['Dx (75)'])
ranksums(df6[df6['no_pets'] == 0]['Dx (90)'], df6[df6['no_pets'] != 0]['Dx (90)'])
ranksums(df6[df6['no_pets'] == 0]['Dx (100)'], df6[df6['no_pets'] != 0]['Dx (100)'])


## Buiding type
df6['building_type'].unique()
'semi', 'detatched', 'townhouse', 'condo'

ranksums(df6[df6['building_type'] == 'semi']['Dx (0)'], df6[df6['building_type'] == 'detatched']['Dx (0)'])
ranksums(df6[df6['building_type'] == 'semi']['Dx (0)'], df6[df6['building_type'] == 'townhouse']['Dx (0)'])
ranksums(df6[df6['building_type'] == 'semi']['Dx (0)'], df6[df6['building_type'] == 'condo']['Dx (0)']) # Significant
ranksums(df6[df6['building_type'] == 'detatched']['Dx (0)'], df6[df6['building_type'] == 'townhouse']['Dx (0)'])
ranksums(df6[df6['building_type'] == 'detatched']['Dx (0)'], df6[df6['building_type'] == 'condo']['Dx (0)']) 
ranksums(df6[df6['building_type'] == 'townhouse']['Dx (0)'], df6[df6['building_type'] == 'condo']['Dx (0)']) # Significant

ranksums(df6[df6['building_type'] == 'semi']['Dx (10)'], df6[df6['building_type'] == 'detatched']['Dx (10)']) # close to significant
ranksums(df6[df6['building_type'] == 'semi']['Dx (10)'], df6[df6['building_type'] == 'townhouse']['Dx (10)'])
ranksums(df6[df6['building_type'] == 'semi']['Dx (10)'], df6[df6['building_type'] == 'condo']['Dx (10)']) # Significant
ranksums(df6[df6['building_type'] == 'detatched']['Dx (10)'], df6[df6['building_type'] == 'townhouse']['Dx (10)'])
ranksums(df6[df6['building_type'] == 'detatched']['Dx (10)'], df6[df6['building_type'] == 'condo']['Dx (10)']) 
ranksums(df6[df6['building_type'] == 'townhouse']['Dx (10)'], df6[df6['building_type'] == 'condo']['Dx (10)']) # close to significant

ranksums(df6[df6['building_type'] == 'semi']['Dx (50)'], df6[df6['building_type'] == 'detatched']['Dx (50)'])
ranksums(df6[df6['building_type'] == 'semi']['Dx (50)'], df6[df6['building_type'] == 'townhouse']['Dx (50)'])
ranksums(df6[df6['building_type'] == 'semi']['Dx (50)'], df6[df6['building_type'] == 'condo']['Dx (50)']) # Significant
ranksums(df6[df6['building_type'] == 'detatched']['Dx (50)'], df6[df6['building_type'] == 'townhouse']['Dx (50)'])
ranksums(df6[df6['building_type'] == 'detatched']['Dx (50)'], df6[df6['building_type'] == 'condo']['Dx (50)'])
ranksums(df6[df6['building_type'] == 'townhouse']['Dx (50)'], df6[df6['building_type'] == 'condo']['Dx (50)'])

ranksums(df6[df6['building_type'] == 'semi']['Dx (90)'], df6[df6['building_type'] == 'detatched']['Dx (90)'])
ranksums(df6[df6['building_type'] == 'semi']['Dx (90)'], df6[df6['building_type'] == 'townhouse']['Dx (90)'])
ranksums(df6[df6['building_type'] == 'semi']['Dx (90)'], df6[df6['building_type'] == 'condo']['Dx (90)']) # Significant
ranksums(df6[df6['building_type'] == 'detatched']['Dx (90)'], df6[df6['building_type'] == 'townhouse']['Dx (90)'])
ranksums(df6[df6['building_type'] == 'detatched']['Dx (90)'], df6[df6['building_type'] == 'condo']['Dx (90)'])
ranksums(df6[df6['building_type'] == 'townhouse']['Dx (90)'], df6[df6['building_type'] == 'condo']['Dx (90)'])


###########################################
### TSP/PM10/PM2.5 vs. House Properties ###
###########################################

## round
ranksums(df6[df6['round'] == 1]['TSP Concentration'], df6[df6['round'] == 2]['TSP Concentration'])
ranksums(df6[df6['round'] == 1]['TSP Concentration'], df6[df6['round'] == 3]['TSP Concentration']) # close to significant
ranksums(df6[df6['round'] == 1]['TSP Concentration'], df6[df6['round'] == 4]['TSP Concentration'])
ranksums(df6[df6['round'] == 2]['TSP Concentration'], df6[df6['round'] == 3]['TSP Concentration'])
ranksums(df6[df6['round'] == 2]['TSP Concentration'], df6[df6['round'] == 4]['TSP Concentration'])
ranksums(df6[df6['round'] == 3]['TSP Concentration'], df6[df6['round'] == 4]['TSP Concentration'])

ranksums(df6[df6['round'] == 1]['PM10'], df6[df6['round'] == 2]['PM10'])
ranksums(df6[df6['round'] == 1]['PM10'], df6[df6['round'] == 3]['PM10'])
ranksums(df6[df6['round'] == 1]['PM10'], df6[df6['round'] == 4]['PM10'])
ranksums(df6[df6['round'] == 2]['PM10'], df6[df6['round'] == 3]['PM10'])
ranksums(df6[df6['round'] == 2]['PM10'], df6[df6['round'] == 4]['PM10'])
ranksums(df6[df6['round'] == 3]['PM10'], df6[df6['round'] == 4]['PM10'])

ranksums(df6[df6['round'] == 1]['PM2.5'], df6[df6['round'] == 2]['PM2.5'])
ranksums(df6[df6['round'] == 1]['PM2.5'], df6[df6['round'] == 3]['PM2.5'])
ranksums(df6[df6['round'] == 1]['PM2.5'], df6[df6['round'] == 4]['PM2.5'])
ranksums(df6[df6['round'] == 2]['PM2.5'], df6[df6['round'] == 3]['PM2.5'])
ranksums(df6[df6['round'] == 2]['PM2.5'], df6[df6['round'] == 4]['PM2.5'])
ranksums(df6[df6['round'] == 3]['PM2.5'], df6[df6['round'] == 4]['PM2.5'])

## PM source evidence
ranksums(df6[df6['evidence_pm_source'] != 'no']['TSP Concentration'], df6[df6['evidence_pm_source'] == 'no']['TSP Concentration'])
ranksums(df6[df6['evidence_pm_source'] != 'no']['PM10'], df6[df6['evidence_pm_source'] == 'no']['PM10'])
ranksums(df6[df6['evidence_pm_source'] != 'no']['PM2.5'], df6[df6['evidence_pm_source'] == 'no']['PM2.5'])

## Building type
ranksums(df6[df6['building_type'] == 'semi']['TSP Concentration'], df6[df6['building_type'] == 'detatched']['TSP Concentration'])
ranksums(df6[df6['building_type'] == 'semi']['TSP Concentration'], df6[df6['building_type'] == 'townhouse']['TSP Concentration'])
ranksums(df6[df6['building_type'] == 'semi']['TSP Concentration'], df6[df6['building_type'] == 'condo']['TSP Concentration'])
ranksums(df6[df6['building_type'] == 'detatched']['TSP Concentration'], df6[df6['building_type'] == 'townhouse']['TSP Concentration'])
ranksums(df6[df6['building_type'] == 'detatched']['TSP Concentration'], df6[df6['building_type'] == 'condo']['TSP Concentration']) 
ranksums(df6[df6['building_type'] == 'townhouse']['TSP Concentration'], df6[df6['building_type'] == 'condo']['TSP Concentration'])

ranksums(df6[df6['building_type'] == 'semi']['PM10'], df6[df6['building_type'] == 'detatched']['PM10'])
ranksums(df6[df6['building_type'] == 'semi']['PM10'], df6[df6['building_type'] == 'townhouse']['PM10'])
ranksums(df6[df6['building_type'] == 'semi']['PM10'], df6[df6['building_type'] == 'condo']['PM10']) # Significant
ranksums(df6[df6['building_type'] == 'detatched']['PM10'], df6[df6['building_type'] == 'townhouse']['PM10'])
ranksums(df6[df6['building_type'] == 'detatched']['PM10'], df6[df6['building_type'] == 'condo']['PM10']) 
ranksums(df6[df6['building_type'] == 'townhouse']['PM10'], df6[df6['building_type'] == 'condo']['PM10'])

ranksums(df6[df6['building_type'] == 'semi']['PM2.5'], df6[df6['building_type'] == 'detatched']['PM2.5'])
ranksums(df6[df6['building_type'] == 'semi']['PM2.5'], df6[df6['building_type'] == 'townhouse']['PM2.5'])
ranksums(df6[df6['building_type'] == 'semi']['PM2.5'], df6[df6['building_type'] == 'condo']['PM2.5']) # Significant
ranksums(df6[df6['building_type'] == 'detatched']['PM2.5'], df6[df6['building_type'] == 'townhouse']['PM2.5'])
ranksums(df6[df6['building_type'] == 'detatched']['PM2.5'], df6[df6['building_type'] == 'condo']['PM2.5']) # Significant
ranksums(df6[df6['building_type'] == 'townhouse']['PM2.5'], df6[df6['building_type'] == 'condo']['PM2.5'])

