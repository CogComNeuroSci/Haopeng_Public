Preprocessing of experiment 2

Preprocessing before the formal data analysis

"preprocess.py"
This is the first preprocessing stratagy, which is also the stratagy used in the paper. In this preprocessing, we did not delete the word pairs that were correctly recognized in phase 4, but incorrectly recognized in phase 5.

"preprocess_stratagy2.py"
This is the second preprocessing stratagy. In this preprocessing, we delete the word pairs that were correctly recognized in phase 4, but incorrectly recognized in phase 5.

"plot.py"
In this script, we draw the distribution of trials in each experimental condition. Besides, we try to use a different stratagy (delete high confidence trials in phase 2) to filter the pre-learning from phase 1, and draw a figure to show the final behavioral pattern. 

"data_all.csv"
This is the data of all participants. Some participants were deleted after preprocessing (know Swahili...).

"data_preprocess.csv"
This is the preprocessed data of all participants

"data_preprocess_higher_than_0.34.csv"
This is the preprocessed data of participants whose accuracies are higher than 34%.

"data1-first-day"
raw data of the first day

"data2-second-day"
raw data of the second day

