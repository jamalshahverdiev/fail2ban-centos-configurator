#!/usr/bin/env python2.7
import sys
import os
from termcolor import colored, cprint
from fabric.api import *
from fabric.tasks import execute
import getpass

fail2ban = colored('Fail2ban', 'green', attrs=['bold', 'underline'])
ipaddress = colored('IP address', 'green', attrs=['bold', 'underline'])
ssh = colored('ssh', 'cyan', attrs=['bold'])
username = colored('username', 'green', attrs=['bold'])
password = colored('password', 'green', attrs=['bold'])
successfully = colored('successfully', 'green', attrs=['bold', 'underline'])
centos = colored('CentOS', 'yellow', attrs=['bold', 'underline'])
enter = colored('Enter', 'cyan', attrs=['bold', 'underline'])

print('Script will unban blocked '+ipaddress+' from selected Jail.')
print('It needs '+ipaddress+', '+username+' and '+password+' to connect '+fail2ban+' configured server.')
env.host_string = raw_input('Please enter '+ipaddress+' of server: ')
env.user = raw_input('Please enter '+username+' for UNIX/Linux server: ')
env.password = getpass.getpass('Please enter '+password+' for UNIX/Linux server: ')

def variables():
    global osver
    osver = run('uname -s')
    global lintype
    lintype = run('cat /etc/centos-release | awk \'{ print $1 }\'')
    global f2banbin
    f2banbin = run('which fail2ban-server')
    global f2banpid
    f2banpid = run('ps waux | grep -v grep | grep fail2ban | awk \'{ print $2 }\'')
    global f2banpidfile
    f2banpidfile = run('cat /var/run/fail2ban/fail2ban.pid')

with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
    variables()

    if osver == 'Linux' and lintype == 'CentOS':
        print('')
        print('OS type is Linux '+centos+'.')
        print('')

        if f2banbin == '/usr/bin/fail2ban-server' and f2banpidfile == f2banpid:
            print(' Please choose one of the following "Jail" names to list banned '+ipaddress+'...')
            print(run('fail2ban-client status | grep "Jail list" | awk \'{ $1=""; print }\''))
            print("")
            jailname = raw_input(''+enter+' Jail name to see banned '+ipaddress+' list: ')
            print(run('fail2ban-client status '+jailname+' | grep Banned | awk \'{ $1=""; print }\''))
            print("")
            print('If you don\'t want unban any '+ipaddress+' just press '+enter+' button!!!')
            ipfromlist = raw_input(''+enter+' '+ipaddress+' to delete from ban list: ')

            if ipfromlist == "":
                sys.exit()
            else:
                run('fail2ban-client set '+jailname+' unbanip '+ipfromlist)

            iptablist = run('iptables -L | egrep "f2b-SSH|'+ipfromlist+'" | grep -v \'f2b-SSH\' | awk \'{ print $4 }\'')
            ipf2blist = run('fail2ban-client status '+jailname+' | grep '+ipfromlist+' | awk \'{ print $2 }\'')

            if iptablist == ipfromlist and ipf2blist == 'Banned':
                print(ipfromlist+' '+ipaddress+' is not '+successfully+' deleted from'+jailname+' jail list')
            else:
                print(ipfromlist+' '+ipaddress+' is '+successfully+' deleted from '+jailname+' jail list')

        elif f2banbin != '/usr/bin/fail2ban-server' and f2banpidfile != f2banpid:
            print(' '+fail2ban+' is not installed and running on this server...')
            print(' If you want install and configure '+fail2ban+' just, use "./install.py" script!!!')
