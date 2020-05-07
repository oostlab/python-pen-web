import requests
from urllib.error import HTTPError
import sys


response = None
# url = 'http://httpbin.org/basic-auth/username/password'
# url = 'https://nu.nl:8000'
url = 'http://192.168.2.6:8080/manager/'
http_timeout = (5, 5)

try:
    response = requests.get(url,
                            timeout=http_timeout)
except requests.exceptions.Timeout:
    print('time out')
except requests.exceptions.TooManyRedirects:
    print('bad url')
except requests.exceptions.RequestException as err:
    print('not valid url')
    print(err)
    reponse = err
    sys.exit(1)

print(response.status_code)
print(response.headers)
if 'WWW-Authenticate' in response.headers:
    print('Site uses basic authentication')
else:
    print('Site does not use basic authentication')
'''auth = response and response.info().getheader('WWW-Authenticate')
if auth and auth.lower().startswith('basic'):
    print(("Requesting {} requires basic authentication".format(url)))
'''
