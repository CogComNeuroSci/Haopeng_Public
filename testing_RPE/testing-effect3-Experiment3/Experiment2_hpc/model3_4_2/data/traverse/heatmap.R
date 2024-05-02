############################################
######heat map: p, b, testing effect########
############################################

## import modules
library(lmerTest)
library(car)
library(bruceR)

heat_data <- data.frame(p=c(0), b=c(0), dif=c(0), effect=c(0))

## formal analysis
row = 1
for (p in seq(0, 1, by = 0.1)) {
  for (b in seq(0, 1, by = 0.1)) {
    data <- read.csv(sprintf('data/traverse_p%.1f%.1f.csv', p, b))
    #data <- read.csv('data/traverse_p0.00.0.csv')
    
    dif <- mean(data[data$TvS==1, 'Model_accuracy']) - mean(data[data$TvS==0, 'Model_accuracy'])
    
    
    ## lmer
    #model <- lmer(data=data, formula=Model_accuracy~TvS+(1|Pars))
    #results <- Anova(model, type=3)
    #effect <- results[2, 1]
    
    heat_data[row, 1] = p
    heat_data[row, 2] = b
    heat_data[row, 3] = dif
    #heat_data[row, 4] = effect
    row = row + 1
    print(row)
  }
}

## save the heat data
?write.table
write.table(heat_data, 'heat_data/heat_data.csv', row.names=FALSE, sep=',')


