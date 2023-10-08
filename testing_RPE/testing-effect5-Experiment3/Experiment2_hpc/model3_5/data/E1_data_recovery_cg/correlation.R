### set the working directory
setwd('C:/Users/haopchen/OneDrive - UGent/Desktop/工作/phd-work/phd2-research/research1-nature-of-testing-effect/testing-effect5-Experiment3/Experiment3-2-models/model3/Experiment2_hpc/model3_5/data/E2_data_recovery_powell')


### load the data
data <- read.csv('parameters_recovery.csv')


library(bruceR)
?bruceR
### correlation analysis
?Corr
Corr(data, digits=3)
