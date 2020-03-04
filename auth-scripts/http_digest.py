from requests.auth import HTTPDigestAuth
import requests


url = 'http://httpbin.org/digest-auth/auth/user/pass'
response = requests.get(url, auth=HTTPDigestAuth('user', 'pass'))
if response.status_code == 200:
    print(response.text)
else:
    print('Authentication failed')
