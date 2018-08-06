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
import logging as log
import subprocess as sp

# Enable logging

log_file = '/var/log/fail2ban.log'

# Match Fail2Ban log format

log.basicConfig(filename=log_file,
                format='%(asctime)s fail2ban.telegram %(pid)14s %(levelname)-7s %(message)s',level=log.INFO)

# set arguments for Fail2Ban variables

parser = argparse.ArgumentParser(description = 'This script is used to send Telegram ' \
						'notifications when a Fail2Ban rule is triggered.')

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

# get fai2ban server PID for log

pid_no = sp.check_output(['pgrep', '-o', 'fail2ban-server']).split('\n')[0]

# get hostname for alert message

host = gethostname().upper()

# IntruderAlertBot details 

token='583669346:AAGuos_nrvBQfVBWaoPrz6v6Tmk2N0y0uW8'
chatid = 425596683

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
				msg.append('<b>' + i.title() + '</b>: ' + str(info[i]).translate(None, '[]\''))
				
		return '\n'.join(msg)
	except Exception as err:
		msg_err = '<b>Issue with IPWhois</b>:\n%s' % err
		return msg_err

# Connect to Telegram bot

def send_alert(token, chatid):

	bot = Bot(token=token)

	ID = chatid

# Send static message if certain Fail2ban rule is triggered

	bot.sendMessage(chat_id=ID, parse_mode='HTML', text='Host <b>%s</b>:\n\nThe IP <b>%s</b> has just been banned by ' \
			                        	    'Fail2ban after <b>%d</b> attempts against <b>%s</b>.\n' \
							    '<b>IP info:</b>\n\n%s' % (host, ip, failed, name, info))

# Error Handling
# Log directly fo Fail2Ban server log

try:
	info = whois(ip, fields)
	send_alert(token, chatid)
	log.info("Alert sent successfully via Telegram.", extra={'pid': '[%s]:' % pid_no})
except TelegramError as tg_err:
	log.error("Unable to send alert, Telegram error: %s" % tg_err, extra={'pid': '[%s]:' % pid_no})
except Exception as err:
	log.error("Unable to send alert via Telegram: %s " % err, extra={'pid': '[%s]:' % pid_no})
