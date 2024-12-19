# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 22:20:07 2024

@author: kygs1996
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
## filter stratagy
filt = 'correct' # correct, no, high_conf

## load data
data_all = pd.read_csv('data_preprocess.csv')

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


if filt == 'correct':
    data_all = data_all.loc[data_all['reward2']==0, :]
elif filt == 'no':
    print('no filter')
elif filt == 'high_conf':
    data_all = data_all.loc[data_all['confidence2']<=0.5, :]


## preprocess
data_all_plot = data_all.groupby(by=['participant', 'reward', 'confidence', 'learning_method'])['accuracy'].mean()
data_all_plot = data_all_plot.reset_index()
data_all_plot.columns = ['Pars', 'Feedback', 'Confidence', 'Testing Vs Studying', 'Human accuracy']

data_all_plot['Human accuracy'] = data_all_plot['Human accuracy'] * 100
data_all_plot = data_all_plot.sort_values(by=['Testing Vs Studying'], ascending=False)
data_all_plot['Testing Vs Studying'].replace([0, 1], ['Studying', 'Testing'], inplace=True)
data_all_plot['Feedback'].replace([0, 1], ['Negative', 'Positive'], inplace=True)



##############################
######## plot ################
##############################

######## setting #############
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12
    })

##### first subplot #######
fig1, ax1 = plt.subplots(dpi=300)
plt.tight_layout()

## bar plot
data_plot = data_all_plot.loc[data_all_plot['Feedback']=='Negative', :]

palette = {'Testing':(1.0, 0.4980392156862745, 0.054901960784313725), 'Studying':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}

sns.barplot(data=data_plot, x='Confidence', y='Human accuracy', hue='Testing Vs Studying',
                    edgecolor = 'black',
                    facecolor = 'white',
                    errorbar='se',
                    linewidth=4,
                    palette=palette,
                    dodge=True,
                    width=0.4,
                    ax=ax1)


for patch in ax1.patches:
    edge_color = palette['Testing']  # Get the edge color from the palette
    patch.set_edgecolor(edge_color)  # Set the edge color
    #patch.set_width(0.8)

## overlay point
sns.stripplot(data=data_plot, x='Confidence', y='Human accuracy', hue='Testing Vs Studying',
                   palette={'Testing':(1.0, 0.4980392156862745, 0.054901960784313725), 'Studying':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)},
                   dodge=True,
                   ax=ax1)

# Set the legend with custom handles and labels
#ax1.legend(handles=legend_handles, title='', fontsize=15, bbox_to_anchor=[1, 1])
ax1.legend_ = None
ax1.set_ylabel('Human accuracy (%)')
ax1.set(yticks=np.arange(0, 120, 20), ylim=[0, 120])
ax1.set_title('Feedback: Negative', fontsize=24)

if full_data:
    fig1.savefig('figs/negative_confidence_all_sub.tif', dpi=300)
else:
    fig1.savefig('figs/negative_confidence_deletion.tif', dpi=300)




##### second subplot #######
fig2, ax2 = plt.subplots()
plt.tight_layout()

## bar plot
data_plot = data_all_plot.loc[data_all_plot['Feedback']=='Positive', :]

palette = {'Testing':(1.0, 0.4980392156862745, 0.054901960784313725), 'Studying':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}

sns.barplot(data=data_plot, x='Confidence', y='Human accuracy', hue='Testing Vs Studying',
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
        edge_color = palette['Studying']
    else:
        edge_color = palette['Testing']  # Get the edge color from the palette
    patch.set_edgecolor(edge_color)  # Set the edge color
    i+=1

# overlay point
sns.stripplot(data=data_plot, x='Confidence', y='Human accuracy', hue='Testing Vs Studying',
                   palette={'Testing':(1.0, 0.4980392156862745, 0.054901960784313725), 'Studying':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)},
                   dodge=True,
                   ax=ax2)

legend_handles = [
    mypatch.Circle((0, 0), radius=0.5, color=palette['Testing'], label='Test'),
    mypatch.Circle((0, 0), radius=0.5, color=palette['Studying'], label='Study')
]

# Set the legend with custom handles and labels
ax2.legend(handles=legend_handles, title='', fontsize=10, bbox_to_anchor=[1.15, 1.1])
#ax2.legend_ = None
ax2.set_ylabel('')
ax2.set(yticks=np.arange(0, 120, 20), ylim=[0, 120])
ax2.set_title('Feedback: Positive', fontsize=24)

# set the ticks
bar_width = 0.40  # Adjust bar width as needed
ticks = (np.array([0, 1, 2, 3]) - bar_width/2).tolist() + [4]
ax2.set_xticks(ticks)

if full_data:
    fig2.savefig('figs/positive_confidence_all_sub.tif', dpi=300)
else:
    fig2.savefig('figs/positive_confidence_deletion.tif', dpi=300)
    
    
    
#%%
##################################################
############# plot: test vs study ################
##################################################

## preprocess
data_all_plot = data_all.groupby(by=['participant', 'reward', 'learning_method'])['accuracy'].mean()
data_all_plot = data_all_plot.reset_index()
data_all_plot.columns = ['Pars', 'Reward', 'Testing Vs Studying', 'Human accuracy']

data_all_plot['Human accuracy'] = data_all_plot['Human accuracy'] * 100
data_all_plot = data_all_plot.sort_values(by=['Testing Vs Studying'], ascending=False)
data_all_plot['Testing Vs Studying'].replace([0, 1], ['Study', 'Test'], inplace=True)


######## setting #############
######## setting #############
plt.rcParams.update({
    'font.size': 16,
    'axes.labelsize': 16,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16
    })

##### first subplot #######
fig, ax = plt.subplots(figsize=[3, 8], dpi=300)
plt.tight_layout(pad=2)

## bar plot
data_plot = data_all_plot.copy()

palette = {'Test':(1.0, 0.4980392156862745, 0.054901960784313725), 'Study':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}

sns.barplot(data=data_plot, x='Testing Vs Studying', y='Human accuracy',
                    edgecolor = 'black',
                    facecolor = 'white',
                    errorbar='se',
                    linewidth=3,
                    dodge=False,
                    width=0.4,
                    ax=ax)

i = 0
for patch in ax.patches:
    if i == 0:
        edge_color = palette['Test']
    else:
        edge_color = palette['Study']  # Get the edge color from the palette
    patch.set_edgecolor(edge_color)  # Set the edge color
    i+=1

## overlay point
sns.stripplot(data=data_plot, x='Testing Vs Studying', y='Human accuracy',
                   palette=palette,
                   dodge=False,
                   ax=ax)

ax.set_xlabel('')
ax.set_yticks(np.arange(0, 110, 20))
fig.subplots_adjust(left=0.28, top=0.95, bottom=0.12, right=0.95)

fig.savefig('figs/test_effect.jpg', dpi=300)

#%% heatmap of confidence effects
data_plot = data_all.loc[data_all['reward']==0, :]
data_plot = data_plot.groupby(by=['confidence2', 'confidence3'])['accuracy'].mean()
data_plot = data_plot.reset_index()
data = data_plot.pivot(index=['confidence2'], columns=['confidence3'], values=['accuracy'])
data.reset_index()
#data.columns = np.arange(0, 1.1, 0.25)
fig, ax = plt.subplots()
ax = sns.heatmap(data, cmap='Reds', vmin=0.4, vmax=1)
ax.invert_yaxis()
fig.subplots_adjust()