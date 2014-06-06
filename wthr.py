#!/usr/bin/env python
"""
wthr.py -- Weather Underground command-line client, written in python
"""
# fetching weather
import urllib2, json

# reading parameters
import os, sys, getopt

# read user configs
USR_HOME_DIR = os.path.expanduser("~")
CONFIG_PATH = "%s/.wthrrc" % USR_HOME_DIR
CONFIG_INFO = json.loads(open(CONFIG_PATH, 'r').read())

global JSON
global SHORT
global UNITS

JSON = None
SHORT = False
UNITS = None

def fetch_data(req):
    """
	  fetches JSON Data
	  """
    global JSON, UNITS

	  # metric/imperial
    UNITS = CONFIG_INFO['units']

    if JSON == None:
				# load info from config file
				key = CONFIG_INFO['key']
				loc = CONFIG_INFO['zip']

				# feed KEY, LOC, and dataType (requested API data) into JSON URL
				wu_url = 'http://api.wunderground.com/api/%s/%s/q/%s.json' % \
				         (key, req, loc)

				JSON = json.loads(urllib2.urlopen(wu_url).read())

def sky():
	  """
	  Gets the current sky conditions
	  """
	  fetch_data("conditions")
	  sky_cond = JSON['current_observation']['weather']
	  if SHORT != True:
	      print "Sky Conditions: " + sky_cond
	  else:
	      print sky_cond

def temp_actual():
		"""
		Gets the current temperature
		"""
		fetch_data("conditions")

		if SHORT != True:
		    print "Temperature: " + \
            JSON['current_observation']['temperature_string']
		elif UNITS == "imperial":
		    print JSON['current_observation']['temp_f']
		elif UNITS == "metric":
			  print JSON['current_observation']['temp_c']
		else:
			  print "invalid units string in config file"

def temp_feels_like():
		"""
		Gets the 'feels like' temperature
		"""
		fetch_data("conditions")
		UNITS = (CONFIG_INFO['units'])	#imperial/metric

		if SHORT != True:
		    print "Feels like: " + JSON['current_observation']['feelslike_string']
		elif UNITS == "imperial":
		    print JSON['current_observation']['feelslike_f']
		elif UNITS == "metric":
			  print JSON['current_observation']['feelslike_c']
		else:
			  print "invalid units string in config file"

def location():
		"""
		Gets the specified location
		"""
		fetch_data("conditions")
		state = (JSON['current_observation']['display_location']['state'])
		city = (JSON['current_observation']['display_location']['city'])
		zipcode = (JSON['current_observation']['display_location']['zip'])

		if SHORT != True:
			  print "Specified Location: " + city + ", " + state + " " + zipcode
		else:
			  print city

def forecast():
    """
    Displays current forecast
    """
    fetch_data("forecast")
    UNITS = (CONFIG_INFO['units'])
    forecast = (JSON['forecast']['txt_forecast'])

    if UNITS == 'metric':
        for day in forecast['forecastday']:
            print day['title'] + ': ' + day['fcttext_metric']
    elif UNITS == 'imperial':
        for day in forecast['forecastday']:
            print day['title'] + ': ' + day['fcttext']

def help():
	  """
		Displays help info
		"""
	  pass

def main(argv):
    """
    Main
    """
    global SHORT

    try:
        opts, args = getopt.getopt(argv, "s", \
        ["help", "sky", "temperature", "feels-like", "location", "forecast"])
    except getopt.GetoptError:
    		print "command usage error; review README file"

    if not argv:
    		print "wthr.py"
    		sys.exit(2)
    for opt, arg in opts:
        if opt == "-s":
        	  SHORT = True
        elif opt == "-h":
        	  #help()
        	  print "wthr.py"
        	  sys.exit(0)
        elif opt == "--help":
        	  #help()
        	  print "wthr.py"
        	  sys.exit(0)
        elif opt == "--sky":
        	  sky()
        elif opt == "--temperature":
        	  temp_actual()
        elif opt == "--feels-like":
        	  temp_feels_like()
        elif opt == "--location":
        	  location()
        elif opt == "--forecast":
            forecast()

if __name__ == "__main__":
		main(sys.argv[1:])
