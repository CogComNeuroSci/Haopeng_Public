# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:25:44 2023

@author: kygs1996

In this script, I summarize the demographic data of participants in Experiment 1
"""

### load the modules
import numpy as np
import pandas as pd



### load the data
data = pd.read_csv('RPE-and-Test-0-Demographic_data.csv')



### preprocess
## only keep the approved subjects
data = data[data['status']=='APPROVED'] # 80 subjects



### describe analysis
## number of participants
sub_number = data.shape[0] # 80

## age
age_mean = data['age'].mean() # 30.35
age_std = data['age'].std() # 6.07
age_min = data['age'].min() # 18
age_max = data['age'].max() # 41

## gender
gender = data.groupby(by=['Sex'])['Sex'].count() # female: 37; male: 43
