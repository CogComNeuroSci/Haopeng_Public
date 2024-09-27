# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 13:26:33 2023

@author: kygs1996

Preprocess data from experiment 1.

keep all the trials of each subject 
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
data_all['reward2'].replace([True, False], [1, 0], inplace=True)
data_all['reward3'].replace([True, False], [1, 0], inplace=True)
data_all['reward4'].replace([True, False], [1, 0], inplace=True)
data_all['reward5'].replace([True, False], [1, 0], inplace=True)

## add the columns of reward and confidence
data_all['reward'] = data_all['reward3']
data_all['confidence'] = data_all['confidence3']

## replace the values of learning method
data_all['learning_method'].replace([1,4], [0,1], inplace=True)

## replace the values of confidence
data_all.loc[:, ['confidence2', 'confidence3', 'confidence4', 'confidence5', 'confidence']] = (data_all.loc[:, ['confidence2', 'confidence3', 'confidence4', 'confidence5', 'confidence']] - 1)/4

## set the confidence in the studying condition as 1
data_all.loc[data_all['learning_method']==0, 'confidence'] = 1

## calculate the srpe and urpe
data_all['srpe'] = data_all['reward'] - data_all['confidence']
data_all['urpe'] = data_all['srpe'].abs()

## cauculate the final accuracy
# binary accuracy
data_all['accuracy_binary'] = data_all['reward4'] + data_all['reward5'] - 1
data_all.loc[data_all['accuracy_binary']==-1, 'accuracy_binary'] = 0
# continuous accuracy
data_all['accuracy_continuous'] = (data_all['reward4'] + data_all['reward5'])/2
 

### calculate the accuracy of every participant
## binary acc
# individual accuracy
data_acc = data_all.groupby(by=['participant'])['accuracy_binary'].mean()
data_acc = data_acc.reset_index()
data_acc.columns = ['participant', 'individual_binary_acc']
# merge the data
data_all = data_all.merge(data_acc, how='left', on='participant')

## continuous acc
# individual accuracy
data_acc = data_all.groupby(by=['participant'])['accuracy_continuous'].mean()
data_acc = data_acc.reset_index()
data_acc.columns = ['participant', 'individual_continuous_acc']
# merge the data
data_all = data_all.merge(data_acc, how='left', on='participant')


### save the data
data_all.to_csv('data_preprocess.csv')

