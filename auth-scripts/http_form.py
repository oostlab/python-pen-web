import requests
payload = {'username': 'Olivia', 'password': 'test'}
r = requests.post('https://httpbin.org/post', data=payload)
print(r.text)
