#!/usr/bin/env python2.7
import sys
import os
from termcolor import colored, cprint
from fabric.api import *
from fabric.tasks import execute
import getpass

codepath = os.getcwd()
jinjadir = codepath+'/jinja2temps/'

fail2ban = colored('Fail2ban', 'green', attrs=['bold', 'underline'])
ipaddress = colored('IP address', 'green', attrs=['bold', 'underline'])
ssh = colored('ssh', 'cyan', attrs=['bold'])
username = colored('username', 'green', attrs=['bold'])
password = colored('password', 'green', attrs=['bold'])
successfully = colored('successfully', 'green', attrs=['bold', 'underline'])
centos = colored('CentOS', 'yellow', attrs=['bold', 'underline'])

print('Script will install '+fail2ban+' and configure '+ssh+' to ban failed login attemps.')
print('It needs '+ipaddress+', '+username+' and '+password+' to start process.')
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
    global getcosver
    getcosver = run('rpm -q --queryformat \'%{VERSION}\' centos-release')
    global c7firewall 
    c7firewall = 'firewalld'
    global c6firewall
    c6firewall = 'iptables'
    global f2banservc 
    f2banservc = 'fail2ban'

def f2bancopyandstart(servicename):
    put(jinjadir+'jail.local', '/etc/fail2ban/')
    put(jinjadir+'sshd.local', '/etc/fail2ban/jail.d/')
    run('chkconfig '+servicename+' on ; service '+servicename+' start')

def f2banconfiger(iptab, firewd):
    if lintype == 'CentOS' and getcosver == '6':
        print(''+centos+' version is "6" !!!')
        run('yum -y install epel-release')
        run('yum -y install fail2ban')
        run('chkconfig '+iptab+' on ; service '+iptab+' start')
        f2bancopyandstart(f2banservc)
    elif lintype == 'CentOS' and getcosver == '7':
        print(''+centos+' version is "7" !!!')
        run('yum -y install epel-release')
        run('yum -y install fail2ban fail2ban-systemd')
        run('systemctl enable '+firewd+' ; systemctl start '+firewd+'')
        f2bancopyandstart(f2banservc)
    run('iptables -L -n')

with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
    variables()

    if osver == 'Linux' and lintype == 'CentOS':
        print('')
        print('OS type Linux '+centos+'.')

        if f2banbin == '/usr/bin/fail2ban-server' and f2banpidfile == f2banpid:
            print('')
            print(' You have already installed and running '+fail2ban+' ...')
            print(' If you want to list and unban blocked '+ipaddress+', just use the "./listunban.py" script!!!')
            sys.exit()

        elif f2banbin != '/usr/bin/fail2ban-server':
            print('')
            print(' Please be patient. '+fail2ban+' will be installed and configured ...')
            print('')
            f2banconfiger(c6firewall, c7firewall)
            variables()

            if f2banpid == f2banpidfile:
            # If you want to see access list, just uncomment following lines.
            #print('Look at new f2b-SSH chain in the server:  ')
            #print(run('iptables -L f2b-SSH -v -n --line-numbers'))
            #print("")
                print('')
                print(''+fail2ban+' is '+successfully+' installed and configured')
            else:
                print('')
                print(''+fail2ban+' is not successfully started!!!')
                sys.exit()

