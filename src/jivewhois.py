#!/usr/bin/python

from os.path import exists, expanduser
import ConfigParser
import pycurl
import json
import argparse
from StringIO import StringIO
import sys
from prettytable import PrettyTable
from datetime import datetime

def error(str):
	print str
	sys.exit(1);

def getLocalTime(tzName):
	tz = timezone(tzName)

	return tz.localize(datetime.now()).strftime("%H:%M")

def readConfig():
	configFile = expanduser("~") + '/.jivewhois.ini'

	if not exists(configFile):
		error("config file does not exist.")

	configParser = ConfigParser.RawConfigParser()
	configParser.read(configFile)

	config = dict()
	config['username'] = configParser.get('authentication', 'username')
	config['password'] = configParser.get('authentication', 'password')
	config['emailDomain'] = configParser.get('authentication', 'emailDomain')
	config['url'] = configParser.get('authentication', 'url')

	return config

config = readConfig()

parser = argparse.ArgumentParser();
parser.add_argument('email')
parser.add_argument('--printJson', '--json', '-j', action = 'store_true')
parser.add_argument('-q', '--quiet', action = 'store_true', help = "Don't print the actual output table")
args = parser.parse_args();

if "@" not in args.email:
	if "emailDomain" in config:
		args.email = args.email + "@" + config['emailDomain']
	else:
		error("That doesn't look like a valid email address, and you don't have an emailDomain in your config")

buf = StringIO()
c = pycurl.Curl();
c.setopt(c.URL, config['url'] + args.email);
c.setopt(c.USERPWD, config['username'] + ":" + config['password'])
c.setopt(c.WRITEDATA, buf)
c.setopt(c.FOLLOWLOCATION, True)
c.perform();

resp = c.getinfo(c.RESPONSE_CODE)

c.close();

if resp != 200:
	error("Response code was: " + str(resp))

body = buf.getvalue();
body = body.replace("throw 'allowIllegalResourceCall is false.';", ""); # wtf

person = json.loads(body);

if args.printJson:
	print json.dumps(person, indent = 4)

if not args.quiet: 
	table = PrettyTable(["key", "value"], header = False)
	table.align["key"] = "r"
	table.align["value"] = "l"
	table.add_row(['Full name', person['displayName']])
	table.add_row(['E-Mail', person['emails'][0]['value']])
	table.add_row(['Job title', person['jive']['profile'][0]['value']])
	table.add_row(['Location', person['location']]);
	table.add_row(['Timezone', person['jive']['timeZone'] + " - " + getLocalTime(person['jive']['timeZone'])])

	table.add_row(["---", "---"])
	for phone in person['phoneNumbers']:
		table.add_row([phone['jive_label'], phone['value']]);

	print table
