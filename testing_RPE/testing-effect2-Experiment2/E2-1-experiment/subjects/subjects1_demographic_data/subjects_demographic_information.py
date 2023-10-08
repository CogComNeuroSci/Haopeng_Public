# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 14:15:10 2023

@author: kygs1996

clear up the subjects data and payments
"""

### set the working directory
import os
os.chdir(r'D:\OneDrive - UGent\Desktop\工作\phd-work\phd2-research\research1-nature-of-testing-effect\testing-effect4-Experiment2\E2-1-experiment\subjects')



### import the modules
import pandas as pd
import numpy as np



### list the files
files = os.listdir('raw_data')



### concat the data
data_all = pd.DataFrame()

for file in files:
    data = pd.read_csv('raw_data/' + file)
    data_all = pd.concat([data_all, data], axis=0)



### only keep the approved subjects
data_all = data_all[data_all['Status']=='APPROVED']



### payments
## most subjects
data_all.loc[data_all['Handedness'].notnull(), ['Experiment', 'Payment', 'Service fee(prolific)', 'VAT(tax)', 'Total']] = ['Nature of testing effect-Experiment2-Part1', 7.5, 2.5, 0.5, 10.5]
data_all.loc[data_all['Handedness'].isnull(), ['Experiment', 'Payment', 'Service fee(prolific)', 'VAT(tax)', 'Total']] = ['Nature of testing effect-Experiment2-Part2', 4.5, 1.5, 0.3, 6.3]
## some subjects
data_all.loc[data_all['Submission id']=='63ce920033335a5dee98f33c', ['Payment', 'Service fee(prolific)', 'VAT(tax)', 'Total']] = [9, 2.995, 0.6, 12.595]
data_all.loc[data_all['Submission id']=='63ce599c672ae7bd96eec015', ['Payment', 'Service fee(prolific)', 'VAT(tax)', 'Total']] = [9, 2.995, 0.6, 12.595]
data_all.loc[data_all['Submission id']=='63cfe7db64b9080f9598d1d6', ['Payment', 'Service fee(prolific)', 'VAT(tax)', 'Total']] = [6, 2, 0.4, 8.4]



### date to pay
data_all['Date of payment'] = data_all['Reviewed at']
data_all['Prolific id'] = data_all['Participant id']



### save
data_payment = data_all.loc[:, ['Experiment', 'Prolific id', 'Started at', 'Completed at', 'Date of payment', 'Payment', 'Service fee(prolific)', 'VAT(tax)', 'Total']]
data_payment = data_payment.sort_values(by=['Prolific id', 'Experiment', 'Started at'])
data_payment.index = range(data_payment.shape[0])

data_all = data_all.sort_values(by=['Prolific id', 'Experiment', 'Started at'])
data_all.index = range(data_all.shape[0])

data_all.to_csv('subjects_demographic_data.csv')
data_payment.to_csv('subjects_payment.csv')

