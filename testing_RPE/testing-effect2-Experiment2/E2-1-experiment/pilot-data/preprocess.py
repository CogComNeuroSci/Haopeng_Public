# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 15:18:22 2023

@author: haopchen
"""

## change the working directory
import os
os.chdir(r'C:\Users\haopchen\OneDrive - UGent\Desktop\工作\phd-work\phd2-research\research1-nature-of-testing-effect\testing-effect4-Experiment1-2\Repetition-1-experiment\pilot-data')

## import the modules
import pandas as pd
import numpy as np

## import the data
data1_3 = pd.read_csv('phase1_3.csv')
data4_5 = pd.read_csv('phase4_5.csv')

## preprocess
# concat
data = pd.concat([data1_3, data4_5], axis=0)

# reset the index
data.index = range(data.shape[0])

# delete the extra information (phase 6)
data = data[data['phase'] != 6] 

# delete the rows of feedback (phase 3)
data_phase3 = data[data['phase'] == 3]
data_delete = data_phase3[data_phase3['rt'].isnull()]
data_delete_index = data_delete.index.tolist()

data = data.drop(data_delete_index, axis=0)
# reset the index
data.index = range(data.shape[0])

# fill the en_word in the na
for i in range(data.shape[0]):
    if data.loc[i, 'en_word'] != data.loc[i, 'en_word']:
        data.loc[i, 'en_word'] = data.loc[i-1, 'en_word']


# pivot: merge the response rows and confidence rows
data_prep = data.pivot(index=['en_word', 'phase'], columns='trial_type', values=['rt', 'certainty'])

data_prep = data_prep.reset_index()
data_prep.columns = ['en_word', 'phase', 'rt_response', 'rt_confidence', 'confidence_na', 'confidence']

data_prep = data_prep.drop('confidence_na', axis=1)

data = data.dropna(axis=0, subset=['options'])
data = data.sort_values(by=['en_word', 'phase'])
data.index = range(data.shape[0])
data = data.drop(['en_word', 'phase'], axis=1)

data_prep = pd.concat([data_prep, data], axis=1)

