import requests
#
basicAuthCredentials = ('username', 'password')

# Send HTTP GET request to server and attempt to receive a response
response = requests.get('http://httpbin.org/basic-auth/username/password', auth=basicAuthCredentials)

# If the HTTP GET request can be served
if response.status_code == 200:
    print(response.text)
else:
    print('Authentication failed')
