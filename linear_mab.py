import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = 'data/processed.csv'

FEATURE_IDX = [1, 2, 3, 4, 5, 6, 13]
NORMALIZATION_QUANTS = [2, 3, 2, 9, 210, 115, 1]
TRUTH_IDX = 34
ALPHA = .5
K = 3
d = len(FEATURE_IDX)

METRIC_ITERS = 100
NUM_REGRESSES = 2

# Returns |table|, a matrix whose rows represent the feature vectors per each
# patient according to |FEATURE_IDX|. Returns |truth_vals|, a vector whose
# entries represent the correct bucketed dosage per patient.
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


# Returns the index of the optimal action for |datum| given the linear model
# |A| and |b|.
def predict_optimal_action_index(A, b, datum):
    theta = np.tile(np.zeros(d), (K, 1))
    probabilities = np.zeros(K)

    # Calculate upper confidence bounds.
    for a_idx in range(K):
        A_inv = np.linalg.inv(A[a_idx])
        theta[a_idx] = A_inv @ b[a_idx]
        probabilities[a_idx] = theta[a_idx] @ datum + ALPHA * np.sqrt(datum @ A_inv @ datum)

    # Formulate prediction.
    pred_opt_action = probabilities.argmax()
    return pred_opt_action


# Trains a linear model A and b using |data| and |truth_vals|. Returns
# trained linear model and metrics that detail the change in misclassifications
# over patients seen.
def regress(data, truth_vals):
    A = np.tile(np.eye(d), (K, 1, 1))
    b = np.tile(np.zeros(d), (K, 1))

    num_correct_preds = 0
    percent_incorrect_metrics = []
    m, _ = data.shape
    for i in range(m):
        pred_opt_a_idx = predict_optimal_action_index(A, b, data[i])
        correct_pred = int(pred_opt_a_idx == truth_vals[i])
        num_correct_preds += correct_pred

        # Update weights.
        datum = data[i, np.newaxis].T
        A[pred_opt_a_idx] = A[pred_opt_a_idx] + datum @ datum.T
        b[pred_opt_a_idx] = b[pred_opt_a_idx] + correct_pred * data[i]

        # Periodically capture incorrect percentage metrics.
        if i % METRIC_ITERS == 0 or i == m - 1:
            percent_correct = test(A, b, data, truth_vals)
            percent_incorrect_metrics.append((i + 1, 1 - percent_correct))

    regret = m - num_correct_preds
    metrics = regret, percent_incorrect_metrics
    return A, b, metrics


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

    all_percents_incorrect = []
    all_regret = []
    for i in range(NUM_REGRESSES):
        print('Regression ' + str(i + 1) + ' out of ' + str(NUM_REGRESSES) + ' in progress...')
        data, truth_vals = shuffle_data(orig_data, orig_truth_vals)
        A, b, metrics = regress(data, truth_vals)

        regret, percent_incorrect_metrics = metrics
        iterates, percents_incorrect = zip(*percent_incorrect_metrics)
        all_percents_incorrect.append(percents_incorrect)
        all_regret.append(regret)

    print('The average regret is ' + str(np.mean(all_regret)) + '.')
    print('The average accuracy is ' + str(1 - np.mean(np.array(all_percents_incorrect)[:, -1])) + '.')
    sns.tsplot(data = all_percents_incorrect, time = iterates)
    plt.show()
