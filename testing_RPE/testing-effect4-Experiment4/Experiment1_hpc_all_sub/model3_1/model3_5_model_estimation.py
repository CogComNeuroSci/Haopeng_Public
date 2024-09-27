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


### settings
# human accuracy: binary or continuous
binary = False
# full data
full = False
# filter or not
filt = False

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

if binary:
    Human_accuracy_3d = np.load('data/E1_data_construction/data_phase4/AccuraciesB.npy')
else:
    Human_accuracy_3d = np.load('data/E1_data_construction/data_phase4/AccuraciesC.npy')

Pars_3d = np.load('data/E1_data_construction/data_phase4/Pars.npy')

InAccB_3d = np.load('data/E1_data_construction/data_phase4/InAccBs.npy')
InAccC_3d = np.load('data/E1_data_construction/data_phase4/InAccCs.npy')

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
    InAccB = InAccB_3d[sub, :, :]
    InAccC = InAccC_3d[sub, :, :]
       
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
    data = pd.DataFrame({'Pars':Pars.flatten()[0:retain], 'individual_binary_acc': InAccB.flatten()[0:retain], 'individual_continuous_acc': InAccC.flatten()[0:retain], 'Reward2':Reward2.flatten()[0:retain], 'Reward3':Reward3.flatten()[0:retain], 'RPE':RPE.flatten()[0:retain], 'TvS': TvS.flatten()[0:retain], 'Model_accuracy': Model_accuracy[0:retain], 'Human_accuracy': Human_accuracy.flatten()[0:retain]})
    
    data_all = pd.concat([data_all, data], axis=0)
    
    parameters_all.loc[sub, 'Pars'] = Pars[1]

### plot
plt.rcParams['font.size'] = 24
plt.rcParams['legend.fontsize'] = 20

## which data?
if full:
    print('full data')
elif not full and binary:
    data_all = data_all.loc[data_all['individual_binary_acc']>=0.34, :]
elif not full and not binary:
    data_all = data_all.loc[data_all['individual_continuous_acc']>=0.34, :]

## data for plot    
data_all_plot = data_all.copy()

if filt:
    data_all_plot = data_all_plot.loc[data_all_plot['Reward2']==0, :]
else:
    print('no filter')

data_all_plot['Confidence'] = data_all_plot['Reward3'] - data_all_plot['RPE']
data_all_plot = data_all_plot.groupby(by=['Pars', 'Reward3', 'Confidence', 'TvS'])[['Model_accuracy', 'Human_accuracy']].mean()
data_all_plot = data_all_plot.reset_index()
data_all_plot.columns = ['Pars', 'Feedback', 'Confidence', 'Testing Vs Studying', 'Model_accuracy', 'Human_accuracy']

data_all_plot['Human_accuracy'] = data_all_plot['Human_accuracy'] * 100
data_all_plot['Model_accuracy'] = data_all_plot['Model_accuracy'] * 100
data_all_plot = data_all_plot.sort_values(by=['Testing Vs Studying'], ascending=False)
data_all_plot['Testing Vs Studying'].replace([0, 1], ['Studying', 'Testing'], inplace=True)
data_all_plot['Feedback'].replace([0, 1], ['Negative', 'Positive'], inplace=True)



fig = sns.catplot(data=data_all_plot, x='Confidence', y='Model_accuracy', hue='Testing Vs Studying'
                  ,col='Feedback'
                  ,legend_out=False
                  ,kind='bar', errorbar='se', sharex=False
                  #,aspect=0.8
                  ,palette={'Testing':(1.0, 0.4980392156862745, 0.054901960784313725), 'Studying':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}
                  )
fig.set(yticks=np.arange(0, 120, 20), ylim=[0, 120])
fig.set_ylabels('Model accuracy (%)')
fig._legend.set_title('')



fig2 = sns.catplot(data=data_all_plot, x='Confidence', y='Human_accuracy', hue='Testing Vs Studying'
                   ,col='Feedback'
                   ,legend_out=False
                   ,kind='bar', errorbar='se', sharex=False
                   #,aspect=0.8
                   ,palette={'Testing':(1.0, 0.4980392156862745, 0.054901960784313725), 'Studying':(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)}
                   )
fig2.set(yticks=np.arange(0, 120, 20), ylim=[0, 120])
fig2.set_ylabels('Human accuracy (%)')
fig2._legend.set_title('')



if not os.path.exists('figs/'):
    os.mkdir('figs/')

fig.savefig('figs/model_performance.tif', dpi=300)
fig2.savefig('figs/human_performance.tif', dpi=300)



#%% testing effect in model
parameters_all.columns = ['index', 'a', 'slope', 'bias', 'log_like', 'AIC', 'success', 'Pars']
parameters_all = parameters_all[['a', 'slope', 'bias', 'log_like', 'AIC', 'Pars']]

data_all = data_all.loc[data_all['Reward2']==0, :]
data_all = data_all.merge(parameters_all, how='left')

data_all = data_all.groupby(by=['Pars', 'a', 'slope', 'bias', 'TvS'])[['Model_accuracy', 'Human_accuracy']].mean()
data_all = data_all.reset_index()

data_all = data_all.pivot(columns=['TvS'], index=['Pars', 'a', 'slope', 'bias'], values=['Model_accuracy', 'Human_accuracy'])
data_all = data_all.reset_index()

data_all.columns = ['Pars', 'a', 'slope', 'bias', 'Model_accuracy_study', 'Model_accuracy_test', 'Human_accuracy_study', 'Human_accuracy_test']
data_all['model_test_effect'] = data_all['Model_accuracy_test'] - data_all['Model_accuracy_study']
data_all['human_test_effect'] = data_all['Human_accuracy_test'] - data_all['Human_accuracy_study']

if not os.path.exists('data/model'):
    os.mkdir('data/model')

data_all.to_csv('data/model/model_simulation.csv')