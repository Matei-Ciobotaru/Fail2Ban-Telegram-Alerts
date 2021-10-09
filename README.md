# Sending Fail2Ban alerts via Telegram

 A simple python script I wrote so I may send [Fail2Ban](https://www.fail2ban.org/wiki/index.php/Main_Page) alerts via Telegram.

## Python Libraries

 You will require the [python-telegram-bot](https://python-telegram-bot.org/) library to use Telegram and the [ipwhois](https://pypi.org/project/ipwhois/) library to query details of the IP.

  ```bash
     # pip install python-telegram-bot ipwhois
  ```

## Telegram Bot

 You will need to create a Telegram bot and edit the python script to add your personal token and chatid.

 Details on how to create a bot [here](https://core.telegram.org/bots#creating-a-new-bot).

## Scripts and configuration files

**fail2ban_alert.py**<br>


 This Python script sends a notification via Telegram containing the banned IP address, the service name and some information gathered from “whois” on that IP.

 The script requires 3 arguments 'ip', 'name' and 'failures', all of which are supplied by Fail2Ban via special action tags (i.e. \<ip\>) when it's executed.

 Based on the supplied IP address, it also performes a whois query and grabs some additional information like ip address range, issuer name, country of origin, description and abuse emails which is included in the Telegram notification message.

 It writes its output in Fail2Ban's default log (`/var/log/fail2ban.log`) using the "fail2ban.telegram" tag and the same format for debugging purposes.


**jail.local**<br>

 This is an extract of a Fail2Ban configuration file, which shows how to set Telegram alert action for a service.
 The file should be created in `/etc/fail2ban/jail.d/jail.local`


**telegram.conf**<br>

 The python script must be specified in a separate "action" file ending in '.conf', located in the `/etc/fail2ban/action.d/` directory.


**fail2ban.log**<br>

 An extract of Fail2ban's log containing some Telegram alert entries.

## Example Telegram alert

<img src="https://i.imgur.com/4lBCaUp.jpg" height="700" width="350">
