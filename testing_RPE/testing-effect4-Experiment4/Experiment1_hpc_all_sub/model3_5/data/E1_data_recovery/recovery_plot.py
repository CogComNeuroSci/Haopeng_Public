# -*- coding: utf-8 -*-
"""
Created on Mon May 15 16:49:39 2023

@author: kygs1996
"""

### import the modules
import numpy as np
import pandas as pd
import seaborn as sns



### load the data
data = pd.read_csv('parameters_recovery.csv')
data.columns = ['invalid','p', 'b', 'slope', 'bias', 'loglike', 'AIC', 'success', 'generate_p', 'generate_b', 'generate_slope', 'generate_bias']


### plot
## p
fig1 = sns.jointplot(data=data, x='generate_p', y='p', kind='reg')
fig1.set_axis_labels(xlabel='Generated p', ylabel='Estimated p', size=15)
fig1.savefig('../../figs/recovery_p.tif', dpi=300)

## b
fig2 = sns.jointplot(data=data, x='generate_b', y='b', kind='reg')
fig2.set_axis_labels(xlabel='Generated b', ylabel='Estimated b', size=15)
fig2.savefig('../../figs/recovery_b.tif', dpi=300)

## slope
fig3 = sns.jointplot(data=data, x='generate_slope', y='slope', kind='reg')
fig3.set_axis_labels(xlabel='Generated slope', ylabel='Estimated slope', size=15)
fig3.savefig('../../figs/recovery_slope.tif', dpi=300)

## bias
fig4 = sns.jointplot(data=data, x='generate_bias', y='bias', kind='reg')
fig4.set_axis_labels(xlabel='Generated bias', ylabel='Estimated bias', size=15)
fig4.savefig('../../figs/recovery_bias.tif', dpi=300)