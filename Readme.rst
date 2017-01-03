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

The purpose of this article is to show how to automatically install/configure Fail2ban the and unban IP address from Jail list.

Each time script will give menu to choose what we want.

In a Linux desktop terminal execute the following command to download codes:

.. code-block:: bash

    # git clone https://github.com/jamalshahverdiev/full-automated-nagios.git 
    
Execute the python-installer.sh to automatically install python2.7, python3.4, and all necessary libraries.

.. code-block:: bash

    # cd full-automated-nagios
    # ./python-installer.sh


Please, execute the following  to start the installation:

.. code-block:: bash

    # ./run.py
    The Program is going to install and configure the Nagios server automatically.
    It is supposed that you have already added all IP addresses of client hosts to the 'clients.txt' file.
    Users must be 'root' with the same passwords on all hosts ...

    =====================================================================================

    Choose one of following options:
    1. To install and configure Nagios server, type 1 and press 'Enter'.
    2. To install and configure 'Nrpe' agents on all client hosts, type 2 and press 'Enter'.
    3. To exit type 3 and press 'Enter'.

    Please choose the installation option: 1

