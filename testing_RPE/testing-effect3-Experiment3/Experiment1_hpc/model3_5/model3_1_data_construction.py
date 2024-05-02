# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 13:04:57 2023

@author: haopchen

In this file, I will construct the data for modelling
There will be {} data. All the data will be 3d matrix, with the first dimension as participant.
X: English words matrix
Y_choice: Choice matrix
Y_feed: feedbak matrix
Y_conf: Confidence matrix
Phase: phase matrix
Reward2: reward in phase 2
Reward3: reward in phase 3
RPE: RPE in phase 3
"""

### set the working directory
import os
#os.chdir(r'D:\OneDrive - UGent\Desktop\工作\phd-work\phd2-research\research1-nature-of-testing-effect\testing-effect5-Experiment3\Experiment3-2-models\model2')



### import the modules
import numpy as np
import pandas as pd



### function: data_construction
def data_construction(data_origin='', phases=[2, 3], file_path=''):
    """This function will construct the data for modelling"""
    
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    ### preprocess the original data
    ## import the original data
    data = pd.read_csv(data_origin)
    
    data_testing = data[data['learning_method']==1]
    data_c3_t_mean = data_testing.groupby(by=['participant'])['confidence3'].mean()
    data_c3_t_mean = data_c3_t_mean.reset_index()
    
    for row in range(data.shape[0]):
        p = data.loc[row, 'participant']
        t = data.loc[row, 'learning_method']
        
        if t == 1:
            data.loc[row, 'confidence3_inter'] = data.loc[row, 'confidence3']
        elif t == 0:
            data.loc[row, 'confidence3_inter'] = data_c3_t_mean[data_c3_t_mean['participant']==p]['confidence3'].values
    
    ## participants
    participants = data['participant'].unique()
    
    ## en_words
    en_words = np.sort(data['en_word'].unique())
    column_x = en_words.copy()
    
    ## swa_words
    swa_lists = data['options2'].str.split(',').values
    
    swa_words = []
    
    for swa_list in swa_lists:
        swa_words += swa_list
    
    swa_words = np.sort(np.unique(np.array(swa_words)))
    column_y = swa_words.copy()
    
    
    
    ### data for modelling
    ## initial
    X = np.ndarray([participants.shape[0], 90*len(phases), en_words.shape[0]])*0
    Y_choice = np.ndarray([participants.shape[0], 90*len(phases), swa_words.shape[0]])*0
    Y_feed = np.ndarray([participants.shape[0], 90*len(phases), swa_words.shape[0]])*0
    Y_conf = np.ndarray([participants.shape[0], 90*len(phases), swa_words.shape[0]])*0
    Y_options = np.ndarray([participants.shape[0], 90*len(phases), 4])
    Y_options = Y_options.astype(str)
    
    W = np.ndarray([participants.shape[0], en_words.shape[0], swa_words.shape[0]])*0
    
    Pars = np.ndarray([participants.shape[0], 90*len(phases), 1])
    Phase = np.ndarray([participants.shape[0], 90*len(phases), 1])
    Reward2 = np.ndarray([participants.shape[0], 90*len(phases), 1])
    Reward3 = np.ndarray([participants.shape[0], 90*len(phases), 1])
    RPE = np.ndarray([participants.shape[0], 90*len(phases), 1])
    TS = np.ndarray([participants.shape[0], 90*len(phases), 1])
    Valids = np.ndarray([participants.shape[0], 90*len(phases), 1])*0
    Accuracies = np.ndarray([participants.shape[0], 90*len(phases), 1])*0
    
    
    ## fill the value
    for dim1 in range(W.shape[0]):
        
        participant = participants[dim1]
        
        ### get the participant data
        data_par = data[data['participant']==participant]
        
        
        ### get the compare matrix
        for phase in phases:
            #!! delete            
            #phase = 2
            
            data_par = data_par.sort_values(by=['trial'+str(phase)])
            
            if phase == phases[0]:
                compare_ens = data_par['en_word'].values[:, np.newaxis]
                compare_choices = data_par['input_word'+str(phase)].values[:, np.newaxis]
                compare_feedbacks = data_par['swa_word'].values[:, np.newaxis]
                if phase == 3:
                    compare_confs = data_par['confidence'+str(phase)+'_inter'].values[:, np.newaxis]
                else:
                    compare_confs = data_par['confidence'+str(phase)].values[:, np.newaxis]
                
                compare_phases = np.ones_like(compare_ens)*phase
                compare_reward2s = data_par['reward2'].values[:, np.newaxis]
                compare_reward3s = data_par['reward3'].values[:, np.newaxis]
                compare_rpes = data_par['srpe'].values[:, np.newaxis]
                compare_tss = data_par['learning_method'].values[:, np.newaxis]
                compare_valids = np.ones_like(compare_ens)
                compare_accuracies = data_par['accuracy'].values[:, np.newaxis]
                
                compare_options = []
                option_lists = data_par['options'+str(phase)].str.split(',')
                for row in range(option_lists.shape[0]):
                    compare_options.append(option_lists.iloc[row])
                compare_options = pd.DataFrame(compare_options)
                
            else:
                compare_en = data_par['en_word'].values[:, np.newaxis]
                compare_ens = np.concatenate([compare_ens, compare_en], axis=0)
                
                compare_choice = data_par['input_word'+str(phase)].values[:, np.newaxis]
                compare_choices = np.concatenate([compare_choices, compare_choice], axis=0)
                
                compare_feedback = data_par['swa_word'].values[:, np.newaxis]
                compare_feedbacks = np.concatenate([compare_feedbacks, compare_feedback], axis=0)
                
                if phase == 3:
                    compare_conf = data_par['confidence'+str(phase)+'_inter'].values[:, np.newaxis]
                else:
                    compare_conf = data_par['confidence'+str(phase)].values[:, np.newaxis]
                compare_confs = np.concatenate([compare_confs, compare_conf], axis=0)
                
                compare_phase = np.ones_like(compare_en)*phase
                compare_phases = np.concatenate([compare_phases, compare_phase], axis=0)
                
                compare_reward2 = data_par['reward2'].values[:, np.newaxis]
                compare_reward2s = np.concatenate([compare_reward2s, compare_reward2], axis=0)
                
                compare_reward3 = data_par['reward3'].values[:, np.newaxis]
                compare_reward3s = np.concatenate([compare_reward3s, compare_reward3], axis=0)
                
                compare_rpe = data_par['srpe'].values[:, np.newaxis]
                compare_rpes = np.concatenate([compare_rpes, compare_rpe], axis=0)
                
                compare_ts = data_par['learning_method'].values[:, np.newaxis]
                compare_tss = np.concatenate([compare_tss, compare_ts], axis=0)
                
                compare_valid = np.ones_like(compare_en)
                compare_valids = np.concatenate([compare_valids, compare_valid], axis=0)
                
                compare_accuracy = data_par['accuracy'].values[:, np.newaxis]
                compare_accuracies = np.concatenate([compare_accuracies, compare_accuracy], axis=0)
                
                compare_option = []
                option_lists = data_par['options'+str(phase)].str.split(',')
                for row in range(option_lists.shape[0]):
                    compare_option.append(option_lists.iloc[row])
                compare_option = pd.DataFrame(compare_option)
                compare_options = np.concatenate([compare_options, compare_option], axis=0)
        
        ### fill value in the modelling matrix
        ## X matrix
        en_words = column_x[np.newaxis, :]
        en_words = np.repeat(en_words, [compare_ens.shape[0]], axis=0)
        
        X_par = (en_words == compare_ens)*1
        X[dim1, 0:X_par.shape[0], :] = X_par
        
        
        ## Y matrix
        swa_words = column_y[np.newaxis, :]
        swa_words = np.repeat(swa_words, [compare_choices.shape[0]], axis=0)
        
        Y_choice_par = (swa_words == compare_choices)*1
        Y_feed_par = (swa_words == compare_feedbacks)*1
        Y_conf_par = (swa_words == compare_choices)*compare_confs
        
        Y_choice[dim1, 0:Y_choice_par.shape[0], :] = Y_choice_par
        Y_feed[dim1, 0:Y_feed_par.shape[0], :] = Y_feed_par
        Y_conf[dim1, 0:Y_conf_par.shape[0], :] = Y_conf_par
        
        Y_options[dim1, 0:compare_options.shape[0], :] = compare_options
        
        
        ## experimental conditions
        Pars[dim1, 0:compare_phases.shape[0], :] = participant
        Phase[dim1, 0:compare_phases.shape[0], :] = compare_phases
        Reward2[dim1, 0:compare_reward2s.shape[0], :] = compare_reward2s
        Reward3[dim1, 0:compare_reward3s.shape[0], :] = compare_reward3s
        RPE[dim1, 0:compare_rpes.shape[0], :] = compare_rpes
        TS[dim1, 0:compare_tss.shape[0], :] = compare_tss
        Valids[dim1, 0:compare_valids.shape[0], :] = compare_valids
        Accuracies[dim1, 0:compare_accuracies.shape[0], :] = compare_accuracies
        
    ### save the data
    np.save(file_path+'X.npy', X)
    np.save(file_path+'Y_choice.npy', Y_choice)
    np.save(file_path+'Y_conf.npy', Y_conf)
    np.save(file_path+'Y_feed.npy', Y_feed)
    np.save(file_path+'Y_options.npy', Y_options)
    
    np.save(file_path+'Pars.npy', Pars)
    np.save(file_path+'Phase.npy', Phase)
    np.save(file_path+'Reward2.npy', Reward2)
    np.save(file_path+'Reward3.npy', Reward3)
    np.save(file_path+'RPE.npy', RPE)
    np.save(file_path+'TS.npy', TS)
    np.save(file_path+'Valids.npy', Valids)
    np.save(file_path+'Accuracies.npy', Accuracies)
    
    np.save(file_path+'column_x.npy', column_x)
    np.save(file_path+'column_y.npy', column_y)
    
    return participants, column_x, column_y    
        
    
data_origin = 'data/E1_original_data/data_preprocess_higher_than_0.34.csv'

phases = [2]
file_path = 'data/E1_data_construction/data_phase2/'
participants, column_x, column_y = data_construction(data_origin, phases, file_path)

phases = [3]
file_path = 'data/E1_data_construction/data_phase3/'
participants, column_x, column_y = data_construction(data_origin, phases, file_path)

phases = [4]
file_path = 'data/E1_data_construction/data_phase4/'
participants, column_x, column_y = data_construction(data_origin, phases, file_path)

phases = [5]
file_path = 'data/E1_data_construction/data_phase5/'
participants, column_x, column_y = data_construction(data_origin, phases, file_path)




