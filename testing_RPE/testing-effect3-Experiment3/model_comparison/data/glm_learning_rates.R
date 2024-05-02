library(bruceR)
library(lmerTest)
library(car)
library(caret)
library(effsize)

data = read.csv('model_simulation.csv')

## model 4
# exp 1
data1 <- data[data$model==4,]
data1 <- data1[data1$Experiment==1,]
data1$b <- scale(data1$b)

model <- glm(data=data1, formula=human_test_effect~b)
GLM_summary(model)
Anova(model, type=3)

# exp2
data2 <- data[data$model==4,]
data2 <- data2[data2$Experiment==2,]
data2$b <- scale(data2$b)

model <- glm(data=data2, formula=human_test_effect~b)
GLM_summary(model)
Anova(model, type=3)


## model 5
# exp 1
data1 <- data[data$model==5,]
data1 <- data1[data1$Experiment==1,]
data1$b <- scale(data1$b)

model <- glm(data=data1, formula=human_test_effect~b)
GLM_summary(model)
Anova(model, type=3)

# exp2
data2 <- data[data$model==5,]
data2 <- data2[data2$Experiment==2,]
#data2 <- data2[data2$Pars!=5,]
data2$b <- scale(data2$b)

model <- glm(data=data2, formula=human_test_effect~b)
GLM_summary(model)
Anova(model, type=3)
