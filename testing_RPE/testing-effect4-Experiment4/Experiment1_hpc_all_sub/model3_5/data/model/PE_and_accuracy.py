#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:31:52 2024

@author: haopengchen

In this script, I will check the relationship between model based PE and final accuracy
"""

######################
### import modules ###
######################
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#######################
###### settings #######
#######################
binary = False
all_trials = False


######################
####### data #########
######################
## human data
data_human = pd.read_csv('data_human.csv')
## model data
data_pe = pd.read_csv('data_pe.csv')
data_pe = data_pe.loc[:, ['Pars', 'en_word', 'PE']]
data_pe.columns = ['participant', 'en_word', 'PE']
## combine the data
data_all = data_human.merge(data_pe, how='inner', on=['participant', 'en_word'])
## accuracy
if binary:
    data_all['accuracy'] = data_all['accuracy_binary']
else:
    data_all['accuracy'] = data_all['accuracy_continuous']

#####################
######## plot #######
#####################
plt.rcParams['font.size'] = 25

## delete correct items in Phase 2?
if all_trials == False:
    data_all = data_all.loc[data_all['reward2']==0, :]
else:
    print('keep all items')

## only keep one decimal place of PE value
data_all['PE'] = data_all['PE'].round(1)
## PE and accuracy
fig, ax = plt.subplots(figsize=[10, 8])
data_plot = data_all.loc[data_all['learning_method']==1, :]
ax = sns.regplot(data=data_plot, x='PE', y='accuracy', x_estimator=np.mean, order=8, label='Test')
data_plot = data_all.loc[data_all['learning_method']==0, :]
ax = sns.regplot(data=data_plot, x='PE', y='accuracy', x_estimator=np.mean, label='Study')
ax.set_xlabel('Prediction error')
ax.set_ylabel('Human accuracy')
ax.set_ylim(0, 1.1)
ax.legend()
plt.show()
fig.savefig('figs/PE_and_accuracy.jpg', dpi=300)




