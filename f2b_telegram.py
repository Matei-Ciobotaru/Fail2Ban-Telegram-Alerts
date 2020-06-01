#!/usr/bin/python3
# -*- coding: utf-8 -*- #

"""

 This script is used to send Telegram notifications
 along with IP details when certain Fail2Ban rules
 are triggered

 Author: Matei Ciobotaru

"""

import logging
import argparse
from socket import gethostname
import ipwhois
from telegram.bot import Bot
from telegram.error import TelegramError


# Telegram bot information
BOT_TOKEN = 'YOUR_SECRET_BOT_TOKEN'
CHAT_ID = 'YOUR_SECRET_CHAT_ID'

# Enable logging
LOG_FILE = '/var/log/fail2ban.log'

# Match Fail2Ban logging format
logging.basicConfig(filename=LOG_FILE,
                    format='%(asctime)s fail2ban.telegram       ' \
                           '[%(process)s]: %(levelname)-7s %(message)s',
                    level=logging.INFO)


def get_args():
    """
    Get Fail2Ban info as script arguments
    """

    parser = argparse.ArgumentParser(description='This script is used to send ' \
                                                 'Telegram notifications when ' \
                                                 'a Fail2Ban rule is triggered.')

    parser.add_argument('-i', '--ip', type=str,
                        help='The IP address of the client.',
                        required=True)
    parser.add_argument('-n', '--name', type=str,
                        help='The name of the Fail2Ban rule.',
                        required=True)
    parser.add_argument('-f', '--failures', type=int,
                        help='The number of failed attempts.',
                        required=True)

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as arg_err:
        parser.print_help()
        logging.error('Unable to send alert,' \
                      'Fail2Ban argument exception: %s', arg_err)

    return args


def get_ip_info(ip_addr):
    """
    Get WHOIS information about the IP adresss
    """

    ip_info = {}
    fields = ['range', 'name', 'country', 'description', 'emails']

    try:
        info = ipwhois.IPWhois(ip_addr).lookup_whois()

        for field in fields:
            value = info['nets'][0].get(field, 'N/A')
            ip_info[field] = value

    except ipwhois.BaseIpwhoisException as ip_err:
        ip_info['error'] = 'Unable to get IP details ({0})'.format(ip_err)

    return ip_info


def alert_message(ip_addr, rule_name, failures, ip_info):
    """
    Create Telegram alert message
    """

    host_name = gethostname()
    header = 'Host: <b>{0}</b>\n\n'.format(host_name.upper())

    description = 'IP <b>{0}</b> has been banned by ' \
                  'Fail2Ban after <b>{1}</b> failed ' \
                  'attempts against "<b>{2}</b>".\n\n'.format(ip_addr, failures, rule_name.upper())

    message = header + description

    for key, value in ip_info.items():

        if isinstance(value, list):
            value = ', '.join(value)

        message += '<b>{0}:</b> {1}\n'.format(key.title(), value)

    return message


def send_alert(token, chatid, message):
    """
    Send Telegram alert message
    """

    try:
        bot = Bot(token=token)
        bot.send_message(chat_id=chatid, parse_mode='HTML', text=message)
        logging.info('Alert sent successfully via Telegram.')
    except TelegramError as tg_err:
        logging.error('Unable to send alert, Telegram exception: %s', tg_err)


def main():
    """
    Execute script
    """

    args = get_args()
    ip_info = get_ip_info(args.ip)
    message = alert_message(args.ip, args.name, args.failures, ip_info)
    send_alert(BOT_TOKEN, CHAT_ID, message)


if __name__ == '__main__':
    main()
