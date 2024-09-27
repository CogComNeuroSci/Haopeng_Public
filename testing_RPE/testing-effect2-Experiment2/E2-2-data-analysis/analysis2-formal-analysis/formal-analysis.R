############################################
###########formal analysis##################
############################################

rm(list=ls())


### import the modules
library(lme4)
library(bruceR)
library(caret)
library(car)


## data without removing subjects?
full_data <- FALSE
binary = FALSE

### import the data
data <- read.csv('data_preprocess.csv')

## full data? binary?
if (full_data & binary) {
  print('full data')
  print('binary accuracy')
  data$accuracy <- data$accuracy_binary
} else if (full_data & !binary) {
  print('full data')
  print('binary accuracy')
  data$accuracy <- data$accuracy_continuous
} else if (!full_data & binary) {
  print('good data')
  print('binary accuracy')
  data <- data[data$individual_binary_acc>=0.34,]
  data$accuracy <- data$accuracy_binary
} else if (!full_data & !binary) {
  print('good data')
  print('continuous accuracy')
  data <- data[data$individual_continuous_acc>=0.34,]
  data$accuracy = data$accuracy_continuous
}


### preprocess
## reward has been encoded as 0,1
## confidence has been encoded as 0-1
## delete the correct items in the pretest
data <- data[data$reward2!=1,]
data$test <- data$learning_method
## mean centered
data$reward <- data$reward - 0.5
data$confidence <- data$confidence - 0.5
data$srpe <- data$srpe - 0
data$urpe <- data$urpe - 0.5
data$learning_method <- data$learning_method - 0.5

#data$reward <- scale(data$reward)
#data$confidence <- scale(data$confidence)
#data$srpe <- scale(data$srpe)
#data$urpe <- scale(data$urpe)
#data$learning_method <- scale(data$learning_method)

### formal analysis 1: all the data
## model 1: testing effect
data1 <- copy(data)

if (binary) {
  model <- glmer(data=data1, formula=accuracy~learning_method+reward+confidence+(learning_method+reward|participant), family=binomial)
} else {
  model <- lmer(data=data1, formula=accuracy~learning_method+reward+confidence+(learning_method+reward|participant))
}

HLM_summary(model)
Anova(model, type=3)

## model2: testing (r3=1) vs studying
data2 <- copy(data)
data2 <- data2[data2$reward3==1,]

if (binary) {
  model <- glmer(data=data2, formula=accuracy~learning_method+(learning_method+reward+confidence|participant), family=binomial)
} else {
  model <- lmer(data=data2, formula=accuracy~learning_method+(learning_method+reward+confidence|participant))
}

HLM_summary(model)
Anova(model, type=3)


## model3: testing (r3=0) vs studying
data3 <- copy(data)
data3 <- data3[data3$reward3==0 | data3$test==0,]

if (binary) {
  model <- glmer(data=data3, formula=accuracy~learning_method+(learning_method+reward+confidence|participant), family=binomial)
} else {
  model <- lmer(data=data3, formula=accuracy~learning_method+(learning_method+reward+confidence|participant))
}

HLM_summary(model)
Anova(model, type=3)
mean(data3[data3$test==1, 'accuracy'])
## model4: testing (r3=1) vs testing (r3=0)
data4 <- copy(data)
data4 <- data4[data4$test==1,]

if (binary) {
  model <- glmer(data=data4, formula=accuracy~reward+(learning_method+reward+confidence|participant), family=binomial)
} else {
  model <- lmer(data=data4, formula=accuracy~reward+(learning_method+reward+confidence|participant))
}

HLM_summary(model)
Anova(model, type=3)






data5 <- data[data$reward==-0.5,]


if (binary) {
  model <- glmer(data=data5, formula=accuracy~confidence+(confidence|participant), family=binomial)
} else {
  model <- lmer(data=data5, formula=accuracy~confidence+(confidence|participant))
}

HLM_summary(model)

Anova(model)



