import csv
import numpy as np

DATA_PATH = 'data/processed.csv'

FEATURE_IDX = [5, 6]
NORMALIZATION_QUANTS = [210, 115]
TRUTH_IDX = 34
ALPHA = 2
K = 3
d = len(FEATURE_IDX)

def get_data():
    with open(DATA_PATH, 'r') as data_csv:
        data_reader = csv.reader(data_csv, delimiter = ',', quotechar = '\"')
        num_rows = sum(1 for row in data_reader)
        data_csv.seek(0)

        table = []
        truth_vals = []
        for i, row in enumerate(data_reader):
            try:
                filtered_row = [float(row[FEATURE_IDX[i]]) / NORMALIZATION_QUANTS[i] for i in range(d)]
            except:
                continue

            truth_vals.append(float(row[TRUTH_IDX]))
            table.append(filtered_row)

        table, truth_vals = np.array(table), np.array(truth_vals)
        return table, truth_vals


def regress(data, truth_vals):
    A = np.tile(np.eye(d), (K, 1, 1))
    b = np.tile(np.zeros(d), (K, 1))

    m, _ = data.shape
    for i in range(m):
        theta = np.tile(np.zeros(d), (K, 1))
        probabilities = np.zeros(K)

        for a_idx in range(K):
            A_inv = np.linalg.inv(A[a_idx])
            theta[a_idx] = A_inv @ b[a_idx]
            probabilities[a_idx] = theta[a_idx] @ data[i] + ALPHA * np.sqrt(data[i] @ A_inv @ data[i])

        pred_opt_a = probabilities.argmax()
        correct_pred = int(pred_opt_a == truth_vals[i])

        datum = data[i, np.newaxis].T
        A[pred_opt_a] = A[pred_opt_a] + datum @ datum.T
        b[pred_opt_a] = b[pred_opt_a] + correct_pred * data[i]

    return A, b


if __name__ == '__main__':
    data, truth_vals = get_data()
    A, b = regress(data, truth_vals)
