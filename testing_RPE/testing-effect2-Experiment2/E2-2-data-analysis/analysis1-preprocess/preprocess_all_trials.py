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




### concat the data
## list the files
files1 = os.listdir('data1-first-day')
files2 = os.listdir('data2-second-day')

## concat the data
data_all = pd.DataFrame()

participant = 0

for file1 in files1:
    
    prolific_id = file1.split('t_')[1].split('.')[0]
    file2 = 'Data_part2_participant_{}.csv'.format(prolific_id)
    
    if file2 in files2:
        participant += 1
        data1 = pd.read_csv('data1-first-day/'+file1)
        data2 = pd.read_csv('data2-second-day/'+file2)
        # concat the data of two days
        data = pd.concat([data1, data2], axis=0)
        data['participant'] = participant
        data['prolific_id'] = prolific_id
        # reset index
        data.index = range(data.shape[0])
        # find the info of swa knowledge and previou subject
        swa_knowledge = data.loc[data.shape[0]-2, 'swahili_knowledge']
        previous_subject = data.loc[data.shape[0]-1, 'previous_subject']
        # drop phase 6
        data = data[data['phase']!=6]
        data['swahili_knowledge'] = swa_knowledge
        data['previous_subject'] = previous_subject
        
        data_all = pd.concat([data_all, data], axis=0)
    else:
        pass

        



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
data_all = data_all.pivot(index=['participant', 'prolific_id', 'en_word', 'swa_word', 'swahili_knowledge', 'previous_subject'], columns=['phase'], values=['accuracy', 'confidence', 'amt_choices', 'rt', 'rt_confidence', 'options', 'correct_answer', 'input_answer', 'input_word', 'trial_index'])
data_all = data_all.reset_index()      

## columns
columns = ['participant', 'prolific_id', 'en_word', 'swa_word', 'swahili_knowledge', 'previous_subject']
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



## encode confidence as 0-4
data_all.loc[:, ['confidence2', 'confidence3', 'confidence4', 'confidence5']] = (data_all.loc[:, ['confidence2', 'confidence3', 'confidence4', 'confidence5']] - 1)/4 

data_all['confidence'] = data_all['confidence3']

# set the confidence in studying as 4
data_all.loc[data_all['learning_method3']==1,'confidence'] = 1 

## encode learning_method as 0,1
data_all['learning_method'] = data_all['learning_method3']
data_all['learning_method'].replace([1,4], [0,1], inplace=True)
data_all = data_all.drop(columns=['learning_method2', 'learning_method3', 'learning_method4', 'learning_method5'])

## srpe and urpe
data_all['srpe'] = data_all['reward'] - data_all['confidence']
data_all['urpe'] = data_all['srpe'].abs() 

## reward4 and reward 5: 4,4=1; 0,0=0; 0,4=0;4,0=-1
data_all.index = range(data_all.shape[0])
for i in range(data_all.shape[0]):
    if data_all.loc[i, 'reward4'] == 1 and data_all.loc[i, 'reward5'] == 1:
        data_all.loc[i,'accuracy'] = 1
    elif data_all.loc[i, 'reward4'] == 0 and data_all.loc[i, 'reward5'] == 0:
        data_all.loc[i,'accuracy'] = 0
    elif data_all.loc[i, 'reward4'] == 0 and data_all.loc[i, 'reward5'] == 1:
        data_all.loc[i,'accuracy'] = 0
    elif data_all.loc[i, 'reward4'] == 1 and data_all.loc[i, 'reward5'] == 0:
        data_all.loc[i,'accuracy'] = 0
    else:
        print('error')
## delete the accuracy==-1
#data_all = data_all[data_all['accuracy']!=-1]



data_all.to_csv('data_81.csv')



### delete some subjects
## did not complete part 2 at the correct time
# number: 1
# 5e3752a476397a6e638bfc5e: complete part 2 three days later
# delete
data_all = data_all[data_all['prolific_id']!='5e3752a476397a6e638bfc5e'] 


## know swahili
sub_know_swa = data_all[data_all['swahili_knowledge']!=1]['prolific_id'].unique()
sub_know_swa_index = data_all[data_all['swahili_knowledge']!=1]['participant'].unique()
# number: 3
# 5d085064a1462600014abf83: 4 
# 598861b3b24ef3000141a129: 2 I asked this subject after the experiment, he did not know swahili at all, just give a wrong choice.
# 614b4820859193e9fba60056: 2 
# correct the wrong choice
data_all.loc[data_all['prolific_id']=='598861b3b24ef3000141a129', 'swahili_knowledge'] = 1
# delete
data_all = data_all[data_all['swahili_knowledge']==1]


## previous subject
sub_pre = data_all[data_all['previous_subject']==True]['prolific_id'].unique()
sub_pre_index = data_all[data_all['previous_subject']==True]['participant'].unique()
# number: 3
# 5b36a113fb22f300017f6373   I asked this subject after the experiment, he took part in an alien language experiment before, not our experiment 1
# 5ec3a5cba4bc9403103a292b
# 60f30cd3b09a237bc5f6cde5
# correct the wrong choice
data_all.loc[data_all['prolific_id']=='5b36a113fb22f300017f6373', 'previous_subject'] = False
# delete
data_all = data_all[data_all['previous_subject']!=True]


### save the data
data_all.to_csv('data_preprocess.csv')


## calculate the mean accuracy
mean_accuracy = data_all.groupby(by=['participant', 'prolific_id'])['accuracy'].mean()
mean_accuracy = mean_accuracy.reset_index()
# plot distribution
fig1 = sns.displot(data=mean_accuracy, x='accuracy'
                   ,bins=30
                   ,kind='hist')
# poor subjects
sub_poor = mean_accuracy[mean_accuracy['accuracy']<=0.34]['prolific_id'].tolist()
sub_poor_number = len(sub_poor)
print(sub_poor)
print(sub_poor_number)
# number: 31
# '54ad30a4fdf99b6f3e1e2b6b', '5711089f52ab8e0011d08d03', '574c17587fd0ec0006b655cc'
# '5929b05b6c835800011a31cc', '595f5d26b752840001ca4451', '5ac228c50527ba0001c1f6bb'
# '5ad0422dfb109b0001a30f35', '5afb134c57516b0001416b48', '5b0ea5ea30d5620001558164'
# '5c2e33e751dcf20001b3204d', '5cd8638310887400162dafec', '5ce6525a185715001708c627'
# '5d53a5e5a8b69800169db103', '5d63f9cd26a2ac001758c70d', '5e19961e1b8014222555c3b2'
# '5e2761b3ce16da9982f88406', '5ec7d68512268325623eb178', '5f0f44ccf585170d7b14c030'
# '5f647d84fc17022190cfac83', '5f8d77f0b348950659f1919e', '606ddb0033f69d1a832059cd'
# '60c86fbb5fb507607c3073bf', '611fb8ddcc7bb35d86ec0714', '6126cf8d9e5187763c6adb73'
# '615f4e20d504f648ffd22972', '6277f267a2d1f33351549d0d', '62aa2bdbe3bab086b19ea5ab'
# '62b1ff970dfb7055f35d6937', '62c5e88d434d3ad81799df4d', '62fb8535d6e34ce6214ba696'
# '63ced2a1d7f0270214c80274'

# delete

for i in sub_poor:
    data_all = data_all[data_all['prolific_id']!=i]




### save the data
data_all.to_csv('data_preprocess_higher_than_0.34.csv')





### remaining subjects
sub_remain = data_all['prolific_id'].unique()
sub_remain_number = data_all['participant'].unique().shape[0]
print(sub_remain)
print(sub_remain_number)
# 45



### main preprocess
data_all = data_all[data_all['reward2']!=4]




### plot
data_plot_srpe = data_all.groupby(by=['participant', 'srpe', 'learning_method', 'reward', 'reward2'])['accuracy'].mean()
data_plot_srpe = data_plot_srpe.reset_index()
data_plot_srpe.columns = ['participants', 'SRPE', 'Testing Vs Studying', 'Feedback (Phase3)', 'Feedback (Phase2)', 'Accuracy']
data_plot_srpe = data_plot_srpe.sort_values(by='Testing Vs Studying')
data_plot_srpe['Testing Vs Studying'].replace([0, 1], ['Studying', 'Testing'], inplace=True)




#plt.rcParams['font.size'] = 8
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['legend.fontsize'] = 15
plt.rcParams['legend.title_fontsize'] = 15
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


fig2 = sns.catplot(data=data_plot_srpe, x='SRPE', y='Accuracy', hue='Testing Vs Studying' 
                   ,col='Feedback (Phase3)'
                   ,row='Feedback (Phase2)'
                   ,kind='bar', errorbar='se')
fig2.set_xlabels('RPE')
#fig2.fig.text(-0.2, 0.8, 'Reward(phase2)=0', size=15)
#fig2.fig.text(-0.2, 0.3, 'Reward(phase2)=4', size=15)
#fig2.fig.text(0.2, 1.05, 'Reward(phase3)=0', size=15)
#fig2.fig.text(0.6, 1.05, 'Reward(phase3)=4', size=15)


fig2.savefig('figs/rpe-and-testing.tif', dpi=300)












"""
### extra analysis
## check how many same input words in phase2 and phase3 in every condition
data_all.loc[data_all['input_word2']==data_all['input_word3'], 'same_word23'] = 1
data_all.loc[data_all['input_word2']!=data_all['input_word3'], 'same_word23'] = 0

data_all.loc[data_all['input_word3']==data_all['input_word4'], 'same_word34'] = 1
data_all.loc[data_all['input_word3']!=data_all['input_word4'], 'same_word34'] = 0

fig3 = sns.catplot(data=data_all, x='srpe', y='same_word34', hue='learning_method', col='reward'
                   ,row='reward2'
                   , kind='bar')
"""