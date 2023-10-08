# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:20:54 2023

@author: haopchen

preprocess the data from experiment 1
"""
### change the directory
import os
#os.chdir(r'C:\Users\haopchen\OneDrive - UGent\Desktop\工作\phd-work\phd2-research\research1-nature-of-testing-effect\testing-effect3-Experiment1\Experiment1-3-preprocess\second-time')



### import the modules
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



### import and concat the data
## list the files in the directory
files = os.listdir('../../Experiment1-2-data/data2-raw-data')

## remove 
# remove the pilot data
files.remove('Data_pilot.csv')
# remove the empty data
files.remove('Data_participant_RANDNR_22900.csv')

## concat the data
data_all = pd.DataFrame()
participant_number = 0
for file in files:
    participant_number += 1
    data = pd.read_csv('../../Experiment1-2-data/data2-raw-data/'+file)
    data['participant'] = participant_number
    data_all = pd.concat([data_all, data], axis=0)



### preprocess
## reset the index
data_all.index = range(data_all.shape[0])

## move the confidence rating and rt to last row
for i in range(data_all.shape[0]):
    if data_all.loc[i, 'trial_type'] == 'html-slider-response':
        data_all.loc[i-1, 'rt_confidence'] = data_all.loc[i, 'rt']
        data_all.loc[i-1, 'confidence'] = data_all.loc[i, 'certainty']
    else:
        pass

## delete the useless rows
# delete confidence rating rows
data_all = data_all.dropna(subset=['en_word'], axis=0)
data_all.index = range(data_all.shape[0])

## pivot the data
data_all = data_all.pivot(index=['participant', 'en_word', 'swa_word'], columns=['phase'], values=['accuracy', 'confidence', 'amt_choices', 'rt', 'rt_confidence', 'options', 'correct_answer', 'input_answer', 'input_word', 'trial_index'])
data_all = data_all.reset_index()
# columns
columns = ['participant', 'en_word', 'swa_word']
for name in ['reward', 'confidence', 'learning_method', 'rt', 'rt_confidence', 'options', 'correct_answer', 'input_answer', 'input_word', 'trial']:
    for phase in ['2', '3', '4', '5']:
        if name=='learning_method' and phase=='3':
            columns.append(name)
        else:
            columns.append(name+phase)
data_all.columns = columns
# delete the useless columns
data_all = data_all.drop(columns=['learning_method2', 'learning_method4', 'learning_method5'])
        
## replace the values of rewards
data_all['reward2'].replace([True, False], [4, 0], inplace=True)
data_all['reward3'].replace([True, False], [4, 0], inplace=True)
data_all['reward4'].replace([True, False], [4, 0], inplace=True)
data_all['reward5'].replace([True, False], [4, 0], inplace=True)

## add the columns of reward and confidence
data_all['reward'] = data_all['reward3']
data_all['confidence'] = data_all['confidence3']

## replace the values of learning method
data_all['learning_method'].replace([1,4], [0,1], inplace=True)

## replace the values of confidence
data_all.loc[:, ['confidence2', 'confidence3', 'confidence4', 'confidence5', 'confidence']] = data_all.loc[:, ['confidence2', 'confidence3', 'confidence4', 'confidence5', 'confidence']] - 1

## set the reward in the studying condition as 4
data_all.loc[data_all['learning_method']==0, 'confidence'] = 4

## calculate the srpe and urpe
data_all['srpe'] = data_all['reward'] - data_all['confidence']
data_all['urpe'] = data_all['srpe'].abs()

## cauculate the final accuracy
# 4,4=1; 0,0=0; 0,4=0; 4,0=-1
data_all.index = range(data_all.shape[0])
for i in range(data_all.shape[0]):
    if data_all.loc[i, 'reward4'] == 4 and data_all.loc[i, 'reward5'] == 4:
        data_all.loc[i, 'accuracy'] = 1
    elif data_all.loc[i, 'reward4'] == 0 and data_all.loc[i, 'reward5'] == 0:
        data_all.loc[i, 'accuracy'] = 0
    elif data_all.loc[i, 'reward4'] == 0 and data_all.loc[i, 'reward5'] == 4:
        data_all.loc[i, 'accuracy'] = 0
    elif data_all.loc[i, 'reward4'] == 4 and data_all.loc[i, 'reward5'] == 0:
        data_all.loc[i, 'accuracy'] = -1
    else:
        print('error')
        
# delete the accuracy==-1
data_all = data_all[data_all['accuracy']!=-1]






### save the data
data_all.to_csv('data_preprocess.csv')



### calculate the accuracy of every participant
accuracy_mean = data_all.groupby(by=['participant'])['accuracy'].mean()
accuracy_mean = accuracy_mean.reset_index()

## distribution of the accuracy
fig1 = sns.displot(data=accuracy_mean, x='accuracy', bins=20)

## find the participants whose accuracy is lower than 34%
poor = accuracy_mean[accuracy_mean['accuracy']<=0.34]
print(poor['participant'].values)
print(poor.shape[0])
# participant: 3 11 13 15 16 21 22 25 35 39 40 43 49 62 65 68 69 70 72
# number: 19


## delete the poor data
data_all.index = range(data_all.shape[0])
for sub in poor['participant']:
    data_all = data_all[data_all['participant']!=sub]




### remaining subjects
sub_remain = data_all['participant'].unique()
sub_remain_number = sub_remain.shape[0]
print(sub_remain_number)
# number: 57



### save the data
data_all.to_csv('data_preprocess_higher_than_0.34.csv')    




### main preprocess
#data_all = data_all[data_all['reward2']!=4]




### fig: testing effect and srpe
## reframe the data as subject level
data_plot_srpe = data_all.groupby(by=['participant', 'learning_method', 'srpe', 'reward', 'reward2'])['accuracy'].mean()
data_plot_srpe = data_plot_srpe.reset_index()
data_plot_srpe.columns = ['participants', 'Testing Vs Studying', 'SRPE', 'Reward(Phase3)', 'Reward(Phase2)', 'Accuracy']
data_plot_srpe['Testing Vs Studying'].replace([0, 1], ['Studying', 'Testing'], inplace=True)

#plt.rcParams['font.size'] = 8
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['legend.fontsize'] = 15
plt.rcParams['legend.title_fontsize'] = 15
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


fig2 = sns.catplot(data=data_plot_srpe, x='SRPE', y='Accuracy', hue='Testing Vs Studying' 
                   ,col='Reward(Phase3)'
                   ,row='Reward(Phase2)'
                   ,kind='bar', errorbar='se')

fig2.fig.text(-0.2, 0.8, 'Reward(phase2)=0', size=15)
fig2.fig.text(-0.2, 0.3, 'Reward(phase2)=4', size=15)
fig2.fig.text(0.2, 1.05, 'Reward(phase3)=0', size=15)
fig2.fig.text(0.6, 1.05, 'Reward(phase3)=4', size=15)

fig2.set_xlabels('RPE')
fig2.savefig('figs/srpe-and-testing.tif', dpi=300)



"""
### fig: the correlation between confidence in phase 2 and confidence in phase 3
## reframe the data as subject level
data_plot_srpe = data_all.groupby(by=['participant', 'learning_method', 'srpe', 'reward', 'reward2'])['confidence2'].mean()
data_plot_srpe = data_plot_srpe.reset_index()
data_plot_srpe.columns = ['participants', 'Testing Vs Studying', 'SRPE', 'Reward(Phase3)', 'Reward(Phase2)', 'Confidence (phase2)']
data_plot_srpe['Testing Vs Studying'].replace([0, 1], ['Studying', 'Testing'], inplace=True)

#plt.rcParams['font.size'] = 8
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['legend.fontsize'] = 15
plt.rcParams['legend.title_fontsize'] = 15
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


fig3 = sns.catplot(data=data_plot_srpe, x='SRPE', y='Confidence (phase2)', hue='Testing Vs Studying' 
                   ,col='Reward(Phase3)'
                   ,row='Reward(Phase2)'
                   ,kind='bar', errorbar='se')

fig3.fig.text(-0.2, 0.8, 'Reward(phase2)=0', size=15)
fig3.fig.text(-0.2, 0.3, 'Reward(phase2)=4', size=15)
fig3.fig.text(0.2, 1.05, 'Reward(phase3)=0', size=15)
fig3.fig.text(0.6, 1.05, 'Reward(phase3)=4', size=15)


fig3.savefig('figs/confidence_phase2_phase3.tif', dpi=300)





### the distrubution of the confidence in phase 2 (reward2=0, srpe=4)
data_all_dis = data_all.copy()
data_all_dis = data_all_dis[data_all_dis['reward2']==0]
data_all_dis = data_all_dis[data_all_dis['srpe']==4]
data_all_dis['confidence2'] = data_all_dis['confidence2']/4

fig4 = sns.displot(data=data_all_dis, x='confidence2', kind='ecdf')
fig4.set_xlabels('Confidence in phase 2')
fig4.set(xticks=[0, 0.25, 0.5, 0.75, 1])
fig4.savefig('figs/distribution_of_confidence2.tif', dpi=300)
"""
