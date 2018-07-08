# Fail2Ban-and-Telgram
# DDOS and Bruteforce prevention and Telegram notifications


 Configured several rules in Fail2Ban which check some application logs for certain REGEXs, which represent logged failed attempts, and bans the respective IPs upon match.

 Set up a custom rule in Fail2Ban which checks the Nextcloud log for failed login attempts, extract the IP and bans it permanently after 3 failed attempts.

 Created a Python script which sends my Telegram bot a notification when a IP is banned containing the banned IP, the “attacked“ service name and some information gathered from “whois” on that IP.

 the python script must be specified in a separate "action" file ending in '.conf', located in the '/etc/fail2ban/action.d/' directory.
