# Dataset of old newspaper article headlines


#### How to generate the dataset
1. Run get_newspaper.sh in data/newspaper/ <br>
   This will download and extract a .tsv of a lager kaggle dataset (https://www.kaggle.com/alvations/old-newspapers)
2. Run the filter_raw_data.py script. <br>
   This will extract the relevant data (newspapers in english language) and write then to the newspaper_dataset.pickle file, which can then be read and processed by helper methods in data_utils.py
3. Delete the .tsv file (optional)