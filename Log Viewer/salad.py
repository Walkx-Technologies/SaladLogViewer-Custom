#readme start

# How to get enablesalad to work:
# 1: Go to app.salad.io
# 2: Click on lock near url
# 3: Go to cookies
# 4: Open app-api.salad.io folder
# 5: Copy salad.antiforgery and salad.authentication into a ".env" file like this:
# SALAD_ANTIFORGERY='Your antiforgery code here!'
# SALAD_AUTHENTICATION='Your authentication code here!'
# 6: Make sure salad.py is in same folder as the .env
# 7: Try starting
# 8: ray that it works
# If it works: yay!
# If it doesn't: Contact SharkOfGod#8424 on Discord!

# readme end

# settings begin

import json
import os
import time
import traceback
try:
	with open('colors.json') as f:
		coloors = json.load(f)
	coloorswork = True
	enablesalad = coloors['settings']['enable_salad_balance_tracker']
	title = coloors['settings']['window_title']
	notifthreshold = coloors['settings']['balance_notification_every']
	class custom_colors:
		pass
	for color in coloors['custom_colors'].keys():
		setattr(custom_colors, color, coloors['custom_colors'][color])
except Exception as e:
	print(traceback.format_exc())
	print('colors.json error using defaults')
	coloorswork = False
	enablesalad = False # balance updates in logs
	title = 'fancy salad miner logs'
	notifthreshold = 1 # ping when balance changes by this

# settings end

# try:
# 	from win32gui import GetWindowText, GetForegroundWindow
# 	if GetWindowText(GetForegroundWindow()) == '': # force cmd.exe usage
# 		os.system('start py salad.py')
# 		exit()
# except ModuleNotFoundError:
# 	pass

os.system('title ' + title)
limit = 10
path = os.getenv('APPDATA')
path = path + '/salad/logs/main.log'

class default_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEFAULT = '\033[37;1m'

def fancytype(words, notime=False, colors=[]):
	colorwords = ''
	for color in colors:
		colorwords = eval(color) + colorwords
	if not notime:
		words = ' ' + colorwords + timenow() + ' ' + words
	else:
		words = ' ' + colorwords + words
	strin = ''
	for let in words:
		strin = strin + let
		print(strin, end='\r')
		time.sleep(0.0078125)
	print(words + default_colors.ENDC + default_colors.DEFAULT)

with open(path) as f:
	oldest = f.readlines()[-1]

from datetime import datetime

if enablesalad:
	try:
		import requests
		from dotenv import load_dotenv
		load_dotenv()
		from win10toast import ToastNotifier
		toaster = ToastNotifier()
		salad_antiforgery = os.getenv('SALAD_ANTIFORGERY')
		salad_authentication = os.getenv('SALAD_AUTHENTICATION')
		if salad_authentication is not None and salad_antiforgery is not None:
			print('[live logs] Live logs are ready!')
		else:
			print('[live logs] Error, please check your .env file!')
			os.system('pause')
			exit()

	except ModuleNotFoundError:
		print('[live logs] Modules not found, press any key to install!')
		os.system('pause')
		os.system('pip install -r requirements.txt --user')
		time.sleep(5)
		import requests
		from dotenv import load_dotenv
		load_dotenv()
		from win10toast import ToastNotifier
		toaster = ToastNotifier()
		salad_antiforgery = os.getenv('SALAD_ANTIFORGERY')
		salad_authentication = os.getenv('SALAD_AUTHENTICATION')

	cookie = {
		"Salad.Antiforgery": salad_antiforgery,
		"Salad.Authentication": salad_authentication
	}
	try:
		r = requests.get(url = 'https://app-api.salad.io/api/v1/profile/balance', cookies = cookie)
		if r.status_code != 200:
			print(f'{default_colors.WARNING}{default_colors.BOLD}[api] Error! Something went wrong with the salad api! Probably a 401... Check the auth tokens in the .env file{default_colors.ENDC}')
			os.system('pause')
		jason = r.json()
		oldbalance = jason['currentBalance']
		pongbal = oldbalance
		e = 0
	except requests.ConnectionError:
		print(f'{default_colors.WARNING}{default_colors.BOLD}Bad error! Either salad is down or the caveman (SharOfGod) running this doesnt have internet{default_colors.ENDC}')
		enablesalad = False

def timenow():
	return '[' + str(datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]) + ']'

def updatever(): # absolutely not copy pasted from my bots code
	if os.path.isfile('noupdate.txt'):
		fancytype('[update] noupdate.txt found! Updates cancelled...', colors=['default_colors.FAIL'])
		return
	try:
		import requests
	except ModuleNotFoundError:
		fancytype('[update] requests api is required to update!')
		return
	try:
		with open('version.txt') as f:
			ver = int(f.read())
		chver = requests.get(url = 'http://api.shruc.ml/saladlog/version', params = {})
		chver = chver.text.replace('\n', '')
		chver = chver.replace('"', '')
		if int(chver) > ver:
			fancytype('[update] Update available! press any key or create noupdate.txt and restart')
			os.system('pause')
			time.sleep(1)
			with open('temp.py', 'w+') as f:
				file = __file__.replace('\\', '/')
				print(file)
				comd = 'print("Hold on im updating myself...")\nimport time\nimport requests\nr = requests.get(url = "http://api.shruc.ml/saladlog/download", params = {})\nwith open("' + file + '", "w+") as f:\n\tf.write(r.text)\nr = requests.get(url = "http://api.shruc.ml/saladlog/version", params = {})\nwith open("version.txt", "w+") as f:\n\tf.write("'+ chver +'")\ntime.sleep(1)\nimport os\nos.system(\'start cmd /c "del temp.py & start py ' + file + '\')'
				f.write(comd)
			print('You can close this window')
			os.system('start cmd /c py temp.py')
			os.system('exit')
			exit()
		else:
			fancytype('[update] Live logs are up to date!')
	except requests.ConnectionError as e:
		print('website went poo >:C')
	except Exception as e:
		print(str(e))
		print('If this is ur first time running SaladLogViewer ignore this!')
		with open('version.txt', 'w+') as f:
			f.write('1')

updatever()
while True:
	time.sleep(0.5)
	matches = False
	try:
		with open(path) as f:
			line = f.readlines()
			for i in range(1, limit+1):
				lien = line[-i].replace('\n', '')
				#print('-------------')
				#print(lien, i)
				#print(oldest)
				if lien == oldest:
					matches = True
					oldest = line[-1].replace('\n', '')
					num = i
					break
			if not matches:
				oldest = line[-1].replace('\n', '')
				num = limit+1
			for i in reversed(range(1, num)):
				lien = line[-i].replace('\n', '')
				if not coloorswork:
					if 'ETH share found!' in lien:
						fancytype(f'{lien}', notime=True, colors=['default_colors.OKGREEN', 'default_colors.BOLD'])
					elif 'GPU' in lien:
						fancytype(f'{lien}', notime=True, colors=['default_colors.OKBLUE', 'default_colors.BOLD'])
					else:
						fancytype(lien, notime=True)
				else:
					found = False
					for blah in coloors['custom_text'].keys():
						if blah in lien:
							fancytype(f'{lien}', notime=True, colors=coloors['custom_text'][blah])
							found = True
							break
					if not found:
						fancytype(lien, notime=True)

		if enablesalad:
			if e >= 1:
				fancytype('[salad] checking balance')
				cookie = {
					"Salad.Antiforgery": salad_antiforgery,
					"Salad.Authentication": salad_authentication
				}
				r = requests.get(url = 'https://app-api.salad.io/api/v1/profile/balance', cookies = cookie)
				print(r.status_code)
				if r.status_code != 200:
					print(f'{default_colors.WARNING}{default_colors.BOLD}[api] Error! Something went wrong with the salad api! Probably a 401... Check the auth tokens in the .env file{default_colors.ENDC}')
					continue
				jason = r.json()
				if jason['currentBalance'] > oldbalance:
					diff = jason['currentBalance'] - oldbalance
					oldbalance = jason['currentBalance']
					fancytype('[salad] Balance increased by $' + str(diff), colors=['default_colors.OKGREEN', 'default_colors.BOLD', 'default_colors.UNDERLINE'])
					fancytype('[salad] New salad balance: $' + str(jason['currentBalance']), colors=['default_colors.OKGREEN', 'default_colors.BOLD', 'default_colors.UNDERLINE'])
					if jason['currentBalance'] - pongbal > notifthreshold:
						fancytype('[salad] Sending desktop notification', colors=['default_colors.OKGREEN', 'default_colors.BOLD', 'default_colors.UNDERLINE'])
						toaster.show_toast("salad log thing", "balance increased by " + str(jason['currentBalance'] - pongbal) + ' since last notification!', threaded=True, icon_path=None, duration=3)
						pongbal = jason['currentBalance']
				else:
					fancytype('[salad] Balance didnt change :c')
				e = 0
			else:
				e += 1
	except Exception as o:
		print(traceback.format_exc())
		print(f'{default_colors.WARNING}{default_colors.BOLD}Bad error!{default_colors.ENDC}{default_colors.DEFAULT}', str(o))
