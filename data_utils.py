import pickle
from enum import Enum
import random

newspaper_datafile = 'data/newspaper/newspaper_dataset.pickle'

city_dict = {  # amount of headlines
    'chicago': ['suntimes.com', 'chicagotribune.com'],  # 31316
    'new york': ['nypostonline.com', 'nydailynews.com', 'wsj.com'],  # 30123
    'san fransisco': ['sfgate.com', 'siliconvalley.com', 'mercurynews.com'],  # 66640
    'atlanta': ['accessatlanta.com', 'ajc.com']  # 11377
}


class DataReader:

    def __init__(self):
        self.data = None

    def read_data(self, file_name=newspaper_datafile):
        with open(file_name, 'rb') as f:
            self.data = pickle.load(f)

    def get_data_most_prominent_papers(self):
        """
            :return: Returns a tuple of the headlines of the two most prominent papers.

            Expected similarities: Within headlines of a single newspaper; Authors
            Expected difference: Author style, regional differences, political stance

            Shape: tuple with two lists of headline strings
        """
        if self.data is None:
            self.read_data()
        counts = [(website, len([i for i in self.data if i[0] == website])) for website in
                  set([x[0] for x in self.data])]
        papers = sorted(counts, key=lambda imp: imp[1])[-2:]
        headlines = [sorted([row[1:] for row in self.data if row[0] == p[0]], key=lambda x: x[1]) for p in papers]
        return [x[-1] for x in headlines[0]], [x[-1] for x in headlines[1]]

    def get_data_time(self):
        """
            :return: Returns all data, ordered by time.

            Expected similarities: Within the same day or two, (inter-)national headlines
            Expected difference: Between days

            Shape: list of lists with date and headline
            """
        if self.data is None:
            self.read_data()
        return [x[1:] for x in sorted(self.data, key=lambda x: x[1])]

    def get_data_region(self):
        """
            :return: Returns data sorted by region and time.

            Expected similarities: Coverage of similar events in a given region
            Expected differences: Coverage oof different events on between regions

            Shape: dict with entries of time-sorted lists of date and headline pairs
        """
        if self.data is None:
            self.read_data()
        ret = {region: [] for region in city_dict}
        for region in city_dict:
            region_data = [x for x in self.data if x[0] in city_dict[region]]
            ret[region] = sorted(region_data, key=lambda x: x[1])
        return ret


class DataCombiner:
    class TransitionMethods(Enum):
        LINEAR = 1
        SIN = 2
        EXP = 3

    def __init__(self,
                 split_point=0.5,
                 balance_classes=True,
                 transition_method=TransitionMethods.LINEAR,
                 transition_length=(2 * 0.2),
                 start_split=0.8,
                 end_split=0.2,
                 random_seed=None
                 ):
        self.split_point = split_point
        self.balance_classes = balance_classes
        self.transition_method = transition_method
        self.transition_length = transition_length
        self.start_split = start_split
        self.end_split = end_split
        if random_seed:
            random.seed(random_seed)

    def prepare_data(self, data):
        """

        :param data: a tuple of two lists. They will be mixed according to the parameters given in the constructor.
        :return: a single list of datapoints of the same form as given in the two lists in data
        """
        assert len(data) == 2  # data must be a tuple of len 2
        assert len(data[0]) == len(data[1])  # both lists must have the same length

        starting_length = (self.split_point - self.transition_length/2) * len(data[0])
        starting_length = int(starting_length)  # amount of data points in the first batch

        ending_length = (1-(self.split_point + self.transition_length/2)) * len(data[0])
        ending_length = int(ending_length)  # amount of data points in the last batch

        data_prep = []  # the final list
        for point in range(starting_length):  # add the first batch
            if random.random() < self.start_split:
                data_prep.append(data[0][point])
            else:
                data_prep.append(data[1][point])

        # add the middle batch
        for point in range(starting_length, len(data[0]) - ending_length):  # add the first batch
            if random.random() < self.transition_function(float(point)/len(data)):
                data_prep.append(data[0][point])
            else:
                data_prep.append(data[1][point])

        for point in range(len(data[0]) - ending_length, len(data[0])):  # add the last batch
            if random.random() < self.end_split:
                data_prep.append(data[0][point])
            else:
                data_prep.append(data[1][point])

        return data_prep

    def transition_function(self, x):
        if self.transition_method == DataCombiner.TransitionMethods.LINEAR:
            return self.transition_linear(x)
        elif self.transition_method == DataCombiner.TransitionMethods.SIN:
            return self.transition_sin(x)
        elif self.transition_method == DataCombiner.TransitionMethods.EXP:
            return self.transition_exp(x)

    def transition_linear(self, x):
        start_trans = self.split_point - self.transition_length/2
        end_trans = self.split_point + self.transition_length/2
        factor = (x-start_trans) / (end_trans-start_trans)
        value = self.start_split + (self.end_split-self.start_split)*factor
        return value

    def transition_sin(self, x):
        return 0.0

    def transition_exp(self, x):
        return 0.0
