# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 12:55:51 2023

@author: haopchen

In this file, we will define the loss function to optimize
there are only four parameters: a, b, slope, bias
"""

### set the working directory
import os
#os.chdir(r'C:\Users\haopchen\OneDrive - UGent\Desktop\工作\phd-work\phd2-research\research1-nature-of-testing-effect\testing-effect5-Experiment3\Experiment3-2-models\model3')



### import the modules
import numpy as np
import pandas as pd
from model3_2_learning_model import model_prelearning, model_learning, model_testing



### logistic function for parameters
def logistic(x):
    return 1/(1+np.exp(-x))



### MSE
def log_like(parameters, W0, X_phase2, Y_conf_phase2,
             X_phase3, Y_conf_phase3, Y_feed_phase3, Y_options_phase3, TvS_phase3, Reward3_phase3,
             X_testing, Y_options_testing, Y_choice_testing, swa_words):
    
    ### use logistic function to set the bounds of the parameters
    ## set the bounds of learning rate as (0, 1)
    parameters[0:2] = np.exp(parameters[0:2])
    parameters[0:2] = parameters[0:2]/parameters[0:2].sum()
    parameters[2] = 1*logistic(parameters[2])
    parameters[3:5] = 10*logistic(parameters[3:5])
    #print(parameters)
    
    
    ### prelearning (phase 2)
    W1 = model_prelearning(a=parameters[0], W=W0.copy(), X=X_phase2.copy(), Y_conf=Y_conf_phase2.copy())
    
    
    ### prelearning (phase 3)
    W2 = model_prelearning(a=parameters[0], W=W1.copy(), X=X_phase3.copy(), Y_conf=Y_conf_phase3.copy())
    
    
    ### formal learning
    W3 = model_learning(b1=parameters[1], b2=parameters[2], slope=parameters[3], bias=parameters[4], W=W2.copy(), X=X_phase3.copy(), Y_feed=Y_feed_phase3.copy(), Y_options=Y_options_phase3.copy(), TvS=TvS_phase3.copy(), Reward3=Reward3_phase3.copy(), swa_words=swa_words.copy())
    
    
    ### model testing
    Y_pred = model_testing(slope=parameters[3], bias=parameters[4], W=W3.copy(), X=X_testing.copy(), Y_options=Y_options_testing.copy(), swa_words=swa_words.copy())
    
    
    ### likelihood
    like = Y_pred[Y_choice_testing==1]
    log_like = -np.log(like).sum()
    

    #print(log_like)    
    
    return log_like
    
