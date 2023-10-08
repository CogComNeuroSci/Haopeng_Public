# -*- coding: utf-8 -*-
"""
Created on Tue May 30 13:13:31 2023

@author: kygs1996

summarize the basic information of participants
"""

### import modules 
import numpy as np
import pandas as pd



### load the data
## subjects
subjects = pd.read_csv('subjects_all.csv')
subjects = subjects[subjects['Experiment']=='Nature of testing effect-Experiment2-Part1']

## data
# data with 81 participants
data_81 = pd.read_csv('data_81.csv')
pid_81 = data_81['prolific_id'].unique()



### subjects
## 81 (80) subjects 
subjects_81_index = (subjects.loc[:, 'Participant id'].values[:, np.newaxis] == pid_81[np.newaxis, :]).sum(axis=1)
subjects_81 = subjects.iloc[subjects_81_index==1, :]
subjects_81.to_csv('subjects_81.csv')



## sex
sex_81 = subjects_81.groupby(by=['Sex'])['Sex'].count()

## age
age_mean_81 = subjects_81['Age'].mean() 
age_std_81 = subjects_81['Age'].std()
age_min_81 = subjects_81['Age'].min()
age_max_81 = subjects_81['Age'].max()


