import csv
import numpy as np

DATA_PATH = 'data/processed.csv'

FEATURE_IDX = [5, 6]
ALPHA = 2
K = 3
d = len(FEATURE_IDX)

def get_data():
    with open(DATA_PATH, 'r') as data_csv:
        data_reader = csv.reader(data_csv, delimiter = ',', quotechar = '\"')
        num_rows = sum(1 for row in data_reader)
        data_csv.seek(0)

        table = np.zeros((num_rows, len(FEATURE_IDX)))
        for i, row in enumerate(data_reader):
            try:
                row = [float(row[idx]) for idx in FEATURE_IDX]
            except:
                continue
            table[i, :] = np.array(row)
            print(row)

        return table


def regress(data):
    A = np.eye(d)
    b = np.zeros((d, 1))

    m, _ = data.shape
    for i in range(m):
        theta = np.linalg.inv(A) * b

        for a in range(K):
            


if __name__ == '__main__':
    data = get_data()
