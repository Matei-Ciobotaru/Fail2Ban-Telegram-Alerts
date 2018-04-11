#!/usr/bin/python2.7

# -*- coding: utf-8 -*- #

#Author = Matei Ciobotaru

### THIS SCRIPT IS USED TO COMPARE THE DIFFERENT ###
### CURRENCY VALUES TO RON BY USING THE "ING" DB ###
### AND SEND TELEGRAM NOTIFICATIONS WHEN CERTAIN ###
### CRITERIA ARE MET (LOWEST VAL, KEYWORD ) ###

import argparse
import telegram
import warnings
from ipwhois import IPWhois

#from datetime import datetime as dt
#from datetime import timedelta as td

# ask user for currency and interval

parser = argparse.ArgumentParser(description = 'This script is used to send Telegram' \
											   ' notifications upon a fail2ban IP ban.')
parser.add_argument('-i', '--ip', type=str, nargs=1,
					help='Enter the IP addr. of the attacker.', required=True)
parser.add_argument('-n', '--name', type=str, nargs=1,
                    help='Enter the name of the fail2ban rule triggered.', required=True)
parser.add_argument('-f', '--failures', type=int, nargs=1, 
					help='Enter the number of failed attempts.', required=True)
args=None

try:
	args = parser.parse_args()
except Exception as err:
	parser.print_help(); print err

# clean args

ip = args.ip[0]
name = args.name[0].upper()
failed = args.failures[0]

# bot details (edited for security)


token='YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
chatid = 99999999

# whois list of fields to send in alert msg

fields = ['range', 'name', 'country', 'description', 'emails']

# Find out IP details and store in dictionary for safe keeping

def whois(ip, fields):

	msg = []
	try:
		with warnings.catch_warnings():
	   		 warnings.filterwarnings("ignore", category=UserWarning)
			 info = IPWhois(ip).lookup_whois()['nets'][0]
			 for i in fields:
				msg.append('*' + i.title() + '*: ' + ''.join(info[i]))
				
		return '\n'.join(msg)
	except Exception as err:
		msg_err = '*Issue with IPWhois*:\n%s' % err
		return msg_err


info = whois(ip, fields)

# Connect to Telegram bot

def send_alert(token, chatid):

	bot = telegram.Bot(token=token)

	ID = chatid

# Send static message if the current EUR price is lower that the minimum and the average

	bot.sendMessage(chat_id=ID, parse_mode='Markdown', text='The IP *%s* has just been banned by ' \
			                                 	'Fail2ban after *%d* attempts against *%s*.\n' \
								'*IP info:*\n\n%s' % (ip, failed, name, info))

send_alert(token, chatid)
