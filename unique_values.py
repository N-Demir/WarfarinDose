import csv

DATA_PATH = 'data/'

unique_values = set()

with open(DATA_PATH + 'warfarin.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='\"')

	for row in reader:
		unique_values.add(row[8])

print('Unique values were: {}'.format(unique_values))