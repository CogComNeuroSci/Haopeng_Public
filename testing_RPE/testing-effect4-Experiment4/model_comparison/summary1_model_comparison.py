# -*- coding: utf-8 -*-
"""
Created on Tue May  9 09:14:32 2023

@author: haopchen

parameters and AIC
"""

### import modules
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


### settings
which_data = 'continuous' # full, binary, continuous
which_model = 'all' # all or part


### models
if which_model=='all':
    models = list(range(1, 11))
else:
    models = list(range(1, 8))


### import data
## used subjects
formal_data_e1 = pd.read_csv(r'../Experiment1_hpc_all_sub/model3_1/data/E1_original_data/data_preprocess.csv')
formal_data_e2 = pd.read_csv(r'../Experiment2_hpc_all_sub/model3_1/data/E1_original_data/data_preprocess.csv')

all_subs_e1 = (formal_data_e1['participant'].unique()).tolist()
all_subs_e2 = (formal_data_e2['participant'].unique()).tolist()

if which_data=='full':
    subjects_e1 = (formal_data_e1['participant'].unique()).tolist()
    subjects_e2 = (formal_data_e2['participant'].unique()).tolist()
elif which_data=='binary':    
    subjects_e1 = (formal_data_e1.loc[formal_data_e1['individual_binary_acc']>=0.34, 'participant'].unique()).tolist()
    subjects_e2 = (formal_data_e2.loc[formal_data_e2['individual_binary_acc']>=0.34, 'participant'].unique()).tolist()
else:
    subjects_e1 = (formal_data_e1.loc[formal_data_e1['individual_continuous_acc']>=0.34, 'participant'].unique()).tolist()
    subjects_e2 = (formal_data_e2.loc[formal_data_e2['individual_continuous_acc']>=0.34, 'participant'].unique()).tolist()

## parameters
data_all = pd.DataFrame()

for j in (1, 2):
    for i in models:
        data = pd.read_csv('../Experiment{}_hpc_all_sub/model3_{}/data/E1_data_parameters/parameters_best.csv'.format(j, i))
        
        if j==1:
            data.index = all_subs_e1
            data = data.loc[subjects_e1, :]
        else:
            data.index = all_subs_e2
            data = data.loc[subjects_e2, :]
        
        
        if data.columns.shape[0] == 7:
            if i == 1:
                data.columns = ['label', 'p', 'slope', 'bias', 'loglike', 'AIC', 'success']
            else:
                data.columns = ['label', 'b', 'slope', 'bias', 'loglike', 'AIC', 'success']
        elif data.columns.shape[0] == 8:
            data.columns = ['label', 'p', 'b', 'slope', 'bias', 'loglike', 'AIC', 'success']
        else:
            data.columns = ['label', 'p', 'b1', 'b2', 'slope', 'bias', 'loglike', 'AIC', 'success']
        
        data['Model'] = i
        data['Experiment'] = 'Experiment'+str(j)
        
        data_all = pd.concat([data_all, data], axis=0)


### waic
data_waics = pd.DataFrame()
for i in [1, 2]:
    data_aic = data_all[data_all['Experiment']=='Experiment'+str(i)]
    data_aic = data_aic.pivot(columns=['Model'], values=['AIC'])
    data_aic = data_aic.reset_index()
    data_delta_aic = data_aic.iloc[:, 1:].values - data_aic.iloc[:, 1:].min(axis=1).values[:, np.newaxis]
    #data_delta_aic = data_aic.iloc[:, 1:].values
    data_waic = np.exp(-(1/2)*data_delta_aic)/np.exp(-(1/2)*data_delta_aic).sum(axis=1)[:, np.newaxis]
    
    data_waic = pd.DataFrame(data_waic)
    data_waic['Experiment'] = 'Experiment'+str(i)
    
    data_waics = pd.concat([data_waics, data_waic], axis=0)


### plot waic
data_waics.columns = models + ['Experiment']
data_waics.to_csv('data/wAIC.csv')
data_waics = data_waics.melt(id_vars=['Experiment'], value_vars=models, var_name=['Model'], value_name='wAIC')

data_waics_e1 = data_waics[data_waics['Experiment']=='Experiment1']

fig2 = sns.catplot(data=data_waics_e1, x='Model', y='wAIC', kind='bar', errorbar='se', aspect=2, color='gray')
fig2.fig.set_dpi(300)
#fig2.fig.set_figwidth(10)
#fig2.fig.set_figheight(5)
#fig2.set_xticklabels(['Pre-learning', 'RPE learning', 'Pre-learning+RPE learning'], rotation=0, size=20)
fig2.set_xticklabels(size=25)
fig2.set_yticklabels(size=25)
fig2.set_xlabels('Model', size=25)
fig2.set_ylabels(size=25)
#fig2.set_ylabels('wAIC', size=18)
#fig2.set(yticks=np.arange(0, 1.2, 0.2))
fig2.savefig('figures/wAIC_all_e1.tif', dpi=300)

data_waics_e2 = data_waics[data_waics['Experiment']=='Experiment2']

fig2 = sns.catplot(data=data_waics_e2, x='Model', y='wAIC', kind='bar', errorbar='se', aspect=2, color='gray')
fig2.fig.set_dpi(300)
fig2.set_xlabels('Model', size=25)
fig2.set_ylabels(size=25)
fig2.set_xticklabels(size=25)
fig2.set_yticklabels(size=25)
fig2.savefig('figures/wAIC_all_e2.tif', dpi=300)


