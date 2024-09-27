### describe the basic information

### library
library(bruceR)



### load the data
data1 <- read.csv('prolific_export_66bc747bc5f486e3e7c6a97a.csv')
data2 <- read.csv('prolific_export_66bdb6c9319946cefc5483c1.csv')

data <- rbind(data1, data2)
data <- data[data$Status=='APPROVED',]

data$Age <- as.double(data$Age)

Describe(data, file='Describe_subjects')

?aggregate
data = data[data$Sex=='Female',]



