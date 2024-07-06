# -*- coding: utf-8 -*-
"""
A program to make a master spreadsheet of all PM measured using Quantitative Filter Forensics Method:
    This program has 5 different steps:
        1) Reading TSP masses and their errors from gravimetric analyses of filters;
        2) Reading in filtration volumes and their errors;
        3) Reading PM2.5 and PM10 Mastersizer mass fraction of dust samples
        4) Combining all different dataframes from previous steps and build the master spreadsheet
    
@author: alima
"""

#### THE OLD VERSION CALCULATES THE ERROR DATA USING A REASONABLY SAME PROC AS STATA
#### HOWEVR, BECAUSE FOR ALMOST HALF OF THE OBSERVATIONS, ERRORS ARE SLIGHTLY DIFFERENT, WE TAKE ERRORS FROM STATA CALCULATIONS


'''
Parameters to take care:
    1) TSP mass (from weight_gain_master) [Check]
    2) Sx: from PSD data (requires combination for multiple filters of the same round)
    3) Eff 2.5 and 10: From efficiency data - RP 1649
    4) Filtration Volumes

Sources of Errors for each of these parameters are important to clarify:
    1) Sx: no error (repeatability of MS results)
    2) Eff2.5 and 10: Directly from 1649
    3) Filtration volumes : Directly from 1649
    4) TSP mass:
        a) Device (constant across all filters) [Check]
        b) Time (per filter type and according to mass filter change post-deployment) [Check]
        c) pre-deploy filter mass (based on Amy's data and our STATA codes) [Check]

How about making a column for each paramter and each source of error if not constant? That works
How about making a fix variable for each fixed error? like device (and maybe pre-deploy error source)? That works, too
How about completing a parameter along with its full error before switching to another parameter? That also works!

'''

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
import numpy as np
exec(open(r'C:\PhD Research\Generic Codes\notion_corrections.py').read())

######################################################################
###### STEP 1: READING TSP MASSES and CALCULATING THEIR ERRORS #######
######################################################################

df = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\DES\Filters_weight_gain_master.xlsx'), sheet_name = 'Gravimetric_analysis_refined')

'''
columns that might be required for later: 'filter_size', 'm_1', 'pre_p', 'm_1_1649_c', 'm_2', 'post_p', 'm_2_1649_c', 'TSPm_1649_intial', 'TSPm_1649_c', 'Commet',
'''

df = df[['SN', 'site', 'round', 'filter_code', 'Ext_loc', 'm_1_1649_c', 
         'm_1_c_cD',  'm_2_c_cD', 'm_3', 'm_4', 'Cyc_N', 'TSPm_am_c']]

df.rename(columns  = {'filter_code': 'ft',
                      'Cyc_N': 'Cycle_N',
                      'TSPm_am_c': 'TSP mass'}, inplace = True)

## Little QA for checking if TSP is correct
df['TSP Check'] = np.where(np.isnan(df['m_3']), df['m_2_c_cD'] - df['m_1_c_cD'], df['m_3'] - df['m_1_c_cD'])
df['TSP Check'] = np.where(df['TSP Check'] < 0, df['m_2_c_cD'] - df['m_1_c_cD'], df['TSP Check'])
df['Check' ] = df['TSP Check'] == df['TSP mass']

df['m_2_f'] = df['m_1_c_cD'] + df['TSP mass'] # This is ultimate post-deploy mass after selection (for error calculation purposes only)

df.drop(['TSP Check', 'Check'], inplace = True, axis = 1)

## Exception handlings for site 3 filters for TSP only (do in a separate df)
df_s3 = df[df['site'] == 3]


agg_list = {'TSP mass': sum,
            'SN' : min,
            'site' : min,
            'Ext_loc' : lambda x: pd.Series.mode(x)[0],
            'ft' : lambda x: pd.Series.mode(x)[0]}

df_s3 = df_s3.groupby('round', as_index = False).agg(agg_list)


df = df[~(df['site'] == 3)]
df = df.append(df_s3)
df = df[df['TSP mass'].notna()]

## Bringing TSP mass errors from dta file
df_tsp_mass_error = pd.read_stata(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\tsp_mass_error.dta'))
df_tsp_mass_error = df_tsp_mass_error[['SN', 'TSP_mass_error']].astype(float)

df = df.merge(df_tsp_mass_error, on = 'SN', how = 'outer')
df.rename(columns = {'TSP_mass_error': 'TSP mass error'}, inplace = True)

tsp_master_df = df[['SN', 'site', 'round', 'ft', 'Ext_loc', 'TSP mass', 'TSP mass error']]


'''
STATA CODES FOR TIME ERROR:
    
gen error_perc = abs(m_2_c_c5 - m_3)/m_2_c_c5
levelsof ft
foreach f in `r(levels)' {
	sum error_perc if ft == `f', detail
	scalar error_`f' = `r(p50)'

scalar error_device = 0.023
scalar error_in = 0.04

foreach f in `r(levels)' {
	replace error_time = sqrt((error_`f' * m_2_f) ^2 + 1.3^2) if ft == `f'
	replace TSP_mass_error = sqrt(error_time^2 + 2*error_device^2  + 2*error_in^2) if ft == `f' // error_device and error_in twice because of measurements both before and after deployment
	}

'''                              

######################################################################
###### STEP 2: READING IN FILTRATION VOLUMES AND THEIR ERRORS ########
######################################################################

## Reading correct filtration volume for site 13 round 1 (not full 3 months)

df_time = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\DES\3_month_schedule_all.xlsx'))

df_time = df_time[['date_start', 'date_end']]
day_diff = (df_time['date_end'] - df_time['date_start']).dt.days

day_diff[12] # this is the number of days you want to keep from the beginning for site 13

df_daily = pd.read_stata(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\DES\filtration volume by day.dta'))
df_daily = df_daily[(df_daily['site'] == '13') & (df_daily['filter_type'] == 'MERV 8')]
df_daily.sort_values('day', inplace = True)
df_daily = df_daily.iloc[:day_diff[12]+1,:]['total_volume_cf']
s13_r1_new_fv = df_daily.sum()

## Reading filtration volume (and correction for s13)

df_val = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\DES\filtration_volume_values.xlsx'), header = None)
df_val = df_val.unstack()
df_val = df_val.to_frame().reset_index()

df_val.rename(columns = {'level_0': 'ft',
                         'level_1': 'site',
                         0: 'filtration volume'}, inplace = True)

df_val.replace({'ft' : {0:1, 
                       1:2, 
                       2:3, 
                       3:4}}, inplace = True)

df_val['site'] = df_val['site'] + 1

s13_r1_old_fv = float(df_val.loc[(df_val['site'] == 13) & (df_val['ft'] == 1), 'filtration volume']) # taking old value for error correction later

df_val.loc[(df_val['site'] == 13) & (df_val['ft'] == 1), 'filtration volume'] = s13_r1_new_fv # correction for site 13 half lifetime filter
df_val['filtration volume'] = df_val['filtration volume'] * 0.0283168 # conversion to cubic meter
# df_val['filtration volume'] = df_val['filtration volume'].fillna(0)
df_val.replace(0 , np.nan, inplace = True)

## Reading filtration volume error (and correction for s13)
df_err = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\DES\filtration_volume_errors.xlsx'), header = None)
df_err = df_err.unstack()
df_err = df_err.to_frame().reset_index()

df_err.rename(columns = {'level_0': 'ft',
                         'level_1': 'site',
                         0: 'filtration volume error'}, inplace = True)

df_err.replace({'ft' : {0:1, 
                       1:2, 
                       2:3, 
                       3:4}}, inplace = True)

df_err['site'] = df_err['site'] + 1
df_err.loc[(df_err['site'] == 13) & (df_err['ft'] == 1), 'filtration volume error'] = (s13_r1_new_fv/s13_r1_old_fv) * df_err['filtration volume error'] # correction for site 13 half lifetime filter
df_err['filtration volume error'] = df_err['filtration volume error'] * 0.0283168
df_err.replace(0 , np.nan, inplace = True)

fv_master_df = pd.merge(df_val, df_err, on = ['site', 'ft'], how = 'outer')


############################################################################
###### STEP 3: READING IN PM2.5 and PM10 Mastersizer Mass Fractions ########
############################################################################

df_sfr = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\psd\natl_psd_master.xlsx'))
Size = df_sfr['Size']
new_cols = [col for col in df_sfr.columns if ('mean' in col) & ('_D_' in col)]
df_sfr = df_sfr[new_cols]
df_sfr = df_sfr.cumsum()
df_sfr = pd.merge(df_sfr.iloc[27,:], df_sfr.iloc[39,:], right_index=True, left_index=True)
df_sfr.reset_index(inplace = True)
df_sfr.rename(columns = {'index' : 'SN',
                         27 : 'PM2.5 Fr',
                         39 : 'PM10 Fr'}, inplace = True)

df_sfr['SN'] = df_sfr['SN'].str[5:8].astype(float)

sn_summary = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\sn_summary.xlsx'))
df_sfr = df_sfr.merge(sn_summary, on = 'SN')
df_sfr = df_sfr.drop_duplicates(['site', 'round', 'ft', 'Ext_loc'], keep = 'first')

ms_master_df = df_sfr[['ft', 'site', 'PM2.5 Fr', 'PM10 Fr']]

##########################################################################
###### STEP 4: READING IN PM2.5 and PM10 Mini-WRAS Mass Fractions ########
##########################################################################

df_eff = pd.read_csv(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\DES\eff_effectiveness.csv'))
df_eff = df_eff[(df_eff['bin'] == 2.5) | (df_eff['bin'] == 10)]
df_eff['mu_filter_eff'] = df_eff['mu_filter_eff'].pow(2) # required for quadrature error calculation
del df_eff['filter_cond']

df_eff = df_eff.groupby(['site', 'filter_type', 'bin'], as_index = False).agg({'filter_eff': 'mean', 
                                                                                      'mu_filter_eff': 'sum'})

df_eff['mu_filter_eff'] = (np.sqrt(df_eff['mu_filter_eff']))/2

df_eff_25 = df_eff[df_eff['bin'] == 2.5].drop(['bin'], axis = 1).rename(columns = {'filter_type': 'ft', 'filter_eff': 'eff_2.5', 'mu_filter_eff' : 'eff_2.5_err'})
df_eff_10 = df_eff[df_eff['bin'] == 10].drop(['bin'], axis = 1).rename(columns = {'filter_type': 'ft', 'filter_eff': 'eff_10', 'mu_filter_eff' : 'eff_10_err'})

eff_master_df = df_eff_25.merge(df_eff_10, on =['site', 'ft'], how = 'outer')


###############################################################################
###### STEP 5: Combining All DFs and Calculation of TSP, PM10, and PM25 #######
###############################################################################

pm_master_df = tsp_master_df.merge(fv_master_df, on = ['site', 'ft'], how = 'outer').merge(ms_master_df, on = ['site', 'ft'], how = 'outer').merge(eff_master_df, on = ['site', 'ft'], how = 'outer')
pm_master_df = pm_master_df.dropna(subset = ['SN'])

## PM conc and error calculations

pm_master_df['TSP Concentration'] = (pm_master_df['TSP mass'] / pm_master_df['filtration volume']) * 1000000
trheshold = pm_master_df['filtration volume'].describe([0.05]).loc['5%']
pm_master_df['TSP Concentration Error'] = pm_master_df['TSP Concentration'] * np.sqrt((pm_master_df['TSP mass error']/pm_master_df['TSP mass']).pow(2) + (pm_master_df['filtration volume error']/pm_master_df['filtration volume']).pow(2))
pm_master_df['PM10'] = pm_master_df['TSP Concentration'] * (pm_master_df['PM10 Fr']/pm_master_df['eff_10'])
pm_master_df['PM2.5'] = pm_master_df['TSP Concentration'] * (pm_master_df['PM2.5 Fr']/pm_master_df['eff_2.5'])

pm_master_df.loc[pm_master_df['filtration volume'] < trheshold, 'TSP Concentration'] = np.nan

## QA for PM10 and PM2.5
pm_master_df.loc[pm_master_df['PM10'] > pm_master_df['TSP Concentration'], 'PM10'] = np.nan
pm_master_df.loc[pm_master_df['PM2.5'] > pm_master_df['TSP Concentration'], 'PM2.5'] = np.nan
pm_master_df.loc[pm_master_df['PM2.5'] > pm_master_df['PM10'], 'PM2.5'] = np.nan


pm_master_df['PM10 error'] = pm_master_df['PM10'] * np.sqrt((pm_master_df['TSP Concentration Error']/pm_master_df['TSP Concentration']).pow(2) + (pm_master_df['eff_10_err']/pm_master_df['eff_10']).pow(2))
pm_master_df['PM2.5 error'] = pm_master_df['PM2.5'] * np.sqrt((pm_master_df['TSP Concentration Error']/pm_master_df['TSP Concentration']).pow(2) + (pm_master_df['eff_2.5_err']/pm_master_df['eff_2.5']).pow(2))

new_col_order = ['SN', 'site', 'round', 'ft', 
                 'TSP Concentration', 'TSP Concentration Error', 'PM10', 'PM10 error', 'PM2.5', 'PM2.5 error', 
                 'TSP mass', 'TSP mass error', 'filtration volume', 'filtration volume error', 'PM2.5 Fr', 'PM10 Fr',
                 'eff_2.5', 'eff_2.5_err', 'eff_10', 'eff_10_err', 
                 'Ext_loc']

pm_master_df = pm_master_df[new_col_order]

pm_master_df.to_excel(backslash_correct(r'C:\PhD Research\Paper 2 - PSD_QFF\Processed\pm_master.xlsx'), index = False)

