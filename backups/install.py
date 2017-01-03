#!/usr/bin/env python
import sys
import os
import jinja2
from termcolor import colored, cprint
from fabric.api import *
from fabric.tasks import execute
import getpass

#codepath = os.path.dirname(__file__)
codepath = os.getcwd()
outputdir = codepath+'/output/'
jinjadir = codepath+'/jinja2temps/'

fail2ban = colored('Fail2ban', 'green', attrs=['bold', 'underline'])
ipaddress = colored('IP address', 'green', attrs=['bold', 'underline'])
ssh = colored('ssh', 'cyan', attrs=['bold'])
username = colored('username', 'green', attrs=['bold'])
password = colored('password', 'green', attrs=['bold'])
successfully = colored('successfully', 'green', attrs=['bold', 'underline'])

print('Script will install '+fail2ban+' and configure '+ssh+' to ban failed login attemps.')
print('It needs '+ipaddress+', '+username+' and '+password+' to start process.')
env.host_string = raw_input('Please enter '+ipaddress+' of server: ')
env.user = raw_input('Please enter '+username+' for UNIX/Linux server: ')
env.password = getpass.getpass('Please enter '+password+' for UNIX/Linux server: ')
f2banname = raw_input("""Please enter directive name for Fail2Ban configuration.
For example: ssh-iptables: """)

templateLoader = jinja2.FileSystemLoader( searchpath=jinjadir )
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPFAFILE = 'jail.local.j2'
tempfa = templateEnv.get_template( TEMPFAFILE )

tempfaVars = { "f2banname" : f2banname, }
outputfaText = tempfa.render( tempfaVars )

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
        print('OS type Linux CentOS.')

        with open(outputdir+'jail.local', 'wb') as f2banssh:
            f2banssh.write(outputfaText)

        if f2banbin == '/usr/bin/fail2ban-server' and f2banpidfile == f2banpid:
            print(' You have already installed and running "fail2ban" ...')
            print(' If you want to list and unban blocked IP address, just use the "listunban.py" script!!!')
            sys.exit()

        elif f2banbin != '/usr/bin/fail2ban-server':
            print(' Please be patient. Fail2ban will be installed and configured ...')
            run('yum -y install fail2ban')
            put(outputdir+'jail.local', '/etc/fail2ban/')
            run('chkconfig fail2ban on ; service fail2ban start')
            run('chkconfig iptables on ; iptables -L')
            # If you want to see access list, just uncomment following lines.
            #print('Look at new f2b-SSH chain in the server:  ')
            #print(run('iptables -L f2b-SSH -v -n --line-numbers'))
            #print("")
            print('Fail2ban '+successfully+' installed and configured')

