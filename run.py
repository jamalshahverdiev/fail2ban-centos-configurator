#!/usr/bin/env python2.7

import subprocess
import sys
from termcolor import colored, cprint

fail2ban = colored('Fail2ban', 'green', attrs=['bold', 'underline'])
ipaddress = colored('IP address', 'green', attrs=['bold', 'underline'])
ssh = colored('ssh', 'cyan', attrs=['bold', 'underline'])
exit = colored('exit', 'cyan', attrs=['bold', 'underline'])
enter = colored('Enter', 'cyan', attrs=['bold', 'underline'])
choose = ""

while choose != "3":
    print("Choose one of the following options:")
    print('1. To install '+fail2ban+' and configure for '+ssh+', type 1 and press '+enter+'.')
    print('2. To list and unban blocked '+ipaddress+', type 2 and press '+enter+'.')
    print('3. To '+exit+' type 3 and press '+enter+'.')
    print('')
    choose = raw_input("  Please choose the installation option: ")
    print('')
    if choose == "1":
        subprocess.call("`pwd`/install.py", shell=True)
        print("")
        print("")
    elif choose == "2":
        print("")
        subprocess.call("`pwd`/listunban.py", shell=True)
        print("")
        print("")
    elif choose == "3":
        sys.exit()
    else:
        print("  You can choose options, only '1','2' or '3' !!!")
        print("")
