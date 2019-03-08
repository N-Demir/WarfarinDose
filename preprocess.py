
"""
Original dataset:
5702 entries

Indexes:

PharmGKB Subject ID: 0
Gender: 1
Race: 2
Ethnicity: 3
Age: 4
Height (cm): 5
Weight (kg): 6
Indication for Warfarin Treatment: 7
Comorbidities: 8
Diabetes: 9
Congestive Heart Failure and/or Cardiomyopathy: 10
Valve Replacement: 11
Medications: 12
Aspirin: 13
Acetaminophen or Paracetamol (Tylenol): 14
Was Dose of Acetaminophen or Paracetamol (Tylenol) >1300mg/day: 15
Simvastatin (Zocor): 16
Atorvastatin (Lipitor): 17
Fluvastatin (Lescol): 18
Lovastatin (Mevacor): 19
Pravastatin (Pravachol): 20
Rosuvastatin (Crestor): 21
Cerivastatin (Baycol): 22
Amiodarone (Cordarone): 23
Carbamazepine (Tegretol): 24
Phenytoin (Dilantin): 25
Rifampin or Rifampicin: 26
Sulfonamide Antibiotics: 27
Macrolide Antibiotics: 28
Anti-fungal Azoles: 29
Herbal Medications, Vitamins, Supplements: 30
Target INR: 31
Estimated Target INR Range Based on Indication: 32
Subject Reached Stable Dose of Warfarin: 33
Therapeutic Dose of Warfarin: 34
INR on Reported Therapeutic Dose of Warfarin: 35
Current Smoker: 36
Cyp2C9 genotypes: 37
Genotyped QC Cyp2C9*2: 38
Genotyped QC Cyp2C9*3: 39
Combined QC CYP2C9: 40
VKORC1 genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T: 41
VKORC1 QC genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T: 42
VKORC1 genotype: 497T>G (5808); chr16:31013055; rs2884737; A/C: 43
VKORC1 QC genotype: 497T>G (5808); chr16:31013055; rs2884737; A/C: 44
VKORC1 genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G: 45
VKORC1 QC genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G: 46
VKORC1 genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G: 47
VKORC1 QC genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G: 48
VKORC1 genotype: 3730 G>A (9041); chr16:31009822; rs7294;  A/G: 49
VKORC1 QC genotype: 3730 G>A (9041); chr16:31009822; rs7294;  A/G: 50
VKORC1 genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G: 51
VKORC1 QC genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G: 52
VKORC1 genotype: -4451 C>A (861); Chr16:31018002; rs17880887; A/C: 53
VKORC1 QC genotype: -4451 C>A (861); Chr16:31018002; rs17880887; A/C: 54
CYP2C9 consensus: 55
VKORC1 -1639 consensus: 56
VKORC1 497 consensus: 57
VKORC1 1173 consensus: 58
VKORC1 1542 consensus: 59
VKORC1 3730 consensus: 60
VKORC1 2255 consensus: 61
VKORC1 -4451 consensus: 62
"""

### Removing malformed entries

import csv

DATA_PATH = 'data/'

AGE_IDX = 4
DOSAGE_IDX = 34

def discretize_age(string):
	if string == '10 - 19':
		return 1
	elif string == '20 - 29':
		return 2
	elif string == '30 - 29':
		return 3
	elif string == '40 - 49':
		return 4
	elif string == '50 - 59':
		return 5
	elif string == '60 - 69':
		return 6
	elif string == '70 - 79':
		return 7
	elif string == '80 - 89':
		return 8

def discetize_dosage(string):
	dosage = float(string)

	if dosage < 21:
		return 0
	elif 21 <= dosage and dosage <= 49:
		return 1
	elif 49 < dosage:
		return 2


with open(DATA_PATH + 'warfarin.csv') as csvfile:
	with open(DATA_PATH + 'processed.csv', 'w') as out_file:
		reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
		writer = csv.writer(out_file, delimiter=',',quotechar='\"')

		i = 0
		for idx, row in enumerate(reader):
			if idx == 0:
				continue


			if row[DOSAGE_IDX] != "NA" and row[DOSAGE_IDX] != "":
				row[AGE_IDX] = discretize_age(row[AGE_IDX])
				row[DOSAGE_IDX] = discetize_dosage(row[DOSAGE_IDX])
				writer.writerow(row)

				i += 1

		print("In total got {} rows".format(i))


