#!/usr/bin/python2.7

# -*- coding: utf-8 -*- #

# Author = Matei Ciobotaru

"""

     This script is used to send 
    Telegram notifications along 
    with IP details when certain 
    Fail2Ban rules are triggered

"""

import argparse
from telegram.bot import Bot
from telegram.error import TelegramError
import warnings
from ipwhois import IPWhois
from socket import gethostname

# set arguments for Fail2Ban variables

parser = argparse.ArgumentParser(description = 'This script is used to send Telegram' \
											   ' notifications when a Fail2Ban rule is triggered.')
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

# get hostname for alert message

host = gethostname().upper()

# Telegram bot details, add your token & chatid below
# Details can be found here: https://core.telegram.org/bots 

token='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
chatid = 999999999

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
				msg.append('*' + i.title() + '*: ' + str(info[i]).translate(None, '[]\''))
				
		return '\n'.join(msg)
	except Exception as err:
		msg_err = '*Issue with IPWhois*:\n%s' % err
		return msg_err

# Connect to Telegram bot

def send_alert(token, chatid):

	bot = Bot(token=token)

	ID = chatid

# Send static message if certain Fail2ban rule is triggered

	bot.sendMessage(chat_id=ID, parse_mode='Markdown', text='Host *%s*:\n\nThe IP *%s* has just been banned by ' \
			                                 	'Fail2ban after *%d* attempts against *%s*.\n' \
								'*IP info:*\n\n%s' % (host, ip, failed, name, info))

# Error Handling

try:
    info = whois(ip, fields)
    send_alert(token, chatid)
except TelegramError as tg_err:
    print("ERROR: Unable to send Telegram message: %s" % tg_err)
except Exception as err:
    print("ERROR: %s " % err)
