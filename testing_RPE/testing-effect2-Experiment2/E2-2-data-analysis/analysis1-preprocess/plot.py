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
## data without removing subjects?
full_data = False

if full_data:
    data_all = pd.read_csv('data_preprocess.csv')
else:
    data_all = pd.read_csv('data_preprocess_higher_than_0.34.csv')

## filter stratagy
filt = 'no' # correct, no, high_conf

if filt == 'correct':
    data_all_plot = data_all.copy()
    data_all_plot = data_all_plot.loc[data_all_plot['reward2']==0, :]
elif filt == 'no':
    data_all_plot = data_all.copy()
elif filt == 'high_conf':
    data_all_plot = data_all.copy()
    data_all_plot = data_all_plot.loc[data_all_plot['confidence2']<=0.5, :]


## preprocess
data_all_plot = data_all_plot.groupby(by=['participant', 'reward', 'confidence', 'learning_method'])['accuracy'].mean()
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
plt.rcParams['font.size'] = 24
plt.rcParams['legend.fontsize'] = 20

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
    if i == 9:
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
ax2.legend(handles=legend_handles, title='', fontsize=10, bbox_to_anchor=[0.9, 1.1])
#ax2.legend_ = None
ax2.set_ylabel('')
ax2.set(yticks=np.arange(0, 120, 20), ylim=[0, 120])
ax2.set_title('Feedback: Positive', fontsize=24)

if full_data:
    fig2.savefig('figs/positive_confidence_all_sub.tif', dpi=300)
else:
    fig2.savefig('figs/positive_confidence_deletion.tif', dpi=300)