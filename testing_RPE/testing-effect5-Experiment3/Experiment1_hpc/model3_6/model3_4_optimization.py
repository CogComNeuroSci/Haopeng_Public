# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 10:32:06 2023

@author: haopchen

optimization: Hebbian learning, Delta learning
"""

### set the current working directory
import os
#os.chdir(r'C:\Users\haopchen\OneDrive - UGent\Desktop\工作\phd-work\phd2-research\research1-nature-of-testing-effect\testing-effect5-Experiment3\Experiment3-2-models\model2')



### import the modules
import numpy as np
import pandas as pd
import random
from scipy.optimize import minimize




### logistic function for parameters
def logistic(x):
    return 1/(1+np.exp(-x))



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
X_testing_3d_1 = np.load('data/E1_data_construction/data_phase4/X.npy')
X_testing_3d_2 = np.load('data/E1_data_construction/data_phase5/X.npy')
X_testing_3d = np.concatenate([X_testing_3d_1, X_testing_3d_2], axis=1)

Y_options_testing_3d_1 = np.load('data/E1_data_construction/data_phase4/Y_options.npy')
Y_options_testing_3d_2 = np.load('data/E1_data_construction/data_phase5/Y_options.npy')
Y_options_testing_3d = np.concatenate([Y_options_testing_3d_1, Y_options_testing_3d_2], axis=1)

Y_choice_testing_3d_1 = np.load('data/E1_data_construction/data_phase4/Y_choice.npy')
Y_choice_testing_3d_2 = np.load('data/E1_data_construction/data_phase5/Y_choice.npy')
Y_choice_testing_3d = np.concatenate([Y_choice_testing_3d_1, Y_choice_testing_3d_2], axis=1)

swa_words = np.load('data/E1_data_construction/data_phase4/column_y.npy')

## optimization
method = 'CG'
maxiter = 10_000


data_all = pd.DataFrame()
#data_success = pd.DataFrame()


### optimization for each participant
for sub in range(X_phase2_3d.shape[0]):
#for sub in [0]:
    ## prepare the data
    X_phase2 = X_phase2_3d[sub, :, :]
    Y_conf_phase2 = Y_conf_phase2_3d[sub, :, :]
    
    X_phase3 = X_phase3_3d[sub, :, :]
    Y_conf_phase3 = Y_conf_phase3_3d[sub, :, :]
    
    Y_feed_phase3 = Y_feed_phase3_3d[sub, :, :]
    Y_options_phase3 = Y_options_phase3_3d[sub, :, :]
    TvS_phase3 = TvS_phase3_3d[sub, :, :]
    Reward3_phase3 = Reward3_phase3_3d[sub, :, :]

    X_testing = X_testing_3d[sub, :, :]
    Y_options_testing = Y_options_testing_3d[sub, :, :]
    Y_choice_testing = Y_choice_testing_3d[sub, :, :]
    
    W0 = np.zeros([X_phase2.shape[1], Y_conf_phase2.shape[1]])
    
    data_sub = pd.DataFrame()

    
    for opt in range(10):
        ## optimization
        from model3_3_loss_function import log_like
    
        # initial parameters
        x0 = random.choices([-1, 1], k=3)*np.random.rand(3)*5
    
        # minimize the loss function
        res = minimize(log_like, x0=x0, method=method,
                       args=(W0.copy(), X_phase2.copy(), Y_conf_phase2.copy(),
                             X_phase3.copy(), Y_conf_phase3.copy(), Y_feed_phase3.copy(), Y_options_phase3.copy(), TvS_phase3.copy(), Reward3_phase3.copy(),
                             X_testing.copy(), Y_options_testing.copy(), Y_choice_testing.copy(), swa_words.copy()),
                       tol=1e-15,
                       options={'maxiter': maxiter, 'disp': True, 
                                #'gtol': 1e-8,
                                #'eps': 1e-10
                                }
                       )
    
    
    
        ## optimal parameters
        optimals = res.x
    
        parameters = np.zeros([3])
        #parameters[0:1] = np.exp(optimals[0:1])
        #parameters[0:1] = parameters[0:1]/parameters[0:1].sum()
        parameters[0:1] = 1
        parameters[1:3] = 10*logistic(optimals[1:3])
    
        log_like = res.fun
        AIC = 2*3 + 2*log_like
        success = res.success*1
        #gradients = res.jac
    
        print('subject: ', sub)
        print('parameters:', parameters)
        print('AIC:', AIC)
        print('success:', success)
        #print('gradients:', gradients)
        
        data = parameters.tolist() + [log_like] + [AIC] + [success] 
        #+ gradients.tolist() 
        data = pd.DataFrame(data).T
        
        data_sub = pd.concat([data_sub, data], axis=0)
        
        
        
    data_best = data_sub[data_sub.iloc[:, 4]==data_sub.iloc[:, 4].min()].iloc[0, :].to_frame().T
    
    data_all = pd.concat([data_all, data_best], axis=0)
    
    #data_success = pd.concat([data_success, data], axis=0)

    #data_success.columns = ['p', 'b', 'slope', 'bias', 'log_like', 'AIC', 'success', 'g1', 'g2', 'g3', 'g4']

    data_all.to_csv('data/E1_data_parameters/parameters_best.csv')
    #data_success.to_csv('data/E1_data_parameters/parameters_success.csv')

