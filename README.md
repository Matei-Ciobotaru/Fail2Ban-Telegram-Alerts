# Fail2Ban-and-Telgram
# DDOS and Bruteforce prevention and notifications


### • Security (Fail2Ban + Telegram Bot):

### ► I’ve configured several rules in fail2ban which check some application logs for certain REGEXs, which represent logged failed attempts, and bans the afferent IPs upon match.

### ► I have set up a custom rule in Fail2Ban which checks the Nextcloud log for failed login attempts, extract the IP and bans it permanently after 3 failed attempts.

### ► I’ve created a Python script which sends my Telegram bot a notification when a IP is banned containing the banned IP, the “attacked“ service name and some information gathered from “whois” on that IP.

### ► My configured Fail2Ban rules are:  apache-auth, apache-badbots, apache-botsearch, apache-fakegooglebot, apache-modsecurity, apache-nohome, apache-noscript, apache-overflows, apache-shellshock, http-get-dos, nextcloud, sshd, sshd-ddos.
