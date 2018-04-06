# -*- coding: utf8 -*-
import datetime
import csv
import json

degradation_coefficient_low = 1.06
degradation_coefficient_high = 1.1
max_grade = 3

def get_data(filename):
	reader = csv.DictReader(open(filename, 'rb'))
	data = []
	for row in reader:
		for key, value in row.iteritems():
			if key in ['distance', 'hr', 'elevation']:
				row[key] = float(row[key])
		data.append(row)

	return data

def save_json_data(filename, data):
	with open(filename, 'w') as fp:
		json.dump(data, fp)

def multiply_n(number, n):
	result = 1
	for i in range(0, n):
		result *= number

	return result

def time_to_seconds(time):
	result = 0
	time_list = time.split(':')

	for k, item in enumerate(reversed(time_list)):
		result += float(item) * multiply_n(60, k)

	return result

def seconds_to_time(number_of_seconds):
	result = str(datetime.timedelta(seconds=number_of_seconds))
	return result

def get_pace(distance, time):
	""" Calculate pace based on distance in kilometers and time as seconds. Returns: seconds """
	pace = (time / distance)
	return pace

def get_time_by_pace(distance, pace):
	""" Calculate time based on distance in kilometers and pace as seconds. Returns: seconds """
	time = (distance * pace)
	return time

# ------------------------ [ main functions ] ---------------------------------

def linear(desired_distance, pace):
	""" Calculate linear time prediction based on distance in kilometers and pace as time string. Returns: seconds """
	predicted_time = get_time_by_pace(desired_distance, time_to_seconds(pace))

	return predicted_time

def riegel(desired_distance, distance, pace, degradation_coefficient):
	""" Calculate time prediction using Pete Riegel formula. Returns: seconds """
	# T2 = T1 * (D2 / D1)^C
	time_seconds = get_time_by_pace(distance, time_to_seconds(pace))
	predicted_time = time_seconds * ( desired_distance / distance ) ** degradation_coefficient

	return predicted_time

def get_coefficient_by_hr(hr):
	return 1

def get_coefficient_by_grade(grade):
	# 3% should be the highest coefficient
	# 0% should be the lowest coefficient

	# 3 = 100% of the (high-low)
	# N = X%
	# X% = (N / 3) * 100
	coefficient_ratio = grade / max_grade
	coefficient_increase = (degradation_coefficient_high - degradation_coefficient_low) * coefficient_ratio

	degradation_coefficient = degradation_coefficient_low + coefficient_increase

	return degradation_coefficient

def get_grade(distance, elevation):
	# grade = elevation(m) / distance(m) * 100
	grade = (elevation / (distance * 1000)) * 100

	return grade

def calculate(distance, elevation):
	prediction_data = []

	degradation_coefficient = get_coefficient_by_grade(get_grade(distance, elevation))

	data = get_data('strava.csv')

	for num, run in enumerate(data):
		print "Run %s" % (num+1)

		LP00 = linear(distance, run['pace'])
		PR0H = riegel(distance, run['distance'], run['pace'], degradation_coefficient_high)
		PRGH = riegel(distance, run['distance'], run['gap'], degradation_coefficient_high)
		PR0M = riegel(distance, run['distance'], run['pace'], degradation_coefficient)
		PRGM = riegel(distance, run['distance'], run['gap'], degradation_coefficient)
		LPG0 = linear(distance, run['gap'])
		PR0L = riegel(distance, run['distance'], run['pace'], degradation_coefficient_low)
		PRGL = riegel(distance, run['distance'], run['gap'], degradation_coefficient_low)		

		prediction_data_value = {
			'LP00': {'time': seconds_to_time(LP00)},
			'PR0H': {'time': seconds_to_time(PR0H)},
			'PRGH': {'time': seconds_to_time(PRGH)},
			'PR0M': {'time': seconds_to_time(PR0M)},
			'PRGM': {'time': seconds_to_time(PRGM)},
			'LPG0': {'time': seconds_to_time(LPG0)},
			'PR0L': {'time': seconds_to_time(PR0L)},
			'PRGL': {'time': seconds_to_time(PRGL)},
		}
		prediction_data.append(prediction_data_value)

		print "Top limit"
		# Linear pace
		print "LP00 prediction: %s" % prediction_data_value['LP00']['time']
		# Pete Riegel (high)
		print "PR0H prediction: %s" % prediction_data_value['PR0H']['time']
		# Pete Riegel GAP (high)
		print "PRGH prediction: %s" % prediction_data_value['PRGH']['time']

		print "Middle limit"
		# Pete Riegel by elevation grade
		print "PR0M prediction: %s" % prediction_data_value['PR0M']['time']
		# Pete Riegel GAP by elevation grade
		print "PRGM prediction: %s" % prediction_data_value['PRGM']['time']

		print "Low limit"
		# Linear GAP
		print "LPG0 prediction: %s" % prediction_data_value['LPG0']['time']
		# Pete Riegel (low)
		print "PR0L prediction: %s" % prediction_data_value['PR0L']['time']
		# Pete Riegel GAP (high)
		print "PRGL prediction: %s" % prediction_data_value['PRGL']['time']

		print "\n"
	save_json_data('output.json', prediction_data)

calculate(42.195, 339)