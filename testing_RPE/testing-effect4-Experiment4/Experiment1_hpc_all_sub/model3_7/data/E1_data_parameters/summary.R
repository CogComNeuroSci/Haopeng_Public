### summarize the parameters

### import
library('bruceR')

### settings
which_data <- 'continuous' # full, binary, continuous

### load the data
formal_data <- read.csv('../E1_original_data/data_preprocess.csv')
all_subs <- unique(formal_data$participant)

data <- read.csv('parameters_best.csv')
data <- data[,c(2, 3, 4, 5)] 

rownames(data) <- all_subs

if (which_data == 'full') {
  print('full data')
} else if (which_data=='binary') {
  subs <- unique(formal_data[formal_data$individual_binary_acc>=0.34, 'participant'])
  data <- data[subs,]
} else {
  subs <- unique(formal_data[formal_data$individual_continuous_acc>=0.34, 'participant'])
  data <- data[subs,]
}

### summary
Describe(data, file='parameters_summary')

