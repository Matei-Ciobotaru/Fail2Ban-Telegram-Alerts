# Sending Fail2Ban alerts via Telegram

This is an updated version of the original script created by Matei Ciobotaru, with changes made by Gubaidullin Eduard. The script is designed to send Fail2Ban alerts via Telegram, providing information about banned IP addresses and relevant details.

## Python Libraries

You will need the following Python libraries installed to use this script:

- [python-telegram-bot](https://python-telegram-bot.org/) - Used to interact with Telegram.
- [ipwhois](https://pypi.org/project/ipwhois/) - Used to query IP details.

You can install the required libraries using the following command:

```bash
pip install python-telegram-bot ipwhois
```

## Telegram Bot

 You will need to create a Telegram bot and edit the python script to add your personal token and chatid.
 Edit the fail2ban_alert.py script and replace YOUR_SECRET_BOT_TOKEN and YOUR_SECRET_CHAT_ID with your actual bot token and chat ID.

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

## Testing
  You can test the script by running the following command with sample values:
  
## Example Telegram alert
```bash
python3.10 fail2ban_alert.py -i xxx.xxx.xxx.xxx -n SSH_BruteForce -f 5
```
  Replace the values with your desired IP address, rule name, and number of failed attempts to simulate the execution of the script.

<img src="https://i.imgur.com/4lBCaUp.jpg" height="700" width="350">
