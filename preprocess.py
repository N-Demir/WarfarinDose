
"""
Original dataset:
5702 entries, of which 42 were malformed (didn't have 66 entries when split)


"""

### Removing malformed entries

DATA_PATH = 'data/'

outFile = open(DATA_PATH + 'removed_malformed.csv','w')

with open(DATA_PATH + 'warfarin.csv','r') as file:
	for line in file:
		parts = line.split(",")
		if len(parts) == 66:
			outFile.write(line)


outFile.close()

### Converting age

with open(DATA_PATH + 'removed_malformed.csv', 'r') as in_file:
	with open(DATA_PATH + 'processed.csv', 'w') as out_file:
		