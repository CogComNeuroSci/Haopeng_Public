# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 22:15:51 2024

@author: haopchen
"""

### import modules
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


### data
data_all = pd.DataFrame()

for e in [1, 2]:
    for m in range(1, 8):
        file_path = '../Experiment{}_hpc_all_sub/model3_{}/data/model/model_simulation.csv'.format(e, m) 
        data = pd.read_csv(file_path)
        data['Experiment'] = e
        data['model'] = m
        
        if m in [1, 2, 4]:
            data['predictive_learning'] = 'Without PL'
        else:
            data['predictive_learning'] = 'With PL'
        
        data_all = pd.concat([data_all, data], axis=0)

data_all.to_csv('data/model_simulation.csv')

#%% model simulation (test effect)
plt.rcParams['font.size'] = 24
plt.rcParams['legend.fontsize'] = 15

# Experiment 1
data_plot = data_all.loc[data_all['Experiment']==1, :]
fig = sns.catplot(data=data_plot, x='model', y='model_test_effect', hue='predictive_learning', kind='bar'
                  ,legend=False
                  ,aspect=2
                  ,palette={'Without PL': 'red', 'With PL': 'green'}
                  ,dodge=False)
fig.ax.axhline(y=0, color='black', linestyle='-')
plt.legend(loc='upper right')
fig.set_xlabels('Model')
fig.set_ylabels('Testing effect (Model)')
fig.savefig('figures/model_based_test_effect_e1.tif', dpi=300)

# Experiment 2
data_plot = data_all.loc[data_all['Experiment']==2, :]
fig = sns.catplot(data=data_plot, x='model', y='model_test_effect', hue='predictive_learning', kind='bar'
                  ,legend=False
                  ,aspect=2
                  ,palette={'Without PL': 'red', 'With PL': 'green'}
                  ,dodge=False)
fig.ax.axhline(y=0, color='black', linestyle='-')
plt.legend(loc='upper right')
fig.set_xlabels('Model')
fig.set_ylabels('Testing effect (Model)')
fig.savefig('figures/model_based_test_effect_e2.tif', dpi=300)




#%% correlation: learning rate and test effect
## Hebbian learning
# Experiment 1
data_plot = data_all.loc[data_all['model']==4, :]
data_plot = data_plot.loc[data_plot['Experiment']==1, :]
fig = sns.jointplot(data=data_plot, x='b', y='human_test_effect', kind='reg')
fig.set_axis_labels(xlabel='Learning rate (Hebbian)', ylabel='Testing effect (Human)')
fig.ax_joint.set_xticks(np.arange(0, 1.0, 0.2))
fig.ax_joint.set_yticks(np.arange(-0.4, 1.0, 0.2))
fig.savefig('figures/learning_rate_test_effect_hebb_e1.tif', dpi=300)

# Experiment 2
data_plot = data_all.loc[data_all['model']==4, :]
data_plot = data_plot.loc[data_plot['Experiment']==2, :]
fig = sns.jointplot(data=data_plot, x='b', y='human_test_effect', kind='reg')
fig.set_axis_labels(xlabel='Learning rate (Hebbian)', ylabel='Testing effect (Human)')
fig.ax_joint.set_xticks(np.arange(0, 1.0, 0.2))
fig.ax_joint.set_yticks(np.arange(-0.4, 1.0, 0.2))
fig.savefig('figures/learning_rate_test_effect_hebb_e2.tif', dpi=300)

#%% Predictive learning
# Experiment 1
data_plot = data_all.loc[data_all['model']==5, :]
data_plot = data_plot.loc[data_plot['Experiment']==1, :]
fig = sns.jointplot(data=data_plot, x='b', y='human_test_effect', kind='reg')
fig.set_axis_labels(xlabel='Learning rate (Predictive)', ylabel='Testing effect (Human)')
fig.ax_joint.set_xticks(np.arange(0, 1.0, 0.2))
fig.ax_joint.set_yticks(np.arange(-0.4, 1.0, 0.2))
fig.savefig('figures/learning_rate_test_effect_pred_e1.tif', dpi=300)

# Experiment 2
data_plot = data_all.loc[data_all['model']==5, :]
data_plot = data_plot.loc[data_plot['Experiment']==2, :]
fig = sns.jointplot(data=data_plot, x='b', y='human_test_effect', kind='reg')
fig.set_axis_labels(xlabel='Learning rate (predictive)', ylabel='Testing effect (Human)')
fig.ax_joint.set_xticks(np.arange(0, 1.0, 0.2))
fig.ax_joint.set_yticks(np.arange(-0.4, 1.0, 0.2))
fig.savefig('figures/learning_rate_test_effect_pred_e2.tif', dpi=300)
