
import mysql.connector as mysql
import time
#

mysql_host = '192.168.2.8'
user = 'root'
password = 'my-secret-pw'


def check_for_mysql(url):
    """Checks if the site uses basic Authentication."""
    return True


def mysql_login(user, password, host):
    """Function for checking the login."""
    conn = mysql.connect(user=user, password=password, host=host, connection_timeout=1, port=3306)
    if conn.is_connected():
        print("--->Connected to MySQL database, username:" + user + ", password:" + password+", host:"+host)
        conn.close()



start = time.time()
mysql_login(user, password, mysql_host)
end = time.time()
print(end - start)
