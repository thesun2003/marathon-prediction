import datetime

def get_data():
	data = [
		{'time': '00:57:02', 'distance': 9.63, 'pace': '5:55', 'gap': '5:32', 'hr': 156},
		{'time': '00:49:34', 'distance': 8.56, 'pace': '5:47', 'gap': '5:28', 'hr': 161},
		{'time': '01:26:13', 'distance': 15.1, 'pace': '5:43', 'gap': '5:21', 'hr': 161},
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

def linear(desired_distance, pace):
	linear_predicted_time = get_time_by_pace(desired_distance, pace)

	return linear_predicted_time

def calculate(distance):
	for run in get_data():
		print "Linear Pace prediction: %s" % linear(distance, get_pace(run['distance'], run['time']))
		print "Linear GAP prediction: %s" % linear(distance, run['gap'])
		# print "Pace: %s" % get_pace(run['distance'], run['time'])
		# print "GAP time: %s" % get_time_by_pace(run['distance'], run['gap'])

calculate(42.195)