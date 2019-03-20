"""
Based on paper found here: http://proceedings.mlr.press/v28/agrawal13.pdf

"""

import csv
import numpy as np
from sklearn import linear_model

DATA_PATH = 'data/processed.csv'

FEATURE_IDX = [1, 2, 3, 4, 5, 6, 13]
NORMALIZATION_QUANTS = [2, 3, 2, 9, 210, 115, 1]
TRUTH_IDX = 34
d = len(FEATURE_IDX)
NUM_ARMS = 3
NUM_REGRESSES = 10

"""
Alg hyperparameters
"""
# epsilon = 0.5 # Between 0 and 1
# delta = 0.1 # No clue what this should be
# R = 0 #No clue what this should be
# v = R * np.sqrt(24 / epsilon * d * np.log(1 / delta))
v_sqrd = 0.01


"""
Returns |table|, a matrix whose rows represent the feature vectors per each
patient according to |FEATURE_IDX|. Returns |truth_vals|, a vector whose
entries represent the correct bucketed dosage per patient.
"""
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

"""
Data is matrix vector with rows of feature vector per patient
"""
def thompson_alg(data, truth_vals):
	num_correct_preds = 0

	m, n = data.shape

	# Keep separate parameters for each arm
	B_s = [np.eye(d) for _ in range(NUM_ARMS)]
	mu_hat_s = [np.zeros((d, 1)) for _ in range(NUM_ARMS)]
	f_s = [np.zeros((d, 1)) for _ in range(NUM_ARMS)]

	for t in range(1, m + 1):
		X_t = data[t - 1]
		Y_t = truth_vals[t - 1]

		X_t = np.reshape(X_t, (-1, 1))

		mu_hat_t_s = [ np.random.multivariate_normal(mu_hat_s[i].reshape(-1), v_sqrd * np.linalg.inv(B_s[i])) for i in range(NUM_ARMS) ]

		arm_choice = np.argmax([ X_t.T @ mu_hat_t for mu_hat_t in mu_hat_t_s ])

		reward = -int(arm_choice != truth_vals[t - 1])
		num_correct_preds += 1 + reward

		B_s[arm_choice] += X_t @ X_t.T
		f_s[arm_choice] += X_t * reward
		mu_hat_s[arm_choice] = np.linalg.inv(B_s[arm_choice]) @ f_s[arm_choice]


	accuracy = num_correct_preds / m
	regret = m - num_correct_preds
	return accuracy, regret

# Returns shuffled data |data| and |truth_vals|.
def shuffle_data(data, truth_vals):
	combined_data = np.hstack((data, truth_vals[np.newaxis].T))
	np.random.shuffle(combined_data)
	shuffled_data, shuffled_truth_vals = combined_data[:, 0:-1], combined_data[:, -1]
	return shuffled_data, shuffled_truth_vals


if __name__ == '__main__':
	orig_data, orig_truth_vals = get_data()

	accuracies = []
	all_regret = []
	for i in range(NUM_REGRESSES):
		print('Regression ' + str(i + 1) + ' out of ' + str(NUM_REGRESSES) + ' in progress...')
		data, truth_vals = shuffle_data(orig_data, orig_truth_vals)
		print('Running thompson sampling alg')
		accuracy, regret = thompson_alg(data, truth_vals)

		accuracies.append(accuracy)
		all_regret.append(regret)

	print('The average regret is ' + str(np.mean(all_regret)) + ' and average accuracy is ' + str(np.mean(accuracies)) + '.')
