

"""
baseline = Warfarin clinical dosing algorithm

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
def baseline_alg(age, height, weight, asian, black, mixed_race, enzyme, amiodarone):
	physical = 4.0376 - 0.2546 * age + 0.0118 * height + 0.0134 * weight
	race = - 0.6752 * asian + 0.4060 * black + 0.0443 * mixed_race
	extras = 1.2799 * enzyme - 0.5695 * amiodarone
	return baseline_alg**2


def run_baseline(in_path, out_path):
	with open(in_path,'r') as in_file:
		with open(out_path, 'w') as out_file:
			reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
			writer = csv.writer(out_file, delimiter=',',quotechar='\"')

			for line in reader:
				parts = line.split(",")

				age = 
				height = 
				weight = 
				asian = 
				black = 
				mixed_race = 
				enzyme = 
				amiodarone = 

				dosage = baseline_alg(age, height, weight, asian, black, mixed_race, enzyme, amiodarone)
				out_file.write(str(dosage))











