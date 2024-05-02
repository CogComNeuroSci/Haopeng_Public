## clear
rm(list=ls())


## import modules
library(bruceR)
library(lmerTest)


## import data
data <- read.csv('data_all.csv')


## preprocess
data$test <- data$test_3
data$test <- data$test - 0.5
data$srpe <- data$srpe - 0
data$urpe <- data$urpe - 1.5

#data <- data[data$accuracy_2=='False',]

## models
# testing effect
model <- glmer(data=data, formula=final_accuracy~test+(1|participant), family='binomial')
summary(model)

model <- glmer(data=data, formula=final_accuracy~srpe+(1|participant), family='binomial')
summary(model)

