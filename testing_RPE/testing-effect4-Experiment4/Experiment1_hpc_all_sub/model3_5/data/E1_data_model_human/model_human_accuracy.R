### import the modules
library(lmerTest)
library(bruceR)
library(car)


### load the data
data <- read.csv('accuracy_model_human.csv')


### model
model <- glmer(formula=Human_accuracy~Model_accuracy+(1|Pars), data=data, family=binomial)
HLM_summary(model)
Anova(model, type=3)
