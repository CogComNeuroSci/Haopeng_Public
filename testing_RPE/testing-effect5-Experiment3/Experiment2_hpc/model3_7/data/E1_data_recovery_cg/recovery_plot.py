# -*- coding: utf-8 -*-
"""
Created on Mon May 15 16:49:39 2023

@author: kygs1996
"""

### import the modules
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



### load the data
data = pd.read_csv('parameters_recovery.csv')
data.columns = ['invalid','p', 'b', 'slope', 'bias', 'loglike', 'AIC', 'success', 'generate_p', 'generate_b', 'generate_slope', 'generate_bias']


### plot
plt.rcParams['font.size'] = 18

## p
fig1 = sns.jointplot(data=data, x='generate_p', y='p', kind='reg')
fig1.set_axis_labels(xlabel='Generated α', ylabel='Estimated α')
fig1.savefig('../../figs/recovery_α.tif', dpi=300)

## b
fig2 = sns.jointplot(data=data, x='generate_b', y='b', kind='reg')
fig2.set_axis_labels(xlabel='Generated β', ylabel='Estimated β')
fig2.savefig('../../figs/recovery_β.tif', dpi=300)

## slope
fig3 = sns.jointplot(data=data, x='generate_slope', y='slope', kind='reg')
fig3.set_axis_labels(xlabel='Generated k', ylabel='Estimated k')
fig3.savefig('../../figs/recovery_k.tif', dpi=300)

## bias
fig4 = sns.jointplot(data=data, x='generate_bias', y='bias', kind='reg')
fig4.set_axis_labels(xlabel='Generated b', ylabel='Estimated b')
fig4.savefig('../../figs/recovery_b.tif', dpi=300)