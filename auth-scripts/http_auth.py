import requests
#

url = basicAuthCredentials = ('username', 'passord')
http_timeout = (5, 5)
url = 'http://httpbin.org/basic-auth/username/password'


def check_for_basicauth(url):
    """Checks if the site uses basic Authentication."""
    try:
        response = requests.get(url,
                                timeout=http_timeout)
    except requests.exceptions.Timeout:
        return False
    except requests.exceptions.TooManyRedirects:
        return False
    except requests.exceptions.RequestException:
        return False
    if 'WWW-Authenticate' in response.headers:
        return True
    else:
        return False


if check_for_basicauth(url):
    try:
        # Send HTTP GET request to server and attempt to receive a response
        response = requests.get('http://httpbin.org/basic-auth/username/password',
                                timeout=http_timeout,
                                auth=basicAuthCredentials)

        # If the HTTP GET request can be served
        if response.status_code == 200:
            print('Authentication is succesvol')
        else:
            print('Authentication failed')
    except BaseException as err:
        print(err)
else:
    print('site does not uses basic authentication')

#
