###########################################
########formal analysis####################
###########################################

### clear
rm(list=ls())



### set the working directory
setwd('C:/Users/haopchen/OneDrive - UGent/Desktop/工作/phd-work/phd2-research/research1-nature-of-testing-effect/testing-effect3-Experiment1/Experiment1-4-formal-analysis/second-time')




### import the library
library(bruceR)
library(lmerTest)
library(caret)
library(car)




### import the data
## there are two sets of data
# data_preprocess.csv: all the data
# data_preprocess_higher_than_0.25.csv: delete the subjects whose performance is lower than chance level
# just choose a set of data to analysis
data <- read.csv('data_preprocess_higher_than_0.34.csv')
#data <- read.csv('data_preprocess.csv')



### preprocess
## reward has been encoded as 0,1
## confidence has been encoded as 0-1
## delete the correct items in the pretest
data <- data[data$reward2!=1,]
## mean centered
data$reward <- data$reward - 0.5
data$confidence <- data$confidence - 0.5
data$srpe <- data$srpe - 0
data$urpe <- data$urpe - 0.5
data$learning_method <- data$learning_method - 0.5




### formal analysis 1: all the data
## model 1: testing effect
data1 <- copy(data)
model1 <- glmer(data=data1, formula=accuracy~learning_method+(1|participant), family=binomial)
HLM_summary(model1)
Anova(model1, type=3)


## model2: testing (r3=1) vs studying
data2 <- copy(data)
data2 <- data2[data2$reward3==1,]
model2 <- glmer(data=data2, formula=accuracy~learning_method+(1|participant), family=binomial)
HLM_summary(model2)
Anova(model2, type=3)


## model3: testing (r3=0) vs studying
data3 <- copy(data)
data3 <- data3[data3$reward3==0 | data3$learning_method==-0.5,]
model3 <- glmer(data=data3, formula=accuracy~learning_method+(1|participant), family=binomial)
HLM_summary(model3)
Anova(model3, type=3)


## model4: testing (r3=1) vs testing (r3=0)
data4 <- copy(data)
data4 <- data4[data4$learning_method==0.5,]
model4 <- glmer(data=data4, formula=accuracy~reward+(1|participant), family=binomial)
HLM_summary(model4)
Anova(model4, type=3)


## model 5: srpe, confidence, testing effect
data5 <- copy(data)
model5 <- glmer(data=data5, formula=accuracy~learning_method+srpe+confidence+(1|participant), family=binomial)
HLM_summary(model5)
Anova(model5)

## model6: srpe, feedback, testing effect
data6 <- copy(data)
model6 <- glmer(data=data6, formula=accuracy~learning_method+srpe+reward+(1|participant), family=binomial)
HLM_summary(model6)
Anova(model6)

## model7: testing(RPE=1) VS studying
data7 <- copy(data)
data7 <- data7[data7$srpe==1 | data7$learning_method==-0.5,]
model7 <- glmer(data=data7, formula=accuracy~learning_method+(1|participant), family=binomial)
HLM_summary(model7)
Anova(model7)

## model8: reaction time (correct in phase 3) effect
data8 <- copy(data)
data8 <- data8[data8$reward3==1,]
data8$rt3z <- as.vector(scale(data8[,'rt3']))
model8 <- glmer(data=data8, formula=accuracy~rt3z+(1|participant), family=binomial)
HLM_summary(model8)
Anova(model8)
