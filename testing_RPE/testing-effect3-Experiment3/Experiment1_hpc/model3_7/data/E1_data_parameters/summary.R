### summarize the parameters

### import
library('bruceR')

### load the data
data <- read.csv('parameters_best.csv')
data <- data[,c(2, 3, 4, 5)] 

### summary
Describe(data, file='parameters_summary')

