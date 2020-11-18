# Twitter dataset for the 2020 election in the USA

This dataset consists of roughly 1.2 million tweets addressing the 2020 presidential candidates, Joe Biden and Donald Trump.
Circa 521k of these tweets address Biden specifically, 680k Donald Trump.
The dataset was mined from [here](https://www.kaggle.com/manchunhui/us-election-2020-tweets).

All data except for the tweet text and the time of publishing was discarded and only tweets in english were included in the dataset.
\#'s and @'s as well as all other alphanumerical characters apart from punctuation were removed from the tweets.

#### How to generate the dataset
1. Run get_election_tweets.sh in data/twitter/<br>
   This will download two .csv files of a kaggle dataset (https://www.kaggle.com/manchunhui/us-election-2020-tweets)
2. Run the filter.py script in the data/twitter/ folder. <br>
   This will extract the relevant data and write then to the election_dataset.pickle file. 
   As this process is not parallelized and detecting the language of the tweets is computationally expensive, this may take a while.
3. Delete the .csv files (optional)

Alternatively:<br>Download the computed election_dataset.pickle file from [TODO]().