# TODO: Start index from 1


"""
Some notes on the algorithm:

Two sets of estimators for each arm:
1) forced-sampling estimates
Since this is trained on iid samples it has convergence guarantees
2) all-sample estimates
Has advantage of being trained on a much larger sample size

Alg:
Uses forced sampling estimator in a pre-processing step to 
select a subset of arms and then uses the all-sample estimator to 
choose the estimated best arm from this subset.

Key: Using forced sampling estimator for pre-processing step
guarantees convergence of the all-sample estimator.

Key: Carefully trading off bias and variance over time by specifying
the regularization paths

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
NUM_REGRESSES = 2

"""
Alg hyperparameters
"""
Q = 1
H = 5
# Forced sample estimate hyperparam
LAMBDA1 = 0.1
# All sample estimate hyperparam
LAMBDA2 = 0.1

# For constructing T_i, which in the alg is an infinite set
MAX_N = 1000

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
Fits a lasso estimator to the old data with hyperparam lambd
Returns the estimate for new data point
"""
def get_lasso_estimate(prev_X, prev_Y, cur_X, lambd):
	clf = linear_model.Lasso(alpha=lambd / 2, fit_intercept=False, max_iter=3000)
	clf.fit(prev_X, prev_Y)
	return clf.predict(cur_X)

"""
Returns an approximation to the infinite set for a given arm i
"""
def get_T_i(i):
	T_i = []
	for n in range(MAX_N):
		for j in range(Q * (i - 1) + 1, Q * i + 1):
			T_i.append((2**n - 1) * NUM_ARMS * Q + j)
	return T_i


"""
Data is matrix vector with rows of feature vector per patient
"""
def lasso_alg(data, truth_vals):
	num_correct_preds = 0
	# percent_incorrect_metrics = []

	m, n = data.shape

	# T_i and S_i
	forced_sample_X = [[] for i in range(NUM_ARMS)]
	forced_sample_Y = [[] for i in range(NUM_ARMS)]
	all_sample_X = [[] for i in range(NUM_ARMS)]
	all_sample_Y = [[] for i in range(NUM_ARMS)]

	lambda2_t = LAMBDA2

	# TODO: Determine T_i, i.e at what t do we force sample an arm
	T = [get_T_i(i) for i in range(1, NUM_ARMS + 1)]

	for t in range(1, m + 1):
		X_t = data[t - 1]
		Y_t = truth_vals[t - 1]
		
		# Check to see first if this t should be a forced sample
		arm_choice = None

		for i, T_i in enumerate(T):
			if t in T_i:
				arm_choice = i
		if arm_choice != None:
			# If the current time t is in forced_sample_times then play it
			forced_sample_X[arm_choice].append(X_t)
			forced_sample_Y[arm_choice].append(-int(arm_choice != truth_vals[t - 1]))
		else:
			# Otherwise
			# 1) Use forced_sample_estimates for pre-processing step:
			#
			# Use the forced sample estimes to find the highest estimated reward
			# achievable across all K arms.
			# 
			# Then select the subset of arms whose rewards are within h/2 of max

			forced_estimated_rewards = np.array([ get_lasso_estimate(forced_sample_X[i], forced_sample_Y[i], [X_t], LAMBDA1) for i in range(NUM_ARMS) ])

			# assert(np.array(forced_estimated_rewards).shape == [1, NUM_ARMS])
			# print(np.array(forced_estimated_rewards).shape)
			forced_estimated_rewards = np.reshape(forced_estimated_rewards, [-1])

			highest_forced_estimated_reward = forced_estimated_rewards.max()

			arms_subset_indices = np.argwhere(forced_estimated_rewards >= highest_forced_estimated_reward - H / 2)

			# 2) Use all_sample estimates to choose the arm with the highest estimated
			# reward within the arms_subset (K^hat)

			arm_choice = np.argmax(np.array([get_lasso_estimate(all_sample_X[i], all_sample_Y[i], [X_t], lambda2_t)[0] for i in range(NUM_ARMS)])[arms_subset_indices])

		# Final step
		lambda2_t = LAMBDA2 * np.sqrt((np.log(t) + np.log(n)) / t)

		all_sample_X[arm_choice].append(X_t)
		all_sample_Y[arm_choice].append(-int(arm_choice != truth_vals[t - 1]))

		# Update our correct metrics
		is_correct_pred = int(arm_choice == truth_vals[t - 1])
		num_correct_preds += is_correct_pred

		# # Periodically capture incorrect percentage metrics.
		# if t % METRIC_ITERS == 0 or t == m - 1:
		#     percent_correct = test(A, b, data, truth_vals)
		#     percent_incorrect_metrics.append((i + 1, 1 - percent_correct))

	accuracy = num_correct_preds / m
	regret = m - num_correct_preds
	return accuracy, regret


# Returns the percentage of correctly classified patients using linear model
# weights and biases |A| and |b|, respectively, on |data|. Correctness is
# determined according to |truth_vals|.
def test(A, b, data, truth_vals):
	num_correct_preds = 0
	m, _ = data.shape
	for i in range(m):
		pred_opt_a = predict_optimal_action_index(A, b, data[i])
		num_correct_preds += int(pred_opt_a == truth_vals[i])

	percent_correct = num_correct_preds / m
	return percent_correct


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
		print('Running lasso alg')
		accuracy, regret = lasso_alg(data, truth_vals)

		accuracies.append(accuracy)
		all_regret.append(regret)

	print('The average regret is ' + str(np.mean(all_regret)) + ' and average accuracy is ' + str(np.mean(accuracies)) + '.')
