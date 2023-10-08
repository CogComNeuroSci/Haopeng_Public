# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 09:55:41 2023

@author: haopchen

Main aim: 
    Draw some pictures to show the current results
"""

## import modules
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


## import the data
data = pd.read_csv('data_all_delete_lower_than_34.csv')


plt.rcParams['font.size'] = 20

## plot: show the behavioral pattern (filter the confidence > 0.5 word pairs in Phase 2)
# preprocess the data
data_plot = data.copy()
data_plot = data_plot[data_plot['confidence2']<=0.5] 
data_plot = data_plot.groupby(by=['participant', 'reward2', 'reward3', 'srpe', 'learning_method'])['accuracy'].mean()
data_plot = data_plot.reset_index()
data_plot.columns = ['Participant', 'Feedback(Phase2)', 'Feedback', 'RPE', 'Testing vs Studying', 'Accuracy']
data_plot = data_plot.sort_values(by=['Testing vs Studying'])
data_plot['Testing vs Studying'].replace([1, 0], ['Testing', 'Studying'], inplace=True)

# plot
fig = sns.catplot(data=data_plot, x='RPE', y='Accuracy', kind='bar', hue='Testing vs Studying', col='Feedback', sharex=False)
fig.savefig('figs/behavioral_pattern_no_high_conf.tif', dpi=300)


## plot: show the behavioral pattern (filter the pre-learning accuracy in each condition)
# preprocess the data
data_plot = data.copy()
data_plot['pre-learning'] = data_plot['reward2'] + data_plot['reward3']
data_plot.loc[data_plot['pre-learning'] > 0, 'pre-learning'] = data_plot.loc[data_plot['pre-learning'] > 0, 'pre-learning'] - 1
data_plot = data_plot.groupby(by=['participant', 'reward2', 'reward3', 'srpe', 'urpe', 'learning_method'])[['pre-learning', 'accuracy']].mean()
data_plot = data_plot.reset_index()
data_plot.columns = ['Participant', 'Feedback(Phase2)', 'Feedback', 'RPE', 'URPE', 'Testing vs Studying', 'Pre-learning', 'Accuracy']
data_plot['Pure accuracy'] = data_plot['Accuracy'] - data_plot['Pre-learning']

# plot
fig = sns.catplot(data=data_plot, x='URPE', y='Accuracy', kind='bar', hue='Testing vs Studying', col='Feedback', sharex=False)
fig = sns.catplot(data=data_plot, x='URPE', y='Pre-learning', kind='bar', hue='Testing vs Studying', col='Feedback', sharex=False)
fig = sns.catplot(data=data_plot, x='URPE', y='Pure accuracy', kind='bar', hue='Testing vs Studying', col='Feedback', sharex=False)
fig.set(ylim=[0, 1])
fig.savefig('figs/behavioral_pattern_conditional_filter.tif', dpi=300)



## plot: show the distribution of conditions (no deletion)
# preprocess the data
data_plot2 = data.copy()
data_plot2 = data_plot2[['participant', 'reward2', 'reward3', 'srpe', 'learning_method', 'accuracy']]
data_plot2.columns = ['Participant', 'Feedback(Phase2)', 'Feedback(Phase3)', 'RPE', 'Testing vs Studying', 'Accuracy']

# plot
fig2 = sns.catplot(data=data_plot2, x='RPE', kind='count', hue='Testing vs Studying', col='Feedback(Phase3)', sharex=False)


## plot: show the distribution of conditions (delete correct items in phase 2)
# preprocess the data
data_plot3 = data.copy()
data_plot3 = data_plot3[data_plot3['reward2']!=1]
data_plot3 = data_plot3[['participant', 'reward2', 'reward3', 'srpe', 'learning_method', 'accuracy']]
data_plot3.columns = ['Participant', 'Feedback(Phase2)', 'Feedback', 'RPE', 'Testing vs Studying', 'Accuracy']
data_plot3['Testing vs Studying'].replace([1, 0], ['Testing', 'Studying'], inplace=True)

# plot
fig3 = sns.catplot(data=data_plot3, x='RPE', kind='count', hue='Testing vs Studying', col='Feedback', sharex=False)
fig3.set_ylabels('Trials')
fig3.savefig('figs/distribution.tif', dpi=300)