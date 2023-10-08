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



### import data
data_all = pd.DataFrame()

for j in (1, 2):
    for i in range(1, 8):
        data = pd.read_csv('Experiment{}_hpc/model3_{}/data/E1_data_parameters/parameters_best.csv'.format(j, i))
        if data.columns.shape[0] == 7:
            if i == 1:
                data.columns = ['label', 'p', 'slope', 'bias', 'loglike', 'AIC', 'success']
            else:
                data.columns = ['label', 'b', 'slope', 'bias', 'loglike', 'AIC', 'success']
        elif data.columns.shape[0] == 8:
            data.columns = ['label', 'p', 'b', 'slope', 'bias', 'loglike', 'AIC', 'success']
        
        data['Model'] = 'model3_{}'.format(i)
        data['Experiment'] = 'Experiment'+str(j)
        
        data_all = pd.concat([data_all, data], axis=0)



### only retain the data of model1, model3, and model5
data_model1 = data_all[data_all['Model']=='model3_1']
data_model3 = data_all[data_all['Model']=='model3_3']
data_model5 = data_all[data_all['Model']=='model3_5']
data_all = pd.concat([data_model1, data_model3, data_model5], axis=0)


### plot AIC
data_all_plot = data_all.copy()
data_all_plot['Model'].replace(['model3_1', 'model3_3', 'model3_5'], ['Pre-learning', 'RPE learning', 'Pre+RPE learning'], inplace=True)

plt.rcParams['font.size'] = 15

fig1 = sns.catplot(data=data_all_plot, x='Experiment', y='AIC', kind='bar', hue='Model', errorbar='se')
fig1.fig.set_dpi(300)
#fig1.legend.set_bbox_to_anchor((0.8, 1.1))
#fig1.fig.set_figwidth(10)
#fig1.fig.set_figheight(5)
fig1.set_xticklabels(size=15)
fig1.set_yticklabels(size=15)
fig1.set_xlabels('Experiment', size=20)
fig1.set_ylabels('AIC', size=20)



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
data_waics.columns = ['model1', 'model3', 'model5', 'Experiment']
data_waics = data_waics.melt(id_vars=['Experiment'], value_vars=['model1', 'model3', 'model5'], var_name=['Model'], value_name='wAIC')

data_waics['Model'].replace(['model1', 'model3', 'model5'], ['Pre', 'RPE', 'Pre+RPE'], inplace=True)

fig2 = sns.catplot(data=data_waics, x='Experiment', y='wAIC', kind='bar', hue='Model', errorbar='se')
fig2.fig.set_dpi(300)
#fig2.fig.set_figwidth(10)
#fig2.fig.set_figheight(5)
#fig2.set_xticklabels(['Pre-learning', 'RPE learning', 'Pre-learning+RPE learning'], rotation=0, size=20)
#fig2.set_yticklabels(size=20)
fig2.set_xlabels('Experiment', size=20)
fig2.set_ylabels('wAIC', size=20)
fig2.set(yticks=np.arange(0, 1.2, 0.2))
fig2.savefig('summary/figures/wAIC.tif', dpi=300)






              





