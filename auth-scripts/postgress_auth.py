""" login file for postgress """
import psycopg2


def postgress_login():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="192.168.2.8", user="postgres", password="mysecretpassword", port=5432, connect_timeout=1)
  
        if conn is not  None:
            print('connected')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if 'password authentication failed' in str(error):
            print('wrong userid and password')
        if 'Connection refused' in str(error):
            print('Connection refused')
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    postgress_login()