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
data1 <- read.csv('data_preprocess_e1.csv')
data1['Experiment'] <- 1
data1['feedback'] <- 1
data1['interval'] <- 0
data1$participant <- data1$participant + 100
data2 <- read.csv('data_preprocess_e2.csv')
data2['Experiment'] <- 2
data2['feedback'] <- 1
data2['interval'] <- 1
data2$participant <- data2$participant + 200
data3 <- read.csv('data_preprocess.csv')
data3['Experiment'] <- 3
data3['feedback'] <- 0
data3['interval'] <- 0
data3$participant <- data3$participant + 300
## delete some useless columns
data2 <- data2[,!names(data2) %in% c('prolific_id', 'swahili_knowledge', 'previous_subject')]
## combine the data
data <- rbind(data1, data2)
data <- rbind(data, data3)

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
data$feedback <- data$feedback - 0.5

#data$reward <- scale(data$reward)
#data$confidence <- scale(data$confidence)
#data$srpe <- scale(data$srpe)
#data$urpe <- scale(data$urpe)
#data$learning_method <- scale(data$learning_method)


### formal analysis: feedback * test
data_formal <- copy(data)

if (binary) {
  model <- glmer(data=data_formal, formula=accuracy~feedback*learning_method+reward+confidence+(learning_method+reward+confidence|participant), family=binomial)
  null_model <- glmer(data=data_formal, formula=accuracy~feedback+learning_method+reward+confidence+(learning_method+reward+confidence|participant), family=binomial)
} else {
  model <- lmer(data=data_formal, formula=accuracy~feedback*learning_method+reward+confidence+(learning_method+reward+confidence|participant))
  null_model <- lmer(data=data_formal, formula=accuracy~feedback+learning_method+reward+confidence+(learning_method+reward+confidence|participant))
}

# omnibus test
anova(null_model, model)

HLM_summary(model)
Anova(model)

### formal analysis: all Experiments
## Interaction
data_formal <- data[data$test==1,]

if (binary) {
  model <- glmer(data=data_formal, formula=accuracy~reward*feedback+(reward|participant), family=binomial)
} else {
  model <- lmer(data=data_formal, formula=accuracy~reward*feedback+(reward|participant))
}

HLM_summary(model)
Anova(model, type=3)

## simple effect: correct test
data_simple <- data_formal[data_formal$reward==0.5,]

if (binary) {
  model <- glmer(data=data_simple, formula=accuracy~feedback+(1|participant), family=binomial)
} else {
  model <- lmer(data=data_simple, formula=accuracy~feedback+(1|participant))
}

HLM_summary(model)
Anova(model, type=3)

## simple effect: incorrect test
data_simple <- data_formal[data_formal$reward==-0.5,]

if (binary) {
  model <- glmer(data=data_simple, formula=accuracy~feedback+(1|participant), family=binomial)
} else {
  model <- lmer(data=data_simple, formula=accuracy~feedback+(1|participant))
}

HLM_summary(model)
Anova(model, type=3)



### formal analysis: Experiments 1 and 3
## Interaction
data_formal <- data[data$Experiment!=2,]
data_formal <- data_formal[data_formal$test==1,]

if (binary) {
  model <- glmer(data=data_formal, formula=accuracy~reward*feedback+(reward|participant), family=binomial)
} else {
  model <- lmer(data=data_formal, formula=accuracy~reward*feedback+(reward|participant))
}

HLM_summary(model)
Anova(model, type=3)

## simple effect: correct test
data_simple <- data_formal[data_formal$reward==0.5,]

if (binary) {
  model <- glmer(data=data_simple, formula=accuracy~feedback+(1|participant), family=binomial)
} else {
  model <- lmer(data=data_simple, formula=accuracy~feedback+(1|participant))
}

HLM_summary(model)
Anova(model, type=3)

## simple effect: incorrect test
data_simple <- data_formal[data_formal$reward==-0.5,]

if (binary) {
  model <- glmer(data=data_simple, formula=accuracy~feedback+(1|participant), family=binomial)
} else {
  model <- lmer(data=data_simple, formula=accuracy~feedback+(1|participant))
}

HLM_summary(model)
Anova(model, type=3)



### formal analysis: reward * test in Exp 1 and 2
## Interaction
data_formal <- data[data$Experiment!=3,]

if (binary) {
  model <- glmer(data=data_formal, formula=accuracy~reward:learning_method+(reward+learning_method|participant), family=binomial)
} else {
  model <- lmer(data=data_formal, formula=accuracy~reward:learning_method+(reward+learning_method|participant))
}

HLM_summary(model)
Anova(model, type=3)
