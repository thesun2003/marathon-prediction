import datetime

degradation_coefficient_low = 1.06
degradation_coefficient_high = 1.1
max_grade = 3

def get_data():
	data = [
		{'time': '00:57:02', 'distance': 9.63, 'pace': '5:55', 'gap': '5:32', 'hr': 156, 'elevation': 214},
		{'time': '00:49:34', 'distance': 8.56, 'pace': '5:47', 'gap': '5:28', 'hr': 161, 'elevation': 169},
		{'time': '01:26:13', 'distance': 15.1, 'pace': '5:43', 'gap': '5:21', 'hr': 161, 'elevation': 307},
	]

	return data

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

def get_ratio():
	return 2.085

def get_pace(distance, time):
	pace = seconds_to_time(time_to_seconds(time) / distance)
	return pace

def get_time_by_pace(distance, pace):
	time = seconds_to_time(distance * time_to_seconds(pace))
	return time

# ------------------------ [ main functions ] ---------------------------------

def linear(desired_distance, pace):
	predicted_time = get_time_by_pace(desired_distance, pace)

	return predicted_time

def riegel(desired_distance, distance, pace, degradation_coefficient):
	# T2 = T1 * (D2 / D1)^C
	time = get_time_by_pace(distance, pace)
	predicted_time = seconds_to_time(time_to_seconds(time) * ( desired_distance / distance ) ** degradation_coefficient)

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
	degradation_coefficient = get_coefficient_by_grade(get_grade(distance, elevation))

	for num, run in enumerate(get_data()):
		print "Run %s" % (num+1)

		print "Linear Pace prediction: %s" % linear(distance, get_pace(run['distance'], run['time']))
		print "Linear GAP prediction: %s" % linear(distance, run['gap'])

		print "Pete Riegel prediction (%s): %s" % (degradation_coefficient_high, riegel(distance, run['distance'], run['pace'], degradation_coefficient_high))
		print "Pete Riegel prediction (%s): %s" % (degradation_coefficient_low, riegel(distance, run['distance'], run['pace'], degradation_coefficient_low))

		print "Pete Riegel GAP prediction (%s): %s" % (degradation_coefficient_high, riegel(distance, run['distance'], run['gap'], degradation_coefficient_high))
		print "Pete Riegel GAP prediction (%s): %s" % (degradation_coefficient_low, riegel(distance, run['distance'], run['gap'], degradation_coefficient_low))

		print "Pete Riegel prediction by elevation grade (%s): %s" % (degradation_coefficient, riegel(distance, run['distance'], run['gap'], degradation_coefficient))

		print "\n"

calculate(42.195, 339)