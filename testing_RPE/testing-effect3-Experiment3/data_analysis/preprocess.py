# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 14:51:13 2023

@author: haopchen

pre-process
keep all the trials
"""

### set the working directory
import os
#os.chdir(r'C:\Users\haopchen\OneDrive - UGent\Desktop\工作\phd-work\phd2-research\research1-nature-of-testing-effect\testing-effect4-Experiment2\E2-3-data-analysis\second-time\analysis1-preprocess')




### import the modules
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl


### remove subjects or not
remove = True


### concat the data
## list the files
files = os.listdir('raw_data')

## concat the data
data_all = pd.DataFrame()

participant = 0

for file in files:
    data = pd.read_csv('raw_data/' + file)
    data['participant'] = participant
    participant+=1    
    
    data_all = pd.concat([data_all, data], axis=0)
    

        

### preprocess
## reset the index
data_all.index = range(data_all.shape[0])

## move the rt_confidence and confidence to the the last row
for i in range(data_all.shape[0]):
    if data_all.loc[i, 'trial_type'] == 'html-slider-response':
        data_all.loc[i-1, 'confidence'] = data_all.loc[i, 'certainty']
        data_all.loc[i-1, 'rt_confidence'] = data_all.loc[i, 'rt']
    else:
        pass
        
## drop the useless rows
data_all = data_all.dropna(subset=['en_word'], axis=0)    

## pivot the data
data_all = data_all.pivot(index=['participant', 'en_word', 'swa_word'], columns=['phase'], values=['accuracy', 'confidence', 'amt_choices', 'rt', 'rt_confidence', 'options', 'correct_answer', 'input_answer', 'input_word', 'trial_index'])
data_all = data_all.reset_index()      

## columns
columns = ['participant', 'en_word', 'swa_word']
for name in ['reward', 'confidence', 'learning_method', 'rt', 'rt_confidence', 'options', 'correct_answer', 'input_answer', 'input_word', 'trial']:
    for number in ['2', '3', '4', '5']:
        column_name = name + number 
        columns.append(column_name)
data_all.columns = columns

## encode reward as 0,4
data_all.loc[:,'reward2'].replace([True, False], [1, 0], inplace=True)
data_all.loc[:,'reward3'].replace([True, False], [1, 0], inplace=True)
data_all.loc[:,'reward4'].replace([True, False], [1, 0], inplace=True)
data_all.loc[:,'reward5'].replace([True, False], [1, 0], inplace=True)

data_all['reward'] = data_all['reward3']



## encode confidence as 0-1
data_all.loc[:, ['confidence2', 'confidence3', 'confidence4', 'confidence5']] = (data_all.loc[:, ['confidence2', 'confidence3', 'confidence4', 'confidence5']] - 1)/4 

data_all['confidence'] = data_all['confidence3']

# set the confidence in studying as 1
data_all.loc[data_all['learning_method3']==1,'confidence'] = 1 

## encode learning_method as 0,1
data_all['learning_method'] = data_all['learning_method3']
data_all['learning_method'].replace([1,4], [0,1], inplace=True)
data_all = data_all.drop(columns=['learning_method2', 'learning_method3', 'learning_method4', 'learning_method5'])

## srpe and urpe
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





