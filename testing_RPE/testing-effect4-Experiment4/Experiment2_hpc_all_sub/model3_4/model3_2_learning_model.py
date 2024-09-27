# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:33:48 2023

@author: haopchen
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 14:24:22 2023

@author: haopchen

In this file, we will try to build the learning model
"""

### set the working directory
import os
#os.chdir(r'C:\Users\haopchen\OneDrive - UGent\Desktop\工作\phd-work\phd2-research\research1-nature-of-testing-effect\testing-effect5-Experiment3\Experiment3-2-models\model2')



### import modules
import numpy as np
import pandas as pd



### logistic function
def logist(x, slope=1, bias=0):
    return 1/(1+np.exp(-slope*(x-bias)))
    
"""
a = 1
W = np.zeros([90, 360])
X = np.load('data/E1_data_construction/data_phase2/X.npy')
Y_conf = np.load('data/E1_data_construction/data_phase2/Y_conf.npy')
X = X[0, :, :]
Y_conf = Y_conf[0, :, :]
"""

### function: model prelearning
def model_prelearning(a, W, X, Y_conf):
    ### prelearning
    X_3d = X.reshape([X.shape[0], X.shape[1], 1])
    Y_conf_3d = Y_conf.reshape([Y_conf.shape[0], 1, Y_conf.shape[1]])
    W_update_3d = a * X_3d * Y_conf_3d
    W_update = W_update_3d.sum(axis=0)
    W += W_update
    
    return W

"""
a = 1
X = np.load('data/E1_data_construction/data_phase3/X.npy')
Y_conf = np.load('data/E1_data_construction/data_phase3/Y_conf.npy')
X = X[0, :, :]
Y_conf = Y_conf[0, :, :]
"""

"""
b = 1
slope=1
bias=1
X = np.load('data/E1_data_construction/data_phase3/X.npy')
Y_feed = np.load('data/E1_data_construction/data_phase3/Y_feed.npy')
Y_options = np.load('data/E1_data_construction/data_phase3/Y_options.npy')
TvS = np.load('data/E1_data_construction/data_phase3/TS.npy')
Reward3 = np.load('data/E1_data_construction/data_phase3/Reward3.npy')
swa_words = np.load('data/E1_data_construction/data_phase3/column_y.npy')
X = X[0, :, :]
Y_feed = Y_feed[0, :, :]
Y_options = Y_options[0, :, :]
TvS = TvS[0, :, :]
Reward3 = Reward3[0, :, :]
"""



### function: model formal learning
def model_learning(b, slope, bias, W, X, Y_feed, Y_options, TvS, Reward3, swa_words):
    ### Options 
    Options = np.sort(Y_options, axis=1)
    
    
    ### Choices
    Swa_words = swa_words[np.newaxis, :]
    Swa_words = np.repeat(Swa_words, [X.shape[0]], axis=0)    
    
    Swa_words_3d = Swa_words.reshape([Swa_words.shape[0], Swa_words.shape[1], 1])
    Options_3d = Options.reshape([Options.shape[0], 1, Options.shape[1]])
    
    Choices = (Swa_words_3d == Options_3d).sum(-1)
    
    
    ### Model prediction
    Y_pred = np.dot(X, W)
    # logistic
    Y_pred[Choices==1] = logist(Y_pred[Choices==1], slope=slope, bias=bias)
    # make sure the swa_words beyond options are 0
    Y_pred[Choices!=1] = 0
    # studying trials
    Y_pred = TvS*Y_pred + (1-TvS)*Y_feed*Y_pred
    
    # softmax
    Y_pred_sum = Y_pred.sum(axis=1)[:, np.newaxis]
    Y_pred_sum[Y_pred_sum==0] = 1
    Y_pred = Y_pred/Y_pred_sum
    
    
    ## learning
    X_3d = X.reshape([X.shape[0], X.shape[1], 1])
    Y_feed_3d = Y_feed.reshape([Y_feed.shape[0], 1, Y_feed.shape[1]])
    Reward3_3d = Reward3.reshape(Reward3.shape[0], 1, 1)
    # Hebbian learning
    W_update_3d = b * X_3d * Y_feed_3d * Reward3_3d
    W_update = W_update_3d.sum(axis=0)
    W += W_update
    # Delta learning
    #Y_pred_3d = Y_pred.reshape([Y_pred.shape[0], 1, Y_pred.shape[1]])
    #W_update_3d = b * X_3d * (Y_feed_3d - Y_pred_3d)
    #W_update = W_update_3d.sum(axis=0)
    #W += W_update
    
    return W


"""
slope = 1
bias = 1
X = np.load('data/E1_data_construction/data_phase4/X.npy')
Y_options = np.load('data/E1_data_construction/data_phase4/Y_options.npy')
swa_words = np.load('data/E1_data_construction/data_phase4/column_y.npy')
X = X[0, :, :]
Y_options = Y_options[0, :, :]
"""


### function: model testing
def model_testing(slope, bias, W, X, Y_options, swa_words):
    ### Options 
    Options = np.sort(Y_options, axis=1)
    
    
    ### Choices
    Swa_words = swa_words[np.newaxis, :]
    Swa_words = np.repeat(Swa_words, [X.shape[0]], axis=0)    
    
    Swa_words_3d = Swa_words.reshape([Swa_words.shape[0], Swa_words.shape[1], 1])
    Options_3d = Options.reshape([Options.shape[0], 1, Options.shape[1]])
    
    Choices = (Swa_words_3d == Options_3d).sum(-1)
    
    
    ### Model prediction
    Y_pred = np.dot(X, W)
    # logistic
    Y_pred[Choices==1] = logist(Y_pred[Choices==1], slope=slope, bias=bias)
    # make sure the swa_words beyond options are 0
    Y_pred[Choices!=1] = 0
    
    # softmax
    Y_pred_sum = Y_pred.sum(axis=1)[:, np.newaxis]
    Y_pred_sum[Y_pred_sum==0] = 1
    Y_pred = Y_pred/Y_pred_sum
        
    return Y_pred
        





    
    
    
    

    
    
    
    
    



