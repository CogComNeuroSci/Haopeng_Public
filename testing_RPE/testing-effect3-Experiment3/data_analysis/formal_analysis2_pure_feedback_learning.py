# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:05:54 2024

@author: haopchen
"""

###############################
######### modules #############
###############################
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mypatch 
import os



###############################
######### data ################
###############################
full_data = False
binary = False

## load data
data_e1 = pd.read_csv('data_preprocess_e1.csv')
data_e1['Experiment'] = 1
data_e3 = pd.read_csv('data_preprocess.csv')
data_e3['Experiment'] = 3

data_all = pd.concat([data_e1, data_e3], axis=0)

## remove subjects? binary or continuous?
if full_data and binary:
    print('full data')
    print('binary accuracy')
    data_all['accuracy'] = data_all['accuracy_binary']
elif full_data and not binary:
    print('full data')
    print('continuous accuracy')
    data_all['accuracy'] = data_all['accuracy_continuous']
elif not full_data and binary:
    print('good data')
    print('binary accuracy')
    data_all = data_all.loc[data_all['individual_binary_acc']>=0.34, :]
    data_all['accuracy'] = data_all['accuracy_binary']
elif not full_data and not binary:
    print('good data')
    print('continuous accuracy')
    data_all = data_all.loc[data_all['individual_continuous_acc']>=0.34, :]
    data_all['accuracy'] = data_all['accuracy_continuous']


## filter stratagy
filt = 'correct' # correct, no, high_conf

if filt == 'correct':
    data_all_plot = data_all.copy()
    data_all_plot = data_all_plot.loc[data_all_plot['reward2']==0, :]
elif filt == 'no':
    data_all_plot = data_all.copy()
elif filt == 'high_conf':
    data_all_plot = data_all.copy()
    data_all_plot = data_all_plot.loc[data_all_plot['confidence2']<=0.5, :]
    

###############################
############ plot #############
###############################

######## setting #############
plt.rcParams.update({
    'font.size': 24,
    'axes.labelsize': 24,
    'xtick.labelsize': 24,
    'ytick.labelsize': 24
    })

data_group = data_all_plot.groupby(['Experiment', 'confidence', 'reward', 'learning_method'])['accuracy'].mean()
data_group = data_group.reset_index()
data_group = data_group.pivot(index=['confidence', 'reward', 'learning_method'], columns=['Experiment'], values=['accuracy'])
data_group = data_group.reset_index()
data_group.columns = ['confidence', 'Correct', 'Test vs Study', 'accuracy_e1', 'accuracy_e2']
data_group['pure_learning'] = (data_group['accuracy_e1'] - data_group['accuracy_e2'])*100
data_group = data_group.sort_values(by=['Test vs Study'], ascending=False)
data_group['Test vs Study'].replace([0, 1], ['Study', 'Test'], inplace=True)
data_group['Correct'].replace([0, 1], ['Incorrect Tests', 'Correct Tests'], inplace=True)


##### first subplot #######
fig1, ax1 = plt.subplots(dpi=300)
plt.tight_layout()

## bar plot
data_plot = data_group.loc[data_group['Correct']=='Incorrect Tests', :]

palette = {'Test':(1.0, 0.4980392156862745, 0.054901960784313725), 'Study':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}

sns.barplot(data=data_plot, x='confidence', y='pure_learning', hue='Test vs Study',
                    edgecolor = 'black',
                    facecolor = 'white',
                    errorbar='se',
                    linewidth=4,
                    palette=palette,
                    dodge=True,
                    width=0.4,
                    ax=ax1)


for patch in ax1.patches:
    edge_color = palette['Test']  # Get the edge color from the palette
    patch.set_edgecolor(edge_color)  # Set the edge color
    #patch.set_width(0.8)

ax1.legend_ = None
ax1.set_ylabel('Feedback learning (%)')
ax1.set(yticks=np.arange(0, 120, 20), ylim=[0, 120])
ax1.set_title('Incorrect tests', fontsize=24)

if full_data:
    fig1.savefig('figs/negative_confidence_all_sub.tif', dpi=300)
else:
    fig1.savefig('figs/negative_confidence_deletion.tif', dpi=300)



##### second subplot #######
fig2, ax2 = plt.subplots()
plt.tight_layout()

## bar plot
data_plot = data_group.loc[data_group['Correct']=='Correct Tests', :]

palette = {'Test':(1.0, 0.4980392156862745, 0.054901960784313725), 'Study':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}

sns.barplot(data=data_plot, x='confidence', y='pure_learning', hue='Test vs Study',
                    edgecolor = 'black',
                    facecolor = 'white',
                    errorbar='se',
                    linewidth=4,
                    palette=palette,
                    dodge=True,
                    ax=ax2)

i = 0
for patch in ax2.patches:
    if i == 5:
        edge_color = palette['Study']
    else:
        edge_color = palette['Test']  # Get the edge color from the palette
    patch.set_edgecolor(edge_color)  # Set the edge color
    i+=1
    
legend_handles = [
    mypatch.Circle((0, 0), radius=0.5, color=palette['Test'], label='Test'),
    mypatch.Circle((0, 0), radius=0.5, color=palette['Study'], label='Study')
]

# Set the legend with custom handles and labels
ax2.legend(handles=legend_handles, title='', fontsize=10, bbox_to_anchor=[1.15, 1.1])
#ax2.legend_ = None
ax2.set_ylabel('')
ax2.set(yticks=np.arange(0, 120, 20), ylim=[0, 120])
ax2.set_title('Correct Tests', fontsize=24)

# set the ticks
bar_width = 0.40  # Adjust bar width as needed
ticks = (np.array([0, 1, 2, 3]) - bar_width/2).tolist() + [4]
ax2.set_xticks(ticks)

if full_data:
    fig2.savefig('figs/positive_confidence_all_sub.tif', dpi=300)
else:
    fig2.savefig('figs/positive_confidence_deletion.tif', dpi=300)


