# -*- coding: utf-8 -*-
"""
Created on Fri May 12 12:30:36 2023

@author: kygs1996

model recovery
1 choose a set of parameters (100) and random input data (X, Y_conf, Y_feed, Y_options, TvS, Reward3) to generate different data (Y_choice)
2 optimize the generating data, and get the optimal parameters
"""

#### import modules
import os
import numpy as np
import pandas as pd
import random
from model3_2_learning_model import model_prelearning, model_learning, model_testing
from scipy.optimize import minimize



#### logistic function for parameters
def logistic(x):
    return 1/(1+np.exp(-x))




#### data generation
### parameters
np.random.seed(6)
A = np.random.rand(100)
B = 1 -A
Slope = 20*np.random.rand(100)
Bias = 20*np.random.rand(100)
 

### input data        
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

#Y_choice_testing_3d_1 = np.load('data/E1_data_construction/data_phase4/Y_choice.npy')
#Y_choice_testing_3d_2 = np.load('data/E1_data_construction/data_phase5/Y_choice.npy')
#Y_choice_testing_3d = np.concatenate([Y_choice_testing_3d_1, Y_choice_testing_3d_2], axis=1)

swa_words = np.load('data/E1_data_construction/data_phase4/column_y.npy')

## random subjects
subjects_all = list(range(X_phase2_3d.shape[0]))
subjects = random.choices(subjects_all, k=100)



data_all = pd.DataFrame()



### generation and simulation
generations = 100
Y_choice_3d = np.zeros([generations, X_testing_3d.shape[1], 360])

for g in range(generations):
#for g in [0, 1, 2]:
    ### parameters
    a = A[g]
    b = B[g]
    slope = Slope[g]
    bias = Bias[g]
    
    
    ### subject number
    sub = subjects[g]
    
    
    ### input data
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
    #Y_choice_testing = Y_choice_testing_3d[sub, :, :]
    
    W0 = np.zeros([X_phase2.shape[1], Y_conf_phase2.shape[1]])
    
    
    ### model training
    ## prelearning (phase 2)
    W1 = model_prelearning(a=a, W=W0.copy(), X=X_phase2, Y_conf=Y_conf_phase2)
    
    ## prelearning (phase 3)
    W2 = model_prelearning(a=a, W=W1.copy(), X=X_phase3, Y_conf=Y_conf_phase3)
    
    ## formal learning
    W3 = model_learning(b=b, slope=slope, bias=slope, W=W2.copy(), X=X_phase3, Y_feed=Y_feed_phase3, Y_options=Y_options_phase3, TvS=TvS_phase3, Reward3=Reward3_phase3, swa_words=swa_words)
    
    ## model prediction
    Y_pred, Choices = model_testing(slope=slope, bias=bias, W=W3.copy(), X=X_testing, Y_options=Y_options_testing, swa_words=swa_words)
    
    Y_pred_options = Y_pred[Choices==1]
    Y_pred_options = Y_pred_options.reshape([int(Y_pred_options.shape[0]/4), 4])
    
    Y_pred_options = Y_pred_options.cumsum(axis=1)
    
    Y_pred_options2 = np.zeros_like(Y_pred_options)
    Y_pred_options2[:, 0] = 0
    Y_pred_options2[:, 1:4] = Y_pred_options[:, 0:3]
    
    Judge = np.random.rand(Y_pred_options.shape[0], 1)
    Judge = np.repeat(Judge, [4], axis=1)
    
    Y_pred_choice = (Y_pred_options2 <= Judge)*1 + (Judge < Y_pred_options)*1 - 1
    
    Y_pred[Choices==1] = Y_pred_choice.flatten()
    
    Y_choice_testing = Y_pred.copy()
    
    #Y_choice_3d[g, :, :] = Y_choice_testing
    
    
    
    ###optimization
    method = 'Powell'
    maxiter = 10_000
    
    data_sub = pd.DataFrame()
    for opt in range(10):
        ## optimization
        from model3_3_loss_function_recovery import log_like
    
        # initial parameters
        x0 = random.choices([-1, 1], k=4)*np.random.rand(4)*5
    
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
    
        parameters = np.zeros([4])
        parameters[0:2] = np.exp(optimals[0:2])
        parameters[0:2] = parameters[0:2]/parameters[0:2].sum()
        parameters[2:4] = 20*logistic(optimals[2:4])
    
        log_like = res.fun
        AIC = 2*4 + 2*log_like
        success = res.success*1
        #gradients = res.jac
    
        print('subject: ', sub)
        print('parameters:', parameters)
        print('AIC:', AIC)
        print('success:', success)
        #print('gradients:', gradients)
        
        data = parameters.tolist() + [log_like] + [AIC] + [success] + [a] + [b] + [slope] + [bias] 
        data = pd.DataFrame(data).T
        
        data_sub = pd.concat([data_sub, data], axis=0)
        
        
        
    data_best = data_sub[data_sub.iloc[:, 5]==data_sub.iloc[:, 5].min()].iloc[0, :].to_frame().T

    data_all = pd.concat([data_all, data_best], axis=0)
    
    if not os.path.exists('data/E1_data_recovery/'):
        os.makedirs('data/E1_data_recovery/')
    
    data_all.to_csv('data/E1_data_recovery/parameters_recovery.csv')
  











