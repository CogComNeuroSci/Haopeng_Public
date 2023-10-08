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
### import data
data_all = pd.DataFrame()

for j in (1, 2):
    for i in range(1, 8):
        data = pd.read_csv('../Experiment{}_hpc/model3_{}/data/E1_data_parameters/parameters_best.csv'.format(j, i))
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




### plot AIC
data_all_plot = data_all.copy()
data_all_plot['Model'].replace(['model3_1', 'model3_2', 'model3_3', 'model3_4', 'model3_5', 'model3_6', 'model3_7'], ['Pre-learning', 'Feedback learning', 'RPE learning', 'Pre+Feedback learning', 'Pre+RPE learning', 'Feedback+RPE learning', 'Pre+Feedback+RPE learning'], inplace=True)

plt.rcParams['font.size'] = 18

fig1 = sns.catplot(data=data_all_plot, x='Experiment', y='AIC', kind='bar', hue='Model', errorbar='se')
fig1.fig.set_dpi(300)
#fig1.legend.set_bbox_to_anchor((0.8, 1.1))
#fig1.fig.set_figwidth(10)
#fig1.fig.set_figheight(5)
#fig1.set_xticklabels(['Pre-learning', 'RPE learning', 'Pre-learning+RPE learning'], rotation=25, size=15)
fig1.set_xlabels('Experiment', size=18)
fig1.set_ylabels('AIC', size=18)



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
data_waics.columns = ['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7', 'Experiment']
data_waics.to_csv('data/wAIC.csv')
data_waics = data_waics.melt(id_vars=['Experiment'], value_vars=['Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7'], var_name=['Model'], value_name='wAIC')

#data_waics['Model'].replace(['model1', 'model2', 'model3', 'model4', 'model5', 'model6', 'model7'], ['Pre', 'Feed', 'RPE', 'Pre+Feed', 'Pre+RPE', 'Feed+RPE', 'Pre+Feed+RPE'], inplace=True)


data_waics_e1 = data_waics[data_waics['Experiment']=='Experiment1']

fig2 = sns.catplot(data=data_waics_e1, x='Model', y='wAIC', kind='bar', errorbar='se', aspect=4, color='C1')
fig2.fig.set_dpi(300)
#fig2.fig.set_figwidth(10)
#fig2.fig.set_figheight(5)
#fig2.set_xticklabels(['Pre-learning', 'RPE learning', 'Pre-learning+RPE learning'], rotation=0, size=20)
fig2.set_xticklabels(size=25)
fig2.set_yticklabels(size=25)
fig2.set_xlabels('', size=25)
fig2.set_ylabels(size=25)
#fig2.set_ylabels('wAIC', size=18)
#fig2.set(yticks=np.arange(0, 1.2, 0.2))
fig2.savefig('figures/wAIC_all_e1.tif', dpi=300)

data_waics_e2 = data_waics[data_waics['Experiment']=='Experiment2']

fig2 = sns.catplot(data=data_waics_e2, x='Model', y='wAIC', kind='bar', errorbar='se', aspect=4, color='C1')
fig2.fig.set_dpi(300)
fig2.set_xlabels('', size=25)
fig2.set_ylabels(size=25)
fig2.set_xticklabels(size=25)
fig2.set_yticklabels(size=25)
fig2.savefig('figures/wAIC_all_e2.tif', dpi=300)




### plot parameters p b
for i in range(1, 8):
    data_model = data_all[data_all['Model']=='model3_{}'.format(i)]
    data_model = data_model.melt(id_vars=['Experiment'], value_vars=['p', 'b'], var_name='Parameter', value_name='Value')
    data_model = data_model.fillna(0)
    data_model.replace(['b'], ['β'], inplace=True)
    
    fig3 = sns.catplot(data=data_model, x='Experiment', y='Value', kind='bar', hue='Parameter', errorbar='se')
    fig3.set_xlabels(size=18)
    fig3.set_ylabels(size=18)
    fig3.set_xticklabels(size=18)
    fig3.set_yticklabels(size=18)
    fig3.set(yticks=np.arange(0, 1.1, 0.1))
    fig3.savefig('figures/model3_{}_pb.tif'.format(i), dpi=300)
    
    
palette = sns.color_palette()
    
### plot parameters slope bias
for i in range(1, 8):
    data_model = data_all[data_all['Model']=='model3_{}'.format(i)]
    data_model = data_model.melt(id_vars=['Experiment'], value_vars=['slope', 'bias'], var_name='Parameter', value_name='Value')
    data_model = data_model.fillna(0)
    data_model.replace(['slope', 'bias'], ['k', 'b'], inplace=True)
    
    fig3 = sns.catplot(data=data_model, x='Experiment', y='Value', kind='bar', hue='Parameter', errorbar='se', palette=['red', 'green'])
    fig3.set_xlabels(size=18)
    fig3.set_ylabels(size=18)
    fig3.set_xticklabels(size=18)
    fig3.set_yticklabels(size=18)
    #fig3.set(yticks=np.arange(0, 1.1, 0.1))
    fig3.savefig('figures/model3_{}_kb.tif'.format(i), dpi=300)




              





