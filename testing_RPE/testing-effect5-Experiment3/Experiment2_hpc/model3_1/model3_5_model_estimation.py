# -*- coding: utf-8 -*-
"""
Created on Thu May  4 09:20:24 2023

@author: haopchen
"""

### import the modules
import os
import numpy as np
import pandas as pd
from model3_2_learning_model import model_prelearning, model_learning, model_testing
import seaborn as sns
import matplotlib.pyplot as plt



### prepare the data        
## prelearning (phase 2)
X_phase2_3d = np.load('data/E1_data_construction/data_phase2/X.npy')
Y_conf_phase2_3d = np.load('data/E1_data_construction/data_phase2/Y_conf.npy')

## prelearning (phase 3)
X_phase3_3d = np.load('data/E1_data_construction/data_phase3/X.npy')
Y_conf_phase3_3d = np.load('data/E1_data_construction/data_phase3/Y_conf.npy')

## formal learning (phase 3)
Y_feed_phase3_3d = np.load('data/E1_data_construction/data_phase3/Y_feed.npy')
Y_options_phase3_3d = np.load('data/E1_data_construction/data_phase3/Y_options.npy')
TvS_phase3_3d = np.load('data/E1_data_construction/data_phase3/TS.npy')
Reward3_phase3_3d = np.load('data/E1_data_construction/data_phase3/Reward3.npy')

## model testing
X_testing_3d = np.load('data/E1_data_construction/data_phase4/X.npy')
Y_options_testing_3d = np.load('data/E1_data_construction/data_phase4/Y_options.npy')
Y_choice_testing_3d = np.load('data/E1_data_construction/data_phase4/Y_choice.npy')

Y_feed_testing_3d = np.load('data/E1_data_construction/data_phase4/Y_feed.npy')
Reward2_3d = np.load('data/E1_data_construction/data_phase4/Reward2.npy')
Reward3_3d = np.load('data/E1_data_construction/data_phase4/Reward3.npy')
RPE_3d = np.load('data/E1_data_construction/data_phase4/RPE.npy')
TvS_3d = np.load('data/E1_data_construction/data_phase4/TS.npy')
Human_accuracy_3d = np.load('data/E1_data_construction/data_phase4/Accuracies.npy')

Pars_3d = np.load('data/E1_data_construction/data_phase4/Pars.npy')

swa_words = np.load('data/E1_data_construction/data_phase4/column_y.npy')

## parameters
parameters_all = pd.read_csv('data/E1_data_parameters/parameters_best.csv')


data_all = pd.DataFrame()



### model performance
for sub in range(X_phase2_3d.shape[0]):
    ## prepare the data
    # pre-learning(phase2)
    X_phase2 = X_phase2_3d[sub, :, :]
    Y_conf_phase2 = Y_conf_phase2_3d[sub, :, :]
    # pre-learning(phase3)
    X_phase3 = X_phase3_3d[sub, :, :]
    Y_conf_phase3 = Y_conf_phase3_3d[sub, :, :]
    # formal learning (phase3)
    Y_feed_phase3 = Y_feed_phase3_3d[sub, :, :]
    Y_options_phase3 = Y_options_phase3_3d[sub, :, :]
    TvS_phase3 = TvS_phase3_3d[sub, :, :]
    Reward3_phase3 = Reward3_phase3_3d[sub, :, :]
    # model testing
    X_testing = X_testing_3d[sub, :, :]
    Y_options_testing = Y_options_testing_3d[sub, :, :]
    Y_choice_testing = Y_choice_testing_3d[sub, :, :]
    
    Y_feed_testing = Y_feed_testing_3d[sub, :, :]
    Reward2 = Reward2_3d[sub, :, :]
    Reward3 = Reward3_3d[sub, :, :]
    RPE = RPE_3d[sub, :, :]
    TvS = TvS_3d[sub, :, :]
    Human_accuracy = Human_accuracy_3d[sub, :, :]
    Pars = Pars_3d[sub, :, :]
    
    
     
    W0 = np.zeros([X_phase2.shape[1], Y_conf_phase2.shape[1]])
    
    parameters = parameters_all.iloc[sub, 1:4]
    #parameters[0:2] = [0.6, 0.4]
    #parameters[2] = 3
    #parameters[3] = 5
    
    ## model training
    # prelearning (phase 2)
    W1 = model_prelearning(a=parameters[0], W=W0.copy(), X=X_phase2, Y_conf=Y_conf_phase2)
    
    # prelearning (phase 3)
    W2 = model_prelearning(a=parameters[0], W=W1.copy(), X=X_phase3, Y_conf=Y_conf_phase3)
    
    # formal learning
    #W3 = model_learning(b1=parameters[1], b2=parameters[2], slope=parameters[3], bias=parameters[4], W=W2.copy(), X=X_phase3, Y_feed=Y_feed_phase3, Y_options=Y_options_phase3, TvS=TvS_phase3, Reward3=Reward3_phase3, swa_words=swa_words)
    
    # model testing
    Y_pred = model_testing(slope=parameters[1], bias=parameters[2], W=W2.copy(), X=X_testing, Y_options=Y_options_testing, swa_words=swa_words)
    Model_accuracy = Y_pred[Y_feed_testing==1]
    
    retain = Model_accuracy.shape[0]
    data = pd.DataFrame({'Pars':Pars.flatten()[0:retain], 'Reward2':Reward2.flatten()[0:retain], 'Reward3':Reward3.flatten()[0:retain], 'RPE':RPE.flatten()[0:retain], 'TvS': TvS.flatten()[0:retain], 'Model_accuracy': Model_accuracy[0:retain], 'Human_accuracy': Human_accuracy.flatten()[0:retain]})
    
    data_all = pd.concat([data_all, data], axis=0)

### plot
"""
data_all_plot = data_all.groupby(by=['Pars', 'Reward2', 'Reward3', 'RPE', 'TvS'])[['Model_accuracy', 'Human_accuracy']].mean()
data_all_plot = data_all_plot.reset_index()

fig = sns.catplot(data=data_all_plot, x='RPE', y='Model_accuracy', hue='TvS', row='Reward2', col='Reward3', kind='bar')
fig2 = sns.catplot(data=data_all_plot, x='RPE', y='Human_accuracy', hue='TvS', row='Reward2', col='Reward3', kind='bar')

if not os.path.exists('figs/'):
    os.mkdir('figs/')

fig.savefig('figs/model_performance.tif', dpi=300)
"""

plt.rcParams['font.size'] = 18


data_all_plot = data_all[data_all['Reward2']==0]
data_all_plot = data_all_plot.groupby(by=['Pars', 'Reward3', 'RPE', 'TvS'])[['Model_accuracy', 'Human_accuracy']].mean()
data_all_plot = data_all_plot.reset_index()
data_all_plot.columns = ['Pars', 'Feedback', 'RPE', 'Testing Vs Studying', 'Model_accuracy', 'Human_accuracy']

data_all_plot = data_all_plot.sort_values(by=['Testing Vs Studying'])
data_all_plot['Testing Vs Studying'].replace([0, 1], ['Studying', 'Testing'], inplace=True)

fig = sns.catplot(data=data_all_plot, x='RPE', y='Model_accuracy', hue='Testing Vs Studying', col='Feedback', kind='bar', errorbar='se', sharex=False, aspect=0.8)
fig.set(yticks=np.arange(0, 1.2, 0.2))
#fig.set_xticklabels(size=18)
#fig.set_yticklabels(size=18)
#fig.set_xlabels(size=18)
fig.set_ylabels('Model accuracy')

#fig.legend.set_fontsize(15)


fig2 = sns.catplot(data=data_all_plot, x='RPE', y='Human_accuracy', hue='Testing Vs Studying', col='Feedback', kind='bar', errorbar='se', sharex=False, aspect=0.8)
fig2.set(yticks=np.arange(0, 1.2, 0.2))
#fig2.set_xticklabels(size=18)
#fig2.set_yticklabels(size=18)
#fig2.set_xlabels(size=18)
fig2.set_ylabels('Human accuracy')

if not os.path.exists('figs/'):
    os.mkdir('figs/')

fig.savefig('figs/model_performance.tif', dpi=300)
fig2.savefig('figs/human_performance.tif', dpi=300)