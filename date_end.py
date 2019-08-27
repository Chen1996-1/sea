import time
date_end = '2019-09-11'
# if time.strptime(date_end,'%Y-%m-%d').__ge__(time.localtime()):
def dat():
	while True:
		now_time = time.localtime()
		if time.strptime(date_end, '%Y-%m-%d').__le__(now_time):
			print('ooooo')
			break
		else:
			print('ok')
			pass
		print('okl')
		time.sleep(5)
		break
dat()
