import csv
import pickle
import datetime


raw_data = []
with open('data/old-newspaper.tsv', 'r') as f:
    for line in csv.reader(f, delimiter='\t'):
        raw_data.append(line)

data = []

for row in raw_data:
    if row[0] != 'English':  # language
        continue
    if not row[1]:  # source
        continue
    if not row[2]:  # date
        continue
    if not row[3]:  # headline
        continue
    date = [int(x) for x in row[2].split('/')]
    row[2] = datetime.date(year=date[0], month=date[1], day=date[2])
    data.append(row[1:])

with open('data/filtered.pickle', 'wb') as f:
    pickle.dump(data, f)
