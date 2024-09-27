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
data = pd.read_csv('data_preprocess.csv')


## settings
binary = False
full = False

if binary and full:
    data['accuracy'] = data['accuracy_binary']
elif binary and not full:
    data['accuracy'] = data['accuracy_binary']
    data = data.loc[data['individual_binary_acc']>=0.34, :]
elif not binary and full:
    data['accuracy'] = data['accuracy_continuous']
else:
    data['accuracy'] = data['accuracy_continuous']
    data = data.loc[data['individual_continuous_acc']>=0.34, :]
    
    
plt.rcParams['legend.fontsize'] = 20
plt.rcParams['font.size'] = 23

#%% plot: show detailed behavioral pattern
# data
data_plot = data.copy()
data_plot = data_plot.groupby(by=['participant', 'reward2', 'reward3', 'srpe', 'learning_method'])['accuracy'].mean()
data_plot = data_plot.reset_index()
data_plot.columns = ['Participant', 'Feedback(Phase2)', 'Feedback', 'RPE', 'Testing vs Studying', 'Accuracy']
data_plot = data_plot.sort_values(by=['Testing vs Studying'], ascending=False)
data_plot['Testing vs Studying'].replace([1, 0], ['Testing', 'Studying'], inplace=True)
data_plot['Confidence'] = data_plot['Feedback'] - data_plot['RPE']
data_plot['Accuracy'] = data_plot['Accuracy'] * 100
data_plot['Feedback'].replace([1, 0], ['Positive', 'Negative'], inplace=True)

# plot
fig = sns.catplot(data=data_plot, x='Confidence', y='Accuracy', hue='Testing vs Studying'
                  ,col='Feedback'
                  ,col_order=['Negative', 'Positive']
                  ,kind='bar', errorbar='se', sharex=False
                  ,legend_out=False
                  ,palette={'Testing':(1.0, 0.4980392156862745, 0.054901960784313725), 'Studying':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}
                  )

# adjustment
fig.set(yticks=np.arange(0, 120, 20), ylim=[0, 120])
fig.set_ylabels('Human accuracy (%)')
fig._legend.set_title('')

fig.savefig('figs/behavioral_pattern.tif', dpi=300)

#%% plot: show the behavioral pattern (filter the correct word pairs in Phase 2)
# data
data_plot = data.copy()
data_plot = data_plot[data_plot['reward2']==0]
data_plot = data_plot.groupby(by=['participant', 'reward2', 'reward3', 'srpe', 'learning_method'])['accuracy'].mean()
data_plot = data_plot.reset_index()
data_plot.columns = ['Participant', 'Feedback(Phase2)', 'Feedback', 'RPE', 'Testing vs Studying', 'Accuracy']
data_plot = data_plot.sort_values(by=['Testing vs Studying'], ascending=False)
data_plot['Testing vs Studying'].replace([1, 0], ['Testing', 'Studying'], inplace=True)
data_plot['Confidence'] = data_plot['Feedback'] - data_plot['RPE']
data_plot['Accuracy'] = data_plot['Accuracy'] * 100
data_plot['Feedback'].replace([1, 0], ['Positive', 'Negative'], inplace=True)

# plot
fig = sns.catplot(data=data_plot, x='Confidence', y='Accuracy', hue='Testing vs Studying'
                  ,col='Feedback'
                  ,col_order=['Negative', 'Positive']
                  ,kind='bar', errorbar='se', sharex=False
                  ,legend_out=False
                  ,palette={'Testing':(1.0, 0.4980392156862745, 0.054901960784313725), 'Studying':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}
                  )

# adjustment
fig.set(yticks=np.arange(0, 120, 20), ylim=[0, 120])
fig.set_ylabels('Human accuracy (%)')
fig._legend.set_title('')

fig.savefig('figs/behavioral_pattern_no_correct.tif', dpi=300)




#%% plot: show the behavioral pattern (filter the confidence > 0.5 word pairs in Phase 2)
# preprocess the data
data_plot = data.copy()
data_plot = data_plot[data_plot['confidence2']<=0.5]
data_plot = data_plot.groupby(by=['participant', 'reward2', 'reward3', 'srpe', 'learning_method'])['accuracy'].mean()
data_plot = data_plot.reset_index()
data_plot.columns = ['Participant', 'Feedback(Phase2)', 'Feedback', 'RPE', 'Testing vs Studying', 'Accuracy']
data_plot = data_plot.sort_values(by=['Testing vs Studying'], ascending=False)
data_plot['Testing vs Studying'].replace([1, 0], ['Testing', 'Studying'], inplace=True)
data_plot['Confidence'] = data_plot['Feedback'] - data_plot['RPE']
data_plot['Accuracy'] = data_plot['Accuracy'] * 100
data_plot['Feedback'].replace([1, 0], ['Positive', 'Negative'], inplace=True)

# plot
fig = sns.catplot(data=data_plot, x='Confidence', y='Accuracy', hue='Testing vs Studying'
                  ,col='Feedback'
                  ,col_order=['Negative', 'Positive']
                  ,kind='bar', errorbar='se', sharex=False
                  ,legend_out=False
                  ,palette={'Testing':(1.0, 0.4980392156862745, 0.054901960784313725), 'Studying':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}
                  )

# adjustment
fig.set(yticks=np.arange(0, 120, 20), ylim=[0, 120])
fig.set_ylabels('Human accuracy (%)')
fig._legend.set_title('')

# plot
fig.savefig('figs/behavioral_pattern_no_high_conf.tif', dpi=300)




#%% plot: show the distribution of conditions
# data
data_plot = data.loc[:, ['participant', 'reward2', 'reward3', 'srpe', 'learning_method', 'accuracy']]
data_plot = data_plot.loc[data_plot['reward2']==0, :]
data_plot.columns = ['Participant', 'Feedback(Phase2)', 'Feedback', 'RPE', 'Testing vs Studying', 'Accuracy']
data_plot = data_plot.sort_values(by=['Testing vs Studying'], ascending=False)
data_plot['Testing vs Studying'].replace([1, 0], ['Testing', 'Studying'], inplace=True)
data_plot['Confidence'] = data_plot['Feedback'] - data_plot['RPE']
data_plot['Feedback'].replace([1, 0], ['Positive', 'Negative'], inplace=True)

# plot
fig = sns.catplot(data=data_plot, x='Confidence', hue='Testing vs Studying'
                  ,col='Feedback'
                  ,col_order=['Negative', 'Positive']
                  ,kind='count', errorbar='se', sharex=False
                  ,legend_out=False
                  ,palette={'Testing':(1.0, 0.4980392156862745, 0.054901960784313725), 'Studying':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}
                  )

# adjustment
fig.set(ylim=[0, 1600])
fig.set_ylabels('Number of trials')
fig._legend.set_title('')

# plot
fig.savefig('figs/Distrubution.tif', dpi=300)

