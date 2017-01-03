*********************
Automated Fail2ban
*********************

.. image:: https://img.shields.io/pypi/pyversions/Django.svg

Python script to install/configure Fail2ban and unban selected IP's.

Program components are the following:

* python-installer.sh - Script to install to your Linux desktop python and libraries.
* listunban.py - Script search Jail name and give menu to write IP address for unban.
* install.py - Automatic installation and configuration of Fail2ban to CentOS6 or CentOS7 server.
* run.py - Installation lunch script with an interactive menu.



=====
Usage
=====

The purpose of this scripts is to show how to automatically install/configure Fail2ban the and unban IP address from Jail list.

Each time script will give menu to choose what you want and must do.

In a Linux desktop terminal execute the following command to download codes:

.. code-block:: bash

    # https://github.com/jamalshahverdiev/fail2ban-centos-configurator.git
    
Execute the python-installer.sh to automatically install python2.7, python3.4, and all necessary libraries to your desktop machine.

.. code-block:: bash

    # cd fail2ban-centos-configurator
    # ./python-installer.sh


Please, execute the following script to see menu and choose what you need:

.. code-block:: bash

    # ./run.py
    Choose one of the following options:
    1. To install Fail2ban and configure for ssh, type 1 and press Enter.
    2. To list and unban blocked IP address, type 2 and press Enter.
    3. To exit type 3 and press Enter.

    Please choose the installation option: 1

    Script will install Fail2ban and configure ssh to ban failed login attemps.
    It needs IP address, username and password to start process.
    Please enter IP address of server: 172.16.100.11
    Please enter username for UNIX/Linux server: root
    Please enter password for UNIX/Linux server:

    OS type Linux CentOS.

    You have already installed and running Fail2ban ...
    If you want to list and unban blocked IP address, just use the "./listunban.py" script!!!


    Choose one of the following options:
    1. To install Fail2ban and configure for ssh, type 1 and press Enter.
    2. To list and unban blocked IP address, type 2 and press Enter.
    3. To exit type 3 and press Enter.

    Please choose the installation option: 3
