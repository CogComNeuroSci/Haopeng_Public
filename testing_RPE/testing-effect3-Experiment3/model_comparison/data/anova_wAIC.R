### compare the wAIC of models by anova


### import modules
library(bruceR)
?bruceR


### load the data
data <- read.csv('wAIC.csv')


### formal analysis
## experiment 1
data1 <- data[data$Experiment=="Experiment1",]
model <- MANOVA(data=data1, dvs="model1:model7", dvs.pattern="model(.)", within="model")
EMMEANS(model=model, effect="model")

## experiment 2
data2 <- data[data$Experiment=="Experiment2",]
model2 <- MANOVA(data=data2, dvs="model1:model7", dvs.pattern="model(.)", within="model")
EMMEANS(model=model2, effect="model")

TTEST(data2, y=c('model5', 'model7'), paired=TRUE)
