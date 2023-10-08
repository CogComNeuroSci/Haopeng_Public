# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 22:08:22 2023

@author: kygs1996

draw the heatmap
"""


## import modules
import pandas as pd
import seaborn as sns


## import data
data = pd.read_csv('heat_data/heat_data.csv')

data = data.pivot(index='p', columns='b', values='dif')


## plot
heatmap = sns.heatmap(data, cmap='Blues')
heatmap.set_xlabel('β')
heatmap.set_ylabel('α')
heatmap.invert_yaxis()

figure = heatmap.get_figure()
figure.savefig('heatmap.tif', dpi=300)
