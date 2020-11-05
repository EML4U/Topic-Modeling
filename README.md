# Topic-Modeling
Using Latent Dirichlet Allocation (LDA) and other approaches to detect artificially created drift in a newspaper headlines dataset.

#### How to generate the dataset
1. Run get_newspaper.sh in data/ 
   This will download and extract a .tsv of a lager kaggle dataset (https://www.kaggle.com/alvations/old-newspapers)
2. Run the filter_raw_data.py script in the main folder. 
   This will extract the relevant data (newspapers in english language) and write then to the filtered.pickle file, which can then be read and processed by helper methods in data_utils.py
3. Delete the .tsv file (optional)

#### Acknowledgements
The research presented here is funded by the German Federal Ministry of Education and Research
(BMBF) through the project EML4U (01IS19080 A-C)