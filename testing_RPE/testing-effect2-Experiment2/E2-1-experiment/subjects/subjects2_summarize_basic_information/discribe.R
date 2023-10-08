### describe the basic information

### library
library(bruceR)



### load the data
data_81 <- read.csv('subjects_81.csv')
Describe(data_81, file='Describe_subjects_81')
?aggregate
aggregate(data_81, by=list(Sex), FUN=count)


