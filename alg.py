
import csv

DOSAGE_IDX = 34

"""
Warfarin clinical dosing algorithm

4.0376
-
0.2546 x
Age in decades
+
0.0118 x
Height in cm
+
0.0134 x
Weight in kg
-
0.6752 x
Asian race
+
0.4060 x
Black or African American
+
0.0443 x
Missing or Mixed race
+
1.2799 x
Enzyme inducer status
-
0.5695 x
Amiodarone status
  =
 Square root of weekly warfarin dose**

"""
def clinical_alg(age, height, weight, asian, black, mixed_race, enzyme, amiodarone):
	physical = 4.0376 - 0.2546 * age + 0.0118 * height + 0.0134 * weight
	race = - 0.6752 * asian + 0.4060 * black + 0.0443 * mixed_race
	extras = 1.2799 * enzyme - 0.5695 * amiodarone
	total = physical + race + extras
	return total**2

def discetize_dosage(dosage):
	if dosage < 21:
		return 0
	elif 21 <= dosage and dosage <= 49:
		return 1
	elif 49 < dosage:
		return 2

def run_clinical_alg(in_path, out_path):
	with open(in_path,'r') as in_file:
		with open(out_path, 'w') as out_file:
			reader = csv.reader(in_file, delimiter=',', quotechar='\"')

			for row in reader:
				if row[4] == 'na' or row[4] == "" or row[5] == 'na' or row[5] == "" or row[6] == 'na' or row[6] == "":
					out_file.write("1" + "\n")
					continue

				medications = row[12].split('; ')

				age = float(row[4])
				height = float(row[5])
				weight = float(row[6])
				asian = 1 if row[2] == 'Asian' else 0
				black = 1 if row[2] == 'Black or African American' else 0
				mixed_race = 1 if row[2] == 'Unknown' else 0
				enzyme = 1 if 'carbamazepine' in medications or 'phenytoin' in medications or 'rifampin' in medications or 'rifampicin' in medications else 0
				amiodarone = 1 if 'amiodarone' in medications else 0

				dosage = clinical_alg(age, height, weight, asian, black, mixed_race, enzyme, amiodarone)
				out_file.write(str(discetize_dosage(dosage)) + "\n")

def run_fixed_dose(in_path, out_path):
	with open(in_path,'r') as in_file:
		with open(out_path, 'w') as out_file:
			for line in in_file:
				out_file.write("1\n")

def get_performance(processed_path, values_path):
	with open(processed_path,'r') as processed_file:
		with open(values_path, 'r') as values_file:
			reader = csv.reader(processed_file, delimiter=',', quotechar='\"')
			values = values_file.readlines()

			count = 0.0
			correct = 0.0
			for row_idx, row in enumerate(reader):
				count += 1.0

				if row[DOSAGE_IDX] == values[row_idx].strip("\n"):
					correct += 1.0

			return correct / count

def main():
	run_clinical_alg('data/processed.csv', 'output/clinical_alg.csv')
	run_fixed_dose('data/processed.csv', 'output/fixed_dose.csv')

	clinical_alg_performance = get_performance('data/processed.csv', 'output/clinical_alg.csv')
	fixed_dose_performance = get_performance('data/processed.csv', 'output/fixed_dose.csv')

	print('Clinical performance: {} and Fixed dose performance: {}'.format(clinical_alg_performance, fixed_dose_performance))


if __name__ == '__main__':
	main()
