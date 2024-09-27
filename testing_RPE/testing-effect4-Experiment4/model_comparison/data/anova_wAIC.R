#############################################
### compare the wAIC of models by anova #####
#############################################

### import modules
library(bruceR)
library(car)

### load the data
data <- read.csv('wAIC.csv')
colnames(data) <- c('index', 'Model1', 'Model2', 'Model3', 'Model4', 'Model5', 'Model6', 'Model7', 'Experiment')

### formal analysis
## experiment 1
data1 <- data[data$Experiment=="Experiment1",]
model <- MANOVA(data=data1, dvs="Model1:Model7", dvs.pattern="Model(.)", within=c("Model"))
EMMEANS(model=model, effect="Model")


## experiment 2
data2 <- data[data$Experiment=="Experiment2",]
model2 <- MANOVA(data=data2, dvs="Model1:Model7", dvs.pattern="Model(.)", within="Model")
EMMEANS(model=model2, effect="model")

TTEST(data2, y=c('model5', 'model7'), paired=TRUE)

