def get_data():
	data = [
		{'time': '57:02', 'distance': 9.63},
		{'time': '49:34', 'distance': 8.56},
		{'time': '01:26:13', 'distance': 15.1},
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
		result += int(item) * multiply_n(60, k)

	return result

def get_ratio():
	return 2.085

def calculate(distance):
	expectation = 1

	for run in get_data():
		print run['time']
		print time_to_seconds(run['time'])

	# print expectation


calculate(42.195)