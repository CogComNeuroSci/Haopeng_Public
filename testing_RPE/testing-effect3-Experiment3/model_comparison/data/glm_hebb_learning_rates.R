library(bruceR)
library(lmerTest)
library(car)
library(caret)

data = read.csv('hebbian_model_simulation.csv')

## model 4
# exp 1
data1 <- data[data$model==2,]
data1 <- data1[data1$Experiment==1,]

model <- lm(data=data1, formula=human_test_effect~b)
summary(model)
Anova(model, type=3)


# exp2
data2 <- data[data$model==2,]
data2 <- data2[data2$Experiment==2,]

model <- lm(data=data2, formula=human_test_effect~b)
summary(model)


## model 4
# exp 1
data1 <- data[data$model==3,]
data1 <- data1[data1$Experiment==1,]

model <- lm(data=data1, formula=human_test_effect~b)
summary(model)

# exp2
data2 <- data[data$model==3,]
data2 <- data2[data2$Experiment==2,]

model <- lm(data=data2, formula=model_test_effect~b)
summary(model)
